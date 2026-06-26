from pathlib import Path

import numpy as np

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


def compute_entropy(probs):
    return -np.sum(probs * np.log2(probs + 1e-12), axis=-1)


def compute_uncertainties(proba_all: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean_probs = np.mean(proba_all, axis=0)

    total_uncertainty = compute_entropy(mean_probs)
    aleatoric_uncertainty = np.mean(compute_entropy(proba_all), axis=0)
    epistemic_uncertainty = total_uncertainty - aleatoric_uncertainty

    return total_uncertainty, aleatoric_uncertainty, epistemic_uncertainty
