import numpy as np

def state_space_step(a_mat: np.ndarray, b_mat: np.ndarray,
                     c_mat: np.ndarray, d_mat: np.ndarray,
                     x_state: np.ndarray, u_input: np.ndarray,
                     dt: float) -> tuple[np.ndarray, np.ndarray]:
    A = np.asarray(a_mat, dtype=float)
    B = np.asarray(b_mat, dtype=float)
    C = np.asarray(c_mat, dtype=float)
    D = np.asarray(d_mat, dtype=float)
    x = np.asarray(x_state, dtype=float)
    u = np.asarray(u_input, dtype=float)
    
    # Continuous to discrete approximation (Euler forward)
    x_next = x + dt * (A @ x + B @ u)
    y_output = C @ x + D @ u
    return x_next, y_output
