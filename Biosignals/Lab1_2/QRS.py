import numpy as np


def create_hamming(N):
    n = np.arange(N)
    hamming = 0.54 - 0.46 * np.cos(2 * np.pi * n / (N - 1))
    return hamming

def create_lowpass(M, fs):
    fc = 15
    fc_hat = fc / fs
    lowpass = np.zeros(2*M + 1)

    for i in range(2*M + 1):
        n = i - M
        if n == 0:
            lowpass[i] = 2 * fc_hat
        else:
            lowpass[i] = np.sin(2*np.pi*fc_hat*n) / (np.pi * n)

    lowpass *= create_hamming(2*M + 1)
    return lowpass

def create_highpass(M, fs):
    fc = 5
    fc_hat = fc / fs
    highpass = np.zeros(2*M + 1)

    for i in range(2*M + 1):
        n = i - M
        if n == 0:
            highpass[i] = 1 - 2*fc_hat
        else:
            highpass[i] = -np.sin(2*np.pi*fc_hat*n) / (np.pi * n)

    highpass *= create_hamming(2*M + 1)
    return highpass

def differentiate(x):
    kernel = -np.array([-1, -2, 0, 2, 1]) / 8.0
    return np.convolve(x, kernel, mode="same")

def integrate(x, C):
    return np.convolve(x, np.ones(C), mode="same") / C


def detect_r_peaks(ecg, fs):
    M = 20

    signal = np.convolve(ecg, create_lowpass(M, fs), mode="same")
    signal = np.convolve(signal, create_highpass(M, fs), mode="same")

    diff = differentiate(signal)

    squared = diff**2

    C = int(0.15 * fs)
    integrated = integrate(squared, C)

    diff_integrated = differentiate(integrated)
    zero_crossings = np.where((diff_integrated[:-1] > 0) & (diff_integrated[1:] < 0))[0]

    # Inicjalizacja progów na podstawie pierwszych sekund scałkowanego sygnału
    init_chunk = integrated[: min(len(integrated), fs * 2)]
    SPKI = np.max(init_chunk) * 0.35 if len(init_chunk) > 0 else 0.1
    NPKI = SPKI * 0.1
    THRESHOLD_I1 = NPKI + 0.25 * (SPKI-NPKI)
    THRESHOLD_I2 = 0.5 * THRESHOLD_I1
    print(f"{THRESHOLD_I1=}, {THRESHOLD_I2=}")

    integrated_peaks = []
    for peak_i in zero_crossings:
        value = integrated[peak_i]
        if value >= THRESHOLD_I1:
            # Signal peak
            SPKI = 0.125 * value + 0.875 * SPKI
            # print(f"{SPKI=}")
            integrated_peaks.append(peak_i)

            THRESHOLD_I1 = NPKI + 0.25 * (SPKI-NPKI)
            THRESHOLD_I2 = 0.5 * THRESHOLD_I1
            # print(f"{THRESHOLD_I1=}, {THRESHOLD_I2=}")
        elif value >= THRESHOLD_I2:
            # Noise peak
            NPKI = 0.125 * value + 0.875 * NPKI
            # print(f"{NPKI=}")

            THRESHOLD_I1 = NPKI + 0.25 * (SPKI-NPKI)
            THRESHOLD_I2 = 0.5 * THRESHOLD_I1
            # print(f"{THRESHOLD_I1=}, {THRESHOLD_I2=}")

    integrated_peaks = np.array(integrated_peaks, dtype=int)

    signal_peaks = []
    search_window = int(0.1 * fs)

    for peak in integrated_peaks:
        left = max(0, peak - search_window)
        right = min(len(signal), peak + search_window)
        real_r = left + np.argmax(ecg[left:right])
        signal_peaks.append(real_r)

    signal_peaks = np.array(signal_peaks, dtype=int)

    # too_close_peaks = np.where(signal_peaks[1:] - signal_peaks[:-1] < MIN_DISTANCE_INDICES)[0] + 1
    # while too_close_peaks.shape[0] > 0:
    #     signal_peaks = np.delete(signal_peaks, too_close_peaks[0])
    #     too_close_peaks = np.where(signal_peaks[1:] - signal_peaks[:-1] < MIN_DISTANCE_INDICES)[0] + 1

    MIN_DISTANCE_S = 0.2
    MIN_DISTANCE_INDICES = fs * MIN_DISTANCE_S
    print(f"{MIN_DISTANCE_INDICES=}")
    if len(signal_peaks) > 0:
        cleaned_peaks = [signal_peaks[0]]
        for p in signal_peaks[1:]:
            if p - cleaned_peaks[-1] >= MIN_DISTANCE_INDICES:
                cleaned_peaks.append(p)
        signal_peaks = np.array(cleaned_peaks, dtype=int)

    return signal_peaks


def evaluate_detections(signal_peaks, gt_peaks, fs):
    tolerance_samples_ms = 30
    tolerance_samples = int(fs * (tolerance_samples_ms / 1000.))
    print(f"{tolerance_samples=}")

    unmatched_detected = list(signal_peaks)

    tp_errors_samples = []
    matched_gt = []
    matched_det = []

    for gt in gt_peaks:
        if len(unmatched_detected) == 0:
            break

        distances = np.abs(np.array(unmatched_detected) - gt)
        min_idx = np.argmin(distances)
        min_dist = distances[min_idx]

        if min_dist <= tolerance_samples:
            closest_det = unmatched_detected.pop(min_idx)

            tp_errors_samples.append(closest_det - gt)
            matched_gt.append(gt)
            matched_det.append(closest_det)

    TP = len(tp_errors_samples)

    FN = len(gt_peaks) - TP

    FP = len(signal_peaks) - TP

    errors_ms = (np.array(tp_errors_samples) / fs) * 1000.0

    if TP > 0:
        mae = np.mean(np.abs(errors_ms))
        sd = np.std(errors_ms)
    else:
        mae, sd = 0.0, 0.0

    metrics = {
        "TP": TP,
        "FP": FP,
        "FN": FN,
        "agreement": TP / (TP + FN + FP),
        "MAE_ms": mae,
        "SD_ms": sd,
        "errors_ms": errors_ms,
        "matched_gt": np.array(matched_gt),
        "matched_det": np.array(matched_det),
    }

    return metrics

