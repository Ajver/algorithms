"""Tests for hrv_frequency.py. Run from this directory with: pytest test_hrv_frequency.py"""
from pathlib import Path

import numpy as np
import pytest
from scipy import interpolate

from hrv_frequency import (
    FS_INTERP,
    _periodogram_classic,
    _periodogram_lombscargle,
    compute_hrv_frequency_metrics,
)

DATA_DIR = Path(__file__).parent / "data"
ALL_METHODS = [
    ("lombscargle", "linear"),
    ("classic", "nearest"),
    ("classic", "linear"),
    ("classic", "spline"),
]
KEYS = {"ULF", "VLF", "LF", "HF", "TP", "LF_HF"}


def modulated_rr(freq, amplitude=0.05, n_beats=12000, mean_rr=0.8):
    """RR series modulated by a sine, so power A^2 / 2 is expected at freq."""
    rr = np.empty(n_beats)
    t = 0.0
    for i in range(n_beats):
        rr[i] = mean_rr + amplitude * np.sin(2 * np.pi * freq * t)
        t += rr[i]
    return rr


def noise_rr(n_beats=2000, seed=0):
    return 0.8 + 0.03 * np.random.default_rng(seed).standard_normal(n_beats)


# --- Eqs. (1)-(3) from the lab instructions, written out literally ---


def literal_p(t, x, f):
    arg = 2 * np.pi * f * t
    return (np.sum(x * np.cos(arg)) ** 2 + np.sum(x * np.sin(arg)) ** 2) / len(x)


def literal_p_ls(t, x, f):
    tau = np.arctan2(np.sum(np.sin(4 * np.pi * f * t)), np.sum(np.cos(4 * np.pi * f * t))) / (4 * np.pi * f)
    arg = 2 * np.pi * f * (t - tau)
    return 0.5 * (
        np.sum(x * np.cos(arg)) ** 2 / np.sum(np.cos(arg) ** 2)
        + np.sum(x * np.sin(arg)) ** 2 / np.sum(np.sin(arg) ** 2)
    )


def test_lombscargle_matches_equations_2_and_3():
    x = noise_rr()
    t = np.cumsum(x)
    periodogram, df, fs = _periodogram_lombscargle(t, x)

    assert df == pytest.approx(1 / (t[-1] - t[0]))
    assert fs == pytest.approx(len(t) / (t[-1] - t[0]))
    assert periodogram[0] == 0
    for k in [1, 7, 100, len(periodogram) - 1]:
        expected = literal_p_ls(t - t[0], x - x.mean(), k * df)
        assert periodogram[k] == pytest.approx(expected, rel=1e-8)


@pytest.mark.parametrize("kind", ["nearest", "linear", "cubic"])
def test_classic_matches_equation_1_on_interpolated_signal(kind):
    x = noise_rr()
    t = np.cumsum(x)
    periodogram, df, fs = _periodogram_classic(t, x, kind)

    t_eq = np.arange(t[0], t[-1], 1 / FS_INTERP)
    x_eq = interpolate.interp1d(t, x, kind=kind)(t_eq)
    x_eq = x_eq - x_eq.mean()

    assert fs == FS_INTERP
    assert df == pytest.approx(FS_INTERP / len(t_eq))
    for k in [1, 50, 500]:
        assert periodogram[k] == pytest.approx(literal_p(t_eq, x_eq, k * df), rel=1e-8)


def test_classic_periodogram_area_equals_variance():
    x = noise_rr()
    t = np.cumsum(x)
    periodogram, df, fs = _periodogram_classic(t, x, "linear")

    t_eq = np.arange(t[0], t[-1], 1 / FS_INTERP)
    x_eq = interpolate.interp1d(t, x)(t_eq)
    n = len(x_eq)

    # Parseval: inner bins count twice, DC and (for even n) Nyquist once.
    weights = np.full(len(periodogram), 2.0)
    weights[0] = 1.0
    if n % 2 == 0:
        weights[-1] = 1.0
    assert np.sum(weights * periodogram) / n == pytest.approx(np.var(x_eq), rel=1e-9)


# --- Band powers ---


@pytest.mark.parametrize("method,interp", ALL_METHODS)
@pytest.mark.parametrize(
    "freq,band",
    [(0.002, "ULF"), (0.02, "VLF"), (0.1, "LF"), (0.25, "HF")],
)
def test_sine_power_lands_in_its_band(freq, band, method, interp):
    result = compute_hrv_frequency_metrics(modulated_rr(freq), method, interp)

    # A^2 / 2 in ms^2. Nearest and linear interpolation act as low-pass filters: on a grid of
    # spacing d they attenuate power by sinc^2(f * d) and sinc^4(f * d), with d = mean RR here.
    attenuation = {"nearest": 2, "linear": 4}.get(interp, 0) if method == "classic" else 0
    expected = 0.05 ** 2 / 2 * 1e6 * np.sinc(freq * 0.8) ** attenuation
    assert result[band] == pytest.approx(expected, rel=0.05)
    assert result[band] > 0.9 * result["TP"]


