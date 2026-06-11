import pytest
import numpy as np
import sys
from pathlib import Path

# Add paths for standalone execution if needed
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))

from core.mathematics.linear_algebra.vectors import magnitude, unit, cross, dot
from core.mathematics.linear_algebra.rotations import rot_z, rot_x, rot_y, euler_to_matrix
from core.mathematics.linear_algebra.quaternions import Quaternion
from core.mathematics.calculus.ode_solvers import rk4, dopri45, euler
from core.mathematics.calculus.root_finding import bisection, newton_raphson


# ===== Test 1: Vector Operations =====
@pytest.mark.math
class TestVectorOperations:
    """Test 1: |A| = 5 for A = (3, 4, 0)."""

    def test_magnitude_3_4_0(self, rtol, atol):
        A = np.array([3, 4, 0])
        mag = magnitude(A)
        assert abs(mag - 5.0) < atol, f"Expected 5.0, got {mag}"

    def test_magnitude_zero(self):
        assert magnitude(np.zeros(3)) == 0.0

    def test_magnitude_unit_vector(self):
        assert abs(magnitude(unit([3, 4, 0])) - 1.0) < 1e-9

    def test_unit_normalization(self):
        v = unit([1, 2, 3])
        assert abs(magnitude(v) - 1.0) < 1e-12

    def test_dot_orthogonal(self):
        assert abs(dot([1, 0, 0], [0, 1, 0])) < 1e-12

    def test_cross_basis(self):
        """e_x × e_y = e_z"""
        z = cross([1, 0, 0], [0, 1, 0])
        assert np.allclose(z, [0, 0, 1], atol=1e-12)


# ===== Test 2: Matrix Rotation =====
@pytest.mark.math
class TestMatrixRotations:
    """Test 2: Rotate (1,0,0) by 90° about Z → (0,1,0)."""

    def test_rot_z_90_degrees(self, atol):
        R = rot_z(np.pi / 2)
        v = np.array([1.0, 0.0, 0.0])
        rotated = R @ v
        expected = np.array([0.0, 1.0, 0.0])
        assert np.allclose(rotated, expected, atol=atol), \
            f"Expected [0,1,0], got {rotated}"

    def test_rot_x_90_degrees(self, atol):
        R = rot_x(np.pi / 2)
        v = np.array([0.0, 1.0, 0.0])
        rotated = R @ v
        assert np.allclose(rotated, [0, 0, 1], atol=atol)

    def test_rot_y_90_degrees(self, atol):
        R = rot_y(np.pi / 2)
        v = np.array([0.0, 0.0, 1.0])
        rotated = R @ v
        assert np.allclose(rotated, [1, 0, 0], atol=atol)

    def test_rotation_inverse(self, atol):
        """R(-θ) = R(θ)^T"""
        for angle in [0.1, 0.5, 1.2, 2.0, 3.14]:
            R = rot_z(angle)
            R_inv = R.T
            assert np.allclose(R @ R_inv, np.eye(3), atol=atol)

    def test_full_rotation_360(self, atol):
        """R(360°) = I"""
        R = rot_z(2 * np.pi)
        assert np.allclose(R, np.eye(3), atol=atol)

    def test_quaternion_equivalence(self, atol):
        """R from quaternion must match R from axis-angle."""
        q = Quaternion.from_axis_angle([0, 0, 1], np.pi / 2)
        Rq = q.to_matrix()
        Rz = rot_z(np.pi / 2)
        assert np.allclose(Rq, Rz, atol=atol)


# ===== Test 3: Numerical Integrator =====
@pytest.mark.math
class TestNumericalIntegrators:
    """Test 3: dx/dt = 1 → x(t) = t. Verifies RK4."""

    def test_rk4_constant_derivative(self, atol):
        """dx/dt = 1; x(0) = 0; x(t) = t."""
        f = lambda t, y: np.array([1.0])
        t, y = rk4(f, 0.0, np.array([0.0]), dt=0.01, n_steps=1000)
        assert abs(y[-1, 0] - 10.0) < atol * 10  # 1000*0.01 = 10

    def test_rk4_linear(self, atol):
        """dx/dt = 2t; x(t) = t²."""
        f = lambda t, y: np.array([2 * t])
        t, y = rk4(f, 0.0, np.array([0.0]), dt=0.001, n_steps=1000)
        expected = 1.0  # x(1) = 1
        assert abs(y[-1, 0] - expected) < 1e-3

    def test_rk4_harmonic_oscillator(self, atol):
        """d²x/dt² + x = 0; x(0)=1, v(0)=0 → x(t)=cos(t)."""
        f = lambda t, y: np.array([y[1], -y[0]])
        t, y = rk4(f, 0.0, np.array([1.0, 0.0]), dt=0.001, n_steps=10000)
        # At t=10, cos(10) ≈ -0.839
        assert abs(y[-1, 0] - np.cos(10.0)) < 0.01

    def test_euler_constant(self, atol):
        """Euler for dx/dt = 1; should give t exactly."""
        f = lambda t, y: np.array([1.0])
        t, y = euler(f, 0.0, np.array([0.0]), dt=0.1, n_steps=100)
        assert abs(y[-1, 0] - 10.0) < atol

    def test_dopri45_adaptive(self, atol):
        """Adaptive RK45 should converge with fewer steps."""
        f = lambda t, y: np.array([1.0])
        t, y = dopri45(f, 0.0, np.array([0.0]), t_end=10.0)
        assert abs(y[-1, 0] - 10.0) < 1e-6
        assert len(t) < 100  # adaptive should be efficient

    def test_bisection_simple(self, atol):
        """Find root of x² - 4 = 0 → x = 2."""
        root = bisection(lambda x: x**2 - 4, 0.0, 5.0)
        assert abs(root - 2.0) < 1e-6

    def test_newton_simple(self, atol):
        """Newton on x² - 2 = 0 → x = √2."""
        root = newton_raphson(
            lambda x: x**2 - 2,
            lambda x: 2.0 * x,
            x0=1.0
        )
        assert abs(root - np.sqrt(2)) < 1e-8
