import pytest
import numpy as np
import sys
from pathlib import Path

# Add paths for standalone execution if needed
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "real-time-engine"))

from core.mathematics.thermal.radiation import (
    stefan_boltzmann, equilibrium_temperature
)
from core.mathematics.thermal.conduction import conduction
from core.mathematics.thermal.capacity import (
    heat_capacity, temperature_rise
)
from core.mathematics.thermal.transient import (
    transient_thermal, thermal_ode_lumped
)
from core.constants.constants import SIGMA_SB


# ===== Test 15: Radiative Cooling =====
@pytest.mark.thermal
class TestRadiativeCooling:
    """Test 15: ε=0.8, A=5m², T=350K."""

    def test_stefan_boltzmann(self, atol):
        Q = stefan_boltzmann(0.8, 5.0, 350.0, 0.0)
        # Q = 0.8 * 5.67e-8 * 5 * 350^4
        expected = 0.8 * SIGMA_SB * 5.0 * 350.0**4
        assert abs(Q - expected) < 1.0
        # ~3,402 W
        assert 3350.0 < Q < 3450.0

    def test_stefan_boltzmann_vs_temp(self):
        """Q ~ T^4"""
        Q1 = stefan_boltzmann(0.8, 1.0, 300.0, 0.0)
        Q2 = stefan_boltzmann(0.8, 1.0, 600.0, 0.0)
        # Q2/Q1 should be 16
        assert abs(Q2 / Q1 - 16.0) < 1e-6


# ===== Test 16: Thermal Equilibrium =====
@pytest.mark.thermal
class TestThermalEquilibrium:
    """Test 16: Q_in = Q_out → stable temperature."""

    def test_equilibrium_temperature(self, atol):
        """α*A_sun*S = ε*A_rad*σ*T^4"""
        T = equilibrium_temperature(0.85, 0.3, 1.0, 0.1, 1361.0)
        # T ≈ 281 K
        assert 270.0 < T < 290.0

    def test_steady_state_ode(self, atol):
        """Run transient long enough → converge to equilibrium."""
        q_in = 100.0
        c_th = 1000.0
        # Steady state: Q_in = eps*sigma*A*T^4
        # T_ss = (100 / (0.85 * 5.67e-8 * 1))^(1/4) ≈ 213 K
        t, T = transient_thermal(q_in, c_th, 0.85, 1.0, 250.0, 3.0,
                                  t_end_s=10000, dt=1.0)
        T_ss = T[-1]
        assert 195.0 < T_ss < 220.0

    def test_stability_no_oscillation(self):
        """No thermal oscillation at steady state."""
        t, T = transient_thermal(100.0, 1000.0, 0.85, 1.0, 200.0, 3.0, 5000.0, 1.0)
        # Last 10% should be flat
        last_10pct = T[int(0.9 * len(T)):]
        assert np.std(last_10pct) < 0.1


# ===== Test 17: Thermal Runaway =====
@pytest.mark.thermal
class TestThermalRunaway:
    """Test 17: Increasing heat → warning triggered."""

    def test_runaway_detection(self):
        from real_time_engine import (
            SpacecraftConfig, StateManager, MissionLoop
        )
        cfg = SpacecraftConfig(
            name="Hot", dry_mass_kg=500, initial_propellant_kg=500,
            n_thermal_nodes=4,
        )
        sm = StateManager(cfg)
        loop = MissionLoop(sm, dt=1.0)
        # Add lots of heat to node 0
        loop.thermal.add_dissipation(0, 500.0)  # 500W continuous
        # Run for 1 hour simulation time
        for _ in range(3600):
            loop.thermal.add_dissipation(0, 500.0)
            loop.thermal.step()
        # Check for runaway
        runaway_nodes = loop.thermal.check_runaway()
        # Should detect at least node 0
        assert len(runaway_nodes) > 0
        assert 0 in runaway_nodes
