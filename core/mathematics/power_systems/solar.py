import numpy as np
from core.constants.constants import AU

def solar_power_generation(efficiency: float, area: float, solar_flux: float,
                           angle_of_incidence_rad: float = 0.0) -> float:
    return float(efficiency * area * solar_flux * np.cos(angle_of_incidence_rad))

def solar_flux_at_distance(solar_flux_1au: float, dist_m: float) -> float:
    if dist_m <= 0:
        return 0.0
    return float(solar_flux_1au * (AU / dist_m)**2)

def solar_array_power(efficiency: float, area: float, dist_au: float) -> float:
    solar_flux = 1361.0 * (1.0 / dist_au)**2
    return float(efficiency * area * solar_flux)

def required_area(target_power_w: float, efficiency: float, dist_au: float) -> float:
    solar_flux = 1361.0 * (1.0 / dist_au)**2
    if efficiency <= 0 or solar_flux <= 0:
        return float("inf")
    return float(target_power_w / (efficiency * solar_flux))
