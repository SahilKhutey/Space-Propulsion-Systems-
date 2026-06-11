import numpy as np

def hohmann_delta_v(r1: float, r2: float, mu: float) -> tuple[float, float]:
    dv1 = np.sqrt(mu / r1) * (np.sqrt(2 * r2 / (r1 + r2)) - 1)
    dv2 = np.sqrt(mu / r2) * (1 - np.sqrt(2 * r1 / (r1 + r2)))
    return float(dv1), float(dv2)

def hohmann_transfer_time(r1: float, r2: float, mu: float) -> float:
    a = (r1 + r2) / 2
    return float(np.pi * np.sqrt(a**3 / mu))

def bi_elliptic_delta_v(r1: float, r2: float, rb: float,
                       mu: float) -> tuple[float, float, float]:
    dv1 = np.sqrt(mu / r1) * (np.sqrt(2 * rb / (r1 + rb)) - 1)
    dv2 = np.sqrt(mu / rb) * (np.sqrt(2 * r2 / (rb + r2))
                              - np.sqrt(2 * r1 / (r1 + rb)))
    dv3 = np.sqrt(mu / r2) * (1 - np.sqrt(2 * r2 / (rb + r2)))
    return float(dv1), float(dv2), float(dv3)

def bi_elliptic_total_dv(r1: float, r2: float, rb: float, mu: float) -> float:
    dvs = bi_elliptic_delta_v(r1, r2, rb, mu)
    return sum(dvs)

def low_thrust_spiral_dv(r1: float, r2: float, mu: float) -> float:
    v1 = np.sqrt(mu / r1)
    v2 = np.sqrt(mu / r2)
    return float(abs(v2 - v1))

def lambert_universal(r1_vec: np.ndarray, r2_vec: np.ndarray, dt: float,
                     mu: float, long_way: bool = False) -> tuple[np.ndarray, np.ndarray]:
    r1 = np.linalg.norm(r1_vec)
    r2 = np.linalg.norm(r2_vec)
    cos_dnu = np.dot(r1_vec, r2_vec) / (r1 * r2)
    cos_dnu = np.clip(cos_dnu, -1.0, 1.0)
    A = np.sin(np.arccos(cos_dnu)) * np.sqrt(r1 * r2 / (1 - cos_dnu))
    if long_way:
        A = -A

    def stumpff_c(z):
        if z > 1e-6:
            return (1 - np.cos(np.sqrt(z))) / z
        if z < -1e-6:
            return (1 - np.cosh(np.sqrt(-z))) / z
        return 0.5

    def stumpff_s(z):
        if z > 1e-6:
            return (np.sqrt(z) - np.sin(np.sqrt(z))) / (z * np.sqrt(z))
        if z < -1e-6:
            return (np.sinh(np.sqrt(-z)) - np.sqrt(-z)) / ((-z) * np.sqrt(-z))
        return 1.0 / 6.0

    z = 0.0
    for _ in range(100):
        c = stumpff_c(z)
        s = stumpff_s(z)
        y = r1 + r2 + A * (z * s - 1) / np.sqrt(c) if c > 0 else 0
        chi = np.sqrt(max(y, 1e-6) / c) if c > 0 else 0
        dt_calc = (chi**3 * s + A * np.sqrt(max(y, 1e-6))) / np.sqrt(mu)
        if abs(dt_calc - dt) < 1e-6:
            break
        dz = 1e-5
        c2 = stumpff_c(z + dz)
        s2 = stumpff_s(z + dz)
        y2 = r1 + r2 + A * ((z + dz) * s2 - 1) / np.sqrt(c2) if c2 > 0 else 0
        chi2 = np.sqrt(max(y2, 1e-6) / c2) if c2 > 0 else 0
        dt2 = (chi2**3 * s2 + A * np.sqrt(max(y2, 1e-6))) / np.sqrt(mu)
        dtdz = (dt2 - dt_calc) / dz
        if abs(dtdz) < 1e-20:
            break
        z -= (dt_calc - dt) / dtdz

    c = stumpff_c(z)
    s = stumpff_s(z)
    y = r1 + r2 + A * (z * s - 1) / np.sqrt(c) if c > 0 else 0
    f = 1 - y / r1
    g = A * np.sqrt(max(y, 1e-6) / mu) if c > 0 else 0
    gdot = 1 - y / r2
    v1 = (r2_vec * f - r1_vec * gdot) / (f * gdot - 1)
    v2 = (r2_vec - r1_vec * f) / g if abs(g) > 1e-12 else r2_vec * 0
    return v1, v2
