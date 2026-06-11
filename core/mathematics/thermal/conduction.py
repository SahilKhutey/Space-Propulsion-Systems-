def conduction(t1: float, t2: float, conductivity: float,
               area: float, length: float) -> float:
    if length <= 0:
        return 0.0
    return float((conductivity * area / length) * (t1 - t2))
