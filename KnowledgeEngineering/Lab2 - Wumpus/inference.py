"""Baza wiedzy agenta i wnioskowanie nad nią za pomocą Clingo.

Baza wiedzy przechowuje wyłącznie to, co agent zaobserwował (odwiedzone pola,
percepcje, wystrzelone strzały).  Wnioski o ukrytej części świata są za każdym
razem wyliczane od nowa przez program ``wumpus_kb.lp``:

* konsekwencje ostrożne (ang. *cautious*, prawdziwe we WSZYSTKICH modelach
  stabilnych) dają wiedzę pewną,
* konsekwencje odważne (ang. *brave*, prawdziwe w PRZYNAJMNIEJ JEDNYM modelu)
  dają to, co jest możliwe,
* (ważone) zliczanie modeli daje prawdopodobieństwo zagrożenia na każdym
  polu pogranicza (:meth:`KnowledgeBase.danger_probabilities`).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import clingo

from world import START, Cell, Direction

# Program ASP opisujący reguły świata z punktu widzenia agenta.
PROGRAM_PATH = Path(__file__).with_name("wumpus_kb.lp")


class InconsistentKnowledge(RuntimeError):
    """Zapisane obserwacje są sprzeczne -- nie pasuje do nich żaden świat."""


@dataclass(frozen=True)
class Shot:
    """Jeden strzał z łuku: skąd, w którą stronę i czy było słychać krzyk wumpusa."""

    origin: Cell
    direction: Direction
    scream: bool


@dataclass(frozen=True)
class Inference:
    """Wnioski wyciągnięte z bazy wiedzy.

    Informacje o jamach mają sens tylko dla pól *pogranicza* (``frontier``),
    czyli nieodwiedzonych pól sąsiadujących z odwiedzonym.  O jamach dalej
    od odwiedzonego obszaru agent po prostu nic nie wie.

    Pola ``*_certain`` pochodzą z konsekwencji ostrożnych (prawda w każdym
    modelu), a ``*_possible`` z konsekwencji odważnych (prawda w jakimś modelu).
    """

    frontier: frozenset[Cell]
    safe: frozenset[Cell]  # pola pogranicza na pewno bez jamy i bez żywego wumpusa
    pit_certain: frozenset[Cell]  # na pewno jama
    pit_possible: frozenset[Cell]  # może być jama
    wumpus_certain: frozenset[Cell]  # na pewno jest tam wumpus (żywy lub martwy)
    wumpus_possible: frozenset[Cell]  # może być wumpus
    alive_certain: frozenset[Cell]  # na pewno żywy wumpus
    alive_possible: frozenset[Cell]  # może być żywy wumpus
    dead_certain: frozenset[Cell]  # na pewno martwy wumpus


@dataclass
class KnowledgeBase:
    """Zbiór faktów zaobserwowanych przez agenta.

    Baza nie wyciąga wniosków sama -- metoda :meth:`infer` tłumaczy fakty na
    program ASP i deleguje rozumowanie do Clingo.
    """

    width: int
    height: int
    n_wumpus: int = 1
    visited: set[Cell] = field(default_factory=set)
    breeze: dict[Cell, bool] = field(default_factory=dict)  # pole -> czy czuć powiew
    stench: dict[Cell, bool] = field(default_factory=dict)  # pole -> czy czuć smród
    shots: list[Shot] = field(default_factory=list)

    def tell_percept(self, cell: Cell, breeze: bool, stench: bool) -> None:
        """Zapisuje, że agent stał na polu ``cell`` i co tam poczuł.

        Zapisujemy zarówno obecność, jak i *brak* powiewu/smrodu -- informacja
        negatywna jest równie cenna (wyklucza jamy/wumpusy na polach sąsiednich).
        """
        self.visited.add(cell)
        self.breeze[cell] = breeze
        self.stench[cell] = stench

    def tell_shot(self, origin: Cell, direction: Direction, scream: bool) -> None:
        """Zapisuje oddany strzał oraz to, czy po nim rozległ się krzyk."""
        self.shots.append(Shot(origin, direction, scream))

    def facts(self) -> str:
        """Zamienia zawartość bazy wiedzy na fakty w składni Clingo.

        Np. ``visited(1,1).``, ``no_breeze(1,1).``, ``shot(0,1,2,e).``,
        ``scream(0).``.  Opis wszystkich predykatów znajduje się w nagłówku
        pliku ``wumpus_kb.lp``.
        """
        lines = [f"size({self.width},{self.height}).", f"wumpus_count({self.n_wumpus})."]
        # Wejście do jaskini jest zawsze bezpieczne, nawet zanim agent cokolwiek zgłosi.
        for x, y in sorted(self.visited | {START}):
            lines.append(f"visited({x},{y}).")
        for (x, y), b in sorted(self.breeze.items()):
            lines.append(f"{'' if b else 'no_'}breeze({x},{y}).")
        for (x, y), s in sorted(self.stench.items()):
            lines.append(f"{'' if s else 'no_'}stench({x},{y}).")
        # Strzały są numerowane, bo ich kolejność ma znaczenie (wumpus zabity
        # wcześniejszą strzałą nie zatrzymuje już następnych).
        for n, shot in enumerate(self.shots):
            x, y = shot.origin
            lines.append(f"shot({n},{x},{y},{shot.direction.value}).")
            lines.append(f"{'' if shot.scream else 'no_'}scream({n}).")
        return "\n".join(lines) + "\n"

    def infer(self) -> Inference:
        """Uruchamia Clingo na regułach świata + faktach i zwraca wnioski.

        Program jest ugruntowywany raz, a następnie rozwiązywany dwukrotnie:
        w trybie konsekwencji ostrożnych (co wiemy na pewno) i odważnych
        (co jest możliwe).  Brak modeli oznacza sprzeczne obserwacje.
        """
        ctl = self._ground()
        cautious = _consequences(ctl, "cautious")
        brave = _consequences(ctl, "brave")
        if cautious is None or brave is None:
            raise InconsistentKnowledge("no world is consistent with the observations")
        return Inference(
            frontier=cautious.get("frontier", frozenset()),
            safe=cautious.get("safe", frozenset()),
            pit_certain=cautious.get("pit", frozenset()),
            pit_possible=brave.get("pit", frozenset()),
            wumpus_certain=cautious.get("wumpus", frozenset()),
            wumpus_possible=brave.get("wumpus", frozenset()),
            alive_certain=cautious.get("alive", frozenset()),
            alive_possible=brave.get("alive", frozenset()),
            dead_certain=cautious.get("dead", frozenset()),
        )

    def danger_probabilities(self, pit_prob: float) -> dict[Cell, float]:
        """Prawdopodobieństwo, że wejście na dane pole pogranicza zabije
        myśliwego (jest tam jama lub żywy wumpus), przy zapisanych obserwacjach.

        Liczone przez ważone zliczanie modeli: Clingo wylicza WSZYSTKIE modele
        stabilne, a każdy z nich to jeden możliwy wygląd ukrytej części świata.
        Rozkład a priori jest taki jak w ``generate_world``: każde pole jest
        jamą niezależnie z prawdopodobieństwem ``pit_prob``, a wumpusy stoją na
        polach wybranych jednostajnie.  Model z ``k`` jamami na pograniczu ma
        więc wagę ``pit_prob**k * (1 - pit_prob)**(n - k)``, gdzie ``n`` to
        liczba pól pogranicza (jamy dalej od odwiedzonego obszaru nie wpływają
        na żadną percepcję, więc się skracają).  Wynik to suma wag modeli,
        w których pole jest groźne, podzielona przez sumę wag wszystkich modeli.

        Uwaga: liczba modeli rośnie wykładniczo z rozmiarem pogranicza i liczbą
        wumpusów, więc metoda nadaje się do małych światów.
        """
        if not 0.0 < pit_prob < 1.0:
            raise ValueError("pit_prob must be in (0, 1)")
        # Czynnik (1 - pit_prob)**n jest wspólny dla wszystkich modeli, więc
        # wystarczy waga względna (pit_prob / (1 - pit_prob))**k.
        odds = pit_prob / (1.0 - pit_prob)
        total = 0.0
        danger: dict[Cell, float] = {}
        frontier: set[Cell] = set()
        ctl = self._ground()
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                atoms: dict[str, set[Cell]] = {}
                for sym in model.symbols(shown=True):
                    atoms.setdefault(sym.name, set()).add(tuple(a.number for a in sym.arguments))
                frontier = atoms.get("frontier", set())  # taki sam w każdym modelu
                weight = odds ** len(atoms.get("pit", set()))
                total += weight
                for c in (atoms.get("pit", set()) | atoms.get("alive", set())) & frontier:
                    danger[c] = danger.get(c, 0.0) + weight
        if total == 0.0:
            raise InconsistentKnowledge("no world is consistent with the observations")
        return {c: danger.get(c, 0.0) / total for c in frontier}

    def _ground(self) -> clingo.Control:
        """Ugruntowany program: reguły świata z ``wumpus_kb.lp`` + fakty z bazy."""
        ctl = clingo.Control(["--models=0"])  # 0 = wyliczaj wszystkie modele
        ctl.load(str(PROGRAM_PATH))
        ctl.add("base", [], self.facts())
        ctl.ground([("base", [])])
        return ctl


def _consequences(ctl: clingo.Control, mode: str) -> dict[str, frozenset[Cell]] | None:
    """Konsekwencje odważne/ostrożne pogrupowane według predykatu albo None, gdy
    program nie ma modelu (UNSAT).

    W tych trybach Clingo nie zwraca kolejnych modeli, tylko stopniowo
    zawęża (ostrożne) lub poszerza (odważne) zbiór atomów z każdym znalezionym
    modelem -- dlatego wynikiem jest ostatni zgłoszony "model".
    Zwracany słownik ma postać np. ``{"pit": {(3, 1)}, "safe": {(1, 2)}}``.
    """
    ctl.configuration.solve.enum_mode = mode
    last: list[clingo.Symbol] | None = None
    with ctl.solve(yield_=True) as handle:
        for model in handle:
            last = model.symbols(shown=True)
    if last is None:
        return None
    grouped: dict[str, set[Cell]] = {}
    for sym in last:
        # Wszystkie pokazywane predykaty (#show) mają postać nazwa(X, Y).
        x, y = (a.number for a in sym.arguments)
        grouped.setdefault(sym.name, set()).add((x, y))
    return {k: frozenset(v) for k, v in grouped.items()}
