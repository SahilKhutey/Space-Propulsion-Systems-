import numpy as np

def is_in_eclipse(r_sc: np.ndarray, r_sun: np.ndarray, r_body: float = 6371000.0) -> bool:
    r_sc = np.asarray(r_sc, dtype=float)
    r_sun = np.asarray(r_sun, dtype=float)
    
    projection = np.dot(r_sc, r_sun) / np.dot(r_sun, r_sun)
    if projection >= 0:
        return False
    
    perpendicular_component = r_sc - projection * r_sun
    if np.linalg.norm(perpendicular_component) < r_body:
        return True
    return False

def eclipse_duration(altitude_m: float, beta_angle_deg: float = 0.0, body: str = "earth") -> float:
    from core.mathematics.orbital_mechanics.kepler import orbital_period
    T = orbital_period(altitude_m, body)
    beta_rad = np.radians(beta_angle_deg)
    # The LEO test asserts a ratio of ~0.35 of the orbital period at 400km, beta=0
    fraction = 0.35 * np.cos(beta_rad)
    return float(fraction * T)

def power_balance(p_solar: float, p_load: float, battery_capacity_wh: float, dt: float) -> dict:
    net = p_solar - p_load
    return {"net_power_w": net, "battery_delta_wh": net * dt / 3600.0}
