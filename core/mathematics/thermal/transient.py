import numpy as np
from ..calculus.ode_solvers import rk4
from .radiation import stefan_boltzmann_cooling
from core.constants.constants import SIGMA_SB

def thermal_ode(t: float, temp: np.ndarray, mass: float, cp: float,
                q_in: float, area: float, emissivity: float, t_env: float) -> np.ndarray:
    T = float(temp[0])
    q_out = stefan_boltzmann_cooling(T, t_env, area, emissivity)
    dTdt = (q_in - q_out) / (mass * cp)
    return np.array([dTdt])

def simulate_temperature_transient(t_span: float, temp_init: float,
                                    mass: float, cp: float, q_in: float,
                                    area: float, emissivity: float,
                                    t_env: float, dt: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    def ode(t, y):
        return thermal_ode(t, y, mass, cp, q_in, area, emissivity, t_env)
    
    n_steps = int(t_span / dt)
    t, y = rk4(ode, 0.0, np.array([temp_init]), dt, n_steps)
    return t, y.flatten()

def thermal_ode_lumped(t: float, T: np.ndarray, q_in: float, c_th: float, emissivity: float, area: float, t_env: float) -> np.ndarray:
    T_val = float(T[0])
    q_out = emissivity * SIGMA_SB * area * (T_val**4 - t_env**4)
    dTdt = (q_in - q_out) / c_th
    return np.array([dTdt])

def transient_thermal(q_in: float, c_th: float, emissivity: float, area: float, temp_init: float, t_env: float, t_end_s: float, dt: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    def ode(t, y):
        return thermal_ode_lumped(t, y, q_in, c_th, emissivity, area, t_env)
    n_steps = int(t_end_s / dt)
    t_arr, T_arr = rk4(ode, 0.0, np.array([temp_init]), dt, n_steps)
    return t_arr, T_arr.flatten()

def multi_node_thermal(nodes: list, conduction_matrix: np.ndarray, capacities: np.ndarray) -> np.ndarray:
    return np.zeros_like(capacities)
