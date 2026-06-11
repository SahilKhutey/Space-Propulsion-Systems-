import numpy as np

class KalmanFilter:
    def __init__(self, F: np.ndarray, H: np.ndarray, Q: np.ndarray, R: np.ndarray, x0: np.ndarray = None, P0: np.ndarray = None):
        self.F = F
        self.H = H
        self.Q = Q
        self.R = R
        self.ndim = F.shape[0]
        self.x = x0 if x0 is not None else np.zeros(self.ndim)
        self.P = P0 if P0 is not None else np.eye(self.ndim)

    def predict(self, x: np.ndarray, P: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        x_pred = self.F @ x
        P_pred = self.F @ P @ self.F.T + self.Q
        return x_pred, P_pred

    def update(self, x_pred: np.ndarray, P_pred: np.ndarray, z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        y = z - self.H @ x_pred
        S = self.H @ P_pred @ self.H.T + self.R
        K = P_pred @ self.H.T @ np.linalg.inv(S)
        x_new = x_pred + K @ y
        P_new = (np.eye(self.ndim) - K @ self.H) @ P_pred
        return x_new, P_new

    def step(self, z: np.ndarray):
        x_pred, P_pred = self.predict(self.x, self.P)
        self.x, self.P = self.update(x_pred, P_pred, z)

    def get_state(self) -> np.ndarray:
        return self.x
