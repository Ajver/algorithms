import torch
from torch import nn

from Model import Model


class TemperatureScaler(nn.Module):
    def __init__(self, model: Model):
        super().__init__()
        self.model = model
        model.eval()
        self.temperature = nn.Parameter(torch.ones(1))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        logits = self.model(x)
        return self.scale(logits)

    def scale(self, logits: torch.Tensor) -> torch.Tensor:
        return logits / self.temperature
