import numpy as np
from typing import Callable

class DormandPrince:
    def __init__(self, rtol: float = 1e-6, atol: float = 1e-9, max_step: float = 60.0):
        self.rtol = rtol
        self.atol = atol
        self.max_step = max_step
        self.dt = 1.0

    def step(self, f: Callable, t: float, y: np.ndarray, dt: float) -> tuple[float, np.ndarray, bool]:
        c2, c3, c4, c5, c6 = 1/5, 3/10, 4/5, 8/9, 1.0
        a21 = 1/5
        a31, a32 = 3/40, 9/40
        a41, a42, a43 = 44/45, -56/15, 32/9
        a51, a52, a53, a54 = 19372/6561, -25360/2187, 64448/6561, -212/729
        a61, a62, a63, a64, a65 = 9017/3168, -355/33, 46732/5247, 49/176, -5103/18656
        a71, a72, a73, a74, a75, a76 = 35/384, 0, 500/1113, 125/192, -2187/6784, 11/84
        b5 = np.array([35/384, 0, 500/1113, 125/192, -2187/6784, 11/84, 0])
        b4 = np.array([5179/57600, 0, 7571/16695, 393/640, -92097/339200, 187/2100, 1/40])

        k1 = f(t, y)
        k2 = f(t + c2*dt, y + dt*a21*k1)
        k3 = f(t + c3*dt, y + dt*(a31*k1 + a32*k2))
        k4 = f(t + c4*dt, y + dt*(a41*k1 + a42*k2 + a43*k3))
        k5 = f(t + c5*dt, y + dt*(a51*k1 + a52*k2 + a53*k3 + a54*k4))
        k6 = f(t + c6*dt, y + dt*(a61*k1 + a62*k2 + a63*k3 + a64*k4 + a65*k5))
        k7 = f(t + dt, y + dt*(a71*k1 + a72*k2 + a73*k3 + a74*k4 + a75*k5 + a76*k6))

        y5 = y + dt * (b5[0]*k1 + b5[1]*k2 + b5[2]*k3 + b5[3]*k4 + b5[4]*k5 + b5[5]*k6 + b5[6]*k7)
        y4 = y + dt * (b4[0]*k1 + b4[1]*k2 + b4[2]*k3 + b4[3]*k4 + b4[4]*k5 + b4[5]*k6 + b4[6]*k7)

        err = np.linalg.norm(y5 - y4)
        norm_y = np.linalg.norm(y5) + self.atol
        accepted = err <= self.rtol * norm_y
        return t + dt if accepted else t, y5 if accepted else y, accepted

    def propagate(self, f: Callable, t0: float, y0: np.ndarray, t_end: float) -> tuple[np.ndarray, np.ndarray]:
        t = t0
        y = np.asarray(y0, dtype=float).copy()
        ts, ys = [t], [y.copy()]
        while t < t_end:
            if t + self.dt > t_end:
                self.dt = t_end - t
            t_new, y_new, ok = self.step(f, t, y, self.dt)
            if ok:
                t, y = t_new, y_new
                ts.append(t)
                ys.append(y.copy())
                self.dt = min(self.dt * 1.5, self.max_step)
            else:
                self.dt = max(self.dt * 0.5, 1e-4)
        return np.array(ts), np.array(ys)
