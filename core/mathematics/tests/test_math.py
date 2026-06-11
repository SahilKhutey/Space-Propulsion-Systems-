import sys
import os

# Add monorepo root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import pytest
import numpy as np

# Import layers
from core.mathematics.linear_algebra import vectors, matrices, rotations, Quaternion
from core.mathematics.calculus import ode_solvers, numerical_integration, root_finding
from core.mathematics.classical_mechanics import newtonian, energy, momentum
# Direct function imports for clashing modules
from core.mathematics.propulsion.thrust import thrust as prop_thrust_fn, effective_exhaust_velocity as prop_ve
from core.mathematics.propulsion.efficiency import propulsive_efficiency
from core.mathematics.electric_propulsion import plasma, hall, ion, vasimr, mpd
from core.mathematics.orbital_mechanics import kepler, transfers, perturbations, propagators
from core.mathematics.mission_design.tsiolkovsky import rocket_equation, required_propellant_mass
from core.mathematics.thermal.radiation import stefan_boltzmann_cooling
from core.mathematics.thermal.transient import simulate_temperature_transient
from core.mathematics.power_systems import solar, battery, eclipse
from core.mathematics.attitude import dynamics as att_dyn, euler as att_euler, quaternion as att_quat
from core.mathematics.optimization import gradient, genetic, bayesian
from core.mathematics.uncertainty import monte_carlo, covariance, kalman
from core.mathematics.digital_twin import state_space, pinn, reduced_order


# --- LAYER 1 TESTS: FOUNDATIONS ---

def test_linear_algebra_vectors():
    v1 = vectors.vec3(1.0, 2.0, 3.0)
    v2 = vectors.vec3(4.0, 5.0, 6.0)
    assert vectors.magnitude(v1) == pytest.approx(np.sqrt(14.0))
    assert np.allclose(vectors.unit(v1), v1 / np.sqrt(14.0))
    assert vectors.dot(v1, v2) == 32.0
    assert np.allclose(vectors.cross(v1, v2), np.array([-3.0, 6.0, -3.0]))
    assert vectors.angle_between(v1, v2) == pytest.approx(0.2257261, abs=1e-5)
    assert np.allclose(vectors.projection(v1, v2), np.array([4.0, 5.0, 6.0]) * (32.0 / 77.0))
    assert vectors.triple_product(v1, v2, vectors.vec3(0, 0, 1)) == -3.0
    
    skew = vectors.skew(v1)
    assert np.allclose(skew @ v2, vectors.cross(v1, v2))


def test_linear_algebra_matrices():
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    assert matrices.is_positive_definite(A)
    sqrt_A = matrices.matrix_sqrt(A)
    assert np.allclose(sqrt_A @ sqrt_A, A)
    b = np.array([3.0, 3.0])
    x = matrices.solve_linear(A, b)
    assert np.allclose(x, np.array([1.0, 1.0]))


def test_linear_algebra_rotations():
    R = rotations.rot_x(np.pi / 2)
    v = np.array([0, 1.0, 0])
    assert np.allclose(R @ v, np.array([0, 0, 1.0]))
    
    R_axis = rotations.rotation_from_axis_angle(np.array([1.0, 0, 0]), np.pi / 2)
    assert np.allclose(R_axis, R)
    
    roll, pitch, yaw = rotations.matrix_to_euler(R, order="zyx")
    assert roll == pytest.approx(np.pi / 2)


def test_linear_algebra_quaternions():
    q1 = Quaternion(1.0, 0.0, 0.0, 0.0)
    q2 = Quaternion.from_axis_angle(np.array([0.0, 0.0, 1.0]), np.pi / 2)
    assert q2.w == pytest.approx(np.cos(np.pi / 4))
    assert q2.z == pytest.approx(np.sin(np.pi / 4))
    
    q_prod = q1 * q2
    assert np.allclose(q_prod.q, q2.q)
    
    R = q2.to_matrix()
    v = np.array([1.0, 0, 0])
    assert np.allclose(R @ v, np.array([0, 1.0, 0]))


