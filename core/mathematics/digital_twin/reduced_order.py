import numpy as np

def proper_orthogonal_decomposition(data_matrix: np.ndarray, n_modes: int = 5) -> tuple[np.ndarray, np.ndarray]:
    """Proper Orthogonal Decomposition (SVD variant) for ROM."""
    # SVD of data matrix (spatial snapshots)
    U, S, Vt = np.linalg.svd(data_matrix, full_matrices=False)
    modes = U[:, :n_modes]
    coefficients = np.diag(S[:n_modes]) @ Vt[:n_modes, :]
    return modes, coefficients
