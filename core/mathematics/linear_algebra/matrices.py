"""
Matrix operations for coordinate transforms, covariance propagation,
state-space systems, and optimization.
"""
import numpy as np
from numpy.typing import ArrayLike

def identity(n: int) -> np.ndarray:
    return np.eye(n)

def diag(v: ArrayLike) -> np.ndarray:
    return np.diag(np.asarray(v, dtype=float))

def symmetric(A: np.ndarray) -> np.ndarray:
    return 0.5 * (A + A.T)

def is_positive_definite(A: np.ndarray, tol: float = 1e-10) -> bool:
    try:
        np.linalg.cholesky(A + tol * np.eye(A.shape[0]))
        return True
    except np.linalg.LinAlgError:
        return False

def matrix_sqrt(A: np.ndarray) -> np.ndarray:
    """Matrix square root via eigendecomposition (real symmetric)."""
    A = np.asarray(A, dtype=float)
    A_sym = symmetric(A)
    w, V = np.linalg.eigh(A_sym)
    w = np.clip(w, 0, None)
    return V @ np.diag(np.sqrt(w)) @ V.T

def solve_linear(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.linalg.solve(A, b)

def least_squares(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.linalg.lstsq(A, b, rcond=None)[0]
