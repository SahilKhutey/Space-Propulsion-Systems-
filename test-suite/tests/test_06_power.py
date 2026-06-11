import pytest
import numpy as np
import sys
from pathlib import Path

# Add paths for standalone execution if needed
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "real-time-engine"))

from core.mathematics.power_systems.solar import (
    solar_array_power, solar_flux_at_distance, required_area
)
from core.mathematics.power_systems.battery import (
    battery_energy, state_of_charge, discharge_time
)
from core.mathematics.power_systems.eclipse import (
    eclipse_duration, power_balance
)


# ===== Test 18: Solar Array =====
@pytest.mark.power
class TestSolarArray:
    """Test 18: 10 m², 30% efficiency, Earth → ~4080 W."""

    def test_solar_earth(self, atol):
        P = solar_array_power(0.30, 10.0, 1.0)
        # 0.3 * 10 * 1361 = 4083 W
        assert abs(P - 4083.0) < 5.0, f"Got {P:.0f} W"

    def test_solar_mars(self):
        """Mars ≈ 43% of Earth solar flux."""
        P_earth = solar_array_power(0.30, 10.0, 1.0)
        P_mars = solar_array_power(0.30, 10.0, 1.524)
        ratio = P_mars / P_earth
        assert 0.40 < ratio < 0.46

    def test_solar_jupiter(self):
        P_earth = solar_array_power(0.30, 10.0, 1.0)
        P_jup = solar_array_power(0.30, 10.0, 5.2)
        ratio = P_jup / P_earth
        # 1/5.2^2 ≈ 0.037 = 3.7%
        assert 0.030 < ratio < 0.045

    def test_required_area(self, atol):
        A = required_area(4080, 0.30, 1.0)
        # 4080 / (0.3 * 1361) = 10.0
        assert abs(A - 10.0) < 0.1


# ===== Test 19: Eclipse =====
@pytest.mark.power
class TestEclipse:
    """Test 19: Eclipse → P_solar=0, battery discharges."""

    def test_eclipse_zero_solar(self):
        from real_time_engine import (
            SpacecraftConfig, StateManager, MissionLoop
        )
        cfg = SpacecraftConfig(
            name="Eclipse", dry_mass_kg=500, initial_propellant_kg=500,
            solar_array_area_m2=10, solar_efficiency=0.30,
            battery_capacity_wh=5000,
        )
        sm = StateManager(cfg)
        loop = MissionLoop(sm, dt=60.0)
        # Sunlit first
        loop.power.set_eclipse(False)
        loop.power.set_load("heater", 100.0)
        e0 = sm.spacecraft.battery_soc
        loop.step()
        # Eclipse
        loop.power.set_eclipse(True)
        e1 = sm.spacecraft.battery_soc
        loop.step()
        e2 = sm.spacecraft.battery_soc
        # Battery should drain during eclipse
        assert e2 < e1

    def test_eclipse_duration(self, atol):
        t = eclipse_duration(400e3, beta_angle_deg=0.0, body="earth")
        # ~35% of orbital period
        from core.mathematics.orbital_mechanics.kepler import orbital_period
        T = orbital_period(400e3, "earth")
        assert abs(t / T - 0.35) < 0.01


# ===== Test 20: Battery Capacity =====
@pytest.mark.power
class TestBatteryCapacity:
    """Test 20: 10 kWh battery, 1 kW load → 10 hours."""

    def test_discharge_time(self, atol):
        t = discharge_time(10000, 1000)
        assert abs(t - 10.0) < 0.1

    def test_soc(self, atol):
        soc = state_of_charge(5000, 10000)
        assert abs(soc - 0.5) < 1e-9

    def test_energy_capacity(self):
        E = battery_energy(voltage_v=28, capacity_ah=100)
        # 28 * 100 = 2800 Wh
        assert E == 2800
