from .future_state import FutureStateProjector

class FailurePredictor:
    def __init__(self, projector_or_sm, thermal_loop=None):
        if hasattr(projector_or_sm, "spacecraft"):
            self.sm = projector_or_sm
            self.projector = FutureStateProjector(projector_or_sm)
        else:
            self.projector = projector_or_sm
            self.sm = projector_or_sm.sm
        self.thermal = thermal_loop

    def predict_failures(self, horizon_s: float) -> dict:
        history = self.projector.project(horizon_s)
        
        critical_temp = 343.15
        thermal_runaway = False
        runaway_time = None
        for step in history:
            temps = step["thermal_k"]
            if any(t > critical_temp for t in temps):
                thermal_runaway = True
                runaway_time = step["sim_time_s"]
                break
                
        final_hours = history[-1]["thruster_hours"] if history else 0.0
        thruster_failed = final_hours > 5000.0
        
        final_soc = history[-1]["battery_soc"] if history else 1.0
        battery_failed = final_soc < 0.10
        
        return {
            "thermal_runaway_predicted": thermal_runaway,
            "thermal_runaway_time_s": runaway_time,
            "thruster_wearout_predicted": thruster_failed,
            "thruster_accumulated_hours": final_hours,
            "battery_critical_depletion": battery_failed
        }

    def thruster_rul(self) -> dict:
        hours_used = float(self.sm.spacecraft.state.thruster_hours)
        max_hours = 10000.0
        remaining = max(0.0, max_hours - hours_used)
        return {
            "max_hours": max_hours,
            "hours_remaining": remaining
        }
