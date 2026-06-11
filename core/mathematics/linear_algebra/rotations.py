"""
Rotation matrices: Euler-axis, Euler angles, principal rotations.
Used in: coordinate transforms, orbit frames, attitude.
"""
import numpy as np

def rot_x(angle_rad: float) -> np.ndarray:
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    return np.array([
        [1, 0,  0],
        [0, c, -s],
        [0, s,  c]
    ])

def rot_y(angle_rad: float) -> np.ndarray:
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    return np.array([
        [ c, 0, s],
        [ 0, 1, 0],
        [-s, 0, c]
    ])

def rot_z(angle_rad: float) -> np.ndarray:
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])

def rotation_from_axis_angle(axis: np.ndarray, angle: float) -> np.ndarray:
    """Rodrigues' rotation formula. r' = Rr."""
    a = np.asarray(axis, dtype=float)
    n = np.linalg.norm(a)
    if n < 1e-12:
        return np.eye(3)
    a = a / n
    K = np.array([
        [0, -a[2], a[1]],
        [a[2], 0, -a[0]],
        [-a[1], a[0], 0]
    ])
    return np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)

def euler_to_matrix(roll: float, pitch: float, yaw: float,
                    order: str = "zyx") -> np.ndarray:
    """Euler angles to rotation matrix."""
    if order == "zyx":
        return rot_z(yaw) @ rot_y(pitch) @ rot_x(roll)
    if order == "xyz":
        return rot_x(roll) @ rot_y(pitch) @ rot_z(yaw)
    raise ValueError(f"Unknown order: {order}")

def matrix_to_euler(R: np.ndarray, order: str = "zyx") -> tuple[float, float, float]:
    if order == "zyx":
        pitch = np.arcsin(-np.clip(R[2, 0], -1, 1))
        if abs(R[2, 0]) < 0.9999:
            roll = np.arctan2(R[2, 1], R[2, 2])
            yaw = np.arctan2(R[1, 0], R[0, 0])
        else:
            roll = 0
            yaw = np.arctan2(-R[0, 1], R[1, 1])
        return roll, pitch, yaw
    raise ValueError(f"Unsupported order: {order}")

def eci_to_ecef_matrix(gmst_rad: float) -> np.ndarray:
    """Earth-Centered Inertial to Earth-Centered Earth-Fixed."""
    return rot_z(gmst_rad)

def eci_to_orbit_matrix(raan: float, inc: float, argp: float) -> np.ndarray:
    """ECI -> perifocal -> orbital frame."""
    return rot_z(raan) @ rot_x(inc) @ rot_z(argp)
