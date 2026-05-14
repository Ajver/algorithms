from torch import nn


class SpeachClassifierModel(nn.Module):
    def __init__(self, dropout_rate: float):
        super().__init__()

        self.model = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=8, kernel_size=13, padding="valid"),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=3),
            nn.Dropout(dropout_rate),

            nn.Conv1d(in_channels=8, out_channels=16, kernel_size=11, padding="valid"),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=3),
            nn.Dropout(dropout_rate),

            nn.Conv1d(in_channels=16, out_channels=32, kernel_size=9, padding="valid"),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=3),
            nn.Dropout(dropout_rate),

            nn.Conv1d(in_channels=32, out_channels=64, kernel_size=7, padding="valid"),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=3),
            nn.Dropout(dropout_rate),

            nn.Flatten(),

            nn.Linear(6080, 256),
            nn.ReLU(),
            nn.Dropout(dropout_rate),

            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(dropout_rate),

            nn.Linear(128, 10),
        )

    def forward(self, x):
        x = self.model(x)
        return x
