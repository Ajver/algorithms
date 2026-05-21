from torch import nn


class SpeachClassifierModel(nn.Module):
    def __init__(self, dropout_rate: float, output_classes: int = 10):
        super().__init__()

        self.model = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=8, kernel_size=65, padding=32),
            nn.BatchNorm1d(8),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=3),
            nn.Dropout(dropout_rate),

            nn.Conv1d(in_channels=8, out_channels=16, kernel_size=11, padding=5),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=3),
            nn.Dropout(dropout_rate),

            nn.Conv1d(in_channels=16, out_channels=32, kernel_size=7, padding=3),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=3),
            nn.Dropout(dropout_rate),

            nn.Conv1d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=3),
            nn.Dropout(dropout_rate),

            nn.Flatten(),

            nn.Linear(64 * 98, 256),
            nn.ReLU(),
            nn.Dropout(dropout_rate),

            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(dropout_rate),

            nn.Linear(128, output_classes),
        )

    def forward(self, x):
        x = self.model(x)
        return x
