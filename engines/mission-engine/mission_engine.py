"""
Mission Trajectory Sizing Engine
"""
import numpy as np
from core.constants.constants import G0, R_EARTH
from core.physics.physics import (
    propellant_mass_for_deltav,
    hohmann_transfer_delta_v,
    transfer_time_hohmann
)

ORBIT_ALTITUDES = {
    "LEO": 400e3,
    "SSO": 800e3,
    "MEO": 20000e3,
    "GEO": 35786e3,
    "HEO": 100000e3,
    "LUNAR": 384400e3,
}

DELTA_V_REFERENCE = {
    ("LEO", "GEO"): 4250.0,
    ("LEO", "MEO"): 2450.0,
    ("LEO", "SSO"): 200.0,
    ("GEO", "LUNAR"): 3130.0,
    ("LUNAR", "MARS_TRANSFER"): 800.0,
    ("LEO", "LUNAR"): 7380.0,
    ("MEO", "GEO"): 1800.0,
}


class MissionEngine:
    """End-to-end mission analysis."""

    def compute(self, params: dict) -> dict:
        name = params.get("name", "GEO Injection Mission")
        initial_orbit = params.get("initial_orbit", "LEO")
        target_orbit = params.get("target_orbit", "GEO")
        payload_mass = float(params.get("payload_mass_kg", 1000.0))
        thruster_type = params.get("thruster_type", "hall_thruster")
        isp = float(params.get("isp_s", 2000.0))
        efficiency = float(params.get("efficiency", 0.60))
        power = float(params.get("power_w", 5000.0))
        safety_factor = float(params.get("safety_factor", 1.2))

        # 1. Determine delta-V (with safety factor)
        raw_dv = self._resolve_delta_v(initial_orbit, target_orbit)
        dv_with_safety = raw_dv * safety_factor

        # 2. Determine propellant mass
        prop_mass = propellant_mass_for_deltav(
            deltav=dv_with_safety,
            isp=isp,
            payload_mass=payload_mass
        )

        initial_mass = payload_mass + prop_mass
        final_mass = payload_mass

        # 3. Determine transfer time and power consumed
        is_electric = self._is_electric(thruster_type)
        ve = isp * G0
        thrust = 2.0 * efficiency * power / ve if is_electric else 500.0
        
        if is_electric:
            mdot = thrust / ve
            t_burn_s = prop_mass / mdot if mdot > 0 else 0.0
            duty_cycle = 0.85
            transfer_time_days = (t_burn_s / duty_cycle) / 86400.0
            power_consumed_kwh = (power * (t_burn_s / 3600.0)) / 1000.0
        else:
            r1 = R_EARTH + ORBIT_ALTITUDES.get(initial_orbit, 400e3)
            r2 = R_EARTH + ORBIT_ALTITUDES.get(target_orbit, 35786e3)
            t_transfer_s = transfer_time_hohmann(r1, r2)
            transfer_time_days = t_transfer_s / 86400.0
            t_burn_s = prop_mass / (thrust / ve) if thrust > 0 else 0.0
            power_consumed_kwh = (power * (t_burn_s / 3600.0)) / 1000.0

        # 4. Thermal load
        thermal_load_w = power * (1.0 - efficiency)

        # 5. Success probability
        success_prob = self._estimate_success_probability(
            thruster_type,
            transfer_time_days,
            safety_factor
        )

        notes = [
            f"Required Delta-V (raw): {raw_dv:.1f} m/s",
            f"Design Delta-V (with {safety_factor} safety factor): {dv_with_safety:.1f} m/s",
            f"Thrust level: {thrust:.3f} N"
        ]

        return {
            "mission_name": name,
            "delta_v_ms": dv_with_safety,
            "propellant_mass_kg": prop_mass,
            "initial_mass_kg": initial_mass,
            "final_mass_kg": final_mass,
            "transfer_time_days": transfer_time_days,
            "power_consumed_kwh": power_consumed_kwh,
            "thermal_load_w": thermal_load_w,
            "success_probability": success_prob,
            "notes": notes
        }

    def _resolve_delta_v(self, start: str, target: str) -> float:
        if start == target:
            return 0.0
        pair = (start, target)
        rev_pair = (target, start)
        if pair in DELTA_V_REFERENCE:
            return DELTA_V_REFERENCE[pair]
        if rev_pair in DELTA_V_REFERENCE:
            return DELTA_V_REFERENCE[rev_pair]

        h1 = ORBIT_ALTITUDES.get(start, 400e3)
        h2 = ORBIT_ALTITUDES.get(target, 35786e3)
        r1 = R_EARTH + h1
        r2 = R_EARTH + h2
        
        try:
            dv1, dv2 = hohmann_transfer_delta_v(r1, r2)
            return abs(dv1) + abs(dv2)
        except Exception:
            if "MARS" in target or "MARS" in start:
                return 5700.0
            if "ASTEROID" in target or "ASTEROID" in start:
                return 8000.0
            return 4500.0

    def _is_electric(self, thruster_type: str) -> bool:
        t = thruster_type.lower()
        return any(x in t for x in ["hall", "ion", "electric", "vasimr", "mpd", "ppt", "arcjet", "resistojet"])

    def _estimate_success_probability(self, thruster_type: str, transfer_days: float, safety_factor: float) -> float:
        t = thruster_type.lower()
        if "chemical" in t:
            base_rel = 0.99
        elif "ion" in t:
            base_rel = 0.97
        elif "hall" in t:
            base_rel = 0.95
        elif "vasimr" in t or "mpd" in t:
            base_rel = 0.88
        elif "ntr" in t:
            base_rel = 0.90
        else:
            base_rel = 0.92

        if self._is_electric(thruster_type):
            time_penalty = np.exp(-transfer_days / (365.25 * 10))
        else:
            time_penalty = 1.0

        safety_bonus = 1.0 - (1.0 - base_rel) / (safety_factor ** 1.5)
        prob = safety_bonus * time_penalty
        return float(np.clip(prob, 0.1, 0.999))
