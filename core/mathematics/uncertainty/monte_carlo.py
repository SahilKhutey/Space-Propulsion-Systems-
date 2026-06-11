import numpy as np
from typing import Callable

def monte_carlo_simulation(model_func: Callable[[dict], float],
                           param_dist_dict: dict[str, tuple[str, float, float]],
                           n_runs: int = 100) -> list[float]:
    """
    Runs Monte Carlo simulation.
    param_dist_dict maps parameter_name -> (distribution_type, mean/lo, std/hi)
    """
    results = []
    for _ in range(n_runs):
        params = {}
        for name, (dist, p1, p2) in param_dist_dict.items():
            if dist == "normal":
                params[name] = np.random.normal(p1, p2)
            elif dist == "uniform":
                params[name] = np.random.uniform(p1, p2)
            else:
                params[name] = p1
        results.append(model_func(params))
    return results
