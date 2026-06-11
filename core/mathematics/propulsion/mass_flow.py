def mass_flow(thrust_n: float, v_e: float) -> float:
    if v_e <= 0:
        return 0.0
    return float(thrust_n / v_e)

def mass_flow_from_power(power_w: float, arg2: float, arg3: float) -> float:
    if arg2 <= 1.0:
        eta_total = arg2
        v_e_or_isp = arg3
    else:
        v_e_or_isp = arg2
        eta_total = arg3
    if v_e_or_isp <= 10000.0:
        from core.constants.constants import G0
        v_e = v_e_or_isp * G0
    else:
        v_e = v_e_or_isp
    if v_e <= 0:
        return 0.0
    return float(2.0 * eta_total * power_w / v_e**2)

def propellant_consumed(m_dot: float, time_s: float) -> float:
    return float(m_dot * time_s)

def mass_ratio(m0: float, mf: float) -> float:
    if mf <= 0:
        return float("inf")
    return float(m0 / mf)
