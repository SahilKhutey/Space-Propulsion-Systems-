"""
System state vector — the single source of truth for the simulation.
X(t) = [position, velocity, mass, temperatures, battery, power, thruster_state, ...]
"""
import numpy as np
from typing import Any
from enum import IntEnum

class StateIndex(IntEnum):
    POS_X = 0
    POS_Y = 1
    POS_Z = 2
    VEL_X = 3
    VEL_Y = 4
    VEL_Z = 5
    MASS_TOTAL = 6
    MASS_PROPELLANT = 7
    Q_W = 8
    Q_X = 9
    Q_Y = 10
    Q_Z = 11
    OMEGA_X = 12
    OMEGA_Y = 13
    OMEGA_Z = 14
    THERMAL_START = 15
    BATTERY_ENERGY = 50
    POWER_SOLAR = 51
    POWER_LOAD = 52
    POWER_BATTERY_FLOW = 53
    THRUSTER_ON = 54
    THRUSTER_POWER = 55
    THRUSTER_TEMP = 56
    THRUSTER_HOURS = 1007
    TIME = 1008
    DELTA_V_USED = 1009

class StateVector:
    BASE_SIZE = 15
    EXTRA_SIZE = 1500

    def __init__(self, n_thermal_nodes: int = 8):
        self.n_thermal = n_thermal_nodes
        self.size = self.BASE_SIZE + n_thermal_nodes + self.EXTRA_SIZE
        self.x = np.zeros(self.size)
        self.x[StateIndex.Q_W] = 1.0
        self.x[StateIndex.MASS_TOTAL] = 1000.0
        self.x[StateIndex.MASS_PROPELLANT] = 500.0
        self.x[StateIndex.BATTERY_ENERGY] = 5000.0

    @property
    def position(self) -> np.ndarray:
        return self.x[StateIndex.POS_X:StateIndex.POS_X+3]

    @position.setter
    def position(self, v: np.ndarray):
        self.x[StateIndex.POS_X:StateIndex.POS_X+3] = v

    @property
    def velocity(self) -> np.ndarray:
        return self.x[StateIndex.VEL_X:StateIndex.VEL_X+3]

    @velocity.setter
    def velocity(self, v: np.ndarray):
        self.x[StateIndex.VEL_X:StateIndex.VEL_X+3] = v

    @property
    def mass_total(self) -> float:
        return float(self.x[StateIndex.MASS_TOTAL])

    @mass_total.setter
    def mass_total(self, v: float):
        self.x[StateIndex.MASS_TOTAL] = v

    @property
    def mass_propellant(self) -> float:
        return float(self.x[StateIndex.MASS_PROPELLANT])

    @mass_propellant.setter
    def mass_propellant(self, v: float):
        v = max(0.0, v)
        self.x[StateIndex.MASS_PROPELLANT] = v

    @property
    def quaternion(self) -> np.ndarray:
        return self.x[StateIndex.Q_W:StateIndex.Q_W+4]

    @quaternion.setter
    def quaternion(self, q: np.ndarray):
        n = np.linalg.norm(q)
        if n > 1e-12:
            self.x[StateIndex.Q_W:StateIndex.Q_W+4] = q / n

    @property
    def omega(self) -> np.ndarray:
        return self.x[StateIndex.OMEGA_X:StateIndex.OMEGA_X+3]

    @omega.setter
    def omega(self, v: np.ndarray):
        self.x[StateIndex.OMEGA_X:StateIndex.OMEGA_X+3] = v

    @property
    def thermal(self) -> np.ndarray:
        return self.x[StateIndex.THERMAL_START:StateIndex.THERMAL_START+self.n_thermal]

    @thermal.setter
    def thermal(self, v: np.ndarray):
        n = min(len(v), self.n_thermal)
        self.x[StateIndex.THERMAL_START:StateIndex.THERMAL_START+n] = v[:n]

    @property
    def battery_energy(self) -> float:
        return float(self.x[StateIndex.BATTERY_ENERGY])

    @battery_energy.setter
    def battery_energy(self, v: float):
        self.x[StateIndex.BATTERY_ENERGY] = max(0.0, v)

    @property
    def thruster_on(self) -> bool:
        return bool(self.x[StateIndex.THRUSTER_ON] > 0.5)

    @thruster_on.setter
    def thruster_on(self, v: bool):
        self.x[StateIndex.THRUSTER_ON] = 1.0 if v else 0.0

    @property
    def thruster_hours(self) -> float:
        return float(self.x[StateIndex.THRUSTER_HOURS])

    def get_thermal_node(self, i: int) -> float:
        return float(self.x[StateIndex.THERMAL_START + i])

    def set_thermal_node(self, i: int, T: float):
        self.x[StateIndex.THERMAL_START + i] = T

    def to_dict(self) -> dict[str, Any]:
        return {
            "position_m": self.position.tolist(),
            "velocity_m_s": self.velocity.tolist(),
            "mass_total_kg": self.mass_total,
            "mass_propellant_kg": self.mass_propellant,
            "quaternion": self.quaternion.tolist(),
            "omega_rad_s": self.omega.tolist(),
            "thermal_k": self.thermal.tolist(),
            "battery_wh": self.battery_energy,
            "thruster_on": self.thruster_on,
            "thruster_hours": self.thruster_hours,
            "time": float(self.x[StateIndex.TIME]),
            "delta_v_used_ms": float(self.x[StateIndex.DELTA_V_USED]),
            "power_solar": float(self.x[StateIndex.POWER_SOLAR]),
            "power_load": float(self.x[StateIndex.POWER_LOAD]),
            "power_battery_flow": float(self.x[StateIndex.POWER_BATTERY_FLOW]),
        }
