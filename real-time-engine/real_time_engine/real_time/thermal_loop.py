import numpy as np
from core.constants.constants import SIGMA_SB
from ..state.state_manager import StateManager
from ..propagators.rk4 import rk4_step
from ..state.state_vector import StateIndex

class ThermalLoop:
    def __init__(self, state_manager: StateManager, dt: float = 1.0, ambient_temp_k: float = 3.0):
        self.sm = state_manager
        self.dt = dt
        self.t_amb = ambient_temp_k
        n = state_manager.spacecraft.config.n_thermal_nodes
        self.C = np.full(n, 1000.0)
        self.eps = np.full(n, 0.85)
        self.area = np.full(n, 0.2)
        self.alpha = np.full(n, 0.3)
        self.k_cond = np.eye(n) * 0.15
        self.q_dissipation = np.zeros(n)
        self.T_critical = 343.15

    def step(self):
        st = self.sm.spacecraft.state
        T = st.thermal.copy()
        
        # Calculate active thruster waste heat
        if st.thruster_on:
            waste_heat = self.sm.spacecraft.config.thruster_power_w * (1 - self.sm.spacecraft.config.thruster_efficiency)
            self.q_dissipation[0] = waste_heat
            
        T_new = rk4_step(self._ode, 0.0, T, self.dt)
        st.thermal = T_new
        self.q_dissipation[:] = 0.0

    def _ode(self, t: float, T: np.ndarray) -> np.ndarray:
        solar = 1361.0
        Q_solar = self.alpha * self.area * solar
        Q_rad = self.eps * SIGMA_SB * self.area * (T**4 - self.t_amb**4)
        Q_cond = np.zeros_like(T)
        n = len(T)
        for i in range(n):
            for j in range(n):
                if i != j:
                    Q_cond[i] += self.k_cond[i, j] * (T[j] - T[i])
        return (Q_solar + self.q_dissipation + Q_cond - Q_rad) / self.C

    def add_dissipation(self, node: int, val: float):
        self.q_dissipation[node] += val

    def check_runaway(self) -> list[int]:
        return [i for i, T in enumerate(self.sm.spacecraft.state.thermal) if T > self.T_critical]
