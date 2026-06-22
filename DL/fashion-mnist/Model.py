import pytorch_lightning as pl
import torch
import torchmetrics
import torchvision
from torch import nn


class Model(pl.LightningModule):
    def __init__(self, fold: int, dropout_rate: float, n_hidden: int, n_width: int, out_features: int, lr: float):
        super().__init__()
        self.save_hyperparameters()

        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout(dropout_rate),
            # 14x14

            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Dropout(dropout_rate),
            # 7x7
        )
        linear = [
            nn.Flatten(),
            nn.Linear(32 * 7*7, n_width),
            nn.ReLU(),
        ]
        for i in range(n_hidden):
            linear.append(nn.Linear(n_width, n_width))
            linear.append(nn.ReLU())
        linear.append(nn.Linear(n_width, out_features))
        self.fully_connected = nn.Sequential(*linear)

        self.model = nn.Sequential(
            self.conv,
            self.fully_connected,
        )

        self.loss_fn = nn.CrossEntropyLoss()

        self.accuracy = torchmetrics.Accuracy("multiclass", num_classes=out_features)

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_pred = self.forward(x)
        loss = self.loss_fn(y_pred, y)
        accuracy = self.accuracy(y_pred, y)
        self.log_dict({
            "train_loss": loss,
            "train_accuracy": accuracy,
        }, on_step=False, on_epoch=True, prog_bar=True)

        if batch_idx % 100 == 0:
            grid = torchvision.utils.make_grid(x[:64])
            self.logger.experiment.add_image("images", grid, self.global_step)

        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_pred = self.forward(x)
        loss = self.loss_fn(y_pred, y)
        accuracy = self.accuracy(y_pred, y)
        self.log_dict({
            "val_loss": loss,
            "val_accuracy": accuracy,
        }, on_step=False, on_epoch=True, prog_bar=True)
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