@pytest.mark.parametrize("method,interp", ALL_METHODS)
def test_power_scales_with_amplitude_squared(method, interp):
    small = compute_hrv_frequency_metrics(modulated_rr(0.1, amplitude=0.01), method, interp)
    large = compute_hrv_frequency_metrics(modulated_rr(0.1, amplitude=0.02), method, interp)
    assert large["LF"] / small["LF"] == pytest.approx(4, rel=0.05)


@pytest.mark.parametrize("method,interp", ALL_METHODS)
def test_tp_and_ratio_are_derived_from_bands(method, interp):
    r = compute_hrv_frequency_metrics(noise_rr(), method, interp)
    assert r["TP"] == pytest.approx(r["ULF"] + r["VLF"] + r["LF"] + r["HF"])
    assert r["LF_HF"] == pytest.approx(r["LF"] / r["HF"])


def test_lombscargle_tp_is_close_to_variance_below_cutoff():
    # White noise at about 1.25 beats/s: bands up to 0.4 Hz hold 0.4 / 0.625 of the variance.
    rr = noise_rr(n_beats=20000)
    tp = compute_hrv_frequency_metrics(rr)["TP"]
    expected = np.var(rr) * 1e6 * 0.4 / (0.5 / np.mean(rr))
    assert tp == pytest.approx(expected, rel=0.05)


# --- Output contract ---


@pytest.mark.parametrize("method,interp", ALL_METHODS)
def test_output_has_expected_keys_and_plain_floats(method, interp):
    result = compute_hrv_frequency_metrics(noise_rr(), method, interp)
    assert set(result) == KEYS
    assert all(type(value) is float for value in result.values())


def test_default_method_is_lombscargle():
    rr = noise_rr()
    assert compute_hrv_frequency_metrics(rr) == compute_hrv_frequency_metrics(rr, method="lombscargle")


def test_lombscargle_ignores_interpolation():
    rr = noise_rr()
    assert compute_hrv_frequency_metrics(rr, "lombscargle", "not-a-kind") == compute_hrv_frequency_metrics(rr)


def test_classic_default_interpolation_is_linear():
    rr = noise_rr()
    assert compute_hrv_frequency_metrics(rr, "classic") == compute_hrv_frequency_metrics(rr, "classic", "linear")


def test_interpolation_kinds_give_different_results():
    rr = noise_rr()
    hf = {kind: compute_hrv_frequency_metrics(rr, "classic", kind)["HF"] for kind in ("nearest", "linear", "spline")}
    assert len(set(hf.values())) == 3


@pytest.mark.parametrize("name,kind", [("nearest", "nearest"), ("linear", "linear"), ("spline", "cubic")])
def test_interpolation_names_map_to_expected_kinds(name, kind):
    rr = noise_rr()
    periodogram, df, fs = _periodogram_classic(np.cumsum(rr), rr, kind)
    psd = 2 * periodogram / fs * 1e6
    f = np.arange(len(psd)) * df
    expected_hf = np.sum(psd[(f >= 0.15) & (f < 0.4)]) * df

    assert compute_hrv_frequency_metrics(rr, "classic", name)["HF"] == pytest.approx(expected_hf)


def test_accepts_list_and_does_not_modify_input():
    rr = noise_rr(n_beats=300)
    original = rr.copy()
    from_array = compute_hrv_frequency_metrics(rr)
    assert np.array_equal(rr, original)
    assert compute_hrv_frequency_metrics(rr.tolist()) == from_array


@pytest.mark.parametrize("method,interp", ALL_METHODS)
def test_constant_rr_has_zero_power(method, interp):
    r = compute_hrv_frequency_metrics(np.full(500, 0.8), method, interp)
    for band in ("ULF", "VLF", "LF", "HF", "TP"):
        assert r[band] == pytest.approx(0, abs=1e-12)


def test_constant_rr_gives_nan_ratio_for_lombscargle():
    assert np.isnan(compute_hrv_frequency_metrics(np.full(500, 0.8))["LF_HF"])


@pytest.mark.parametrize("method,interp", ALL_METHODS)
def test_record_too_short_for_ulf_reports_zero_ulf(method, interp):
    r = compute_hrv_frequency_metrics(noise_rr(n_beats=100), method, interp)  # About 80 s
    assert r["ULF"] == 0
    assert r["TP"] > 0


# --- Physiological filtering ---


@pytest.mark.parametrize("artefact", [0.25, 2.5, 20.0])
def test_artefacts_are_filtered_and_later_beats_keep_their_timing(artefact):
    rr = noise_rr(n_beats=500)
    with_artefact = np.insert(rr, 250, artefact)

    # The artefact's duration must remain on the time axis, while its value is dropped.
    t = np.cumsum(with_artefact)
    keep = np.arange(len(with_artefact)) != 250
    periodogram, df, fs = _periodogram_lombscargle(t[keep], with_artefact[keep])
    psd = 2 * periodogram / fs * 1e6
    f = np.arange(len(psd)) * df
    expected_hf = np.sum(psd[(f >= 0.15) & (f < 0.4)]) * df

    assert compute_hrv_frequency_metrics(with_artefact)["HF"] == pytest.approx(expected_hf)


