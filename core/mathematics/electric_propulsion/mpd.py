import numpy as np
from core.constants.constants import G0

def mpd_thrust(power_w: float, efficiency: float, isp_s: float) -> float:
    v_e = isp_s * G0
    if v_e <= 0:
        return 0.0
    return float(2.0 * efficiency * power_w / v_e)

def mpd_self_field_thrust(current_ka: float, electrode_radius_m: float) -> float:
    mu_0 = 4 * np.pi * 1e-7
    I = current_ka * 1e3
    return float((mu_0 * I**2 / (4 * np.pi)) * np.log(electrode_radius_m / 0.01))

def mpd_critical_current(mass_flow_kg_s: float, propellant_ion_mass_kg: float,
                        electrode_radius_m: float) -> float:
    if mass_flow_kg_s <= 0 or electrode_radius_m <= 0:
        return float("inf")
    return float(np.sqrt(2.0 * np.pi * mass_flow_kg_s * propellant_ion_mass_kg)
                 / (4.65e-3 * electrode_radius_m))
