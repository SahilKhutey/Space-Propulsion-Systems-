"""
Root finding techniques.
"""
from typing import Callable

def bisection(f: Callable[[float], float], lo: float, hi: float,
              tol: float = 1e-8, max_iter: int = 200) -> float:
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        raise ValueError(f"No sign change on [{lo}, {hi}]")
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        fmid = f(mid)
        if abs(fmid) < tol or (hi - lo) < tol:
            return mid
        if flo * fmid < 0:
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid
    return 0.5 * (lo + hi)

def newton_raphson(f: Callable, fprime: Callable, x0: float,
                   tol: float = 1e-10, max_iter: int = 50) -> float:
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        dfx = fprime(x)
        if abs(dfx) < 1e-30:
            break
        x -= fx / dfx
    return x

def secant(f: Callable, x0: float, x1: float,
           tol: float = 1e-8, max_iter: int = 50) -> float:
    f0, f1 = f(x0), f(x1)
    for _ in range(max_iter):
        if abs(f1) < tol:
            return x1
        if abs(f1 - f0) < 1e-30:
            break
        x_new = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, f0 = x1, f1
        x1, f1 = x_new, f(x_new)
    return x1
