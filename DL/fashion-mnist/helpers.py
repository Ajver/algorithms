from pathlib import Path

CHECKPOINTS_DIR = Path("./checkpoints")


def get_latest_run_dir() -> Path:
    run_dates = []
    for run_folder in CHECKPOINTS_DIR.iterdir():
        if run_folder.is_dir() and run_folder.name.startswith("run_"):
            run_date = run_folder.name[len("run_"):]
            run_dates.append(run_date)

    run_dates = sorted(run_dates)
    print(run_dates)

    latest_run = run_dates[-1]
    print("Latest run:", latest_run)

    latest_run_dir = CHECKPOINTS_DIR / f"run_{latest_run}"
    print("Latest run dir:", latest_run_dir)
    return latest_run_dir
