"""
Thrust Modeling Engine

Computes thrust for Hall, Ion, MPD, VASIMR, Arcjet, Resistojet, Chemical,
and Nuclear propulsion systems.
"""
from core.constants.constants import G0


class ThrustEngine:
    """Unified thrust calculator for electric, chemical, and nuclear propulsion."""

    def compute(self, design_type: str, params: dict) -> dict:
        """
        Computes thrust and related performance metrics.
        params contains keys: power_w, efficiency, isp_s, mass_flow_kg_s, propellant.
        """
        # Clean inputs
        power = float(params.get("power_w", 0.0))
        efficiency = float(params.get("efficiency", 0.0))
        isp = float(params.get("isp_s", 0.0))
        mass_flow = float(params.get("mass_flow_kg_s", 0.0))
        propellant = params.get("propellant", "xenon")

        ve = isp * G0

        if "hall" in design_type.lower():
            thrust = 2.0 * efficiency * power / ve if ve > 0 else 0.0
            mdot = mass_flow or (thrust / ve if ve > 0 else 0.0)
            notes = "Hall effect thruster model."
        elif "ion" in design_type.lower():
            thrust = 2.0 * efficiency * power / ve if ve > 0 else 0.0
            mdot = thrust / ve if ve > 0 else 0.0
            notes = "Gridded ion engine model."
        elif "vasimr" in design_type.lower():
            thrust = 2.0 * efficiency * power / ve if ve > 0 else 0.0
            mdot = thrust / ve if ve > 0 else 0.0
            notes = "VASIMR variable-Isp engine model."
        elif "mpd" in design_type.lower():
            thrust = 2.0 * efficiency * power / ve if ve > 0 else 0.0
            mdot = thrust / ve if ve > 0 else 0.0
            notes = "High-power MPD thruster model."
        elif "chemical" in design_type.lower():
            # Pressure-corrected thrust F = mdot * Ve * 1.05
            thrust = mass_flow * ve * 1.05
            power = 0.5 * mass_flow * ve**2
            efficiency = 0.95
            mdot = mass_flow
            notes = f"Chemical {propellant} thruster model."
        elif "ntr" in design_type.lower() or "nuclear" in design_type.lower():
            thrust = mass_flow * ve
            efficiency = 0.85
            mdot = mass_flow
            notes = "Nuclear Thermal Rocket model."
        else:
            # default electrothermal (resistojet/arcjet)
            thrust = 2.0 * efficiency * power / ve if ve > 0 else 0.0
            mdot = thrust / ve if ve > 0 else 0.0
            notes = f"{design_type} model."

        return {
            "thruster_type": design_type,
            "thrust_n": float(thrust),
            "isp_s": float(isp),
            "exhaust_velocity_ms": float(ve),
            "power_w": float(power),
            "efficiency": float(efficiency),
            "mass_flow_kg_s": float(mdot),
            "specific_power_w_per_n": float(power / thrust) if thrust > 0 else float("inf"),
            "notes": notes
        }
