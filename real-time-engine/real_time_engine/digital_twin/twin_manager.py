from ..state.state_manager import StateManager
from .telemetry_sync import TelemetrySynchronizer

class DigitalTwinManager:
    def __init__(self, state_manager: StateManager):
        self.sm = state_manager
        self.sync = TelemetrySynchronizer(state_manager)

    def process_telemetry_tick(self, telemetry: dict):
        self.sync.sync(telemetry)
