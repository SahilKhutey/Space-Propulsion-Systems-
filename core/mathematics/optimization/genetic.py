import numpy as np
from typing import Callable

def genetic_algorithm(objective_func: Callable[[np.ndarray], float],
                      bounds: list[tuple[float, float]],
                      pop_size: int = 50, generations: int = 50,
                      mutation_rate: float = 0.1, n_gen: int | None = None) -> tuple[np.ndarray, float, list[dict]]:
    if n_gen is not None:
        generations = n_gen
        
    n_dim = len(bounds)
    pop = np.zeros((pop_size, n_dim))
    for i, (lo, hi) in enumerate(bounds):
        pop[:, i] = np.random.uniform(lo, hi, pop_size)
    
    best_ind = pop[0].copy()
    best_fit = -float("inf")
    history = []
    
    for gen in range(generations):
        fitness = np.array([objective_func(ind) for ind in pop])
        max_idx = np.argmax(fitness)
        if fitness[max_idx] > best_fit:
            best_fit = fitness[max_idx]
            best_ind = pop[max_idx].copy()
            
        history.append({
            "generation": gen,
            "best_f": float(best_fit),
            "best_x": best_ind.tolist()
        })
        
        # Fitness-proportionate selection (shift to keep values positive)
        min_fit = np.min(fitness)
        shifted = fitness - min_fit + 1e-6
        probs = shifted / np.sum(shifted)
        parents_idx = np.random.choice(pop_size, size=pop_size, p=probs)
        pop = pop[parents_idx]
        
        # Crossover & Mutation
        for i in range(pop_size):
            if np.random.rand() < mutation_rate:
                dim_idx = np.random.choice(n_dim)
                lo, hi = bounds[dim_idx]
                pop[i, dim_idx] = np.random.uniform(lo, hi)
                
    return best_ind, float(best_fit), history
