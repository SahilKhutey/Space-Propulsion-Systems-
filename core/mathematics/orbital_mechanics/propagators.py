import numpy as np
from ..calculus.ode_solvers import rk4, dopri45
from .perturbations import j2_perturbation_acceleration

def two_body_ode(t: float, state: np.ndarray, mu: float) -> np.ndarray:
    r = state[:3]
    v = state[3:]
    r_mag = np.linalg.norm(r)
    if r_mag < 1e-6:
        return np.zeros(6)
    a = -mu * r / r_mag**3
    return np.concatenate([v, a])

def two_body_j2_ode(t: float, state: np.ndarray, mu: float, r_body: float, j2: float) -> np.ndarray:
    r = state[:3]
    v = state[3:]
    r_mag = np.linalg.norm(r)
    if r_mag < 1e-6:
        return np.zeros(6)
    a_grav = -mu * r / r_mag**3
    a_j2 = j2_perturbation_acceleration(r, mu, r_body, j2)
    return np.concatenate([v, a_grav + a_j2])

def propagate_orbit(state_init: np.ndarray, t_end: float, dt: float,
                    mu: float, j2: float = 0.0, r_body: float = 6371000.0) -> tuple[np.ndarray, np.ndarray]:
    if j2 > 0:
        def ode(t, y): return two_body_j2_ode(t, y, mu, r_body, j2)
    else:
        def ode(t, y): return two_body_ode(t, y, mu)
    
    n_steps = int(t_end / dt)
    return rk4(ode, 0.0, state_init, dt, n_steps)
