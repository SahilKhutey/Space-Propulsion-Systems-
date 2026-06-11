"""
Layer 1.4: ODE Solvers.
Supports: Euler, RK4, Dormand-Prince RK45, Adams-Bashforth.
"""
import numpy as np
from typing import Callable

ODEFunction = Callable[[float, np.ndarray], np.ndarray]

def euler(f: ODEFunction, t0: float, y0: np.ndarray,
          dt: float, n_steps: int) -> tuple[np.ndarray, np.ndarray]:
    """Forward Euler."""
    t = np.zeros(n_steps + 1)
    y = np.zeros((n_steps + 1, *np.atleast_1d(y0).shape))
    t[0], y[0] = t0, np.asarray(y0, dtype=float)
    for i in range(n_steps):
        y[i+1] = y[i] + dt * f(t[i], y[i])
        t[i+1] = t[i] + dt
    return t, y

def rk4(f: ODEFunction, t0: float, y0: np.ndarray,
        dt: float, n_steps: int) -> tuple[np.ndarray, np.ndarray]:
    """Classical 4th-order Runge-Kutta."""
    t = np.zeros(n_steps + 1)
    y = np.zeros((n_steps + 1, *np.atleast_1d(y0).shape))
    t[0], y[0] = t0, np.asarray(y0, dtype=float)
    for i in range(n_steps):
        k1 = f(t[i], y[i])
        k2 = f(t[i] + dt/2, y[i] + dt*k1/2)
        k3 = f(t[i] + dt/2, y[i] + dt*k2/2)
        k4 = f(t[i] + dt,   y[i] + dt*k3)
        y[i+1] = y[i] + dt * (k1 + 2*k2 + 2*k3 + k4) / 6
        t[i+1] = t[i] + dt
    return t, y

def dopri45(f: ODEFunction, t0: float, y0: np.ndarray,
            t_end: float, rtol: float = 1e-6, atol: float = 1e-9,
            dt_init: float | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Dormand-Prince RK45 with adaptive step size."""
    y = np.asarray(y0, dtype=float)
    t = float(t0)
    if dt_init is None:
        dt_init = (t_end - t0) / 100.0
    dt = dt_init

    ts = [t]
    ys = [y.copy()]

    c2, c3, c4, c5, c6 = 1/5, 3/10, 4/5, 8/9, 1.0
    a21 = 1/5
    a31, a32 = 3/40, 9/40
    a41, a42, a43 = 44/45, -56/15, 32/9
    a51, a52, a53, a54 = 19372/6561, -25360/2187, 64448/6561, -212/729
    a61, a62, a63, a64, a65 = 9017/3168, -355/33, 46732/5247, 49/176, -5103/18656
    a71, a72, a73, a74, a75, a76 = 35/384, 0, 500/1113, 125/192, -2187/6784, 11/84
    b5 = [35/384, 0, 500/1113, 125/192, -2187/6784, 11/84, 0]
    b4 = [5179/57600, 0, 7571/16695, 393/640, -92097/339200, 187/2100, 1/40]

    while t < t_end:
        if t + dt > t_end:
            dt = t_end - t
        k1 = f(t, y)
        k2 = f(t + c2*dt, y + dt*a21*k1)
        k3 = f(t + c3*dt, y + dt*(a31*k1 + a32*k2))
        k4 = f(t + c4*dt, y + dt*(a41*k1 + a42*k2 + a43*k3))
        k5 = f(t + c5*dt, y + dt*(a51*k1 + a52*k2 + a53*k3 + a54*k4))
        k6 = f(t + c6*dt, y + dt*(a61*k1 + a62*k2 + a63*k3 + a64*k4 + a65*k5))
        k7 = f(t + dt, y + dt*(a71*k1 + a72*k2 + a73*k3 + a74*k4 + a75*k5 + a76*k6))
        y5 = y + dt * sum(b5[i] * [k1, k2, k3, k4, k5, k6, k7][i] for i in range(7))
        y4 = y + dt * sum(b4[i] * [k1, k2, k3, k4, k5, k6, k7][i] for i in range(7))
        err = np.linalg.norm(y5 - y4)
        norm_y = np.linalg.norm(y5) + atol
        if err <= rtol * norm_y:
            t += dt
            y = y5
            ts.append(t)
            ys.append(y.copy())
            if err > 0:
                factor = 0.9 * (rtol * norm_y / err) ** 0.2
                dt = min(dt * max(0.1, min(5.0, factor)), 1.0)
        else:
            factor = 0.9 * (rtol * norm_y / max(err, 1e-30)) ** 0.25
            dt = dt * max(0.1, min(0.5, factor))
    return np.array(ts), np.array(ys)

def adams_bashforth_4(f: ODEFunction, t0: float, y0: np.ndarray,
                      dt: float, n_steps: int) -> tuple[np.ndarray, np.ndarray]:
    """4th-order explicit Adams-Bashforth (multistep)."""
    _, y_init = rk4(f, t0, y0, dt, 3)
    t = np.zeros(n_steps + 1)
    y = np.zeros((n_steps + 1, *np.atleast_1d(y0).shape))
    t[:4] = np.arange(4) * dt + t0
    y[:4] = y_init
    f_hist = [f(t[i], y[i]) for i in range(4)]
    for i in range(3, n_steps):
        f_i = f_hist[-4:]
        y[i+1] = y[i] + dt * (55*f_i[3] - 59*f_i[2] + 37*f_i[1] - 9*f_i[0]) / 24
        t[i+1] = t[i] + dt
        f_hist.append(f(t[i+1], y[i+1]))
    return t, y
