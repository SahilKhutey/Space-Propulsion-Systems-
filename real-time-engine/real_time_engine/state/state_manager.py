import time
from collections import deque
from .state_vector import StateVector, StateIndex
from .spacecraft_state import SpacecraftState, SpacecraftConfig
from typing import Callable

class StateManager:
    def __init__(self, config: SpacecraftConfig, history_size: int = 10_000):
        self.spacecraft = SpacecraftState(config)
        self.history = deque(maxlen=history_size)
        self.subscribers = []
        self._t0 = time.time()
        self._t_sim = 0.0

    def subscribe(self, callback: Callable[[dict], None]):
        self.subscribers.append(callback)

    def update(self, dt: float):
        self._t_sim += dt
        self.spacecraft.state.x[StateIndex.TIME] = self._t_sim
        snap = self.spacecraft.snapshot()
        snap["sim_time_s"] = self._t_sim
        snap["wall_time_s"] = time.time() - self._t0
        self.history.append(snap)
        for cb in self.subscribers:
            try:
                cb(snap)
            except Exception as e:
                pass

    def get_history(self) -> list[dict]:
        return list(self.history)
