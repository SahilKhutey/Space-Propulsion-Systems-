import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from power_engine import PowerEngine


def test_power_budget():
    engine = PowerEngine()
    params = {
        "solar_array_area_m2": 10.0,
        "solar_efficiency": 0.30,
        "distance_au": 1.0,
        "battery_capacity_wh": 2000.0,
        "eclipse_duration_min": 35.0,
        "orbit_period_min": 90.0,
        "thruster_power_w": 1000.0,
        "thruster_duty_cycle": 0.20
    }
    res = engine.compute(params)
    assert res["solar_power_w"] > 0.0
    assert abs(res["solar_power_w"] - 4083.0) < 50.0
    assert res["feasible"] is True
