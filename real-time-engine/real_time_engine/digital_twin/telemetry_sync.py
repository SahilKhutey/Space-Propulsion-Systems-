import numpy as np
from ..state.state_manager import StateManager

class TelemetrySynchronizer:
    def __init__(self, state_manager: StateManager):
        self.sm = state_manager

    def sync(self, telemetry: dict):
        st = self.sm.spacecraft.state
        if "position_m" in telemetry:
            st.position = np.array(telemetry["position_m"])
        if "velocity_m_s" in telemetry:
            st.velocity = np.array(telemetry["velocity_m_s"])
        if "battery_wh" in telemetry:
            st.battery_energy = float(telemetry["battery_wh"])
        if "thermal_k" in telemetry:
            st.thermal = np.array(telemetry["thermal_k"])
