import pickle

import pandas as pd
from fastmlapi import MLController, preprocessing, postprocessing
import numpy as np

COLUMNS = ['radius', 'texture', 'area', 'smoothness', 'compactness', 'symmetry']


class MLAPIServer(MLController):
    model_name = "my-classifier"
    model_version = "1.0.0"

    def load_model(self):
        model = pickle.load(open("best_model.pkl", "rb"))
        return model

    @preprocessing
    def preprocess(self, data: list[list[float]]) -> pd.DataFrame:
        X = pd.DataFrame(data=data, columns=COLUMNS, dtype=np.float32)
        return X

    @postprocessing
    def postprocess(self, prediction: np.ndarray) -> list:
        response = prediction.tolist()
        return response


if __name__ == "__main__":
    MLAPIServer().run()