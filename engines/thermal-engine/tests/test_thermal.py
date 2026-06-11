import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from thermal_engine import ThermalEngine


def test_thermal_transient():
    engine = ThermalEngine()
    params = {
        "power_dissipation_w": 500.0,
        "ambient_temp_k": 3.0,
        "component_area_m2": 0.5,
        "emissivity": 0.85,
        "radiator_area_m2": 1.0,
        "radiator_emissivity": 0.85,
        "solar_irradiance_w_m2": 1361.0,
        "absorptivity": 0.30,
        "time_hours": 12.0,
        "time_step_s": 120.0
    }
    res = engine.compute(params)
    assert res["steady_state_k"] > 0.0
    assert len(res["time_series"]) > 0
