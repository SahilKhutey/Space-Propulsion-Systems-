from .future_state import FutureStateProjector

class ThermalProjector:
    def __init__(self, projector: FutureStateProjector):
        self.projector = projector

    def project_max_temp_profile(self, horizon_s: float) -> list[tuple[float, float]]:
        history = self.projector.project(horizon_s)
        return [(step["sim_time_s"], step["max_temp_k"]) for step in history]
