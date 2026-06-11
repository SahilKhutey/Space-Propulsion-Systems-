import numpy as np

def linear_momentum(mass: float, velocity: np.ndarray) -> np.ndarray:
    return mass * np.asarray(velocity)

def momentum_conservation(m1: float, v1: np.ndarray,
                          m2: float, v2: np.ndarray) -> np.ndarray:
    return m1 * np.asarray(v1) + m2 * np.asarray(v2)

def angular_momentum(mass: float, position: np.ndarray,
                     velocity: np.ndarray) -> np.ndarray:
    return mass * np.cross(position, velocity)

def angular_momentum_inertia(I: np.ndarray, omega: np.ndarray) -> np.ndarray:
    return np.asarray(I) @ np.asarray(omega)

def elastic_collision_2d(m1: float, v1: np.ndarray, m2: float, v2: np.ndarray,
                        restitution: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    v1, v2 = np.asarray(v1), np.asarray(v2)
    m1, m2 = float(m1), float(m2)
    total_m = m1 + m2
    v1p = ((m1 - restitution*m2)*v1 + (1+restitution)*m2*v2) / total_m
    v2p = ((1+restitution)*m1*v1 + (m2 - restitution*m1)*v2) / total_m
    return v1p, v2p
