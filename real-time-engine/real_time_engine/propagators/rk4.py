import numpy as np
from typing import Callable

def rk4_step(f: Callable[[float, np.ndarray], np.ndarray], t: float, y: np.ndarray, dt: float) -> np.ndarray:
    k1 = f(t, y)
    k2 = f(t + dt/2, y + dt*k1/2)
    k3 = f(t + dt/2, y + dt*k2/2)
    k4 = f(t + dt, y + dt*k3)
    return y + dt * (k1 + 2*k2 + 2*k3 + k4) / 6

def rk4_propagate(f: Callable[[float, np.ndarray], np.ndarray],
                 t0: float, y0: np.ndarray, dt: float,
                 n_steps: int) -> tuple[np.ndarray, np.ndarray]:
    t = np.zeros(n_steps + 1)
    y = np.zeros((n_steps + 1, *np.atleast_1d(y0).shape))
    t[0], y[0] = t0, np.asarray(y0, dtype=float)
    for i in range(n_steps):
        y[i+1] = rk4_step(f, t[i], y[i], dt)
        t[i+1] = t[i] + dt
    return t, y
