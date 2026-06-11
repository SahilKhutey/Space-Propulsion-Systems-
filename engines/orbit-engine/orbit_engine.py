"""
Orbit Dynamics Engine

Generates 3D coordinates for visualization client.
"""
import numpy as np
from core.constants.constants import R_EARTH


class OrbitEngine:
    """Generates Keplerian coordinate matrices for orbit visualizations."""

    @staticmethod
    def generate_orbit_points(altitude: float, num_points: int = 120) -> list[dict[str, float]]:
        r = R_EARTH + altitude
        theta = np.linspace(0, 2 * np.pi, num_points)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return [{"x": float(px), "y": float(py), "z": 0.0} for px, py in zip(x, y)]

    @staticmethod
    def generate_hohmann_transfer_points(
        start_alt: float,
        target_alt: float,
        num_points: int = 100
    ) -> dict[str, list]:
        r1 = R_EARTH + start_alt
        r2 = R_EARTH + target_alt
        
        theta_init = np.linspace(0, 2 * np.pi, num_points)
        init_orbit = [{"x": float(r1 * np.cos(t)), "y": float(r1 * np.sin(t)), "z": 0.0} for t in theta_init]
        final_orbit = [{"x": float(r2 * np.cos(t)), "y": float(r2 * np.sin(t)), "z": 0.0} for t in theta_init]
        
        a_trans = (r1 + r2) / 2
        e_trans = abs(r2 - r1) / (r1 + r2)
        
        theta_trans = np.linspace(0, np.pi, num_points)
        r_trans = a_trans * (1.0 - e_trans**2) / (1.0 + e_trans * np.cos(theta_trans))
        phase = 0.0 if r1 < r2 else np.pi
        
        transfer_orbit = [
            {
                "x": float(r * np.cos(t + phase)),
                "y": float(r * np.sin(t + phase)),
                "z": 0.0
            }
            for r, t in zip(r_trans, theta_trans)
        ]
        
        return {
            "initial_orbit": init_orbit,
            "final_orbit": final_orbit,
            "transfer_orbit": transfer_orbit
        }

    @staticmethod
    def generate_plume_geometry(thrust_n: float, power_w: float) -> dict:
        length = float(0.5 + 2.0 * np.log10(1.0 + thrust_n * 10.0))
        width = float(0.1 + 0.5 * np.log10(1.0 + power_w / 1000.0))
        
        if power_w == 0:
            color = "#ff4500"
            plume_type = "chemical"
        elif power_w > 50000:
            color = "#00ffff"
            plume_type = "high_power_electric"
        elif power_w > 1000:
            color = "#8a2be2"
            plume_type = "standard_electric"
        else:
            color = "#dda0dd"
            plume_type = "low_power_electric"
            
        return {
            "length": length,
            "width": width,
            "divergence_angle_deg": 15.0 + 10.0 * np.clip(1.0 - thrust_n, 0.0, 1.0),
            "color": color,
            "type": plume_type,
            "opacity": float(np.clip(0.3 + 0.5 * np.log10(1.0 + thrust_n), 0.2, 0.95))
        }
