import numpy as np
from core.constants.constants import K_BOLTZMANN, EPSILON_0, E_CHARGE

def debye_length(electron_density_m3: float, electron_temp_k: float) -> float:
    if electron_density_m3 <= 0 or electron_temp_k <= 0:
        return 0.0
    return float(np.sqrt(EPSILON_0 * K_BOLTZMANN * electron_temp_k
                          / (electron_density_m3 * E_CHARGE**2)))

def lorentz_force(charge: float, electric_field: np.ndarray,
                  velocity: np.ndarray, magnetic_field: np.ndarray) -> np.ndarray:
    return charge * (np.asarray(electric_field) + np.cross(velocity, magnetic_field))

def plasma_frequency(electron_density_m3: float) -> float:
    m_e = 9.109e-31
    if electron_density_m3 <= 0:
        return 0.0
    return float(np.sqrt(electron_density_m3 * E_CHARGE**2
                          / (EPSILON_0 * m_e)))

def ion_acceleration_kinetic(charge: float, voltage_v: float, mass_kg: float) -> float:
    if mass_kg <= 0:
        return 0.0
    return float(np.sqrt(2.0 * charge * voltage_v / mass_kg))

def child_langmuir_current(voltage_v: float, gap_m: float,
                           mass_kg: float, charge: float = E_CHARGE) -> float:
    if gap_m <= 0 or mass_kg <= 0:
        return 0.0
    return float((4.0/9.0) * EPSILON_0 * np.sqrt(2.0 * charge / mass_kg)
                 * voltage_v**1.5 / gap_m**2)

def ionization_energy(atom: str) -> float:
    table = {
        "xenon": 12.13, "argon": 15.76, "krypton": 14.0,
        "hydrogen": 13.6, "helium": 24.59, "mercury": 10.44,
        "bismuth": 7.29, "iodine": 10.45,
    }
    return table.get(atom.lower(), 12.0)
