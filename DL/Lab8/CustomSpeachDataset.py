from pathlib import Path

import librosa
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset


class CustomSpeachDataset(Dataset):
    def __init__(self, dataset_dir: Path) -> None:
        self.dataset_dir = dataset_dir

        labels_num_samples_path = self.dataset_dir / "labels_num_samples.csv"
        df = pd.read_csv(labels_num_samples_path)
        self.LABEL_NAMES = df["label"].to_numpy(dtype=str)
        self.label_counts = df["num_samples"].to_numpy(dtype=int)

        self._filepaths = []
        self.y = []
        for label_folder in self.dataset_dir.iterdir():
            if not label_folder.is_dir():
                continue

            for file in label_folder.iterdir():
                self._filepaths.append(file)
                self.y.append(np.argwhere(self.LABEL_NAMES == label_folder.name).item())

        self._filepaths = np.array(self._filepaths, dtype=str)
        self.y = np.array(self.y, dtype=int)

    def __len__(self) -> int:
        return self._filepaths.shape[0]

    def __getitem__(self, idx):
        filepath = self._filepaths[idx]
        y = self.y[idx]

        if isinstance(filepath, str):
            samples, _ = librosa.load(filepath, sr=8_000)
            x = torch.tensor(samples)
            return x, y
        else:
            # idx is a list of indices
            X = torch.stack([torch.tensor(librosa.load(one_file, sr=8_000)[0]) for one_file in filepath])
            return X, y


# tests
# dataset = CustomSpeachDataset(Path("preprocessed_dataset"))
# print(len(dataset))
# print(dataset.y[1000:1005])
# print(dataset[[0, 1]])

