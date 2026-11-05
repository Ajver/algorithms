import numpy as np
from scipy import interpolate

# RR intervals outside this range (HR of 30-200 bpm) are treated as acquisition errors.
PHYSIO_RR = (0.3, 2.0)  # s

FS_INTERP = 4.0

F_MAX = 0.4  # Hz, upper limit of the HF band

INTERPOLATION_KINDS = {"nearest": "nearest", "linear": "linear", "spline": "cubic"}


def _periodogram_classic(t, x, kind):
    t_eq = np.arange(t[0], t[-1], 1 / FS_INTERP)
    x_eq = interpolate.interp1d(t, x, kind=kind)(t_eq)
    x_eq = x_eq - np.mean(x_eq)

    periodogram = np.abs(np.fft.rfft(x_eq)) ** 2 / len(x_eq)
    return periodogram, FS_INTERP / len(x_eq), FS_INTERP


def _periodogram_lombscargle(t, x):
    T = t[-1] - t[0]
    df = 1 / T
    n_freqs = int(np.ceil(F_MAX / df))
    N = len(t)
    t = t - t[0]
    x = x - np.mean(x)

    z_step = np.exp(2j * np.pi * df * t)
    z = np.ones(N, dtype=complex)

    periodogram = np.zeros(n_freqs + 1)
    for k in range(1, n_freqs + 1):
        z *= z_step

        w = np.sum(z * z)
        rotated = np.sum(x * z) * np.exp(-0.5j * np.angle(w))

        sum_cos_sq = (N + np.abs(w)) / 2
        sum_sin_sq = (N - np.abs(w)) / 2

        power = rotated.real ** 2 / sum_cos_sq
        if sum_sin_sq > 1e-9 * N:
            power += rotated.imag ** 2 / sum_sin_sq
        periodogram[k] = 0.5 * power

    return periodogram, df, N / T


def compute_hrv_frequency_metrics(
    rr_intervals,
    method="lombscargle",
    interpolation="linear"
):
    """
    Parametry
    ----------
    rr_intervals : array_like
        Kolejne odstępy RR [s]

    method : str
        Metoda estymacji widma:
        - "classic"
        - "lombscargle"

    interpolation : str
        Wykorzystywana wyłącznie dla method="classic":
        - "nearest"
        - "linear"
        - "spline"

    Zwraca
    -------
    dict
        {
            "ULF": float,
            "VLF": float,
            "LF": float,
            "HF": float,
            "TP": float,
            "LF_HF": float
        }

        Moce pasm oraz TP = ULF + VLF + LF + HF są wyrażone w ms².
        Moc pasma, którego nie obejmuje siatka częstotliwości (zbyt krótki
        zapis), wynosi 0. Gdy HF = 0, LF_HF to NaN.

    """
    rr = np.asarray(rr_intervals, dtype=float)
    if rr.ndim != 1 or not np.all(np.isfinite(rr)):
        raise ValueError("rr_intervals must be a 1-D array of finite values")

    # Calculate cumsum BEFORE filtering, to keep correct timings
    t = np.cumsum(rr)
    physio_idx = (rr >= PHYSIO_RR[0]) & (rr <= PHYSIO_RR[1])
    rr = rr[physio_idx]
    t = t[physio_idx]

    if method == "classic":
        periodogram, df, fs = _periodogram_classic(t, rr, INTERPOLATION_KINDS[interpolation])
    else:
        periodogram, df, fs = _periodogram_lombscargle(t, rr)

    psd = 2 * periodogram / fs * 1e6
    f = np.arange(len(psd)) * df

    # Task Force (1996) bands [Hz]
    ulf_mask = (f > 0) & (f < 0.003)
    vlf_mask = (f >= 0.003) & (f < 0.04)
    lf_mask = (f >= 0.04) & (f < 0.15)
    hf_mask = (f >= 0.15) & (f < F_MAX)

    # With bins of width df the area under the PSD is a plain sum
    ulf = float(np.sum(psd[ulf_mask]) * df)
    vlf = float(np.sum(psd[vlf_mask]) * df)
    lf = float(np.sum(psd[lf_mask]) * df)
    hf = float(np.sum(psd[hf_mask]) * df)

    tp = ulf + vlf + lf + hf
    lf_hf = lf / hf if hf > 0 else float("nan")

    return {
        "ULF": ulf,
        "VLF": vlf,
        "LF": lf,
        "HF": hf,
        "TP": tp,
        "LF_HF": lf_hf,
    }
