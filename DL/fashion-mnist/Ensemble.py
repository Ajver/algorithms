import json
from pathlib import Path

import torch
from torch import nn

from Model import Model, ModelParams
from TemperatureScaler import TemperatureScaler

OUT_FEATURES = 10


class Ensemble(nn.Module):
    def __init__(self, run_dir: Path):
        super().__init__()

        with open(run_dir / "model_params.json", "r") as f:
            s = f.read()
            model_params = ModelParams(**json.loads(s))

        models = []
        scalers = []
        for fold_dir in run_dir.iterdir():
            if not fold_dir.is_dir():
                continue

            fold = int(fold_dir.name[-1])
            model_path = next(fold_dir.iterdir())
            print(f"Model for {fold=}:", model_path)

            model = Model(fold, OUT_FEATURES, model_params)
            checkpoint_state = torch.load(model_path)
            model.load_state_dict(checkpoint_state["state_dict"])

            scaler = TemperatureScaler(model)
            scaler.temperature = torch.load(fold_dir/"temperature.pt")
            print(f"Temperature for {fold=}:", scaler.temperature.item())

            models.append(model)
            scalers.append(scaler)

        self.models = nn.ModuleList(models)
        self.scalers = nn.ModuleList(scalers)

        self.eval()

    def predict_proba_all(self, x: torch.Tensor, scale_temperature: bool = True) -> torch.Tensor:
        if scale_temperature:
            models_arr = self.scalers
        else:
            models_arr = self.models

        proba_all = torch.zeros(len(self.scalers), x.shape[0], OUT_FEATURES)

        for fold, model in enumerate(models_arr):
            logits = model(x)
            proba = torch.softmax(logits, dim=-1)
            proba_all[fold] = proba

        return proba_all

    def predict_proba(self, x: torch.Tensor, scale_temperature: bool = True) -> torch.Tensor:
        proba_all = self.predict_proba_all(x, scale_temperature)
        proba = torch.mean(proba_all, dim=0)
        return proba

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        proba_all = self.predict_proba_all(x)
        all_preds = torch.argmax(proba_all, dim=-1)
        majority_votes, _ = torch.mode(all_preds, dim=0)
        return majority_votes
