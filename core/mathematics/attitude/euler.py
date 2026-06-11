import numpy as np

def euler_rates_to_omega(euler_angles: np.ndarray, euler_rates: np.ndarray,
                         order: str = "zyx") -> np.ndarray:
    """Transform Euler rates to body angular velocity ω."""
    phi, theta, psi = euler_angles
    dphi, dtheta, dpsi = euler_rates
    if order == "zyx":
        # Standard aerospace 3-2-1 transformation
        wx = dphi - dpsi * np.sin(theta)
        wy = dtheta * np.cos(phi) + dpsi * np.sin(phi) * np.cos(theta)
        wz = -dtheta * np.sin(phi) + dpsi * np.cos(phi) * np.cos(theta)
        return np.array([wx, wy, wz])
    raise ValueError(f"Order {order} not implemented")
