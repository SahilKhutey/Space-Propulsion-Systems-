import numpy as np
from typing import Callable

def gradient_descent(objective_func: Callable[[np.ndarray], float], x0: np.ndarray,
                     learning_rate: float = 0.01, max_iter: int = 200,
                     tol: float = 1e-6) -> tuple[np.ndarray, float]:
    x = np.asarray(x0, dtype=float).copy()
    h = 1e-5
    for _ in range(max_iter):
        grad = np.zeros_like(x)
        for i in range(len(x)):
            xh = x.copy()
            xh[i] += h
            grad[i] = (objective_func(xh) - objective_func(x)) / h
        
        x_new = x - learning_rate * grad
        if np.linalg.norm(x_new - x) < tol:
            x = x_new
            break
        x = x_new
    return x, float(objective_func(x))
