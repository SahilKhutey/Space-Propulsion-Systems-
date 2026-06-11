import sys
import os
# Add monorepo root and engine root to sys.path to handle dashed folders
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from thrust_engine import ThrustEngine


def test_hall_thruster():
    engine = ThrustEngine()
    params = {"power_w": 5000.0, "efficiency": 0.60, "isp_s": 2000.0}
    res = engine.compute("hall_thruster", params)
    assert res["thruster_type"] == "hall_thruster"
    assert abs(res["thrust_n"] - 0.3059) < 0.01
