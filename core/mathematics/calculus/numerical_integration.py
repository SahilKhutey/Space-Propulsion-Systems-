"""
Numerical integration helper functions.
"""
import numpy as np
from typing import Callable

def trapezoid(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.trapezoid(y, x))

def simpson(x: np.ndarray, y: np.ndarray) -> float:
    n = len(x) - 1
    if n % 2 != 0:
        raise ValueError("Simpson requires odd number of intervals")
    h = (x[-1] - x[0]) / n
    s = y[0] + y[-1] + 4 * sum(y[1:-1:2]) + 2 * sum(y[2:-2:2])
    return float(s * h / 3)

def gauss_legendre(f: Callable[[float], float], a: float, b: float, n: int = 5) -> float:
    """n-point Gauss-Legendre quadrature on [a, b]."""
    nodes, weights = np.polynomial.legendre.leggauss(n)
    t = 0.5 * (b - a) * nodes + 0.5 * (a + b)
    return float(0.5 * (b - a) * sum(w * f(ti) for w, ti in zip(weights, t)))

def cumulative_trapezoid(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.concatenate([[0], np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x))])
