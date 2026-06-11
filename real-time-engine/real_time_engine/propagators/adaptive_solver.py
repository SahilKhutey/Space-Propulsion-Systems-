import numpy as np
from typing import Callable
from .rk4 import rk4_propagate
from .rk45 import DormandPrince

def adaptive_propagate(f: Callable, t0: float, y0: np.ndarray,
                      t_end: float, method: str = "rk45", **kwargs) -> tuple[np.ndarray, np.ndarray]:
    if method == "rk4":
        dt = kwargs.get("dt", 1.0)
        n_steps = int((t_end - t0) / dt)
        return rk4_propagate(f, t0, y0, dt, n_steps)
    dp = DormandPrince(rtol=kwargs.get("rtol", 1e-6), atol=kwargs.get("atol", 1e-9))
    return dp.propagate(f, t0, y0, t_end)
