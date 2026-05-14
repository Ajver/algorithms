from torch import nn


class SpeachClassifierModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.model = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=8, kernel_size=13),
            nn.MaxPool1d(kernel_size=3),
            nn.Dropout(0.3),

            nn.Conv1d(in_channels=8, out_channels=16, kernel_size=11),
            nn.MaxPool1d(kernel_size=3),
            nn.Dropout(0.3),

            nn.Conv1d(in_channels=16, out_channels=32, kernel_size=9),
            nn.MaxPool1d(kernel_size=3),
            nn.Dropout(0.3),

            nn.Conv1d(in_channels=32, out_channels=64, kernel_size=7),
            nn.MaxPool1d(kernel_size=3),
            nn.Dropout(0.3),

            nn.Flatten(),
            nn.Linear(6080, 256),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.Dropout(0.3),

            nn.Linear(128, 10),
        )

    def forward(self, x):
        x = self.model(x)
        return x
