import numpy as np

class OrbitRenderer:
    def generate_orbit_points(self, semi_major_axis_m: float, eccentricity: float, n_points: int = 100) -> list[tuple[float, float, float]]:
        points = []
        for theta in np.linspace(0, 2*np.pi, n_points):
            r = semi_major_axis_m * (1 - eccentricity**2) / (1 + eccentricity * np.cos(theta))
            points.append((float(r * np.cos(theta)), float(r * np.sin(theta)), 0.0))
        return points
