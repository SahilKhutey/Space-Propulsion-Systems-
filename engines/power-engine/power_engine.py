"""
Power Sizing Engine
"""
import numpy as np
from core.physics.physics import solar_flux_at_distance


class PowerEngine:
    """Spacecraft power budget and energy balance."""

    def compute(self, params: dict) -> dict:
        area = float(params.get("solar_array_area_m2", 10.0))
        efficiency = float(params.get("solar_efficiency", 0.30))
        distance = float(params.get("distance_au", 1.0))
        battery = float(params.get("battery_capacity_wh", 1000.0))
        thruster_power = float(params.get("thruster_power_w", 1000.0))
        duty_cycle = float(params.get("thruster_duty_cycle", 0.25))
        eclipse_duration = float(params.get("eclipse_duration_min", 35.0))
        orbit_period = float(params.get("orbit_period_min", 90.0))

        # 1. Available solar power
        solar_power = efficiency * area * solar_flux_at_distance(distance)

        # 2. Eclipse loss
        eclipse_frac = min(1.0, eclipse_duration / orbit_period)
        avg_load = thruster_power * duty_cycle
        eclipse_time_s = eclipse_duration * 60
        eclipse_loss_wh = avg_load * eclipse_time_s / 3600

        # 3. Energy produced per orbit
        sunlit_time_s = (orbit_period - eclipse_duration) * 60
        energy_per_orbit_wh = solar_power * sunlit_time_s / 3600

        # 4. Energy used per orbit
        energy_per_orbit_load_wh = avg_load * orbit_period * 60 / 3600

        # 5. Battery margin
        if energy_per_orbit_wh <= 0:
            battery_margin = -1.0
            feasible = False
        else:
            net = (energy_per_orbit_wh - energy_per_orbit_load_wh) / battery
            battery_margin = float(net)
            feasible = net >= 0 and battery >= eclipse_loss_wh

        # 6. Average power
        avg_power = solar_power * (1 - eclipse_frac)

        notes = []
        if not feasible:
            notes.append("Insufficient power: increase solar array or battery, or reduce duty cycle.")
        if solar_power < thruster_power:
            notes.append(
                f"Peak solar ({solar_power:.0f} W) < thruster peak ({thruster_power:.0f} W); "
                "duty cycle must compensate."
            )

        return {
            "solar_power_w": float(solar_power),
            "average_power_w": float(avg_power),
            "eclipse_loss_wh": float(eclipse_loss_wh),
            "thruster_energy_per_orbit_wh": float(energy_per_orbit_load_wh),
            "battery_margin": float(battery_margin),
            "feasible": feasible,
            "notes": notes
        }
