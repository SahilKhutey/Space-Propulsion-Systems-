"""
PropSim Mathematical Foundation Library.
12-layer architecture supporting all engines from Hall thruster
trade studies to full digital-twin spacecraft systems.
"""
from . import linear_algebra, calculus, classical_mechanics
from . import propulsion, electric_propulsion, orbital_mechanics
from . import mission_design, thermal, power_systems, attitude
from . import optimization, uncertainty, digital_twin

__version__ = "2.0.0"
__all__ = [
    "linear_algebra", "calculus", "classical_mechanics",
    "propulsion", "electric_propulsion", "orbital_mechanics",
    "mission_design", "thermal", "power_systems", "attitude",
    "optimization", "uncertainty", "digital_twin",
]
