import pytest
import numpy as np
import sys
from pathlib import Path

# Add paths for standalone execution if needed
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))

from core.constants.constants import G, M_EARTH, R_EARTH
from core.mathematics.orbital_mechanics.kepler import (
    orbital_velocity_circular, escape_velocity, orbital_period,
    semi_major_axis_from_period
)
from core.mathematics.orbital_mechanics.transfers import (
    hohmann_delta_v, hohmann_transfer_time
)


# ===== Test 8: Circular Orbit =====
@pytest.mark.orbital
class TestCircularOrbit:
    """Test 8: LEO 400 km → v ≈ 7670 m/s."""

    def test_leo_circular_velocity(self, atol):
        v = orbital_velocity_circular(400e3, "earth")
        assert abs(v - 7672.0) < 5.0, f"Got {v:.2f} m/s"

    def test_leo_circular_velocity_via_sqrt(self, atol):
        mu = G * M_EARTH
        r = R_EARTH + 400e3
        v = np.sqrt(mu / r)
        assert abs(v - 7672.0) < 1.0

    def test_geo_circular_velocity(self, atol):
        v = orbital_velocity_circular(35786e3, "earth")
        # GEO velocity ≈ 3075 m/s
        assert abs(v - 3075.0) < 5.0


# ===== Test 9: Escape Velocity =====
@pytest.mark.orbital
class TestEscapeVelocity:
    """Test 9: Earth surface → 11,186 m/s."""

    def test_earth_surface_escape(self, atol):
        v_esc = escape_velocity(0, "earth")
        # √(2μ/R) ≈ 11,186 m/s
        assert abs(v_esc - 11186.0) < 5.0, f"Got {v_esc:.2f} m/s"

    def test_escape_velocity_formula(self, atol):
        mu = G * M_EARTH
        v = np.sqrt(2 * mu / R_EARTH)
        assert abs(v - 11186.0) < 5.0

    def test_escape_at_altitude(self):
        """v_esc decreases with altitude."""
        v0 = escape_velocity(0, "earth")
        v1 = escape_velocity(400e3, "earth")
        assert v1 < v0


# ===== Test 10: Orbital Period =====
@pytest.mark.orbital
class TestOrbitalPeriod:
    """Test 10: LEO 400 km → ~92 minutes."""

    def test_leo_period(self, atol):
        T = orbital_period(400e3, "earth")
        T_min = T / 60
        assert abs(T_min - 92.7) < 0.5, f"Got {T_min:.2f} min"

    def test_geo_period(self, atol):
        T = orbital_period(35786e3, "earth")
        T_hr = T / 3600
        # GEO period = sidereal day = 23.93 hr
        assert abs(T_hr - 23.93) < 0.2

    def test_period_via_kepler_third_law(self):
        """T² = 4π²a³/μ"""
        mu = G * M_EARTH
        a = R_EARTH + 400e3
        T = 2 * np.pi * np.sqrt(a**3 / mu)
        T_min = T / 60
        assert abs(T_min - 92.7) < 0.5

    def test_inverse_calculation(self):
        """Given T, recover a."""
        mu = G * M_EARTH
        T = orbital_period(R_EARTH + 400e3, mu)
        a = semi_major_axis_from_period(T, mu)
        # Should be R_EARTH + 400e3
        assert abs(a - (R_EARTH + 400e3)) < 1.0


# ===== Test 11: Hohmann Transfer =====
@pytest.mark.orbital
class TestHohmannTransfer:
    """Test 11: LEO → GEO → ~3.9 km/s total ΔV."""

    def test_leo_geo_total_dv(self, atol):
        mu = G * M_EARTH
        r1 = R_EARTH + 400e3
        r2 = R_EARTH + 35786e3
        dv1, dv2 = hohmann_delta_v(r1, r2, mu)
        total = dv1 + dv2
        # Standard: ~3.9 km/s total (some sources say 3.9-4.2)
        assert 3500 < total < 4500, f"Got {total:.0f} m/s"

    def test_leo_geo_dv1(self, atol):
        mu = G * M_EARTH
        r1 = R_EARTH + 400e3
        r2 = R_EARTH + 35786e3
        dv1, _ = hohmann_delta_v(r1, r2, mu)
        # First burn ≈ 2400 m/s
        assert 2390 < dv1 < 2500

    def test_leo_geo_transfer_time(self, atol):
        mu = G * M_EARTH
        r1 = R_EARTH + 400e3
        r2 = R_EARTH + 35786e3
        t = hohmann_transfer_time(r1, r2, mu)
        t_hr = t / 3600
        # ~5.3 hours
        assert 5 < t_hr < 6

    def test_identical_orbits_zero_dv(self):
        mu = G * M_EARTH
        r = R_EARTH + 400e3
        dv1, dv2 = hohmann_delta_v(r, r, mu)
        assert abs(dv1) < 1e-6
        assert abs(dv2) < 1e-6
