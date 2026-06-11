import numpy as np
from dataclasses import dataclass
from .state_vector import StateVector

@dataclass
class SpacecraftConfig:
    name: str = "PROPSIM-SC"
    dry_mass_kg: float = 500.0
    initial_propellant_kg: float = 500.0
    battery_capacity_wh: float = 5000.0
    solar_array_area_m2: float = 10.0
    solar_efficiency: float = 0.30
    thruster_type: str = "hall_thruster"
    thruster_power_w: float = 5000.0
    thruster_isp_s: float = 1800.0
    thruster_efficiency: float = 0.55
    n_thermal_nodes: int = 8
    radiator_area_m2: float = 1.0
    radiator_emissivity: float = 0.85
    base_load_w: float = 100.0
    mission_name: str = "default"
    target_horizon_days: float = 365.0

class SpacecraftState:
    def __init__(self, config: SpacecraftConfig):
        self.config = config
        self.state = StateVector(n_thermal_nodes=config.n_thermal_nodes)
        self.state.mass_total = config.dry_mass_kg + config.initial_propellant_kg
        self.state.mass_propellant = config.initial_propellant_kg
        self.state.battery_energy = config.battery_capacity_wh
        self.state.thermal = np.full(config.n_thermal_nodes, 250.0)

    @property
    def position(self) -> np.ndarray: return self.state.position
    @property
    def velocity(self) -> np.ndarray: return self.state.velocity
    @property
    def orbital_radius(self) -> float: return float(np.linalg.norm(self.position))
    @property
    def speed(self) -> float: return float(np.linalg.norm(self.velocity))
    @property
    def propellant_remaining(self) -> float: return self.state.mass_propellant
    @property
    def propellant_fraction(self) -> float:
        return self.propellant_remaining / self.config.initial_propellant_kg
    @property
    def battery_soc(self) -> float:
        return self.state.battery_energy / self.config.battery_capacity_wh
    @property
    def max_temperature(self) -> float: return float(np.max(self.state.thermal))
    @property
    def min_temperature(self) -> float: return float(np.min(self.state.thermal))

    def snapshot(self) -> dict:
        snap = self.state.to_dict()
        snap.update({
            "name": self.config.name,
            "orbital_radius_m": self.orbital_radius,
            "speed_m_s": self.speed,
            "propellant_fraction": self.propellant_fraction,
            "battery_soc": self.battery_soc,
            "max_temp_k": self.max_temperature,
            "min_temp_k": self.min_temperature,
        })
        return snap
