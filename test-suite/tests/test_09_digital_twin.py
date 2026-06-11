import pytest
import numpy as np
import time
import sys
from pathlib import Path

# Add paths for standalone execution if needed
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "real-time-engine"))

from real_time_engine import (
    SpacecraftConfig, TelemetryStream, TelemetryPacket,
    DigitalTwin, KalmanFilter, ExtendedKalmanFilter
)


# ===== Test 27: Telemetry Sync =====
@pytest.mark.digital_twin
class TestTelemetrySync:
    """Test 27: Inject measurements → twin state updated."""

    def test_twin_receives_telemetry(self):
        cfg = SpacecraftConfig(name="Twin", dry_mass_kg=500, initial_propellant_kg=500)
        stream = TelemetryStream()
        twin = DigitalTwin(cfg, stream, estimator="ekf")
        pkt = TelemetryPacket(
            timestamp=time.time(),
            source="ground",
            measurements={"x": 7.0e6, "y": 0.0, "z": 0.0, "vx": 0.0, "vy": 7500.0, "vz": 0.0}
        )
        stream.push(pkt)
        twin.run_step()
        assert twin.last_telemetry is not None
        assert twin.last_telemetry["x"] == 7.0e6


# ===== Test 28: Sensor Failure =====
@pytest.mark.digital_twin
class TestSensorFailure:
    """Test 28: No telemetry → estimator still predicts."""

    def test_estimator_predicts_without_telemetry(self):
        cfg = SpacecraftConfig(name="NoSensors", dry_mass_kg=500, initial_propellant_kg=500)
        stream = TelemetryStream()
        twin = DigitalTwin(cfg, stream, estimator="kf")
        # Run sim steps without telemetry
        for _ in range(10):
            twin.run_step()
        # Estimator should still have a state
        state = twin.get_estimated_state()
        assert state is not None
        assert len(state) == 6


# ===== Test 29: Kalman Filter =====
@pytest.mark.digital_twin
class TestKalmanFilter:
    """Test 29: With noise → filtered state closer to truth."""

    def test_kf_reduces_noise(self):
        F = np.eye(2)
        F[0, 1] = 1.0
        H = np.eye(2)
        Q = np.eye(2) * 0.01
        R = np.eye(2) * 1.0
        kf = KalmanFilter(F, H, Q, R, x0=np.array([0.0, 1.0]))
        # Truth: constant velocity 1
        truth = np.array([0.0, 1.0])
        np.random.seed(42)
        for k in range(50):
            truth = F @ truth
            z = truth + np.random.normal(0, 0.5, 2)
            kf.step(z)
        est = kf.get_state()
        # Filtered should be within 0.5 of truth
        assert abs(est[0] - truth[0]) < 0.5
        assert abs(est[1] - truth[1]) < 0.5

    def test_ekf_orbit_convergence(self):
        from core.constants.constants import G, M_EARTH, R_EARTH
        mu = G * M_EARTH
        r = R_EARTH + 400e3
        v = np.sqrt(mu / r)

        def f_cont(x, u=None):
            r_vec = x[:3]
            v_vec = x[3:]
            r_mag = np.linalg.norm(r_vec)
            a = -mu * r_vec / r_mag**3 if r_mag > 1e-6 else np.zeros(3)
            return np.concatenate([v_vec, a])

        def h(x):
            return x

        def F_jac_cont(x):
            r_vec = x[:3]
            r_mag = np.linalg.norm(r_vec)
            J = np.zeros((6, 6))
            J[:3, 3:] = np.eye(3)
            if r_mag > 1e-6:
                J[3:, :3] = -mu * (np.eye(3) / r_mag**3 - 3.0 * np.outer(r_vec, r_vec) / r_mag**5)
            return J

        def H_jac(x):
            return np.eye(6)

        dt = 0.1
        def f_discrete(x, u=None):
            return x + f_cont(x) * dt

        def F_jac_discrete(x):
            return np.eye(6) + F_jac_cont(x) * dt

        ekf = ExtendedKalmanFilter(
            f_discrete, h, F_jac_discrete, H_jac,
            Q=np.eye(6) * 1e-6, R=np.eye(6) * 1.0,
            x0=np.array([r, 0.0, 0.0, 0.0, v, 0.0]), P0=np.eye(6) * 100.0
        )
        state = np.array([r, 0.0, 0.0, 0.0, v, 0.0])
        np.random.seed(42)
        for _ in range(100):
            state = f_discrete(state, None)
            z = state + np.random.normal(0, 1.0, 6)
            ekf.step(z)
        err = np.linalg.norm(ekf.x - state)
        # EKF should reduce noise to within 100m position
        assert err < 100.0
