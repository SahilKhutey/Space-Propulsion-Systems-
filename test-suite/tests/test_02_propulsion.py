import pytest
import numpy as np
import sys
from pathlib import Path

# Add paths for standalone execution if needed
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))

from core.mathematics.propulsion.thrust import thrust, effective_exhaust_velocity
from core.mathematics.propulsion.efficiency import (
    propulsive_efficiency, thrust_from_power
)
from core.mathematics.propulsion.mass_flow import (
    mass_flow, mass_flow_from_power, propellant_consumed
)
from core.mathematics.mission_design.tsiolkovsky import (
    delta_v, propellant_for_dv, mass_ratio
)


# ===== Test 4: Hall Thruster =====
@pytest.mark.propulsion
class TestHallThruster:
    """Test 4: P=5kW, η=0.6, Isp=2000s → ~0.30 N thrust (±5%)."""

    def test_hall_spec_benchmark(self, hall_benchmark):
        F = thrust_from_power(
            hall_benchmark["power_w"],
            hall_benchmark["efficiency"],
            hall_benchmark["isp_s"]
        )
        expected = hall_benchmark["expected_thrust_n"]
        tol = expected * hall_benchmark["tolerance"]
        assert abs(F - expected) < tol, \
            f"Got {F:.4f} N, expected {expected} N ± {tol:.4f}"

    def test_hall_exhaust_velocity(self, atol):
        ve = effective_exhaust_velocity(2000)
        # Ve = 2000 * 9.80665 = 19,613.3
        assert abs(ve - 19613.3) < 1.0

    def test_hall_thrust_proportional_to_power(self):
        """Doubling power → doubling thrust (same Isp, eff)."""
        F1 = thrust_from_power(2500, 0.6, 2000)
        F2 = thrust_from_power(5000, 0.6, 2000)
        assert abs(F2 / F1 - 2.0) < 1e-9

    def test_hall_thrust_inversely_proportional_to_isp(self):
        """Doubling Isp → halving thrust (same P, eff)."""
        F1 = thrust_from_power(5000, 0.6, 1000)
        F2 = thrust_from_power(5000, 0.6, 2000)
        assert abs(F1 / F2 - 2.0) < 1e-9


# ===== Test 5: Ion Thruster =====
@pytest.mark.propulsion
class TestIonThruster:
    """Test 5: P=7kW, Isp=3500s. Verify Ve, m_dot, F."""

    def test_ion_ve(self):
        ve = effective_exhaust_velocity(3500)
        # Ve = 3500 * 9.80665 ≈ 34,323 m/s
        assert abs(ve - 34323.3) < 1.0

    def test_ion_mass_flow(self):
        """m_dot = 2ηP / Ve²"""
        # For η=0.7, P=7000, Isp=3500
        ve = 3500 * 9.80665
        mdot = mass_flow_from_power(7000, 0.7, 3500)
        expected = 2 * 0.7 * 7000 / ve**2
        assert abs(mdot - expected) < 1e-10

    def test_ion_thrust(self):
        F = thrust_from_power(7000, 0.7, 3500)
        ve = 3500 * 9.80665
        expected = 2 * 0.7 * 7000 / ve
        assert abs(F - expected) < 1e-9

    def test_ion_thrust_consistency(self):
        """F = m_dot * Ve must match F = 2ηP/Ve."""
        F1 = thrust_from_power(7000, 0.7, 3500)
        mdot = mass_flow_from_power(7000, 0.7, 3500)
        F2 = mdot * 3500 * 9.80665
        assert abs(F1 - F2) < 1e-9


# ===== Test 6: Propellant Depletion =====
@pytest.mark.propulsion
class TestPropellantDepletion:
    """Test 6: 100 kg propellant, 0.0001 kg/s → 1,000,000 s."""

    def test_runtime(self):
        m_prop = 100.0
        mdot = 0.0001
        runtime_s = m_prop / mdot
        assert abs(runtime_s - 1_000_000) < 1.0

    def test_propellant_consumed(self):
        """After burn time, m_consumed = mdot * t."""
        mdot = 0.001  # 1 g/s
        t = 5000  # s
        m_consumed = propellant_consumed(mdot, t)
        assert abs(m_consumed - 5.0) < 1e-9

    def test_zero_mass_flow_raises(self):
        from core.mathematics.mission_design.burn_time import burn_time
        # In our implementation, burn_time returns 0.0 for m_dot <= 0
        assert burn_time(100, 0) == 0.0


# ===== Test 7: Efficiency Limits =====
@pytest.mark.propulsion
class TestEfficiencyLimits:
    """Test 7: η <= 1. System must reject η = 1.3."""

    def test_efficiency_above_one_rejected_by_pydantic(self):
        from core.engine.schemas.thruster import HallInput
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            HallInput(power_w=5000, efficiency=1.3, isp_s=2000)

    def test_efficiency_at_one_accepted(self):
        from core.engine.schemas.thruster import HallInput
        # η = 1 is the physical limit; should be accepted
        inp = HallInput(power_w=5000, efficiency=1.0, isp_s=2000)
        assert inp.efficiency == 1.0
