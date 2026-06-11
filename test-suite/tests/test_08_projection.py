import pytest
import numpy as np
import sys
from pathlib import Path

# Add paths for standalone execution if needed
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "real-time-engine"))

from real_time_engine import (
    SpacecraftConfig, StateManager, MissionLoop,
    FutureStateProjector, BatteryProjector, FailurePredictor
)


# ===== Test 24: 24-Hour Forecast =====
@pytest.mark.projection
class Test24HourForecast:
    """Test 24: 24h forecast vs actual simulation."""

    def test_forecast_accuracy(self):
        cfg = SpacecraftConfig(
            name="Forecast", dry_mass_kg=500, initial_propellant_kg=500,
            thruster_power_w=5000, thruster_isp_s=1800, thruster_efficiency=0.55,
        )
        sm = StateManager(cfg)
        sm.spacecraft.state.thruster_on = True
        loop = MissionLoop(sm, dt=60.0)

        # Run 24h worth of steps
        steps_per_hour = 60
        actual_prop = []
        for hour in range(24):
            for _ in range(steps_per_hour):
                loop.step()
            actual_prop.append(sm.spacecraft.state.mass_propellant)

        # Reset and project
        sm2 = StateManager(cfg)
        sm2.spacecraft.state.thruster_on = True
        loop2 = MissionLoop(sm2, dt=60.0)
        proj = FutureStateProjector(loop2, dt=60.0)
        forecast = proj.project(sm2, scenarios={"thruster_on": True})

        # Compare 24h forecast to actual
        forecast_24h = forecast["24h"]["state"]["mass_propellant_kg"]
        actual_24h = actual_prop[23]
        
        # Should be within 5%
        assert abs(forecast_24h - actual_24h) / actual_24h < 0.05


# ===== Test 25: Battery Projection =====
@pytest.mark.projection
class TestBatteryProjection:
    """Test 25: Forecast battery life vs actual."""

    def test_battery_forecast(self):
        cfg = SpacecraftConfig(
            name="Bat", dry_mass_kg=500, initial_propellant_kg=500,
            battery_capacity_wh=5000,
        )
        sm = StateManager(cfg)
        sm.spacecraft.state.battery_energy = 1000.0
        proj = BatteryProjector(sm)
        t = proj.predict_depletion(current_load_w=200.0)
        # t = 1000 * 3600 / 200 = 18,000 s = 5 h
        assert abs(t - 18000) < 1.0


# ===== Test 26: Thruster Lifetime =====
@pytest.mark.projection
class TestThrusterLifetime:
    """Test 26: Hall thruster erosion-based lifetime."""

    def test_hall_thruster_lifetime(self):
        cfg = SpacecraftConfig(
            name="Hall", dry_mass_kg=500, initial_propellant_kg=500,
            thruster_type="hall_thruster",
        )
        sm = StateManager(cfg)
        loop = MissionLoop(sm, dt=1.0)
        pred = FailurePredictor(sm, loop.thermal)
        rul = pred.thruster_rul()
        # Hall thruster: ~10,000 hours max
        assert rul["max_hours"] == 10000.0
        assert rul["hours_remaining"] == 10000.0  # no usage yet
        
        # Use some hours
        sm.spacecraft.state.x[1007] = 5000.0  # 5000 hours used
        rul2 = pred.thruster_rul()
        assert rul2["hours_remaining"] == 5000.0
