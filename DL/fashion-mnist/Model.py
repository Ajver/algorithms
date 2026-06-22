import pytorch_lightning as pl
import torch
import torchmetrics
from sklearn.metrics import accuracy_score
from torch import nn


class Model(pl.LightningModule):
    def __init__(self, n_hidden: int, n_width: int, out_features: int, lr: float):
        super().__init__()
        self.save_hyperparameters()

        self.model = nn.Sequential(
            nn.Linear(28 * 28, n_width),
            nn.ReLU(),
            nn.Linear(n_width, out_features),
        )

        self.loss_fn = nn.CrossEntropyLoss()

        self.accuracy = torchmetrics.Accuracy("multiclass", num_classes=out_features)

    def forward(self, x):
        x = x.reshape(-1, 28 * 28)  # for linear input layer
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_pred = self.forward(x)
        loss = self.loss_fn(y_pred, y)
        accuracy = self.accuracy(y_pred, y)
        self.log_dict({
            "train_loss": loss,
            "train_accuracy": accuracy,
        }, on_step=False, on_epoch=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_pred = self.forward(x)
        loss = self.loss_fn(y_pred, y)
        accuracy = self.accuracy(y_pred, y)
        self.log_dict({
            "val_loss": loss,
            "val_accuracy": accuracy,
        }, on_step=False, on_epoch=True)
        return loss

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_pred = self.forward(x)
        loss = self.loss_fn(y_pred, y)
        accuracy = self.accuracy(y_pred, y)
        self.log_dict({
            "val_loss": loss,
            "val_accuracy": accuracy,
        }, on_step=False, on_epoch=True)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)