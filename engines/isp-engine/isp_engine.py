"""
ISP Sizing Engine
"""
import numpy as np
from core.constants.constants import G0


class IspEngine:
    """Isp analysis and system-level mass / lifetime calculations."""

    @staticmethod
    def isp_from_thrust_power(thrust_n: float, power_w: float) -> float:
        if thrust_n <= 0:
            return 0.0
        return 2 * power_w / (thrust_n * G0)

    @staticmethod
    def propellant_consumption(thrust_n: float, isp_s: float, time_s: float) -> float:
        if isp_s <= 0 or time_s <= 0:
            return 0.0
        mdot = thrust_n / (isp_s * G0)
        return mdot * time_s

    @staticmethod
    def mission_lifetime_years(propellant_kg: float, thrust_n: float,
                              isp_s: float, duty_cycle: float = 1.0) -> float:
        if thrust_n <= 0 or isp_s <= 0:
            return 0.0
        mdot = thrust_n / (isp_s * G0)
        if mdot == 0:
            return float("inf")
        seconds = (propellant_kg / mdot) * duty_cycle
        return seconds / (365.25 * 24 * 3600)

    @staticmethod
    def delta_v_capability(isp_s: float, propellant_kg: float,
                           dry_mass_kg: float) -> float:
        m0 = propellant_kg + dry_mass_kg
        mf = dry_mass_kg
        if mf <= 0 or m0 <= mf:
            return 0.0
        return isp_s * G0 * np.log(m0 / mf)
