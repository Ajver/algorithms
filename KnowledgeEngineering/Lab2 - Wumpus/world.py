"""Świat Wumpusa: geometria, losowe generowanie świata i środowisko.

Współrzędne to ``(x, y)``, gdzie ``1 <= x <= width`` i ``1 <= y <= height``.
Wejście do jaskini jest na polu ``(1, 1)``; myśliwy zaczyna tam, patrząc na
wschód, tak jak w AIMA.

Cały ten moduł to czysty Python: środowisko zna prawdziwy stan świata i tylko
przekazuje agentowi percepcje; samo nie prowadzi żadnego rozumowania.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum

Cell = tuple[int, int]

START: Cell = (1, 1)


class Direction(Enum):
    """Kierunek świata (północ, wschód, południe, zachód)."""

    N = "n"
    E = "e"
    S = "s"
    W = "w"

    @property
    def delta(self) -> tuple[int, int]:
        """Wektor przesunięcia ``(dx, dy)`` odpowiadający krokowi w tym kierunku."""
        return _DELTAS[self]

    def left(self) -> Direction:
        """Kierunek po obrocie o 90° w lewo."""
        return _LEFT[self]

    def right(self) -> Direction:
        """Kierunek po obrocie o 90° w prawo."""
        return _RIGHT[self]


_DELTAS = {Direction.N: (0, 1), Direction.E: (1, 0), Direction.S: (0, -1), Direction.W: (-1, 0)}
_LEFT = {Direction.N: Direction.W, Direction.W: Direction.S, Direction.S: Direction.E, Direction.E: Direction.N}
# Obrót w prawo jest odwrotnością obrotu w lewo.
_RIGHT = {v: k for k, v in _LEFT.items()}


class Action(Enum):
    """Akcje dostępne dla myśliwego (jak w AIMA)."""

    LEFT = "left"  # obrót o 90° w lewo
    RIGHT = "right"  # obrót o 90° w prawo
    FORWARD = "forward"  # krok naprzód
    GRAB = "grab"  # podniesienie złota
    SHOOT = "shoot"  # strzał z łuku w kierunku patrzenia
    CLIMB = "climb"  # wyjście z jaskini (tylko na polu startowym)


@dataclass(frozen=True)
class Percept:
    """To, co myśliwy odczuwa po wykonaniu akcji."""

    stench: bool = False  # smród -- na sąsiednim polu jest wumpus (żywy lub martwy)
    breeze: bool = False  # powiew -- na sąsiednim polu jest jama
    glitter: bool = False  # blask -- na tym polu leży złoto
    bump: bool = False  # uderzenie w ścianę przy próbie wyjścia poza planszę
    scream: bool = False  # krzyk -- strzała właśnie zabiła wumpusa


def in_bounds(cell: Cell, width: int, height: int) -> bool:
    """Czy pole ``cell`` leży na planszy ``width`` x ``height``."""
    x, y = cell
    return 1 <= x <= width and 1 <= y <= height


def step(cell: Cell, direction: Direction) -> Cell:
    """Pole sąsiednie do ``cell`` w kierunku ``direction`` (bez sprawdzania granic)."""
    dx, dy = direction.delta
    return cell[0] + dx, cell[1] + dy


def neighbours(cell: Cell, width: int, height: int) -> list[Cell]:
    """Pola sąsiadujące z ``cell`` krawędzią (2--4 pola, zależnie od położenia)."""
    return [n for d in Direction if in_bounds(n := step(cell, d), width, height)]


def ray(cell: Cell, direction: Direction, width: int, height: int) -> list[Cell]:
    """Pola, przez które leci strzała wystrzelona z ``cell`` w kierunku
    ``direction``, od najbliższego do ściany."""
    cells = []
    cur = step(cell, direction)
    while in_bounds(cur, width, height):
        cells.append(cur)
        cur = step(cur, direction)
    return cells


@dataclass(frozen=True)
class WorldConfig:
    """Ukryty układ jaskini: rozmiar oraz położenie jam, wumpusów i złota."""

    width: int
    height: int
    pits: frozenset[Cell]
    wumpuses: frozenset[Cell]
    gold: frozenset[Cell]

    def __post_init__(self) -> None:
        """Sprawdza poprawność układu: nic nie stoi na wejściu, wszystko mieści
        się na planszy i jest co najmniej jeden wumpus."""
        if self.width < 1 or self.height < 1:
            raise ValueError("world must be at least 1x1")
        for name in ("pits", "wumpuses", "gold"):
            cells = getattr(self, name)
            if START in cells:
                raise ValueError(f"{name} may not contain the entrance {START}")
            if not all(in_bounds(c, self.width, self.height) for c in cells):
                raise ValueError(f"{name} contains cells outside the world")
        if not self.wumpuses:
            raise ValueError("world needs at least one wumpus")


def generate_world(
    width: int = 4,
    height: int = 4,
    pit_prob: float = 0.2,
    n_wumpus: int = 1,
    n_gold: int = 1,
    gold_in_pit: bool = False,
    rng: random.Random | int | None = None,
) -> WorldConfig:
    """Generuje losową jaskinię.

    Każde pole poza wejściem niezależnie z prawdopodobieństwem ``pit_prob``
    staje się jamą.  ``n_wumpus`` wumpusów i ``n_gold`` sztuk złota umieszcza
    się na różnych polach (innych niż wejście) wybranych losowo z rozkładu
    jednostajnego; wumpus może dzielić pole z jamą (jak w AIMA).  Jeśli nie
    ustawiono ``gold_in_pit``, złoto trafia tylko na pola bez jam.
    ``rng`` może być generatorem albo ziarnem losowości.
    """
    if not 0.0 <= pit_prob <= 1.0:
        raise ValueError("pit_prob must be in [0, 1]")
    if not isinstance(rng, random.Random):
        rng = random.Random(rng)
    cells = [(x, y) for x in range(1, width + 1) for y in range(1, height + 1) if (x, y) != START]
    if n_wumpus < 1 or n_wumpus > len(cells):
        raise ValueError(f"n_wumpus must be between 1 and {len(cells)}")
    pits = frozenset(c for c in cells if rng.random() < pit_prob)
    wumpuses = frozenset(rng.sample(cells, n_wumpus))
    gold_candidates = cells if gold_in_pit else [c for c in cells if c not in pits]
    if n_gold > len(gold_candidates):
        raise ValueError("not enough free cells for gold")
    gold = frozenset(rng.sample(gold_candidates, n_gold))
    return WorldConfig(width, height, pits, wumpuses, gold)


# Jaskinia 4x4 z AIMA (Russell & Norvig), rysunek 7.2.
AIMA_WORLD = WorldConfig(
    4,
    4,
    pits=frozenset({(3, 1), (3, 3), (4, 4)}),
    wumpuses=frozenset({(1, 3)}),
    gold=frozenset({(2, 3)}),
)

# Jaskinia 4x4 pokazująca przewagę zliczania modeli nad heurystyką "liczby
# rodzajów zagrożeń".  Po odwiedzeniu (1,1), (2,1) i (1,2) agent czuje powiew
# na (2,1) i (1,2) oraz smród na (1,2), więc wumpus na pewno siedzi na (1,3).
# Do wyboru zostają (2,2) i (3,1) -- na obu możliwa jest tylko jama.  Zwykły
# ryzykant nie widzi różnicy i idzie na bliższe (2,2), a to jama.  Zliczanie
# modeli (rozdział 12/13 AIMA): jedna jama na (2,2) wyjaśnia oba powiewy, więc
# przy p = 0.2 P(jama na (2,2)) ≈ 0.86, a P(jama na (3,1)) ≈ 0.31.
COUNTING_WORLD = WorldConfig(
    4,
    4,
    pits=frozenset({(2, 2)}),
    wumpuses=frozenset({(1, 3)}),
    gold=frozenset({(4, 1)}),
)


@dataclass
class World:
    """Środowisko: prawdziwy stan jaskini plus ciało myśliwego.

    ``execute`` wykonuje akcję i zwraca wynikającą z niej percepcję.
    """

    config: WorldConfig
    n_arrows: int | None = None  # None = tyle strzał, ile wumpusów
    pos: Cell = START
    direction: Direction = Direction.E
    alive: bool = True
    climbed: bool = False
    arrows: int = field(init=False)
    live_wumpuses: set[Cell] = field(init=False)
    gold_left: set[Cell] = field(init=False)  # złoto jeszcze niepodniesione
    gold_carried: int = 0
    actions_taken: int = 0
    arrows_used: int = 0

    def __post_init__(self) -> None:
        """Ustawia stan początkowy: liczbę strzał, żywe wumpusy i leżące złoto."""
        self.arrows = len(self.config.wumpuses) if self.n_arrows is None else self.n_arrows
        self.live_wumpuses = set(self.config.wumpuses)
        self.gold_left = set(self.config.gold)

    @property
    def width(self) -> int:
        """Szerokość planszy."""
        return self.config.width

    @property
    def height(self) -> int:
        """Wysokość planszy."""
        return self.config.height

    @property
    def done(self) -> bool:
        """Czy gra się skończyła (myśliwy zginął albo wyszedł z jaskini)."""
        return not self.alive or self.climbed

    def percept(self, bump: bool = False, scream: bool = False) -> Percept:
        """Percepcja na bieżącej pozycji myśliwego.  Martwe wumpusy nadal śmierdzą.

        ``bump`` i ``scream`` zależą od właśnie wykonanej akcji, więc
        przekazuje je :meth:`execute`.
        """
        around = neighbours(self.pos, self.width, self.height)
        return Percept(
            stench=any(c in self.config.wumpuses for c in around),
            breeze=any(c in self.config.pits for c in around),
            glitter=self.pos in self.gold_left,
            bump=bump,
            scream=scream,
        )

    def execute(self, action: Action) -> Percept:
        """Wykonuje akcję myśliwego, aktualizuje stan świata i zwraca nową percepcję.

        Wejście na pole z jamą lub żywym wumpusem kończy się śmiercią.  Strzała
        leci prosto aż do ściany i zabija pierwszego żywego wumpusa na swojej
        drodze.  CLIMB działa tylko na polu startowym.
        """
        if self.done:
            raise RuntimeError("the game is over")
        self.actions_taken += 1
        bump = scream = False
        if action is Action.LEFT:
            self.direction = self.direction.left()
        elif action is Action.RIGHT:
            self.direction = self.direction.right()
        elif action is Action.FORWARD:
            target = step(self.pos, self.direction)
            if in_bounds(target, self.width, self.height):
                self.pos = target
                if target in self.config.pits or target in self.live_wumpuses:
                    self.alive = False
            else:
                bump = True  # ściana: myśliwy zostaje na miejscu
        elif action is Action.GRAB:
            if self.pos in self.gold_left:
                self.gold_left.remove(self.pos)
                self.gold_carried += 1
        elif action is Action.SHOOT:
            if self.arrows > 0:
                self.arrows -= 1
                self.arrows_used += 1
                for c in ray(self.pos, self.direction, self.width, self.height):
                    if c in self.live_wumpuses:
                        self.live_wumpuses.remove(c)
                        scream = True
                        break
        elif action is Action.CLIMB:
            if self.pos == START:
                self.climbed = True
        return self.percept(bump=bump, scream=scream)

    def score(self) -> int:
        """Punktacja z AIMA: +1000 za każde wyniesione złoto, -1000 za śmierć,
        -10 za każdą wystrzeloną strzałę, -1 za każdą akcję."""
        s = -self.actions_taken - 10 * self.arrows_used
        if not self.alive:
            s -= 1000
        elif self.climbed:
            s += 1000 * self.gold_carried
        return s

    def render(self) -> str:
        """Mapa prawdziwego świata, górny wiersz pierwszy.  Każde pole to
        4 znaki: jama (``P``), wumpus (``W`` żywy, ``w`` martwy), złoto (``G``)
        oraz strzałka wskazująca pozycję i kierunek myśliwego."""
        arrow = {Direction.N: "^", Direction.E: ">", Direction.S: "v", Direction.W: "<"}[self.direction]
        rows = []
        for y in range(self.height, 0, -1):
            row = []
            for x in range(1, self.width + 1):
                c = (x, y)
                s = ""
                s += "P" if c in self.config.pits else "."
                if c in self.live_wumpuses:
                    s += "W"
                elif c in self.config.wumpuses:
                    s += "w"
                else:
                    s += "."
                s += "G" if c in self.gold_left else "."
                s += arrow if c == self.pos else " "
                row.append(s)
            rows.append(" ".join(row))
        return "\n".join(rows)
