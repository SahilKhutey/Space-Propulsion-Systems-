import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import numpy as np

from real_time_engine.state import SpacecraftConfig, SpacecraftState, StateManager
from real_time_engine.propagators import DormandPrince
from real_time_engine.real_time import PropulsionLoop, ThermalLoop, PowerLoop, OrbitLoop, MissionLoop
from real_time_engine.projection import FutureStateProjector, FailurePredictor
from real_time_engine.monte_carlo import UncertaintyPropagator, MissionSuccessCalculator
from real_time_engine.digital_twin import UnscentedKalmanFilter


def test_spacecraft_state():
    cfg = SpacecraftConfig(name="TEST-SC")
    sc = SpacecraftState(cfg)
    assert sc.config.name == "TEST-SC"
    assert sc.state.mass_total == 1000.0
    assert sc.state.mass_propellant == 500.0
    assert sc.battery_soc == 1.0
    assert len(sc.state.thermal) == 8


def test_propagators_rk45():
    def f(t, y): return -1.0 * y
    dp = DormandPrince(rtol=1e-5, atol=1e-5)
    t, y = dp.propagate(f, 0.0, np.array([10.0]), 2.0)
    assert y[-1][0] == pytest.approx(10.0 * np.exp(-2.0), abs=1e-2)


def test_subsystem_loops():
    cfg = SpacecraftConfig(thruster_power_w=5000.0, solar_array_area_m2=2.0, initial_propellant_kg=200.0)
    sm = StateManager(cfg)
    st = sm.spacecraft.state
    st.position = np.array([7000000.0, 0.0, 0.0])
    st.thruster_on = True
    prop = PropulsionLoop(sm, dt=1.0)
    prop.step()
    assert st.mass_propellant < 200.0
    assert np.linalg.norm(st.velocity) > 0.0
    
    # 2. Thermal
    thermal = ThermalLoop(sm, dt=1.0)
    st.thermal = np.full(8, 250.0)
    thermal.step()
    assert st.thermal[0] > 250.0 # waste heat from thruster
    
    # 3. Power
    power = PowerLoop(sm, dt=1.0)
    power.step()
    assert st.battery_energy < 5000.0 # Loads exceed generation in LEO L0
    
    # 4. Orbit (Velocity Verlet Verlet step)
    orbit = OrbitLoop(sm, dt=1.0)
    orbit.step()
    assert np.linalg.norm(st.position - np.array([7000000.0, 0.0, 0.0])) > 1e-3


def test_mission_loop():
    cfg = SpacecraftConfig()
    sm = StateManager(cfg)
    st = sm.spacecraft.state
    st.position = np.array([7000000.0, 0.0, 0.0])
    st.velocity = np.array([0.0, 7500.0, 0.0])
    
    loop = MissionLoop(sm, dt=1.0)
    loop.step()
    assert len(sm.history) == 1
    assert sm.history[0]["sim_time_s"] == 1.0


def test_projection_and_failures():
    cfg = SpacecraftConfig(thruster_power_w=500.0)
    sm = StateManager(cfg)
    st = sm.spacecraft.state
    st.position = np.array([7000000.0, 0.0, 0.0])
    st.velocity = np.array([0.0, 7500.0, 0.0])
    st.thruster_on = True
    
    projector = FutureStateProjector(sm)
    predictor = FailurePredictor(projector)
    
    failures = predictor.predict_failures(horizon_s=60.0)
    assert not failures["thermal_runaway_predicted"]
    assert failures["thruster_accumulated_hours"] == pytest.approx(60.0 / 3600.0)


def test_monte_carlo():
    cfg = SpacecraftConfig()
    sm = StateManager(cfg)
    st = sm.spacecraft.state
    st.position = np.array([7000000.0, 0.0, 0.0])
    st.velocity = np.array([0.0, 7500.0, 0.0])
    
    prop = UncertaintyPropagator(sm)
    calc = MissionSuccessCalculator(prop)
    
    success_rate = calc.calculate_success_rate(horizon_s=30.0, n_runs=5)
    assert 0.0 <= success_rate <= 1.0


def test_unscented_kalman_filter():
    def f(x): return x * 1.05
    def h(x): return x**2
    Q = np.array([[0.1]])
    R = np.array([[0.1]])
    ukf = UnscentedKalmanFilter(f, h, Q, R)
    x = np.array([2.0])
    P = np.array([[0.5]])
    z = np.array([4.2])
    x_new, P_new = ukf.step(x, P, z)
    assert x_new[0] > 0.0
