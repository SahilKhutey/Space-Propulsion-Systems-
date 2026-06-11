def battery_energy(voltage_v: float, capacity_ah: float) -> float:
    return float(voltage_v * capacity_ah)

def battery_state_of_charge(total_energy: float, remaining_energy: float) -> float:
    if total_energy <= 0:
        return 0.0
    return float(remaining_energy / total_energy)

def battery_voltage_model(soc: float, v_nominal: float = 3.7,
                          v_full: float = 4.2, v_empty: float = 3.0) -> float:
    soc = min(max(soc, 0.0), 1.0)
    return float(v_empty + soc * (v_full - v_empty))

def state_of_charge(remaining_energy: float, total_energy: float) -> float:
    if total_energy <= 0:
        return 0.0
    return float(remaining_energy / total_energy)

def discharge_time(capacity_wh: float, load_w: float) -> float:
    if load_w <= 0:
        return float("inf")
    return float(capacity_wh / load_w)
