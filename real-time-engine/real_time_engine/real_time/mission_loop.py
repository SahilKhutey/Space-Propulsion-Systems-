from ..state.state_manager import StateManager
from .propulsion_loop import PropulsionLoop
from .thermal_loop import ThermalLoop
from .power_loop import PowerLoop
from .orbit_loop import OrbitLoop

class MissionLoop:
    def __init__(self, state_manager: StateManager, dt: float = 1.0):
        self.sm = state_manager
        self.dt = dt
        
        self.orbit = OrbitLoop(state_manager, dt=dt)
        self.thermal = ThermalLoop(state_manager, dt=dt)
        self.power = PowerLoop(state_manager, dt=dt)
        self.propulsion = PropulsionLoop(state_manager, dt=dt)

    def step(self):
        self.orbit.step()
        self.thermal.step()
        self.power.step()
        self.propulsion.step()
        self.sm.update(self.dt)

    def run(self, n_steps: int):
        for _ in range(n_steps):
            self.step()
