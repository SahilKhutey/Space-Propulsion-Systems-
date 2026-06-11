def thermal_capacity_heat(mass: float, cp: float, dt: float) -> float:
    return float(mass * cp * dt)

def heat_capacity(mass: float, cp: float) -> float:
    return float(mass * cp)

def temperature_rise(q_w: float, mass: float, cp: float, dt: float) -> float:
    if mass <= 0 or cp <= 0:
        return 0.0
    return float(q_w * dt / (mass * cp))
