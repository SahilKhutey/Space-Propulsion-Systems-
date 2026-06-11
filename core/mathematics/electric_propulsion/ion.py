import numpy as np
from core.constants.constants import E_CHARGE, G0

def ion_velocity(beam_voltage_v: float, ion_mass_kg: float,
                charge: float = E_CHARGE) -> float:
    if ion_mass_kg <= 0:
        return 0.0
    return float(np.sqrt(2.0 * charge * beam_voltage_v / ion_mass_kg))

def ion_isp(beam_voltage_v: float, ion_mass_kg: float,
            charge: float = E_CHARGE) -> float:
    return float(ion_velocity(beam_voltage_v, ion_mass_kg, charge) / G0)

def ion_thrust(beam_current_a: float, beam_voltage_v: float,
              ion_mass_kg: float, charge: float = E_CHARGE) -> float:
    if charge <= 0:
        return 0.0
    return float(beam_current_a * np.sqrt(2.0 * ion_mass_kg * beam_voltage_v / charge))

def ion_power(beam_voltage_v: float, beam_current_a: float,
              keeper_voltage_v: float = 15.0, keeper_current_a: float = 0.5,
              neutralizer_power_w: float = 10.0) -> float:
    return float(beam_voltage_v * beam_current_a
                 + keeper_voltage_v * keeper_current_a
                 + neutralizer_power_w)

def ion_thruster_efficiency(power_w: float, thrust_n: float, v_e: float) -> float:
    if power_w <= 0:
        return 0.0
    return float(thrust_n * v_e / (2.0 * power_w))
