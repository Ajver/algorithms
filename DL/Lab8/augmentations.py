import torch
import torch.nn as nn
from torchvision import transforms
import torchaudio


class AddRandomNoise(nn.Module):
    def __init__(self, min_snr: float, max_snr: float):
        super().__init__()
        self.min_snr = min_snr
        self.max_snr = max_snr

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        noise_level = torch.empty(1).uniform_(self.min_snr, self.max_snr).item()
        noise = torch.randn_like(waveform) * noise_level
        return waveform + noise


class RandomSpeedPitchShift(nn.Module):
    def __init__(self, sample_rate: int, min_steps: int, max_steps: int):
        super().__init__()
        self.sample_rate = sample_rate
        self.min_steps = min_steps
        self.max_steps = max_steps

        # Pre-build one resampler per possible n_steps — kernel computed once here,
        # cached as a buffer, moved to GPU with .to(device) / .cuda()
        self.resamplers = nn.ModuleDict()
        for n_steps in range(min_steps, max_steps + 1):
            if n_steps == 0:
                continue
            factor = 2.0 ** (n_steps / 12.0)
            orig_freq = round(sample_rate * factor)   # round, not int-truncate
            self.resamplers[str(n_steps)] = torchaudio.transforms.Resample(
                orig_freq=orig_freq,
                new_freq=sample_rate,
            )

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        print("START")
        n_steps = torch.randint(self.min_steps, self.max_steps + 1, (1,)).item()
        if n_steps == 0:
            print("early exit")
            return waveform

        orig_len = waveform.size(-1)
        augmented = self.resamplers[str(n_steps)](waveform)  # kernel already on GPU

        resampled_len = augmented.size(-1)
        print(f"{augmented.shape=}")

        diff = orig_len - resampled_len
        if diff > 0:
            pad_left = diff // 2
            augmented = nn.functional.pad(
                augmented, (pad_left, diff - pad_left), value=0.0
            )
        elif diff < 0:
            crop_left = (-diff) // 2
            augmented = augmented[..., crop_left : crop_left + orig_len]

        return augmented


audio_transform = nn.Sequential(
    transforms.RandomApply([
        AddRandomNoise(min_snr=0.001, max_snr=0.008)
    ], p=0.5),
    transforms.RandomApply([
        RandomSpeedPitchShift(sample_rate=8000, min_steps=-3, max_steps=3)
    ], p=0.5),
)
