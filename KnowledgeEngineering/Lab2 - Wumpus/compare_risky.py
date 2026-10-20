from simulate import main

argv = [
    "--quiet",
    "--size", "8",
    "--pits", "0.15",
    "--wumpus", "2",
    "--seed", "3",
    "--max-actions", "30",
    "--games", "100",
]
main(argv)
main(argv + ["--risky"])
