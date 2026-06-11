import numpy as np
from typing import Callable

class ExtendedKalmanFilter:
    def __init__(self, f_func: Callable, h_func: Callable, F_jac: Callable, H_jac: Callable,
                 Q: np.ndarray, R: np.ndarray, x0: np.ndarray = None, P0: np.ndarray = None):
        self.f = f_func
        self.h = h_func
        self.F_jac = F_jac
        self.H_jac = H_jac
        self.Q = Q
        self.R = R
        self.ndim = len(x0) if x0 is not None else Q.shape[0]
        self.x = x0 if x0 is not None else np.zeros(self.ndim)
        self.P = P0 if P0 is not None else np.eye(self.ndim) * 1.0

    def step(self, z: np.ndarray):
        # Predict step
        # Check if f takes one or two arguments
        import inspect
        sig = inspect.signature(self.f)
        if len(sig.parameters) >= 2:
            x_pred = self.f(self.x, None)
        else:
            x_pred = self.f(self.x)
            
        F = self.F_jac(self.x)
        P_pred = F @ self.P @ F.T + self.Q
        
        # Update step
        y = z - self.h(x_pred)
        H = self.H_jac(x_pred)
        S = H @ P_pred @ H.T + self.R
        K = P_pred @ H.T @ np.linalg.inv(S)
        
        self.x = x_pred + K @ y
        self.P = (np.eye(self.ndim) - K @ H) @ P_pred