def test_calculus_ode_solvers():
    # Exponential decay: dy/dt = -y
    def f(t, y):
        return -y
        
    t, y = ode_solvers.rk4(f, 0.0, np.array([1.0]), 0.1, 10)
    assert y[-1][0] == pytest.approx(np.exp(-1.0), abs=1e-4)
    
    t_ad, y_ad = ode_solvers.dopri45(f, 0.0, np.array([1.0]), 1.0)
    assert y_ad[-1][0] == pytest.approx(np.exp(-1.0), abs=1e-4)


def test_calculus_integration():
    x = np.linspace(0, np.pi, 101)
    y = np.sin(x)
    assert numerical_integration.trapezoid(x, y) == pytest.approx(2.0, abs=1e-3)
    
    # Gauss Legendre on sin(x) from 0 to pi
    val = numerical_integration.gauss_legendre(np.sin, 0, np.pi, n=5)
    assert val == pytest.approx(2.0, abs=1e-6)


def test_calculus_root_finding():
    def f(x): return x**2 - 4.0
    def fp(x): return 2.0*x
    assert root_finding.bisection(f, 0, 5) == pytest.approx(2.0)
    assert root_finding.newton_raphson(f, fp, 1.5) == pytest.approx(2.0)
    assert root_finding.secant(f, 1.0, 3.0) == pytest.approx(2.0)


# --- LAYER 2 TESTS: CLASSICAL MECHANICS ---

def test_classical_mechanics():
    # Newton
    assert np.allclose(newtonian.newton_second_law(np.array([10.0, 0, 0]), 2.0), np.array([5.0, 0, 0]))
    
    # Energy
    ke = energy.kinetic_energy(2.0, np.array([3.0, 4.0, 0]))
    assert ke == 25.0
    
    # Specific energy & Vis-Viva
    # Orbit: circular at radius 7000km around Earth
    mu_earth = 3.986004418e14
    v_circ = energy.vis_viva(7e6, 7e6, mu_earth)
    assert v_circ == pytest.approx(np.sqrt(mu_earth / 7e6))


# --- LAYER 3 TESTS: PROPULSION ---

def test_propulsion():
    # Thrust
    F = prop_thrust_fn(m_dot=0.01, v_e=3000.0, p_e=1000.0, p_a=0.0, a_e=0.05)
    assert F == 0.01 * 3000.0 + (1000.0 - 0.0) * 0.05
    
    # Isp
    assert prop_ve(300.0) == pytest.approx(300.0 * 9.80665)
    
    # Efficiency
    eta = propulsive_efficiency(thrust_n=30.0, v_e=3000.0, power_w=50000.0)
    assert eta == (30.0 * 3000.0) / (2 * 50000.0)


# --- LAYER 4 TESTS: ELECTRIC PROPULSION ---

def test_electric_propulsion():
    # Debye length
    ld = plasma.debye_length(1e17, 20000) # n_e = 1e17 m^-3, T_e = 2e4 K
    assert ld > 0
    
    # Ion velocity
    v_ion = ion.ion_velocity(300.0, 131.3 * 1.66054e-27) # Xe+ in 300V
    assert v_ion > 10000.0
    
    # Hall magnetic field
    B = hall.hall_magnetic_field(0.1, 0.05)
    assert B > 0


# --- LAYER 5 TESTS: ORBITAL MECHANICS ---

def test_orbital_mechanics():
    mu_earth = 3.986004418e14
    
    # Kepler elements
    period = kepler.orbital_period(7000000.0, mu_earth)
    assert period == pytest.approx(2 * np.pi * np.sqrt(7000000.0**3 / mu_earth))
    
    # Hohmann Transfer
    dv1, dv2 = transfers.hohmann_delta_v(7000000.0, 42000000.0, mu_earth)
    assert dv1 > 0
    assert dv2 > 0


