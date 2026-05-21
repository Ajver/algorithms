import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.transforms import Compose
import torchaudio.functional as F


class Gain(nn.Module):
    def __init__(self, min_gain: float, max_gain: float):
        super().__init__()
        self.min_gain = min_gain
        self.max_gain = max_gain

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        gain = torch.empty(1, device=x.device, dtype=x.dtype).uniform_(self.min_gain, self.max_gain)
        return x * gain


class Noise(nn.Module):
    def __init__(self, min_snr: float, max_snr: float):
        super().__init__()
        self.min_snr = min_snr
        self.max_snr = max_snr

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        signal_power = torch.mean(x ** 2)
        snr = torch.empty(1, device=x.device, dtype=x.dtype).uniform_(self.min_snr, self.max_snr)

        noise_power = signal_power * snr
        noise = torch.randn_like(x) * torch.sqrt(noise_power)
        return x + noise


class PitchShift(nn.Module):
    def __init__(self, sample_rate: int, min_steps: int, max_steps: int):
        super().__init__()
        self.sample_rate = sample_rate
        self.min_steps = min_steps
        self.max_steps = max_steps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Determine the target steps (must be an integer for pitch shifting)
        # We use torch.randint to get a separate target per forward pass
        steps = torch.randint(self.min_steps, self.max_steps + 1, (1,)).item()

        if steps == 0:
            return x

        return F.pitch_shift(x, self.sample_rate, steps)


class FadeIn(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        fade_ramp = torch.linspace(0.0, 1.0, steps=x.shape[-1], device=x.device)
        return x * fade_ramp


class FadeOut(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        fade_ramp = torch.linspace(1.0, 0.0, steps=x.shape[-1], device=x.device)
        return x * fade_ramp


audio_transform = Compose([
    transforms.RandomApply([Gain(min_gain=0.5, max_gain=1.5)], p=0.5),
    transforms.RandomApply([Noise(min_snr=0.001, max_snr=0.010)], p=0.2),
    # transforms.RandomApply([PitchShift(sample_rate=8000, min_steps=-4, max_steps=4)], p=0.3),
    transforms.RandomApply([FadeIn()], p=0.3),
    transforms.RandomApply([FadeOut()], p=0.3),
])
