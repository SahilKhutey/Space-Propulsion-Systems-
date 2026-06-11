import numpy as np
from ..linear_algebra.quaternions import Quaternion

def quaternion_rates(q: Quaternion, omega: np.ndarray) -> np.ndarray:
    """q_dot = 0.5 * q ⊗ [0, ω]"""
    w = Quaternion(0, omega[0], omega[1], omega[2])
    q_dot = q * w
    return 0.5 * q_dot.q
