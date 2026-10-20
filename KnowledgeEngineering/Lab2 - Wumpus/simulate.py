"""Uruchamia agenta opartego na Clingo w losowo generowanych światach Wumpusa
(albo w standardowym świecie z AIMA).

Przykłady::

    python simulate.py                          # jedna gra 4x4, wypisywana krok po kroku
    python simulate.py --size 8 --pits 0.15 --wumpus 2 --seed 3
    python simulate.py --games 100 --quiet      # tylko statystyki
    python simulate.py --aima                   # stały świat 4x4 z książki Russella i Norviga
"""

from __future__ import annotations

import argparse
import random
import sys
import time
from dataclasses import dataclass

from agent import Agent
from world import AIMA_WORLD, World, WorldConfig, generate_world


@dataclass(frozen=True)
class GameResult:
    """Podsumowanie jednej rozegranej gry."""

    score: int
    actions: int
    gold: int
    alive: bool
    climbed: bool
    seconds: float  # czas spędzony przez agenta na wnioskowaniu i planowaniu


def run_game(
    config: WorldConfig,
    max_actions: int = 1000,
    risky: bool = False,
    agent_knows_gold: bool = True,
    verbose: bool = True,
) -> GameResult:
    """Rozgrywa jedną grę agenta w świecie ``config`` i zwraca jej wynik.

    Pętla gry: środowisko podaje percepcję -> agent wybiera akcję ->
    środowisko ją wykonuje.  Gra kończy się śmiercią myśliwego, wyjściem
    z jaskini albo po ``max_actions`` akcjach.  ``agent_knows_gold`` mówi, czy
    agent zna liczbę sztuk złota; ``verbose`` włącza wypisywanie przebiegu gry
    (prawdziwego świata, kolejnych akcji i mapy wiedzy agenta przy zmianie celu).
    """
    world = World(config)
    # Agent zna rozmiar świata, liczbę wumpusów i strzał, ale nie ich położenie.
    agent = Agent(
        config.width,
        config.height,
        n_wumpus=len(config.wumpuses),
        n_gold=len(config.gold) if agent_knows_gold else None,
        n_arrows=world.arrows,
        risky=risky,
    )
    t0 = time.perf_counter()
    percept = world.percept()  # percepcja na polu startowym
    if verbose:
        print("True world (P pit, W/w live/dead wumpus, G gold):")
        print(world.render(), end="\n\n")
        print("Agent knowledge description:")
        print(agent.render_knowledge_description(), end="\n\n")
    while not world.done and world.actions_taken < max_actions:
        action = agent.act(percept, verbose=verbose)
        percept = world.execute(action)
        if verbose:
            flags = [k for k, v in vars(percept).items() if v]
            print(f"{world.actions_taken:4d}. {action.value:8s} -> {world.pos} {' '.join(flags)}")
    elapsed = time.perf_counter() - t0
    result = GameResult(world.score(), world.actions_taken, world.gold_carried, world.alive, world.climbed, elapsed)
    if verbose:
        outcome = "died" if not world.alive else ("climbed out" if world.climbed else "ran out of actions")
        print(f"\nHunter {outcome} with {world.gold_carried} gold after {world.actions_taken} actions.")
        print(f"Score: {result.score}   (inference + planning took {elapsed:.2f}s)")
    return result


def main(argv) -> None:
    """Punkt wejścia z linii poleceń: parsuje argumenty, rozgrywa ``--games``
    gier i (dla więcej niż jednej gry) wypisuje zbiorcze statystyki."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--size", type=int, default=4, help="square world size (default 4)")
    ap.add_argument("--width", type=int, help="overrides --size")
    ap.add_argument("--height", type=int, help="overrides --size")
    ap.add_argument("--pits", type=float, default=0.2, help="pit probability per cell (default 0.2)")
    ap.add_argument("--wumpus", type=int, default=1, help="number of wumpuses (default 1)")
    ap.add_argument("--gold", type=int, default=1, help="number of gold pieces (default 1)")
    ap.add_argument("--seed", type=int, help="random seed")
    ap.add_argument("--aima", action="store_true",
                    help="use the standard Russell & Norvig 4x4 world (ignores size/pits/wumpus/gold/seed)")
    ap.add_argument("--games", type=int, default=1, help="number of games to play")
    ap.add_argument("--risky", action="store_true", help="gamble when nothing is provably safe")
    ap.add_argument("--unknown-gold", action="store_true", help="agent does not know how much gold there is")
    ap.add_argument("--max-actions", type=int, default=1000)
    ap.add_argument("--quiet", action="store_true", help="only print the summary")
    args = ap.parse_args(argv)

    # Jeden generator na wszystkie gry: przy ustalonym --seed seria gier jest powtarzalna.
    rng = random.Random(args.seed)
    if args.aima:
        width, height = AIMA_WORLD.width, AIMA_WORLD.height
        # Nadpisujemy parametry, żeby statystyki odnosiły się do świata AIMA.
        args.wumpus, args.gold = len(AIMA_WORLD.wumpuses), len(AIMA_WORLD.gold)
    else:
        width = args.width or args.size
        height = args.height or args.size
    results = []
    for i in range(args.games):
        if args.aima:
            config = AIMA_WORLD
        else:
            config = generate_world(width, height, args.pits, args.wumpus, args.gold, rng=rng)
        verbose = not args.quiet
        if verbose and args.games > 1:
            print(f"\n=========== game {i + 1} ===========")
        results.append(run_game(config, args.max_actions, args.risky, not args.unknown_gold, verbose))

    if args.games > 1:
        n = len(results)
        risky_print = "(risky)" if args.risky else ""
        if args.aima:
            print(f"\n{n} games on the AIMA {width}x{height} world", risky_print)
        else:
            print(f"\n{n} games on {width}x{height}, pits {args.pits}, {args.wumpus} wumpus(es), {args.gold} gold", risky_print)
        print(f"  mean score     {sum(r.score for r in results) / n:8.1f}")
        print(f"  gold brought   {sum(r.gold for r in results if r.climbed)}/{n * args.gold}")
        print(f"  deaths         {sum(not r.alive for r in results)}")
        print(f"  mean actions   {sum(r.actions for r in results) / n:8.1f}")
        print(f"  mean time [s]  {sum(r.seconds for r in results) / n:8.3f}")


if __name__ == "__main__":
    main(sys.argv[1:])
