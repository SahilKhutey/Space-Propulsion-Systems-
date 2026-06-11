import numpy as np
from core.constants.constants import G, M_EARTH, R_EARTH

def j2_perturbation_acceleration(r_vec: np.ndarray, mu: float = G*M_EARTH,
                                 R_body: float = R_EARTH,
                                 J2: float = 1.08263e-3) -> np.ndarray:
    r = np.asarray(r_vec, dtype=float)
    r_mag = np.linalg.norm(r)
    if r_mag < 1e-6:
        return np.zeros(3)
    z = r[2]
    factor = 1.5 * J2 * mu * R_body**2 / r_mag**5
    ax = factor * r[0] * (5 * z**2 / r_mag**2 - 1)
    ay = factor * r[1] * (5 * z**2 / r_mag**2 - 1)
    az = factor * z * (5 * z**2 / r_mag**2 - 3)
    return np.array([ax, ay, az])

def atmospheric_drag_acceleration(r_vec: np.ndarray, v_vec: np.ndarray,
                                  cd: float, area: float, mass: float,
                                  scale_height: float = 7500.0,
                                  rho_ref: float = 1.225,
                                  alt_ref: float = 0.0,
                                  r_body: float = R_EARTH) -> np.ndarray:
    r = np.asarray(r_vec, dtype=float)
    v = np.asarray(v_vec, dtype=float)
    r_mag = np.linalg.norm(r)
    altitude = r_mag - r_body
    rho = rho_ref * np.exp(-(altitude - alt_ref) / scale_height)
    v_mag = np.linalg.norm(v)
    if mass <= 0:
        return np.zeros(3)
    return -0.5 * rho * cd * (area / mass) * v_mag * v

def srp_acceleration(r_vec: np.ndarray, r_sun_vec: np.ndarray,
                     cr: float, area: float, mass: float,
                     p_srp: float = 4.56e-6) -> np.ndarray:
    """Solar radiation pressure."""
    r_sc_sun = r_sun_vec - r_vec
    d_sun = np.linalg.norm(r_sc_sun)
    if d_sun < 1e-6 or mass <= 0:
        return np.zeros(3)
    u_sun = r_sc_sun / d_sun
    return cr * (area / mass) * p_srp * u_sun
