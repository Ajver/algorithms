from pathlib import Path

import kagglehub
import pandas as pd
import pytorch_lightning as pl
import torch
from sklearn.model_selection import StratifiedKFold
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.data.dataset import Subset


class Datamodule(pl.LightningDataModule):
    def __init__(self):
        super().__init__()

        self.test_dataset = None
        self.cv = StratifiedKFold(n_splits=5, shuffle=True)

        self.dataset_path = None

        self.train_val_dataset = None
        self.test_dataset = None

        # For stratified k-fold split
        self.y_train_val = None

    def prepare_data(self):
        dataset_path = kagglehub.dataset_download("zalando-research/fashionmnist")
        self.dataset_path = Path(dataset_path)

    def setup(self, stage):
        train_df = pd.read_csv(self.dataset_path / "fashion-mnist_train.csv")
        test_df = pd.read_csv(self.dataset_path / "fashion-mnist_test.csv")

        X_train_val = _df_to_X(train_df)
        X_test = _df_to_X(test_df)

        self.y_train_val = torch.tensor(train_df["label"].values, dtype=torch.long)
        y_test = torch.tensor(test_df["label"].values, dtype=torch.long)

        self.train_val_dataset = TensorDataset(X_train_val, self.y_train_val)
        self.test_dataset = TensorDataset(X_test, y_test)

    def cv_train_val_splits(self) -> list[tuple[int, DataLoader, DataLoader]]:
        to_return = []
        for fold, (train_idx, val_idx) in enumerate(self.cv.split(self.y_train_val, self.y_train_val)):
            train_loader = DataLoader(Subset(self.train_val_dataset, train_idx), batch_size=256, shuffle=True)
            val_loader = DataLoader(Subset(self.train_val_dataset, val_idx), batch_size=512, shuffle=False)
            tpl = (fold, train_loader, val_loader)
            to_return.append(tpl)

        return to_return

    def test_dataloader(self) -> DataLoader:
        return DataLoader(self.test_dataset, batch_size=512, shuffle=False)


def _df_to_X(df: pd.DataFrame) -> torch.Tensor:
    X = df.drop("label", axis=1).to_numpy(dtype=float)
    X = torch.tensor(X, dtype=torch.float32)
    X = X / 255.0
    X = X.reshape(-1, 1, 28, 28)
    return X
