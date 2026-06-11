import numpy as np
from core.constants.constants import G0

def burn_time(mp: float, m_dot: float) -> float:
    if m_dot <= 0:
        return 0.0
    return float(mp / m_dot)

def propellant_fraction(m0: float, mp: float) -> float:
    if m0 <= 0:
        return 0.0
    return float(mp / m0)

def burn_time_from_thrust(m_prop: float, thrust_n: float, isp_s: float) -> float:
    ve = isp_s * G0
    if ve <= 0 or thrust_n <= 0:
        return float("inf")
    m_dot = thrust_n / ve
    return float(m_prop / m_dot)

def burn_time_from_delta_v(dv_ms: float, thrust_n: float, isp_s: float, m0: float) -> float:
    ve = isp_s * G0
    if ve <= 0 or thrust_n <= 0:
        return float("inf")
    m_dot = thrust_n / ve
    mp = m0 * (1.0 - np.exp(-dv_ms / ve))
    return float(mp / m_dot)
