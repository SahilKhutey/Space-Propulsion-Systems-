import numpy as np

def euler_rotational_dynamics(inertia_matrix: np.ndarray, omega: np.ndarray,
                              external_torque: np.ndarray) -> np.ndarray:
    """I * w_dot + w x (I*w) = torque -> w_dot = I^-1 * (torque - w x (I*w))"""
    I = np.asarray(inertia_matrix, dtype=float)
    w = np.asarray(omega, dtype=float)
    t = np.asarray(external_torque, dtype=float)
    
    Iw = I @ w
    w_cross_Iw = np.cross(w, Iw)
    return np.linalg.solve(I, t - w_cross_Iw)
