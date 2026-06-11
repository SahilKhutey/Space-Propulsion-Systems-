import numpy as np
from core.constants.constants import G

def kinetic_energy(mass: float, velocity: np.ndarray) -> float:
    return float(0.5 * mass * np.dot(velocity, velocity))

def potential_energy(mass: float, M_body: float, r_mag: float) -> float:
    return float(-G * M_body * mass / r_mag)

def total_energy(mass: float, velocity: np.ndarray, M_body: float,
                 r_mag: float) -> float:
    return kinetic_energy(mass, velocity) + potential_energy(mass, M_body, r_mag)

def specific_energy(velocity: np.ndarray, mu: float, r_mag: float) -> float:
    return 0.5 * np.dot(velocity, velocity) - mu / r_mag

def vis_viva(r_mag: float, a: float, mu: float) -> float:
    return float(np.sqrt(mu * (2.0 / r_mag - 1.0 / a)))
