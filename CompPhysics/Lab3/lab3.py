#%%
import numpy as np
import matplotlib.pyplot as plt
#%%

def euler(t, beta, gamma, s0, i0):
    dt = t[1] - t[0]

    s = np.zeros_like(t)
    i = np.zeros_like(t)
    iters_per_t = np.zeros_like(t)

    # War pocz.
    s[0] = s0
    i[0] = i0

    # Metoda niejawna Eulera
    MAX_ITER = 150
    TOL = 1e-6

    for n in range(t.shape[0] - 1):
        s_n = s[n]
        i_n = i[n]

        s_old = s_n
        i_old = i_n

        for iters_counter in range(MAX_ITER):
            s_new = s_n - dt * beta * s_old * i_old
            i_new = i_n + dt * (beta * s_old * i_old - gamma * i_old)

            if abs(s_new - s_old) < TOL and abs(i_new - i_old) < TOL:
                # Hit tolerance limit
                break

            s_old = s_new
            i_old = i_new

        s[n + 1] = s_new
        i[n + 1] = i_new
        iters_per_t[n + 1] = iters_counter

    fig, axs = plt.subplots(3, 1, figsize=(6, 12))
    ax = axs[0]
    ax.scatter(t, s, label='s', color='orange')
    ax.scatter(t, i, label='i', color='blue')
    ax.set_title(f"Euler, iter dt = {dt}")
    ax.legend()

    r = 1 - s - i
    ax = axs[1]
    ax.plot(t, r)
    ax.set_ylabel("r(t)")
    ax.set_title("Euler, iter")

    ax = axs[2]
    ax.plot(t, iters_per_t)
    ax.set_ylabel("# Iterations")
    ax.set_title("Euler, iter")

    fig.subplots_adjust(bottom=0.2)

    return s, i, iters_per_t
#%%

def trapez(t, beta, gamma, s0, i0):
    dt = t[1] - t[0]

    s = np.zeros_like(t)
    i = np.zeros_like(t)
    iters_per_t = np.zeros_like(t)

    # War pocz.
    s[0] = s0
    i[0] = i0

    # Metoda niejawna Eulera
    MAX_ITER = 150
    TOL = 1e-6

    for n in range(t.shape[0] - 1):
        s_n = s[n]
        i_n = i[n]

        # warunki w chwili t_n
        f_n = -beta * s_n * i_n
        g_n = beta * s_n * i_n - gamma * i_n

        s_old = s_n
        i_old = i_n

        for iters_counter in range(MAX_ITER):
            f_old = -beta * s_old * i_old
            g_old = beta * s_old * i_old - gamma * i_old

            s_new = s_n + (dt / 2) * (f_n + f_old)
            i_new = i_n + (dt / 2) * (g_n + g_old)

            if abs(s_new - s_old) < TOL and abs(i_new - i_old) < TOL:
                # Hit tolerance limit
                break

            s_old = s_new
            i_old = i_new

        s[n + 1] = s_new
        i[n + 1] = i_new
        iters_per_t[n + 1] = iters_counter

    fig, axs = plt.subplots(3, 1, figsize=(6, 12))
    ax = axs[0]
    ax.scatter(t, s, label='s', color='orange')
    ax.scatter(t, i, label='i', color='blue')
    ax.set_title(f"Trapez, iter dt = {dt}")
    ax.legend()

    r = 1 - s - i
    ax = axs[1]
    ax.plot(t, r)
    ax.set_ylabel("r(t)")
    ax.set_title("Trapez, iter")

    ax = axs[2]
    ax.plot(t, iters_per_t)
    ax.set_ylabel("# Iterations")
    ax.set_title("Trapez, iter")

    fig.subplots_adjust(bottom=0.2)

    return s, i, iters_per_t
#%%
def wrapper():
    T_MAX = 350

    run_params = [
        {
            "dt": 10.,
            "beta": 0.34,
            "gamma": 0.07,
            "s0": 0.9,
            "i0": 0.1,
            "method": euler,
        },
        {
            "dt": 0.1,
            "beta": 0.34,
            "gamma": 0.07,
            "s0": 0.9,
            "i0": 0.1,
            "method": euler,
        },
        {
            "dt": 10,
            "beta": 0.34,
            "gamma": 0.07,
            "s0": 0.9,
            "i0": 0.1,
            "method": trapez,
        },
        {
            "dt": 0.1,
            "beta": 0.34,
            "gamma": 0.07,
            "s0": 0.9,
            "i0": 0.1,
            "method": trapez,
        },
        {
            "dt": 10.,
            "beta": 0.06,
            "gamma": 0.07,
            "s0": 0.9,
            "i0": 0.1,
            "method": trapez,
        }
    ]

    t_s_i_per_method = []
    iters_per_method = []

    for params in run_params:
        beta = params["beta"]
        gamma = params["gamma"]
        dt = params["dt"]
        t = np.arange(0, T_MAX + dt, dt, dtype=float)

        s0 = params["s0"]
        i0 = params["i0"]

        method = params["method"]
        s, i, iters_per_t = method(t, beta, gamma, s0, i0)

        t_s_i_per_method.append((t, s, t))
        iters_per_method.append((t, iters_per_t))

wrapper()
