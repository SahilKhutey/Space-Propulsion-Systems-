import numpy as np
from collections import deque

class TelemetryPacket:
    def __init__(self, timestamp: float, source: str, measurements: dict):
        self.timestamp = timestamp
        self.source = source
        self.measurements = measurements

class TelemetryStream:
    def __init__(self):
        self.packets = deque()
        
    def push(self, packet: TelemetryPacket):
        self.packets.append(packet)
        
    def pop(self) -> TelemetryPacket:
        if self.packets:
            return self.packets.popleft()
        return None
        
    def has_packets(self) -> bool:
        return len(self.packets) > 0

class DigitalTwin:
    def __init__(self, config, stream: TelemetryStream, estimator: str = "ekf"):
        self.config = config
        self.stream = stream
        self.estimator_type = estimator
        self.last_telemetry = None
        # Position & Velocity: LEO 400km default
        from core.constants.constants import G, M_EARTH, R_EARTH
        r = R_EARTH + 400e3
        v = np.sqrt(G * M_EARTH / r)
        self.state = np.array([r, 0.0, 0.0, 0.0, v, 0.0])

    def run_step(self):
        if self.stream.has_packets():
            pkt = self.stream.pop()
            self.last_telemetry = pkt.measurements
            meas = pkt.measurements
            if "x" in meas: self.state[0] = meas["x"]
            if "y" in meas: self.state[1] = meas["y"]
            if "z" in meas: self.state[2] = meas["z"]
            if "vx" in meas: self.state[3] = meas["vx"]
            if "vy" in meas: self.state[4] = meas["vy"]
            if "vz" in meas: self.state[5] = meas["vz"]
        else:
            # Propagate state with simple two-body model
            mu = 3.986004418e14
            r_vec = self.state[:3]
            v_vec = self.state[3:]
            r_mag = np.linalg.norm(r_vec)
            if r_mag > 1e-6:
                a_vec = -mu * r_vec / r_mag**3
                dt = 1.0
                self.state[:3] += v_vec * dt
                self.state[3:] += a_vec * dt

    def get_estimated_state(self) -> np.ndarray:
        return self.state
