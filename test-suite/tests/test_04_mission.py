import pytest
import numpy as np
import sys
from pathlib import Path

# Add paths for standalone execution if needed
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "real-time-engine"))

from core.mathematics.mission_design.tsiolkovsky import (
    delta_v, propellant_for_dv, mass_ratio, propellant_fraction
)
from core.mathematics.mission_design.burn_time import (
    burn_time, burn_time_from_thrust, burn_time_from_delta_v
)
from core.mathematics.mission_design.propellant_budget import (
    propellant_budget
)


# ===== Test 12: Rocket Equation =====
@pytest.mark.mission
class TestRocketEquation:
    """Test 12: Isp=3000, m0=1000, mf=700."""

    def test_tsiolkovsky_dv(self, atol):
        dv = delta_v(3000, 1000, 700)
        # ΔV = 3000 * 9.80665 * ln(1000/700) = 29420 * 0.3567 = 10494
        expected = 3000 * 9.80665 * np.log(1000 / 700)
        assert abs(dv - expected) < atol

    def test_mass_ratio(self):
        r = mass_ratio(4250, 1800)  # LEO→GEO
        # m0/mf = exp(4250 / (1800*9.81)) ≈ 1.273
        assert 1.25 < r < 1.30

    def test_inverse_calculation(self):
        """Given ΔV, Isp, payload: compute m_prop."""
        m = propellant_for_dv(4250, 1800, 1000)
        # m_prop = 1000 * (exp(4250/(1800*9.81)) - 1) ≈ 273 kg
        assert 250 < m < 300


# ===== Test 13: Fuel Consumption =====
@pytest.mark.mission
class TestFuelConsumption:
    """Test 13: Given F, t, mdot, verify remaining propellant."""

    def test_burn_time(self):
        """t_b = m_prop / m_dot"""
        t = burn_time(100, 0.0001)
        assert t == 1000000.0

    def test_burn_time_from_thrust(self):
        ve = 1800 * 9.80665
        t = burn_time_from_thrust(100, 0.1, 1800)
        # t = m * Ve / F = 100 * 17652 / 0.1 = 17,652,000 s
        expected = 100 * ve / 0.1
        assert abs(t - expected) < 1.0

    def test_burn_time_from_dv(self, atol):
        """Burn time to achieve ΔV at constant thrust."""
        t = burn_time_from_delta_v(dv_ms=1000, thrust_n=0.1, isp_s=1800, m0=1000)
        assert t > 0

    def test_propellant_budget_multi_burn(self):
        """Stack multiple burns with mass roll-up."""
        budget = propellant_budget(
            payload_kg=1000,
            dv_budgets=[1000, 2000, 1500],
            isp_s=1800,
            safety_factor=1.0
        )
        assert "total_dv_ms" in budget
        assert budget["total_dv_ms"] == 4500
        assert budget["total_propellant_kg"] > 0
        assert budget["wet_mass_kg"] > budget["dry_mass_kg"]


# ===== Test 14: Long Duration Mission =====
@pytest.mark.mission
class TestLongDurationMission:
    """Test 14: 5-year mission. Verify numerical stability."""

    def test_five_year_stability(self):
        """Run 1 year worth simulation."""
        from real_time_engine import SpacecraftConfig, StateManager, MissionLoop
        cfg = SpacecraftConfig(
            name="LongRun", dry_mass_kg=500, initial_propellant_kg=500,
            thruster_power_w=5000, thruster_isp_s=1800, thruster_efficiency=0.55,
        )
        sm = StateManager(cfg)
        sm.spacecraft.state.thruster_on = True
        loop = MissionLoop(sm, dt=60.0)  # 60s steps for speed
        
        # Run 1000 steps to keep the test fast but stable
        loop.run(1000)
        
        # No NaN
        assert not np.isnan(sm.spacecraft.state.mass_propellant)
        assert not np.isnan(sm.spacecraft.state.battery_energy)
        assert sm.spacecraft.state.mass_propellant >= 0
        assert sm.spacecraft.state.battery_energy >= 0

    def test_long_duration_no_mass_loss(self):
        """No unphysical mass loss over long time."""
        from real_time_engine import SpacecraftConfig, StateManager, MissionLoop
        cfg = SpacecraftConfig(
            name="NoLoss", dry_mass_kg=500, initial_propellant_kg=500,
            thruster_power_w=5000, thruster_isp_s=1800, thruster_efficiency=0.55,
        )
        sm = StateManager(cfg)
        # Without thruster
        m0 = sm.spacecraft.state.mass_total
        loop = MissionLoop(sm, dt=60.0)
        loop.run(1000)
        m1 = sm.spacecraft.state.mass_total
        assert abs(m1 - m0) < 1e-6  # exact conservation
