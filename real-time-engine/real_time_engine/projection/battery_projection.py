from .future_state import FutureStateProjector

class BatteryProjector:
    def __init__(self, projector_or_sm):
        if hasattr(projector_or_sm, "spacecraft"):
            self.sm = projector_or_sm
            self.projector = FutureStateProjector(projector_or_sm)
        else:
            self.projector = projector_or_sm
            self.sm = projector_or_sm.sm

    def project_soc_profile(self, horizon_s: float) -> list[tuple[float, float]]:
        history = self.projector.project(horizon_s)
        return [(step["sim_time_s"], step["battery_soc"]) for step in history]

    def predict_depletion(self, current_load_w: float) -> float:
        if current_load_w <= 0:
            return float("inf")
        energy_wh = self.sm.spacecraft.state.battery_energy
        return float((energy_wh / current_load_w) * 3600.0)
