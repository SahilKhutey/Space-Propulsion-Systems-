import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from mission_engine import MissionEngine


def test_mission_orbit_raising():
    engine = MissionEngine()
    params = {
        "name": "GEO Insertion Mission",
        "initial_orbit": "LEO",
        "target_orbit": "GEO",
        "payload_mass_kg": 1000.0,
        "thruster_type": "hall_thruster",
        "isp_s": 2000.0,
        "efficiency": 0.60,
        "power_w": 5000.0,
        "safety_factor": 1.2
    }
    res = engine.compute(params)
    assert res["mission_name"] == "GEO Insertion Mission"
    assert res["delta_v_ms"] > 0.0
    assert res["propellant_mass_kg"] > 0.0
    assert res["transfer_time_days"] > 0.0
    assert res["success_probability"] > 0.0
