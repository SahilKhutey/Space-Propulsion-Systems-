import numpy as np
from core.constants.constants import AU
from ..state.state_manager import StateManager
from ..state.state_vector import StateIndex

class PowerLoop:
    def __init__(self, state_manager: StateManager, dt: float = 1.0):
        self.sm = state_manager
        self.dt = dt
        self.eclipse = False
        self.loads = {}

    def set_eclipse(self, val: bool):
        self.eclipse = val

    def set_load(self, name: str, val: float):
        self.loads[name] = val

    def step(self):
        sc = self.sm.spacecraft
        st = sc.state
        
        # Solar array power generation
        if self.eclipse:
            p_solar = 0.0
        else:
            r = np.linalg.norm(st.position)
            dist_sun = r if r > 1e9 else AU
            solar_flux = 1361.0 * (AU / dist_sun)**2
            p_solar = sc.config.solar_efficiency * sc.config.solar_array_area_m2 * solar_flux
        
        # Power Load
        p_load = sc.config.base_load_w + sum(self.loads.values())
        if st.thruster_on:
            p_load += sc.config.thruster_power_w
            
        net = p_solar - p_load
        st.battery_energy = max(0.0, min(sc.config.battery_capacity_wh, st.battery_energy + net * self.dt / 3600.0))
        
        st.x[StateIndex.POWER_SOLAR] = p_solar
        st.x[StateIndex.POWER_LOAD] = p_load
        st.x[StateIndex.POWER_BATTERY_FLOW] = net