# --- LAYER 6 TESTS: MISSION DESIGN ---

def test_mission_design():
    # Rocket equation
    dv = rocket_equation(isp_s=300.0, m0=1000.0, mp=500.0)
    assert dv == pytest.approx(300.0 * 9.80665 * np.log(2.0))
    
    # Sizing
    mp = required_propellant_mass(300.0, 500.0, dv)
    assert mp == pytest.approx(500.0)


# --- LAYER 7 TESTS: THERMAL ---

def test_thermal():
    # Stefan-Boltzmann cooling
    q = stefan_boltzmann_cooling(300.0, 3.0, 2.0, 0.8)
    assert q > 0
    
    # Transient simulation
    # Simple cooling of a 10kg aluminum block
    t, temp = simulate_temperature_transient(
        t_span=100.0, temp_init=350.0, mass=10.0, cp=900.0,
        q_in=10.0, area=1.5, emissivity=0.8, t_env=3.0, dt=1.0
    )
    assert len(t) == 101
    assert temp[-1] < 350.0 # It should cool down


# --- LAYER 8 TESTS: POWER SYSTEMS ---

def test_power_systems():
    # Solar generation
    p = solar.solar_power_generation(0.3, 5.0, 1361.0, 0.0)
    assert p == 0.3 * 5.0 * 1361.0
    
    # Shadow check
    assert eclipse.is_in_eclipse(np.array([7000000.0, 0, 0]), np.array([-1.496e11, 0, 0]))


# --- LAYER 9 TESTS: ATTITUDE DYNAMICS ---

def test_attitude_dynamics():
    # Rotational Euler dynamics
    I = np.diag([10.0, 12.0, 15.0])
    w = np.array([0.1, 0.2, 0.3])
    t = np.array([0, 0, 0])
    w_dot = att_dyn.euler_rotational_dynamics(I, w, t)
    # Since t=0, w_dot is I^-1 * (-w x Iw)
    Iw = I @ w
    w_cross_Iw = np.cross(w, Iw)
    expected_w_dot = np.linalg.solve(I, -w_cross_Iw)
    assert np.allclose(w_dot, expected_w_dot)


# --- LAYER 10 TESTS: OPTIMIZATION ---

def test_optimization():
    # Minimize x^2
    def obj(x): return float(x[0]**2)
    x_opt, val = gradient.gradient_descent(obj, np.array([2.0]), learning_rate=0.1)
    assert abs(x_opt[0]) < 0.05
    
    x_gen, val_gen = genetic.genetic_algorithm(obj, [(-5.0, 5.0)], pop_size=20, generations=20)
    assert abs(x_gen[0]) < 1.0


# --- LAYER 11 TESTS: UNCERTAINTY ---

def test_uncertainty():
    # Kalman filter check
    x = np.array([0.0])
    P = np.array([[1.0]])
    z = np.array([1.1])
    F = np.array([[1.0]])
    H = np.array([[1.0]])
    Q = np.array([[0.1]])
    R = np.array([[0.1]])
    x_new, P_new = kalman.kalman_filter_step(x, P, z, F, H, Q, R)
    assert x_new[0] > 0.0 # Measurement was 1.1, so estimate should pull positive


# --- LAYER 12 TESTS: DIGITAL TWIN ---

def test_digital_twin():
    # State space step
    A = np.array([[-1.0]])
    B = np.array([[1.0]])
    C = np.array([[1.0]])
    D = np.array([[0.0]])
    x, y = state_space.state_space_step(A, B, C, D, np.array([1.0]), np.array([0.5]), 0.1)
    # x_next = x + dt * (A*x + B*u) = 1.0 + 0.1 * (-1.0*1.0 + 1.0*0.5) = 1.0 + 0.1 * (-0.5) = 0.95
    assert x[0] == pytest.approx(0.95)
