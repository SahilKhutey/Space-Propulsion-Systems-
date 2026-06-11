import numpy as np
from typing import Callable
from .rk4 import rk4_propagate

def gauss_jackson_propagate(f: Callable, t0: float, y0: np.ndarray,
                           dt: float, n_steps: int, order: int = 8) -> tuple[np.ndarray, np.ndarray]:
    t, y = rk4_propagate(f, t0, y0, dt, order)
    f_hist = [f(t[i], y[i]) for i in range(order + 1)]
    for i in range(order, n_steps):
        # Adams-Bashforth style prediction
        y_pred = y[i] + dt * f_hist[-1]
        f_pred = f(t[i] + dt, y_pred)
        # Corrector
        y_corr = y[i] + dt * 0.5 * (f_hist[-1] + f_pred)
        t_next = t[i] + dt
        y = np.vstack([y, y_corr])
        t = np.append(t, t_next)
        f_hist.append(f(t_next, y_corr))
    return t, y
