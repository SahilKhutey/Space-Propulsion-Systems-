import numpy as np
from core.constants.constants import G0
from ..state.state_manager import StateManager
from ..state.state_vector import StateIndex

class PropulsionLoop:
    def __init__(self, state_manager: StateManager, dt: float = 1.0):
        self.sm = state_manager
        self.dt = dt
        self.cfg = state_manager.spacecraft.config
        
        ve = self.cfg.thruster_isp_s * G0
        self.ve = ve
        self.mdot = (2 * self.cfg.thruster_efficiency * self.cfg.thruster_power_w / ve**2) if ve > 0 else 0.0
        self.thrust = self.mdot * ve
        self.thrust_direction = np.array([1.0, 0.0, 0.0])

    def step(self):
        sc = self.sm.spacecraft
        st = sc.state
        if not st.thruster_on:
            return
        
        # Propellant flow
        new_prop = max(0.0, st.mass_propellant - self.mdot * self.dt)
        delta_m = st.mass_propellant - new_prop
        st.mass_propellant = new_prop
        st.mass_total -= delta_m

        # Force application
        if st.mass_total > 1e-3:
            accel = (self.thrust * self.thrust_direction) / st.mass_total
            st.velocity = st.velocity + accel * self.dt
            dv = self.thrust * self.dt / st.mass_total
            st.x[StateIndex.DELTA_V_USED] += dv

        # Record metrics
        st.x[StateIndex.THRUSTER_HOURS] += self.dt / 3600.0
