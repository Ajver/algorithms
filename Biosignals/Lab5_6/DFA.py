import numpy as np

# Physiologically acceptable range of HR and distances between R.
# Signals outside of it are treated like acquisition error and filtered out.
PHYSIO_HR = np.array([30, 200])
PHYSIO_RR = (60 / PHYSIO_HR)[::-1]


def filter_physio(RR_raw):
    """
    Usuwa interwały RR spoza zakresu fizjologicznego.

    Zwraca przefiltrowane interwały RR oraz odpowiadające im czasy uderzeń.
    """
    # Calculate cumsum BEFORE filtering, to keep correct timings
    RR_t_raw = np.cumsum(RR_raw)

    # Filter out non-physiological
    physio_idx = (RR_raw >= PHYSIO_RR[0]) & (RR_raw <= PHYSIO_RR[1])
    RR = RR_raw[physio_idx]
    RR_t = RR_t_raw[physio_idx]

    return RR, RR_t


def F(n, RR_int, RR_t):
    """
    Funkcja fluktuacji F(n) dla okien o długości n.

    RR_int : scałkowany sygnał y(k)
    RR_t   : czasy uderzeń (oś x dla dopasowania trendów)
    """
    N = int(np.floor(len(RR_int) / n) * n)
    sub_RR_int = RR_int[:N]
    ly_global = np.zeros_like(sub_RR_int)
    for i in range(0, N, n):
        x_offset = RR_t[i]
        x, y = RR_t[i:i + n] - x_offset, sub_RR_int[i:i + n]

        b = np.polyfit(x, y, 1)
        ly = b[0]*x + b[1]

        ly_global[i:i + n] = ly

    err = np.mean((sub_RR_int - ly_global)**2)
    F_n = np.sqrt(err)
    return F_n


def calc_alpha(alpha_n, alpha_F):
    alpha_n = np.log10(alpha_n)
    alpha_F = np.log10(alpha_F)
    alpha = np.polyfit(alpha_n, alpha_F, 1)[0]
    return alpha


def dfa(rr_intervals, scales=None, split_scale=16):
    """
    Detrended Fluctuation Analysis (DFA)

    Parameters
    ----------
    rr_intervals : array-like
        Surowe (nieprzefiltrowane) interwały RR [s]

    scales : array-like or None
        Długości okien n.
        Domyślnie n = 4..64

    split_scale : int
        Granica pomiędzy alpha1 i alpha2

    Returns
    -------
    F : ndarray
        Funkcja fluktuacji dla kolejnych skali

    alpha1 : float
        Współczynnik DFA dla małych skal

    alpha2 : float
        Współczynnik DFA dla dużych skal

    log_n : ndarray
        log10(skali)

    log_F : ndarray
        log10(F(n))
    """
    if scales is None:
        scales = np.arange(4, 65)
    ns = np.asarray(scales)

    RR, RR_t = filter_physio(np.asarray(rr_intervals, dtype=float))
    RR_int = np.cumsum(RR - np.mean(RR))

    F_total = np.array([F(n, RR_int, RR_t) for n in ns])

    alpha1 = calc_alpha(ns[ns <= split_scale], F_total[ns <= split_scale])
    alpha2 = calc_alpha(ns[ns > split_scale], F_total[ns > split_scale])

    return F_total, alpha1, alpha2, np.log10(ns), np.log10(F_total)


if __name__ == "__main__":
    RR_chf_raw = np.loadtxt("data/chf206.dat")
    _, alpha1, alpha2, _, _ = dfa(RR_chf_raw)
    print(f"chf206: {alpha1=:.4f} {alpha2=:.4f}")
