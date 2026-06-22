import pytorch_lightning as pl
import torch
from sklearn.metrics import accuracy_score
from torch import nn


class Model(pl.LightningModule):
    def __init__(self, n_hidden: int, n_width: int, lr: float):
        super().__init__()

        self.model = nn.Sequential(
            nn.Linear(28 * 28, n_width),
            nn.ReLU(),
            nn.Linear(n_width, 10),
        )

        self.loss_fn = nn.CrossEntropyLoss()

    def forward(self, x):
        x = x.reshape(-1, 28 * 28)  # for linear input layer
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_pred = self.forward(x)
        loss = self.loss_fn(y_pred, y)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_pred = self.forward(x)
        loss = self.loss_fn(y_pred, y)
        self.log("val_loss", loss)

        accuracy = self.score(y_pred, y)
        self.log("val_accuracy", accuracy)
        return loss

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_pred = self.forward(x)
        loss = self.loss_fn(y_pred, y)
        self.log("test_loss", loss)
        return loss

    def score(self, y_pred, y_true) -> float:
        accuracy = accuracy_score(y_true, y_pred)
        return accuracy

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)