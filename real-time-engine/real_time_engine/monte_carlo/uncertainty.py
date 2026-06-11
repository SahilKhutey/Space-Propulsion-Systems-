import numpy as np
import copy
from .sampling import ParameterSampler
from ..real_time.mission_loop import MissionLoop

class UncertaintyPropagator:
    def __init__(self, base_manager):
        self.base_sm = base_manager

    def propagate_runs(self, horizon_s: float, n_runs: int = 15, dt: float = 30.0) -> list[list[dict]]:
        results = []
        sampler = ParameterSampler()
        for _ in range(n_runs):
            cloned_sm = copy.deepcopy(self.base_sm)
            cloned_sm.subscribers = []
            
            # Apply perturbed parameters
            cfg = cloned_sm.spacecraft.config
            cfg.solar_efficiency = sampler.sample_normal(cfg.solar_efficiency, 0.02)
            cfg.dry_mass_kg = sampler.sample_uniform(cfg.dry_mass_kg - 10, cfg.dry_mass_kg + 10)
            
            loop = MissionLoop(cloned_sm, dt=dt)
            steps = int(horizon_s / dt)
            for _ in range(steps):
                loop.step()
                
            results.append(list(cloned_sm.history))
        return results
