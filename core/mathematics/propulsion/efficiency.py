def propulsive_efficiency(thrust_n: float, v_e: float, power_w: float) -> float:
    if power_w <= 0:
        return 0.0
    return float(thrust_n * v_e / (2.0 * power_w))

def electrical_to_thrust_efficiency(eta_e: float, eta_p: float) -> float:
    return float(eta_e * eta_p)

def thrust_from_power(power_w: float, eta_total: float, v_e_or_isp: float) -> float:
    if v_e_or_isp <= 10000.0:
        from core.constants.constants import G0
        v_e = v_e_or_isp * G0
    else:
        v_e = v_e_or_isp
    if v_e <= 0:
        return 0.0
    return float(2.0 * eta_total * power_w / v_e)

def power_from_thrust(thrust_n: float, v_e: float, eta_total: float) -> float:
    if eta_total <= 0:
        return float("inf")
    return float(thrust_n * v_e / (2.0 * eta_total))
