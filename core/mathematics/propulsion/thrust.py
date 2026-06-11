from core.constants.constants import G0

def thrust(m_dot: float, v_e: float,
           p_e: float = 0.0, p_a: float = 0.0, a_e: float = 0.0,
           pressure_correction: bool = True) -> float:
    F = m_dot * v_e
    if pressure_correction and a_e > 0:
        F += (p_e - p_a) * a_e
    return float(F)

def thrust_from_isp(isp_s: float, m_dot: float,
                    p_e: float = 0.0, p_a: float = 0.0, a_e: float = 0.0) -> float:
    v_e = isp_s * G0
    return thrust(m_dot, v_e, p_e, p_a, a_e)

def effective_exhaust_velocity(isp_s: float) -> float:
    return float(isp_s * G0)

def total_impulse(thrust_n: float, burn_time_s: float) -> float:
    return float(thrust_n * burn_time_s)

def thrust_coefficient(chamber_pressure_pa: float, throat_area_m2: float,
                       p_a: float = 0.0) -> float:
    if chamber_pressure_pa <= 0 or throat_area_m2 <= 0:
        return 0.0
    return float(chamber_pressure_pa * throat_area_m2)
