import numpy as np
from core.constants.constants import G

def newton_second_law(force: np.ndarray, mass: float) -> np.ndarray:
    if mass <= 0:
        raise ValueError("Mass must be positive")
    return np.asarray(force) / mass

def gravity_force(m1: float, m2: float, r_vec: np.ndarray) -> np.ndarray:
    r = np.asarray(r_vec, dtype=float)
    r_mag = np.linalg.norm(r)
    if r_mag < 1e-6:
        return np.zeros(3)
    return -G * m1 * m2 * r / r_mag**3

def gravitational_parameter(M: float) -> float:
    return G * M
