import numpy as np

def propagate_covariance(f_jacobian: np.ndarray, p_cov: np.ndarray,
                         q_noise: np.ndarray) -> np.ndarray:
    """P_k+1 = F * P_k * F^T + Q"""
    F = np.asarray(f_jacobian, dtype=float)
    P = np.asarray(p_cov, dtype=float)
    Q = np.asarray(q_noise, dtype=float)
    return F @ P @ F.T + Q
