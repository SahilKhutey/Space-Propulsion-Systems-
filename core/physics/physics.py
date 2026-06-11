"""
Core physics functions used across all propulsion simulation modules.
All functions are pure, vectorized (NumPy), and unit-agnostic via explicit SI.
"""
import numpy as np
from ..constants.constants import G, G0, M_EARTH, R_EARTH, AU, SOLAR_FLUX


# ----- Orbital mechanics -----

def circular_velocity(altitude: float, planet_mass: float = M_EARTH,
                      planet_radius: float = R_EARTH) -> float:
    """Velocity for circular orbit at given altitude [m/s]."""
    r = planet_radius + altitude
    return float(np.sqrt(G * planet_mass / r))


def escape_velocity(altitude: float, planet_mass: float = M_EARTH,
                    planet_radius: float = R_EARTH) -> float:
    """Escape velocity from altitude [m/s]."""
    r = planet_radius + altitude
    return float(np.sqrt(2 * G * planet_mass / r))


def orbital_period(altitude: float, planet_mass: float = M_EARTH,
                   planet_radius: float = R_EARTH) -> float:
    """Orbital period [s]."""
    r = planet_radius + altitude
    return float(2 * np.pi * np.sqrt(r**3 / (G * planet_mass)))


# ----- Rocket equation (Tsiolkovsky) -----

def delta_v(isp: float, m0: float, mf: float) -> float:
    """Tsiolkovsky delta-V [m/s]."""
    if mf <= 0 or m0 <= mf:
        raise ValueError("Invalid masses: require m0 > mf > 0")
    return float(isp * G0 * np.log(m0 / mf))


def propellant_mass_for_deltav(deltav: float, isp: float, payload_mass: float) -> float:
    """Solve rocket equation for required propellant mass [kg]."""
    mass_ratio = np.exp(deltav / (isp * G0))
    m0 = payload_mass * mass_ratio
    return float(m0 - payload_mass)


def mass_ratio_for_deltav(deltav: float, isp: float) -> float:
    """Required mass ratio (m0/mf) for given delta-V."""
    return float(np.exp(deltav / (isp * G0)))


# ----- Power / solar -----

def solar_flux_at_distance(distance_au: float) -> float:
    """Solar flux [W/m^2] at given distance in AU."""
    return float(SOLAR_FLUX["earth"] / distance_au**2)


def solar_power(efficiency: float, area_m2: float, distance_au: float = 1.0) -> float:
    """Power from solar panel [W]."""
    return float(efficiency * area_m2 * solar_flux_at_distance(distance_au))


def eclipse_fraction(altitude: float, beta_angle: float = 0.0) -> float:
    """
    Approximate eclipse fraction per orbit.
    beta_angle: sun-orbit angle [deg]. 0 = full eclipse, 90 = none.
    """
    beta = np.deg2rad(beta_angle)
    return float(max(0.0, np.cos(beta)) * 0.35)  # ~35% max for LEO


# ----- Thermal -----

def radiation_heat(emissivity: float, area_m2: float,
                   t_hot: float, t_cold: float) -> float:
    """Net radiated heat [W] between two surfaces."""
    return float(emissivity * 5.670374419e-8 * area_m2 *
                 (t_hot**4 - t_cold**4))


def conduction_heat(conductivity: float, area_m2: float,
                    delta_t: float, length: float) -> float:
    """Conductive heat transfer [W] (Fourier's law)."""
    if length <= 0:
        raise ValueError("Length must be positive")
    return float(conductivity * area_m2 * delta_t / length)


# ----- Mission -----

def hohmann_transfer_delta_v(r1: float, r2: float,
                             planet_mass: float = M_EARTH) -> tuple[float, float]:
    """
    Hohmann transfer between two coplanar circular orbits.
    Returns (dv1, dv2) [m/s].
    """
    mu = G * planet_mass
    dv1 = np.sqrt(mu / r1) * (np.sqrt(2 * r2 / (r1 + r2)) - 1)
    dv2 = np.sqrt(mu / r2) * (1 - np.sqrt(2 * r1 / (r1 + r2)))
    return float(dv1), float(dv2)


def transfer_time_hohmann(r1: float, r2: float,
                          planet_mass: float = M_EARTH) -> float:
    """Hohmann transfer time [s]."""
    mu = G * planet_mass
    a = (r1 + r2) / 2
    return float(np.pi * np.sqrt(a**3 / mu))
