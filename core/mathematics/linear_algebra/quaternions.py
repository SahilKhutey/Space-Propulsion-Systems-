"""
Quaternions for attitude representation. Avoids gimbal lock.
Hamilton convention: q = [w, x, y, z].
"""
import numpy as np

class Quaternion:
    """Hamilton quaternion [w, x, y, z]."""
    def __init__(self, w: float = 1.0, x: float = 0.0,
                 y: float = 0.0, z: float = 0.0):
        self.q = np.array([w, x, y, z], dtype=float)

    @property
    def w(self): return self.q[0]
    @property
    def x(self): return self.q[1]
    @property
    def y(self): return self.q[2]
    @property
    def z(self): return self.q[3]

    def __mul__(self, other: "Quaternion") -> "Quaternion":
        w1, x1, y1, z1 = self.q
        w2, x2, y2, z2 = other.q
        return Quaternion(
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        )

    def conjugate(self) -> "Quaternion":
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def normalize(self) -> "Quaternion":
        n = np.linalg.norm(self.q)
        if n < 1e-12:
            return Quaternion(1, 0, 0, 0)
        return Quaternion(*(self.q / n))

    def to_matrix(self) -> np.ndarray:
        w, x, y, z = self.q
        return np.array([
            [1-2*(y*y+z*z), 2*(x*y-w*z),   2*(x*z+w*y)],
            [2*(x*y+w*z),   1-2*(x*x+z*z), 2*(y*z-w*x)],
            [2*(x*z-w*y),   2*(y*z+w*x),   1-2*(x*x+y*y)]
        ])

    @staticmethod
    def from_axis_angle(axis: np.ndarray, angle: float) -> "Quaternion":
        a = np.asarray(axis, dtype=float)
        n = np.linalg.norm(a)
        if n < 1e-12:
            return Quaternion(1, 0, 0, 0)
        a = a / n
        s = np.sin(angle / 2)
        return Quaternion(np.cos(angle / 2), a[0]*s, a[1]*s, a[2]*s)

    def to_axis_angle(self) -> tuple[np.ndarray, float]:
        n = np.linalg.norm(self.q[1:])
        if n < 1e-12:
            return np.array([0, 0, 1]), 0.0
        axis = self.q[1:] / n
        angle = 2 * np.arctan2(n, self.q[0])
        return axis, float(angle)

    @staticmethod
    def from_matrix(R: np.ndarray) -> "Quaternion":
        tr = R[0, 0] + R[1, 1] + R[2, 2]
        if tr > 0:
            S = 2 * np.sqrt(tr + 1)
            return Quaternion(0.25*S,
                              (R[2,1]-R[1,2])/S,
                              (R[0,2]-R[2,0])/S,
                              (R[1,0]-R[0,1])/S)
        elif (R[0,0] > R[1,1]) and (R[0,0] > R[2,2]):
            S = 2 * np.sqrt(1 + R[0,0] - R[1,1] - R[2,2])
            return Quaternion((R[2,1]-R[1,2])/S, 0.25*S,
                              (R[0,1]+R[1,0])/S,
                              (R[0,2]+R[2,0])/S)
        elif R[1,1] > R[2,2]:
            S = 2 * np.sqrt(1 + R[1,1] - R[0,0] - R[2,2])
            return Quaternion((R[0,2]-R[2,0])/S,
                              (R[0,1]+R[1,0])/S, 0.25*S,
                              (R[1,2]+R[2,1])/S)
        else:
            S = 2 * np.sqrt(1 + R[2,2] - R[0,0] - R[1,1])
            return Quaternion((R[1,0]-R[0,1])/S,
                              (R[0,2]+R[2,0])/S,
                              (R[1,2]+R[2,1])/S, 0.25*S)

    def __repr__(self):
        return f"Q({self.w:.4f}, {self.x:.4f}, {self.y:.4f}, {self.z:.4f})"

def quaternion_derivative(q: Quaternion, omega: np.ndarray) -> Quaternion:
    """q_dot = 0.5 * q ⊗ [0, omega]"""
    w = Quaternion(0, omega[0], omega[1], omega[2])
    return q * w * 0.5
