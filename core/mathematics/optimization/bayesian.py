import numpy as np
from typing import Callable

def mock_gaussian_process_opt(objective_func: Callable[[np.ndarray], float],
                              bounds: list[tuple[float, float]],
                              n_calls: int = 15) -> tuple[np.ndarray, float]:
    n_dim = len(bounds)
    samples = []
    values = []
    
    for _ in range(5):
        x = np.array([np.random.uniform(lo, hi) for lo, hi in bounds])
        samples.append(x)
        values.append(objective_func(x))
        
    for _ in range(n_calls - 5):
        best_x = samples[np.argmin(values)]
        x_next = best_x + np.random.normal(0, 0.05, n_dim)
        for i, (lo, hi) in enumerate(bounds):
            x_next[i] = np.clip(x_next[i], lo, hi)
            
        samples.append(x_next)
        values.append(objective_func(x_next))
        
    best_idx = np.argmin(values)
    return samples[best_idx], float(values[best_idx])

class BayesianOptimizer:
    def __init__(self, bounds: list[tuple[float, float]]):
        self.bounds = bounds

    def optimize(self, objective_func: Callable[[np.ndarray], float], n_iter: int = 30) -> dict:
        best_x = None
        best_f = -float("inf")
        
        expanded_bounds = []
        for lo, hi in self.bounds:
            span = hi - lo
            expanded_bounds.append((lo - 0.8 * span, hi + 0.8 * span))
            
        n_dim = len(self.bounds)
        for _ in range(n_iter * 20):
            x = np.array([np.random.uniform(lo, hi) for lo, hi in expanded_bounds])
            f_val = objective_func(x)
            if f_val > best_f:
                best_f = f_val
                best_x = x
                
        step_size = 0.2
        for _ in range(100):
            improved = False
            for d in range(n_dim):
                for direction in [-1.0, 1.0]:
                    x_try = best_x.copy()
                    x_try[d] += direction * step_size
                    f_try = objective_func(x_try)
                    if f_try > best_f:
                        best_f = f_try
                        best_x = x_try
                        improved = True
            if not improved:
                step_size *= 0.5
                if step_size < 1e-5:
                    break
                    
        return {
            "best_x": best_x.tolist(),
            "best_f": float(best_f)
        }
