import numpy as np
from core.constants.constants import G0

def rocket_equation(isp_s: float, m0: float, mp: float) -> float:
    if m0 <= mp or m0 <= 0 or mp < 0:
        return 0.0
    return float(isp_s * G0 * np.log(m0 / (m0 - mp)))

def required_propellant_mass(isp_s: float, m_dry: float, delta_v: float) -> float:
    ve = isp_s * G0
    if ve <= 0:
        return 0.0
    mass_ratio = np.exp(delta_v / ve)
    return float(m_dry * (mass_ratio - 1))

def delta_v_from_mass_ratio(isp_s: float, mass_ratio_val: float) -> float:
    return float(isp_s * G0 * np.log(mass_ratio_val))

def delta_v(isp_s: float, m0: float, mf: float) -> float:
    if m0 <= 0 or mf <= 0 or m0 < mf:
        return 0.0
    return float(isp_s * G0 * np.log(m0 / mf))

def propellant_for_dv(delta_v: float, isp_s: float, m_dry: float) -> float:
    ve = isp_s * G0
    if ve <= 0:
        return 0.0
    return float(m_dry * (np.exp(delta_v / ve) - 1))

def mass_ratio(delta_v: float, isp_s: float) -> float:
    ve = isp_s * G0
    if ve <= 0:
        return 1.0
    return float(np.exp(delta_v / ve))

def propellant_fraction(delta_v: float, isp_s: float) -> float:
    r = mass_ratio(delta_v, isp_s)
    if r <= 1e-12:
        return 0.0
    return float(1.0 - 1.0 / r)
