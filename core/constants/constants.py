"""
Physical constants and reference data for aerospace propulsion simulations.
All SI units unless otherwise noted.
"""
from dataclasses import dataclass

# Fundamental constants
G0 = 9.80665           # Earth surface gravity [m/s^2]
G = 6.67430e-11        # Gravitational constant [m^3/kg/s^2]
K_BOLTZMANN = 1.380649e-23  # Boltzmann constant [J/K]
SIGMA_SB = 5.670374419e-8  # Stefan-Boltzmann constant [W/m^2/K^4]
AU = 1.495978707e11    # Astronomical unit [m]
C_LIGHT = 299792458    # Speed of light [m/s]
R_EARTH = 6.371e6      # Earth radius [m]
M_EARTH = 5.972e24     # Earth mass [kg]
R_SUN = 6.957e8        # Sun radius [m]
EPSILON_0 = 8.8541878128e-12 # Vacuum permittivity [F/m]
E_CHARGE = 1.602176634e-19   # Elementary charge [C]

# Solar flux at reference distances [W/m^2]
SOLAR_FLUX = {
    "mercury": 9126.0,
    "venus": 2611.0,
    "earth": 1361.0,
    "mars": 586.0,
    "jupiter": 50.0,
    "saturn": 14.9,
    "uranus": 3.7,
    "neptune": 1.5,
    "pluto": 0.9
}

# Standard reference Isp ranges [s] for trade studies
ISP_RANGES = {
    "chemical_bipropellant": (300, 450),
    "chemical_monopropellant": (200, 280),
    "chemical_solid": (200, 290),
    "chemical_LOX_LH2": (380, 480),
    "chemical_LOX_methane": (320, 380),
    "resistojet": (150, 350),
    "arcjet": (400, 1200),
    "hall_thruster": (1000, 3000),
    "ion_thruster": (2500, 10000),
    "MPD": (2000, 8000),
    "PPT": (500, 2000),
    "VASIMR": (3000, 30000),
    "NTR": (700, 1000),
    "NEP": (2000, 10000)
}

# Thruster technology categories
THRUSTER_CATEGORIES = {
    "electric": ["resistojet", "arcjet", "hall_thruster", "ion_thruster",
                 "MPD", "PPT", "VASIMR"],
    "chemical": ["chemical_bipropellant", "chemical_monopropellant",
                 "chemical_solid", "chemical_LOX_LH2", "chemical_LOX_methane"],
    "nuclear": ["NTR", "NEP"]
}

# Common propellant combinations
PROPELLANTS = {
    "xenon": {"molar_mass": 0.1313, "category": "electric"},
    "argon": {"molar_mass": 0.0399, "category": "electric"},
    "hydrazine": {"molar_mass": 0.0320, "category": "chemical_monopropellant"},
    "N2H4_N2O4": {"molar_mass": 0.0460, "category": "chemical_bipropellant"},
    "LOX_LH2": {"molar_mass": 0.0080, "category": "chemical_LOX_LH2"},
    "LOX_methane": {"molar_mass": 0.0200, "category": "chemical_LOX_methane"},
    "hydrogen_NTR": {"molar_mass": 0.0020, "category": "NTR"}
}

# Orbital mechanics reference
ORBITAL_REGIMES = {
    "LEO": {"altitude": 400e3, "description": "Low Earth Orbit"},
    "SSO": {"altitude": 800e3, "description": "Sun-synchronous Orbit"},
    "MEO": {"altitude": 20000e3, "description": "Medium Earth Orbit"},
    "GEO": {"altitude": 35786e3, "description": "Geostationary Orbit"},
    "HEO": {"altitude": 100000e3, "description": "High Earth Orbit"},
    "LUNAR": {"altitude": 384400e3, "description": "Lunar distance"},
    "MARS": {"altitude": 225e9, "description": "Mars transfer"}
}


@dataclass(frozen=True)
class PlanetData:
    name: str
    radius: float          # m
    mass: float            # kg
    semi_major_axis: float # m
    eccentricity: float
    solar_flux: float      # W/m^2


PLANETS = {
    "earth": PlanetData("Earth", 6.371e6, 5.972e24, 1.496e11, 0.0167, 1361.0),
    "mars": PlanetData("Mars", 3.3895e6, 6.39e23, 2.279e11, 0.0934, 586.0),
    "venus": PlanetData("Venus", 6.0518e6, 4.867e24, 1.082e11, 0.0068, 2611.0),
    "jupiter": PlanetData("Jupiter", 6.9911e7, 1.898e27, 7.785e11, 0.0489, 50.0),
    "saturn": PlanetData("Saturn", 5.8232e7, 5.683e26, 1.434e12, 0.0565, 14.9),
}
