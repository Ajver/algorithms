from pathlib import Path

import librosa
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset


class CustomSpeachDataset(Dataset):
    def __init__(self, dataset_dir: Path, preload: bool = False) -> None:
        self.dataset_dir = dataset_dir
        self.preload = preload

        if self.preload:
            print("Preloading dataset from disk...")

        labels_num_samples_path = self.dataset_dir / "labels_num_samples.csv"
        df = pd.read_csv(labels_num_samples_path)
        self.LABEL_NAMES = df["label"].to_numpy(dtype=str)
        self.label_counts = df["num_samples"].to_numpy(dtype=int)

        self.X = []
        self._filepaths = []
        self.y = []
        for label_folder in self.dataset_dir.iterdir():
            if not label_folder.is_dir():
                continue

            for file in label_folder.iterdir():
                if self.preload:
                    self.X.append(self._load_file(file))
                self._filepaths.append(file)
                self.y.append(np.argwhere(self.LABEL_NAMES == label_folder.name).item())

        self.X = torch.stack(self.X)
        self._filepaths = np.array(self._filepaths, dtype=str)
        self.y = torch.tensor(self.y, dtype=torch.long)

    def __len__(self) -> int:
        return self._filepaths.shape[0]

    def __getitem__(self, idx) -> tuple[torch.Tensor, torch.Tensor]:
        y = self.y[idx]

        if self.preload:
            x = self.X[idx]
            return x, y

        filepath = self._filepaths[idx]

        if isinstance(filepath, str):
            x = self._load_file(filepath)
            return x, y
        else:
            # idx is a list of indices
            X = torch.stack([self._load_file(one_file) for one_file in filepath])
            return X, y

    def _load_file(self, filepath: str|Path) -> torch.Tensor:
        samples, _ = librosa.load(filepath, sr=8_000)
        x = torch.tensor(samples).reshape(1, 8000)
        return x

# tests
# dataset = CustomSpeachDataset(Path("preprocessed_dataset"))
# print(len(dataset))
# print(dataset.y[1000:1005])
# print(dataset[0])
# print(dataset[[0, 1]])

