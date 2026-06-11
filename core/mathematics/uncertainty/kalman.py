import numpy as np

def kalman_filter_step(x_est: np.ndarray, p_cov: np.ndarray, z_meas: np.ndarray,
                       f_mat: np.ndarray, h_mat: np.ndarray,
                       q_noise: np.ndarray, r_noise: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    F = np.asarray(f_mat, dtype=float)
    H = np.asarray(h_mat, dtype=float)
    Q = np.asarray(q_noise, dtype=float)
    R = np.asarray(r_noise, dtype=float)
    x = np.asarray(x_est, dtype=float)
    P = np.asarray(p_cov, dtype=float)
    z = np.asarray(z_meas, dtype=float)
    
    # Predict
    x_pred = F @ x
    P_pred = F @ P @ F.T + Q
    
    # Update
    y = z - H @ x_pred
    S = H @ P_pred @ H.T + R
    K = P_pred @ H.T @ np.linalg.inv(S)
    
    x_new = x_pred + K @ y
    P_new = (np.eye(len(x)) - K @ H) @ P_pred
    return x_new, P_new

def extended_kalman_filter_step(x_est: np.ndarray, p_cov: np.ndarray, z_meas: np.ndarray,
                               f_func: callable, h_func: callable,
                               f_jac: np.ndarray, h_jac: np.ndarray,
                               q_noise: np.ndarray, r_noise: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    F_j = np.asarray(f_jac, dtype=float)
    H_j = np.asarray(h_jac, dtype=float)
    Q = np.asarray(q_noise, dtype=float)
    R = np.asarray(r_noise, dtype=float)
    x = np.asarray(x_est, dtype=float)
    P = np.asarray(p_cov, dtype=float)
    z = np.asarray(z_meas, dtype=float)
    
    # Predict
    x_pred = f_func(x)
    P_pred = F_j @ P @ F_j.T + Q
    
    # Update
    y = z - h_func(x_pred)
    S = H_j @ P_pred @ H_j.T + R
    K = P_pred @ H_j.T @ np.linalg.inv(S)
    
    x_new = x_pred + K @ y
    P_new = (np.eye(len(x)) - K @ H_j) @ P_pred
    return x_new, P_new
