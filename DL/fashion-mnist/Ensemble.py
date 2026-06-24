import json
from pathlib import Path

import torch
from torch import nn

from Model import Model, ModelParams

OUT_FEATURES = 10


class Ensemble(nn.Module):
    def __init__(self, run_dir: Path):
        super().__init__()

        with open(run_dir / "model_params.json", "r") as f:
            s = f.read()
            model_params = ModelParams(**json.loads(s))

        models = []
        for fold_dir in run_dir.iterdir():
            if not fold_dir.is_dir():
                continue

            fold = int(fold_dir.name[-1])
            model_path = next(fold_dir.iterdir())
            print(f"Model for {fold=}:", model_path)

            model = Model(fold, OUT_FEATURES, model_params)
            checkpoint_state = torch.load(model_path)
            model.load_state_dict(checkpoint_state["state_dict"])
            models.append(model)

        self.models = nn.ModuleList(models)
