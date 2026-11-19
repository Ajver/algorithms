def dfa(rr_intervals, scales=None, split_scale=16):
    """
    Detrended Fluctuation Analysis (DFA)

    Parameters
    ----------
    rr_intervals : array-like
        Interwały RR [ms]

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


    pass