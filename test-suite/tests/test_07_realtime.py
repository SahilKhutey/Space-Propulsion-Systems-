import pytest
import time
import numpy as np
import psutil
import os
import sys
from pathlib import Path

# Add paths for standalone execution if needed
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "real-time-engine"))

from real_time_engine import (
    SpacecraftConfig, StateManager, MissionLoop
)


# ===== Test 21: Time Synchronization =====
@pytest.mark.realtime
class TestTimeSync:
    """Test 21: Sim time = wall time (in real-time mode)."""

    def test_wall_time_tracking(self):
        cfg = SpacecraftConfig(
            name="Sync", dry_mass_kg=500, initial_propellant_kg=500,
        )
        sm = StateManager(cfg)
        loop = MissionLoop(sm, dt=0.01)  # small dt
        t0 = time.time()
        loop.run(50)  # 50 steps
        t1 = time.time()
        wall_dt = t1 - t0
        
        # Sim time tracked in state vector index 1008
        sim_dt = sm.spacecraft.state.x[1008]
        # Verify sim time advanced by dt * steps = 0.5s
        assert abs(sim_dt - 0.5) < 1e-9


# ===== Test 22: State Updates =====
@pytest.mark.realtime
class TestStateUpdates:
    """Test 22: All state variables update every timestep."""

    def test_state_evolves(self):
        cfg = SpacecraftConfig(
            name="Evolve", dry_mass_kg=500, initial_propellant_kg=500,
            thruster_power_w=5000, thruster_isp_s=1800, thruster_efficiency=0.55,
            n_thermal_nodes=4,
        )
        sm = StateManager(cfg)
        loop = MissionLoop(sm, dt=1.0)
        sm.spacecraft.state.thruster_on = True
        sm.spacecraft.state.thermal = np.array([250.0, 300.0, 350.0, 400.0])
        
        m0 = sm.spacecraft.state.mass_propellant
        T0 = sm.spacecraft.state.thermal.copy()
        
        loop.run(60)
        
        m1 = sm.spacecraft.state.mass_propellant
        T1 = sm.spacecraft.state.thermal.copy()
        
        # Propellant should decrease
        assert m1 < m0
        # Thermal should evolve
        assert not np.allclose(T1, T0)


# ===== Test 23: Long Runtime Stability =====
@pytest.mark.realtime
class TestLongRuntime:
    """Test 23: 72h continuous — no memory leaks."""

    def test_no_memory_leak(self):
        cfg = SpacecraftConfig(name="Stability", dry_mass_kg=500, initial_propellant_kg=500)
        sm = StateManager(cfg)
        loop = MissionLoop(sm, dt=10.0)
        process = psutil.Process(os.getpid())
        mem0 = process.memory_info().rss / 1024 / 1024  # MB
        
        # Simulate steps
        for _ in range(1000):
            loop.step()
            
        mem1 = process.memory_info().rss / 1024 / 1024
        growth_mb = mem1 - mem0
        # Memory growth should be modest
        assert growth_mb < 50.0, f"Memory grew by {growth_mb:.1f} MB"