@pytest.mark.parametrize("edge", [0.3, 2.0])
def test_filter_range_includes_its_limits(edge):
    rr = noise_rr(n_beats=500)
    rr[250] = edge
    t = np.cumsum(rr)
    periodogram, df, fs = _periodogram_lombscargle(t, rr)
    psd = 2 * periodogram / fs * 1e6
    f = np.arange(len(psd)) * df
    expected_hf = np.sum(psd[(f >= 0.15) & (f < 0.4)]) * df

    assert compute_hrv_frequency_metrics(rr)["HF"] == pytest.approx(expected_hf)


# --- Input validation ---

@pytest.mark.parametrize(
    "bad",
    [
        [0.8, 0.8, np.nan, 0.8, 0.8],
        [0.8, 0.8, np.inf, 0.8, 0.8],
        [[0.8, 0.8], [0.8, 0.8]],
    ],
)
def test_non_finite_or_multidimensional_input_raises(bad):
    with pytest.raises(ValueError, match="1-D"):
        compute_hrv_frequency_metrics(bad)


# --- Known defects from the code review. strict=True: the test fails once the defect is fixed, ---
# --- which is the signal to remove the marker.                                                 ---


@pytest.mark.xfail(strict=True, reason="No check for too few beats after filtering")
@pytest.mark.parametrize("method,interp", ALL_METHODS)
@pytest.mark.parametrize(
    "rr",
    [
        pytest.param([], id="empty"),
        pytest.param([800.0, 810.0, 790.0, 800.0], id="milliseconds"),
        pytest.param([0.8], id="one-beat"),
        pytest.param([0.8, 0.8, 0.8], id="three-beats"),
    ],
)
def test_too_few_beats_raises_clear_error(rr, method, interp):
    with pytest.raises(ValueError, match="(?i)physiological|beats|intervals"):
        compute_hrv_frequency_metrics(rr, method, interp)


@pytest.mark.xfail(strict=True, reason="Negative RR moves the time axis backwards before it is filtered out")
def test_negative_rr_raises():
    rr = noise_rr(n_beats=500)
    rr[250] = -5.0
    with pytest.raises(ValueError):
        compute_hrv_frequency_metrics(rr)


@pytest.mark.xfail(strict=True, reason="Grid goes up to 0.4 Hz even when Nyquist of the beat rate is lower")
def test_slow_rhythm_does_not_report_more_power_than_variance():
    rr = 1.5 + 0.05 * np.random.default_rng(0).standard_normal(3000)  # 40 bpm, Nyquist about 0.33 Hz
    assert compute_hrv_frequency_metrics(rr)["TP"] <= 1.05 * np.var(rr) * 1e6


@pytest.mark.xfail(strict=True, reason="Rounding noise (about 1e-58 ms^2) makes HF > 0, so the ratio is meaningless")
@pytest.mark.parametrize("interp", ["nearest", "linear", "spline"])
def test_constant_rr_gives_nan_ratio_for_classic(interp):
    assert np.isnan(compute_hrv_frequency_metrics(np.full(500, 0.8), "classic", interp)["LF_HF"])


# --- Real recordings: values reported in raport/raport.tex ---


EXPECTED_REAL = {
    ("nsr001", "lombscargle", "linear"): (24471, 1983, 510, 253, 27218, 2.01),
    ("nsr001", "classic", "nearest"): (27651, 2194, 715, 428, 30988, 1.67),
    ("nsr001", "classic", "linear"): (27654, 2191, 700, 350, 30895, 2.00),
    ("nsr001", "classic", "spline"): (27698, 2199, 731, 488, 31117, 1.50),
    ("chf206", "lombscargle", "linear"): (1660, 138, 93, 198, 2089, 0.47),
    ("chf206", "classic", "nearest"): (1251, 155, 233, 393, 2033, 0.59),
    ("chf206", "classic", "linear"): (1251, 153, 218, 292, 1915, 0.75),
    ("chf206", "classic", "spline"): (1258, 248, 369, 548, 2424, 0.67),
}


@pytest.fixture(scope="module")
def real_rr():
    return {name: np.loadtxt(DATA_DIR / f"{name}.dat") for name in ("nsr001", "chf206")}


@pytest.mark.parametrize("name,method,interp", EXPECTED_REAL)
def test_real_recordings_match_report_table(real_rr, name, method, interp):
    r = compute_hrv_frequency_metrics(real_rr[name], method, interp)
    actual = [r[key] for key in ("ULF", "VLF", "LF", "HF", "TP")]
    expected = EXPECTED_REAL[name, method, interp]

    assert actual == pytest.approx(expected[:5], abs=0.51)  # The table is rounded to integers
    assert r["LF_HF"] == pytest.approx(expected[5], abs=0.0051)
