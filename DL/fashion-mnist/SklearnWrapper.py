import torch
from sklearn.base import ClassifierMixin, BaseEstimator

from Ensemble import Ensemble


class SklearnWrapper(ClassifierMixin, BaseEstimator):
    def __init__(self, ensemble: Ensemble):
        self.ensemble = ensemble
        self.ensemble.eval()

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.ensemble.to(device)

    def fit(self, X, y):
        raise NotImplementedError()

    def _to_tensor(self, X) -> torch.Tensor:
        if not torch.is_tensor(X):
            X = torch.tensor(X)

        X = X.reshape(-1, 1, 28, 28)
        X = X.to(self.device)
        return X

    def predict(self, X):
        with torch.no_grad():
            X = self._to_tensor(X)
            return self.ensemble(X)

    def predict_proba(self, X):
        with torch.no_grad():
            X = self._to_tensor(X)
            return self.ensemble.predict_proba(X)

    @property
    def device(self):
        return next(self.ensemble.parameters()).device
