from pathlib import Path

import torch
from torch import nn

from SpeachClassifierModel import SpeachClassifierModel


class Ensemble(nn.Module):
    def __init__(self, models_dir: Path):
        super().__init__()

        self.model_params = torch.load(models_dir/"model_params.pth")

        device = "cuda" if torch.cuda.is_available() else "cpu"

        models = []
        for model_path in models_dir.iterdir():
            if model_path.name.startswith("fold"):
                model = SpeachClassifierModel(self.model_params["dropout_rate"])
                model.load_state_dict(torch.load(model_path, map_location=device))
                models.append(model)

        self.models = nn.ModuleList(models)

    def forward(self, x):
        ensemble_probs = self.predict_each_model(x).mean(dim=0)
        return ensemble_probs

    def predict_each_model(self, x):
        all_probs = []

        for model in self.models:
            logits = model(x)
            probs = nn.functional.softmax(logits, dim=1)
            all_probs.append(probs)

        ensemble_probs = torch.stack(all_probs)
        return ensemble_probs

    def majority_vote(self, x) -> tuple[torch.Tensor, torch.Tensor]:
        all_outputs = torch.stack([model(x) for model in self.models], dim=0)
        all_preds = torch.argmax(all_outputs, dim=-1)
        majority_votes, _ = torch.mode(all_preds, dim=0)

        num_classes = 10

        vote_counts = nn.functional.one_hot(all_preds, num_classes=num_classes).sum(dim=0).float()

        num_models = len(self.models)

        probs = vote_counts / num_models
        entropy = -torch.sum(probs * torch.log2(probs + 1e-9), dim=1)
        max_entropy = torch.log2(torch.tensor(float(num_models), device=x.device))

        confidence = 1.0 - (entropy / (max_entropy + 1e-9))
        return majority_votes, confidence


# Testing
# ensemble = Ensemble(Path("checkpoints/training"))
#
# dataset = CustomSpeachDataset(Path("preprocessed_dataset"))
#
# X, y = dataset[[0, 1, 2]]
# print(ensemble(X))
# print(y)
