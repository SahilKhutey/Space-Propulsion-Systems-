import numpy as np
from core.constants.constants import SIGMA_SB

def stefan_boltzmann_cooling(t_k: float, t_env_k: float, area_m2: float,
                             emissivity: float) -> float:
    return float(emissivity * SIGMA_SB * area_m2 * (t_k**4 - t_env_k**4))

def solar_heating(solar_flux: float, area_m2: float, absorptivity: float,
                  aspect_angle_rad: float = 0.0) -> float:
    return float(solar_flux * area_m2 * absorptivity * np.cos(aspect_angle_rad))

def stefan_boltzmann(emissivity: float, area_m2: float, t_k: float, t_env_k: float) -> float:
    return float(emissivity * SIGMA_SB * area_m2 * (t_k**4 - t_env_k**4))

def equilibrium_temperature(absorptivity: float, emissivity: float, area_rad: float, area_sun: float, solar_flux: float) -> float:
    if emissivity <= 0 or area_rad <= 0:
        return 0.0
    val = (absorptivity * area_sun * solar_flux) / (emissivity * area_rad * SIGMA_SB)
    return float(val ** 0.25)
