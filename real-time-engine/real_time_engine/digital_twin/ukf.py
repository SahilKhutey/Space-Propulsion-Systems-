import numpy as np
from typing import Callable

class UnscentedKalmanFilter:
    def __init__(self, f_func: Callable, h_func: Callable, Q: np.ndarray, R: np.ndarray, alpha: float = 1e-3, beta: float = 2.0, kappa: float = 0.0):
        self.f = f_func
        self.h = h_func
        self.Q = Q
        self.R = R
        self.alpha = alpha
        self.beta = beta
        self.kappa = kappa

    def compute_sigma_points(self, x: np.ndarray, P: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        n = len(x)
        lam = self.alpha**2 * (n + self.kappa) - n
        gamma = np.sqrt(n + lam)
        
        # Matrix square root
        sP = np.linalg.cholesky(P)
        
        sigmas = np.zeros((2*n + 1, n))
        sigmas[0] = x
        for i in range(n):
            sigmas[i + 1] = x + gamma * sP[:, i]
            sigmas[i + n + 1] = x - gamma * sP[:, i]
            
        # Weights
        w_m = np.zeros(2*n + 1)
        w_c = np.zeros(2*n + 1)
        w_m[0] = lam / (n + lam)
        w_c[0] = w_m[0] + (1 - self.alpha**2 + self.beta)
        for i in range(1, 2*n + 1):
            w_m[i] = 1.0 / (2 * (n + lam))
            w_c[i] = w_m[i]
            
        return sigmas, w_m, w_c

    def step(self, x: np.ndarray, P: np.ndarray, z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        n = len(x)
        sigmas, w_m, w_c = self.compute_sigma_points(x, P)
        
        # Predict State
        sigmas_f = np.array([self.f(sig) for sig in sigmas])
        x_pred = np.sum(sigmas_f * w_m[:, None], axis=0)
        
        # Predict Covariance
        P_pred = self.Q.copy()
        for i in range(2*n + 1):
            diff = sigmas_f[i] - x_pred
            P_pred += w_c[i] * np.outer(diff, diff)
            
        # Predict Measurement
        sigmas_h = np.array([self.h(sig) for sig in sigmas_f])
        z_pred = np.sum(sigmas_h * w_m[:, None], axis=0)
        
        # Measurement Covariance
        S = self.R.copy()
        for i in range(2*n + 1):
            diff_z = sigmas_h[i] - z_pred
            S += w_c[i] * np.outer(diff_z, diff_z)
            
        # Cross Covariance
        P_xz = np.zeros((n, len(z)))
        for i in range(2*n + 1):
            diff_x = sigmas_f[i] - x_pred
            diff_z = sigmas_h[i] - z_pred
            P_xz += w_c[i] * np.outer(diff_x, diff_z)
            
        # Update
        K = P_xz @ np.linalg.inv(S)
        x_new = x_pred + K @ (z - z_pred)
        P_new = P_pred - K @ S @ K.T
        return x_new, P_new
