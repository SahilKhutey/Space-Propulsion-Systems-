import numpy as np
import copy
from ..state.state_manager import StateManager
from ..real_time.mission_loop import MissionLoop

class FutureStateProjector:
    def __init__(self, loop_or_sm, dt: float = 10.0):
        if hasattr(loop_or_sm, "sm"):
            self.loop = loop_or_sm
            self.sm = loop_or_sm.sm
            self.dt = loop_or_sm.dt
        else:
            self.sm = loop_or_sm
            self.dt = dt
            self.loop = MissionLoop(self.sm, dt=dt)

    def project(self, *args, **kwargs) -> list[dict] | dict:
        # Check if first arg is float/int (horizon_s)
        if len(args) > 0 and isinstance(args[0], (int, float)):
            horizon_s = args[0]
            dt = args[1] if len(args) > 1 else self.dt
            cloned_sm = copy.deepcopy(self.sm)
            cloned_sm.subscribers = []
            loop = MissionLoop(cloned_sm, dt=dt)
            steps = int(horizon_s / dt)
            for _ in range(steps):
                loop.step()
            return list(cloned_sm.history)
        
        # Scenario-based project(self, sm, scenarios=None)
        sm = args[0] if len(args) > 0 else kwargs.get("sm", self.sm)
        scenarios = args[1] if len(args) > 1 else kwargs.get("scenarios", None)
        
        cloned_sm = copy.deepcopy(sm)
        cloned_sm.subscribers = []
        
        if scenarios:
            for k, v in scenarios.items():
                if k == "thruster_on":
                    cloned_sm.spacecraft.state.thruster_on = v
                    
        # Simulate for 24h = 86400 seconds
        dt = self.dt
        loop = MissionLoop(cloned_sm, dt=dt)
        steps = int(86400.0 / dt)
        for _ in range(steps):
            loop.step()
            
        return {
            "24h": {
                "state": {
                    "mass_propellant_kg": float(cloned_sm.spacecraft.state.mass_propellant),
                    "battery_wh": float(cloned_sm.spacecraft.state.battery_energy),
                    "thermal_k": cloned_sm.spacecraft.state.thermal.tolist()
                }
            }
        }
