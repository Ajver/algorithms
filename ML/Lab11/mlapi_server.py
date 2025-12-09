import pickle

import pandas as pd
from fastmlapi import MLController, preprocessing, postprocessing
import numpy as np

COLUMNS = ['radius', 'texture', 'area', 'smoothness', 'compactness', 'symmetry']

"""  Example request body
{
	"data": [
        [18,13,409,0.095,0.055,0.192],
        [11,11,466,0.088,0.094,0.193],
        [10,24,645,0.105,0.187,0.225],
        [11,11,1104,0.091,0.219,0.231],
        [17,21,503,0.098,0.052,0.159]
	]
}
"""


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