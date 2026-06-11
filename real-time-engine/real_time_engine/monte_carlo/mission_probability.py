from .uncertainty import UncertaintyPropagator

class MissionSuccessCalculator:
    def __init__(self, propagator: UncertaintyPropagator):
        self.propagator = propagator

    def calculate_success_rate(self, horizon_s: float, n_runs: int = 15) -> float:
        trials = self.propagator.propagate_runs(horizon_s, n_runs=n_runs)
        successes = 0
        for run in trials:
            # Criteria: battery energy does not go to 0 and thermal runaway is avoided
            battery_depleted = any(step["battery_wh"] < 0.1 for step in run)
            thermal_runaway = any(step["max_temp_k"] > 343.15 for step in run)
            if not battery_depleted and not thermal_runaway:
                successes += 1
        return successes / n_runs
