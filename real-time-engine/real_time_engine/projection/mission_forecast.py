from .future_state import FutureStateProjector

class MissionForecaster:
    def __init__(self, projector: FutureStateProjector):
        self.projector = projector

    def forecast_resources(self, horizon_s: float) -> dict:
        history = self.projector.project(horizon_s)
        if not history:
            return {}
            
        final_state = history[-1]
        battery_empty = any(step["battery_wh"] <= 1e-3 for step in history)
        propellant_empty = any(step["mass_propellant_kg"] <= 1e-3 for step in history)
        
        return {
            "horizon_projected_s": horizon_s,
            "final_battery_wh": final_state["battery_wh"],
            "final_propellant_kg": final_state["mass_propellant_kg"],
            "battery_depleted_risk": battery_empty,
            "propellant_depleted_risk": propellant_empty,
            "delta_v_delivered_m_s": final_state["delta_v_used_ms"]
        }
