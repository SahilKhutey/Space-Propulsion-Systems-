import numpy as np

def orbital_velocity_circular(r_mag_or_alt: float, mu_or_body: float | str) -> float:
    if isinstance(mu_or_body, str):
        body = mu_or_body.lower()
        if body == "earth":
            from core.constants.constants import G, M_EARTH, R_EARTH
            mu = G * M_EARTH
            r_mag = R_EARTH + r_mag_or_alt
        else:
            raise ValueError(f"Unknown body: {mu_or_body}")
    else:
        mu = mu_or_body
        r_mag = r_mag_or_alt
    if r_mag <= 0:
        return 0.0
    return float(np.sqrt(mu / r_mag))

def escape_velocity(r_mag_or_alt: float, mu_or_body: float | str) -> float:
    if isinstance(mu_or_body, str):
        body = mu_or_body.lower()
        if body == "earth":
            from core.constants.constants import G, M_EARTH, R_EARTH
            mu = G * M_EARTH
            r_mag = R_EARTH + r_mag_or_alt
        else:
            raise ValueError(f"Unknown body: {mu_or_body}")
    else:
        mu = mu_or_body
        r_mag = r_mag_or_alt
    if r_mag <= 0:
        return 0.0
    return float(np.sqrt(2.0 * mu / r_mag))

def orbital_period(semi_major_axis_m_or_alt: float, mu_or_body: float | str) -> float:
    if isinstance(mu_or_body, str):
        body = mu_or_body.lower()
        if body == "earth":
            from core.constants.constants import G, M_EARTH, R_EARTH
            mu = G * M_EARTH
            semi_major_axis_m = R_EARTH + semi_major_axis_m_or_alt
        else:
            raise ValueError(f"Unknown body: {mu_or_body}")
    else:
        mu = mu_or_body
        semi_major_axis_m = semi_major_axis_m_or_alt
    if semi_major_axis_m <= 0:
        return 0.0
    return float(2.0 * np.pi * np.sqrt(semi_major_axis_m**3 / mu))

def semi_major_axis_from_period(period_s: float, mu_or_body: float | str) -> float:
    if isinstance(mu_or_body, str):
        body = mu_or_body.lower()
        if body == "earth":
            from core.constants.constants import G, M_EARTH
            mu = G * M_EARTH
        else:
            raise ValueError(f"Unknown body: {mu_or_body}")
    else:
        mu = mu_or_body
    return float((mu * period_s**2 / (4 * np.pi**2)) ** (1/3))

def orbital_energy(semi_major_axis_m: float, mass_kg: float, mu: float) -> float:
    if semi_major_axis_m <= 0:
        return 0.0
    return float(-mu * mass_kg / (2.0 * semi_major_axis_m))

def eccentricity_from_rv(r_vec: np.ndarray, v_vec: np.ndarray, mu: float) -> float:
    r = np.asarray(r_vec, dtype=float)
    v = np.asarray(v_vec, dtype=float)
    h = np.cross(r, v)
    e_vec = np.cross(v, h) / mu - r / np.linalg.norm(r)
    return float(np.linalg.norm(e_vec))

def semi_latus_rectum(semi_major_axis_m: float, eccentricity: float) -> float:
    return float(semi_major_axis_m * (1 - eccentricity**2))

def radius_from_true_anomaly(true_anomaly_rad: float, a: float, e: float) -> float:
    return float(semi_latus_rectum(a, e) / (1 + e * np.cos(true_anomaly_rad)))

def mean_motion(semi_major_axis_m: float, mu: float) -> float:
    if semi_major_axis_m <= 0:
        return 0.0
    return float(np.sqrt(mu / semi_major_axis_m**3))

def true_anomaly_from_eccentric(eccentric_anomaly_rad: float, eccentricity: float) -> float:
    return float(2 * np.arctan2(
        np.sqrt(1 + eccentricity) * np.sin(eccentric_anomaly_rad / 2),
        np.sqrt(1 - eccentricity) * np.cos(eccentric_anomaly_rad / 2)
    ))

def eccentric_anomaly_from_mean(mean_anomaly_rad: float, eccentricity: float,
                                tol: float = 1e-10) -> float:
    E = mean_anomaly_rad
    for _ in range(50):
        f = E - eccentricity * np.sin(E) - mean_anomaly_rad
        fp = 1 - eccentricity * np.cos(E)
        dE = -f / fp
        E += dE
        if abs(dE) < tol:
            break
    return float(E)

def mean_anomaly_from_eccentric(eccentric_anomaly_rad: float, eccentricity: float) -> float:
    return float(eccentric_anomaly_rad - eccentricity * np.sin(eccentric_anomaly_rad))
