from core.constants.constants import E_CHARGE, G0

def vasimr_thrust(power_w: float, efficiency: float, isp_s: float) -> float:
    v_e = isp_s * G0
    if v_e <= 0:
        return 0.0
    return float(2.0 * efficiency * power_w / v_e)

def vasimr_ion_energy(icrf_power_w: float, ion_flux_per_s: float,
                     charge: float = E_CHARGE) -> float:
    if ion_flux_per_s <= 0:
        return 0.0
    return float(icrf_power_w / (ion_flux_per_s * charge))

def vasimr_plasma_creation(helicon_power_w: float, ionization_cost_eV: float = 30.0) -> float:
    energy_per_ion = ionization_cost_eV * E_CHARGE
    if energy_per_ion <= 0:
        return 0.0
    return float(helicon_power_w / energy_per_ion)
