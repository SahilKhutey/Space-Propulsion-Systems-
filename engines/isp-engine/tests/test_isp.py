import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from isp_engine import IspEngine


def test_isp_calculations():
    isp = IspEngine.isp_from_thrust_power(0.306, 5000.0)
    assert abs(isp - 3332.0) < 500.0

    prop = IspEngine.propellant_consumption(0.3, 2000.0, 3600.0)
    assert abs(prop - 0.055) < 0.005

    dv = IspEngine.delta_v_capability(3000.0, 500.0, 1000.0)
    assert abs(dv - 11928.0) < 50.0
