import numpy as np
from ..propulsion.efficiency import thrust_from_power

def hall_thrust(power_w: float, efficiency: float, v_e: float) -> float:
    return thrust_from_power(power_w, efficiency, v_e)

def hall_magnetic_field(current_ka: float, channel_radius_m: float) -> float:
    mu_0 = 4 * np.pi * 1e-7
    if channel_radius_m <= 0:
        return 0.0
    return float(mu_0 * current_ka * 1e3 / (2 * np.pi * channel_radius_m))

def hall_charge_lifetime(cathode_current_a: float, propellant_flow_kg_s: float) -> float:
    if propellant_flow_kg_s <= 0:
        return 0.0
    coulomb_per_kg = 1e9
    return float(coulomb_per_kg * 1.0 / propellant_flow_kg_s)

def hall_thruster_efficiency(utilization: float, divergence_loss: float = 0.95,
                            multiplier_loss: float = 0.98,
                            beam_current_eff: float = 0.92) -> float:
    return float(utilization * divergence_loss * multiplier_loss * beam_current_eff)
