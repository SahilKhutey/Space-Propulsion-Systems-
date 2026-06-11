"""
Layer 1.1: Vector Operations
Used in: spacecraft state, force/torque, magnetic/electric fields, attitude.
"""
import numpy as np
from numpy.typing import ArrayLike
from typing import Union

Vector = Union[ArrayLike, np.ndarray]

def vec3(x: float = 0, y: float = 0, z: float = 0) -> np.ndarray:
    """Construct a 3-vector."""
    return np.array([x, y, z], dtype=float)

def magnitude(v: Vector) -> float:
    return float(np.linalg.norm(v))

def unit(v: Vector) -> np.ndarray:
    n = np.linalg.norm(v)
    if n < 1e-12:
        return np.zeros(3)
    return np.asarray(v, dtype=float) / n

def dot(a: Vector, b: Vector) -> float:
    return float(np.dot(a, b))

def cross(a: Vector, b: Vector) -> np.ndarray:
    return np.cross(a, b)

def angle_between(a: Vector, b: Vector) -> float:
    """Returns angle [rad] between two vectors."""
    cos_t = np.clip(dot(unit(a), unit(b)), -1.0, 1.0)
    return float(np.arccos(cos_t))

def projection(a: Vector, b: Vector) -> np.ndarray:
    """Project a onto b."""
    bn = np.dot(b, b)
    if bn < 1e-12:
        return np.zeros(3)
    return np.asarray(b) * (np.dot(a, b) / bn)

def triple_product(a: Vector, b: Vector, c: Vector) -> float:
    return float(np.dot(a, np.cross(b, c)))

def skew(v: Vector) -> np.ndarray:
    """Skew-symmetric matrix from a 3-vector (for cross products)."""
    v = np.asarray(v, dtype=float).flatten()
    x, y, z = v[0], v[1], v[2]
    return np.array([
        [0, -z, y],
        [z, 0, -x],
        [-y, x, 0]
    ])
