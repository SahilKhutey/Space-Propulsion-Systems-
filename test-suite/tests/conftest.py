import sys
from pathlib import Path
import pytest
import numpy as np

# Add monorepo paths
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "engines" / "thrust-engine"))
sys.path.insert(0, str(ROOT / "real-time-engine"))

@pytest.fixture
def rtol():
    """Relative tolerance for floating-point comparisons."""
    return 1e-6

@pytest.fixture
def atol():
    """Absolute tolerance."""
    return 1e-9

@pytest.fixture
def earth_orbit_state():
    """Standard LEO 400 km initial state."""
    from core.constants.constants import G, M_EARTH, R_EARTH
    mu = G * M_EARTH
    r = R_EARTH + 400e3
    v = np.sqrt(mu / r)
    return {
        "position_m": [r, 0, 0],
        "velocity_m_s": [0, v, 0],
        "mass_total_kg": 1000.0,
        "mass_propellant_kg": 500.0,
        "battery_wh": 5000.0,
        "thermal_k": [280.0] * 8,
    }

@pytest.fixture
def hall_benchmark():
    """Spec: P=5kW, η=0.6, Isp=2000s → 0.306 N."""
    return {
        "power_w": 5000.0,
        "efficiency": 0.60,
        "isp_s": 2000.0,
        "expected_thrust_n": 0.3059,
        "tolerance": 0.05,  # ±5%
    }
