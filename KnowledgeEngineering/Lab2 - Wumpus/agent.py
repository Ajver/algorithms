"""Agent oparty na wiedzy polujący w świecie Wumpusa.

Agent przechowuje swoje obserwacje w ``KnowledgeBase`` i za każdym razem, gdy
potrzebuje nowego celu, pyta Clingo, co z tych obserwacji wynika.  Zamiana
celu na ciąg elementarnych akcji to zwykłe przeszukiwanie wszerz (BFS) po
stanach ``(pole, kierunek)``, ograniczone do pól, o których wiadomo, że są
bezpieczne.

Strategia (w kolejności preferencji):

1. podnieś złoto, gdy czujesz blask (glitter);
2. gdy niesiesz już całe złoto, wróć do wejścia i wyjdź z jaskini;
3. idź do najbliższego pola pogranicza, którego bezpieczeństwo jest dowiedzione;
4. strzel w pole pogranicza, które na pewno nie jest jamą, ale może być na nim
   żywy wumpus -- strzał oddawany jest z sąsiedniego odwiedzonego pola, więc
   po nim pole jest na pewno bezpieczne niezależnie od tego, czy był krzyk;
5. (tylko przy ``risky=True``) idź na najmniej podejrzane pole pogranicza,
   które nie jest na pewno śmiertelne;
6. w przeciwnym razie poddaj się: wróć do wejścia i wyjdź z jaskini.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterable

from inference import Inference, KnowledgeBase
from world import START, Action, Cell, Direction, Percept, in_bounds, step

# Stan ciała agenta istotny dla planowania: pozycja i kierunek patrzenia.
State = tuple[Cell, Direction]


def plan_route(
    start: State,
    is_goal: Callable[[Cell, Direction], bool],
    allowed: Iterable[Cell],
) -> list[Action] | None:
    """Najkrótsza lista akcji LEFT/RIGHT/FORWARD prowadząca ze stanu ``start``
    do stanu spełniającego ``is_goal``, stąpająca wyłącznie po polach ``allowed``.
    Zwraca None, jeśli żaden stan docelowy nie jest osiągalny.

    Jest to BFS w grafie stanów ``(pole, kierunek)``: z każdego stanu można
    obrócić się w lewo, w prawo lub zrobić krok naprzód (o ile pole przed
    agentem jest dozwolone).  Każda akcja kosztuje 1, więc BFS daje plan
    o minimalnej liczbie akcji.
    """
    allowed = set(allowed)
    if is_goal(*start):
        return []
    # parents[s] = (poprzedni stan, akcja prowadząca do s); służy do odtworzenia ścieżki.
    parents: dict[State, tuple[State, Action] | None] = {start: None}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        cell, d = state
        successors = [((cell, d.left()), Action.LEFT), ((cell, d.right()), Action.RIGHT)]
        if (nxt := step(cell, d)) in allowed:
            successors.append(((nxt, d), Action.FORWARD))
        for succ, action in successors:
            if succ in parents:
                continue
            parents[succ] = (state, action)
            if is_goal(*succ):
                return _unwind(parents, succ)
            queue.append(succ)
    return None


def _unwind(parents: dict[State, tuple[State, Action] | None], state: State) -> list[Action]:
    """Odtwarza ciąg akcji od stanu startowego do ``state``, cofając się po
    wskaźnikach ``parents`` i odwracając wynik."""
    actions = []
    while (entry := parents[state]) is not None:
        state, action = entry
        actions.append(action)
    return actions[::-1]


class Agent:
    """Myśliwy: łączy bazę wiedzy (co wiem), wnioskowanie (co z tego wynika)
    i planowanie trasy (jak tam dojść)."""

    def __init__(
        self,
        width: int,
        height: int,
        n_wumpus: int = 1,
        n_gold: int | None = 1,
        n_arrows: int | None = None,
        risky: bool = False,
    ) -> None:
        """Tworzy agenta stojącego na wejściu (1, 1) i patrzącego na wschód.

        ``n_gold=None`` oznacza, że agent nie wie, ile jest złota, i eksploruje
        jaskinię, dopóki zostały jakieś bezpieczne pola.  ``n_arrows=None``
        oznacza tyle strzał, ile jest wumpusów.  ``risky=True`` pozwala
        agentowi zaryzykować wejście na niepewne pole, gdy nic nie jest
        na pewno bezpieczne.
        """
        self.width, self.height = width, height
        self.n_gold = n_gold
        self.arrows = n_wumpus if n_arrows is None else n_arrows
        self.risky = risky
        self.kb = KnowledgeBase(width, height, n_wumpus)
        self.pos: Cell = START
        self.direction = Direction.E
        self.gold_carried = 0
        self.plan: deque[Action] = deque()  # akcje zaplanowane, jeszcze niewykonane
        self.goal = "start"  # opis bieżącego celu (do wyświetlania)
        self.last_action: Action | None = None
        self.last_inference: Inference | None = None

    # --- percepcja --------------------------------------------------------

    def _observe(self, percept: Percept) -> None:
        """Dopisuje bieżącą percepcję do bazy wiedzy.

        Jeśli poprzednią akcją był strzał, zapisuje go razem z informacją
        o krzyku i porzuca dotychczasowy plan, bo obraz świata się zmienił.
        """
        if self.last_action is Action.SHOOT:
            self.kb.tell_shot(self.pos, self.direction, percept.scream)
            self.plan.clear()  # obraz świata się zmienił; planujemy od nowa
        if percept.bump:
            # Nie powinno się zdarzyć przy znanym rozmiarze świata; na wszelki
            # wypadek planujemy od nowa.
            self.plan.clear()
        self.kb.tell_percept(self.pos, percept.breeze, percept.stench)

    # --- działanie --------------------------------------------------------

    def act(self, percept: Percept) -> Action:
        """Główna pętla agenta: przyjmuje percepcję, zwraca następną akcję.

        Blask złota ma najwyższy priorytet (natychmiastowe GRAB).  W pozostałych
        przypadkach agent wykonuje kolejne akcje z planu, a gdy plan się
        skończy, wybiera nowy cel metodą :meth:`_decide`.
        """
        self._observe(percept)
        if percept.glitter:
            action = Action.GRAB
            self.plan.clear()
        else:
            if not self.plan:
                self.plan = deque(self._decide())
            action = self.plan.popleft()
        self._apply(action)
        return action

    def _apply(self, action: Action) -> None:
        """Aktualizuje własny stan agenta (pozycję, kierunek, złoto, strzały)
        po wykonaniu akcji; odzwierciedla ``World.execute`` dla akcji
        zaplanowanych.  Agent nie widzi stanu świata, więc musi go śledzić sam."""
        if action is Action.LEFT:
            self.direction = self.direction.left()
        elif action is Action.RIGHT:
            self.direction = self.direction.right()
        elif action is Action.FORWARD:
            nxt = step(self.pos, self.direction)
            if in_bounds(nxt, self.width, self.height):
                self.pos = nxt
        elif action is Action.GRAB:
            self.gold_carried += 1
        elif action is Action.SHOOT:
            self.arrows -= 1
        self.last_action = action

    # --- podejmowanie decyzji ---------------------------------------------

    def _decide(self) -> list[Action]:
        """Wybiera nowy cel według strategii z opisu modułu i zwraca plan
        (listę akcji) jego realizacji.  To tutaj wywoływane jest wnioskowanie
        w Clingo."""
        state = (self.pos, self.direction)
        visited = self.kb.visited

        # Całe złoto zebrane -> wracamy do domu (bez potrzeby wnioskowania).
        if self.n_gold is not None and self.gold_carried >= self.n_gold:
            return self._go_home("bring the gold home")

        inf = self.kb.infer()
        self.last_inference = inf

        # Najbliższe na pewno bezpieczne pole pogranicza.  Trasa prowadzi
        # tylko przez pola odwiedzone lub bezpieczne.
        if inf.safe:
            route = plan_route(state, lambda c, d: c in inf.safe, visited | inf.safe)
            if route is not None:
                self.goal = f"explore {route_target(state, route)}"
                return route

        # Uczyń strzałą bezpiecznym pole pogranicza, na którym na pewno nie ma jamy.
        if self.arrows > 0:
            targets = (inf.frontier & inf.alive_possible) - inf.pit_possible
            # Strzelamy z odwiedzonego sąsiada, żeby cel był pierwszym polem na
            # torze lotu strzały.  Wtedy: krzyk -> wumpus tam zginął; brak
            # krzyku -> nie było tam żywego wumpusa.  W obu przypadkach pole
            # staje się bezpieczne.
            route = plan_route(
                state,
                lambda c, d: c in visited and step(c, d) in targets,
                visited,
            )
            if route is not None:
                self.goal = f"shoot {route_target(state, route, shoot=True)}"
                return route + [Action.SHOOT]

        if self.risky:
            # Pomijamy pola, o których wiadomo, że zabijają.
            deadly = inf.pit_certain | inf.alive_certain
            candidates = inf.frontier - deadly
            # TODO (RISKY)

        return self._go_home("nothing safe left, leave the cave")

    def _go_home(self, why: str) -> list[Action]:
        """Plan powrotu do wejścia po odwiedzonych polach zakończony akcją CLIMB.
        ``why`` to opis celu wyświetlany podczas symulacji."""
        self.goal = why
        route = plan_route((self.pos, self.direction), lambda c, d: c == START, self.kb.visited)
        assert route is not None, "visited cells are always connected to the entrance"
        return route + [Action.CLIMB]

    # --- wyświetlanie -----------------------------------------------------

    def render_knowledge_description(self) -> str:
        """Legenda do mapy zwracanej przez :meth:`render_knowledge`."""
        return """
        Each cell has 4 characters:
        * hunter position: one of "^", ">", "v", "<" or " " if the hunter is somewhere else
        * general status: "." -> visited, "s" -> provably safe, "?" unknown
        * pit status: "P" -> certain, "p" -> possible, "b" -> breeze felt here, " " -> away from frontier
        * wumpus status: "W" -> certainly alive, "X" -> certainly dead, "w" -> possibly alive, "~" -> stench felt here, " " -> away from frontier
        """

    def render_knowledge(self) -> str:
        """Mapa wiedzy agenta, górny wiersz pierwszy.  Każde pole to 4 znaki:

        myśliwy (``^>v<``), status (``.`` odwiedzone, ``s`` na pewno
        bezpieczne, ``?`` nieznane), jama (``P`` pewna, ``p`` możliwa,
        ``b`` poczuto tu powiew), wumpus (``W`` na pewno żywy, ``X`` na pewno
        martwy, ``w`` może być żywy, ``~`` poczuto tu smród).
        """
        inf = self.last_inference
        arrow = {Direction.N: "^", Direction.E: ">", Direction.S: "v", Direction.W: "<"}
        rows = []
        for y in range(self.height, 0, -1):
            row = []
            for x in range(1, self.width + 1):
                c = (x, y)
                # 1. znak: pozycja i kierunek myśliwego
                s = arrow[self.direction] if c == self.pos else " "
                # 2. znak: status pola
                if c in self.kb.visited:
                    s += "."
                elif inf is not None and c in inf.safe:
                    s += "s"
                else:
                    s += "?"
                # 3. znak: jamy
                if self.kb.breeze.get(c):
                    s += "b"
                elif inf is not None and c in inf.pit_certain:
                    s += "P"
                elif inf is not None and c in inf.frontier and c in inf.pit_possible:
                    s += "p"
                else:
                    s += " "
                # 4. znak: wumpusy
                if inf is not None and c in inf.alive_certain:
                    s += "W"
                elif inf is not None and c in inf.dead_certain:
                    s += "X"
                elif inf is not None and c in inf.frontier and c in inf.alive_possible:
                    s += "w"
                elif self.kb.stench.get(c):
                    s += "~"
                else:
                    s += " "
                row.append(s)
            rows.append("|".join(row))
        return "\n".join(rows)


def route_target(start: State, route: list[Action], shoot: bool = False) -> Cell:
    """Pole, na którym kończy się trasa ``route`` (lub, przy ``shoot=True``,
    pole, w które agent patrzy na końcu trasy -- czyli cel strzału).
    Symuluje trasę krok po kroku, startując ze stanu ``start``."""
    cell, d = start
    for a in route:
        if a is Action.LEFT:
            d = d.left()
        elif a is Action.RIGHT:
            d = d.right()
        elif a is Action.FORWARD:
            cell = step(cell, d)
    return step(cell, d) if shoot else cell
