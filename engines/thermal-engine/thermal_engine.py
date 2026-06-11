"""
Thermal Simulation Engine
"""
import numpy as np
from core.constants.constants import SIGMA_SB


class ThermalEngine:
    """Lumped-capacitance transient thermal solver."""

    def __init__(self, thermal_mass_j_per_k: float = 1000.0,
                 max_safe_temp_k: float = 343.15):
        self.C = thermal_mass_j_per_k
        self.T_max = max_safe_temp_k

    def compute(self, params: dict) -> dict:
        power_dissipation = float(params.get("power_dissipation_w", 500.0))
        ambient_temp = float(params.get("ambient_temp_k", 3.0))
        component_area = float(params.get("component_area_m2", 0.1))
        emissivity = float(params.get("emissivity", 0.85))
        radiator_area = float(params.get("radiator_area_m2", 0.5))
        solar_irradiance = float(params.get("solar_irradiance_w_m2", 1361.0))
        absorptivity = float(params.get("absorptivity", 0.3))
        time_hours = float(params.get("time_hours", 24.0))
        time_step = float(params.get("time_step_s", 60.0))

        # Time grid
        n_steps = max(10, int(time_hours * 3600 / time_step))
        t = np.linspace(0, time_hours * 3600, n_steps)

        # Internal dissipation
        Q_diss = power_dissipation

        # Solar input (assume constant)
        Q_solar = absorptivity * solar_irradiance * component_area

        def net_radiated(T):
            return emissivity * SIGMA_SB * radiator_area * (T**4 - ambient_temp**4)

        # Solve steady state numerically
        T_ss = self._solve_steady_state(Q_diss + Q_solar, net_radiated, ambient_temp)

        # Transient simulation
        T = np.zeros_like(t)
        T[0] = ambient_temp
        for i in range(1, len(t)):
            dt = t[i] - t[i-1]
            q_out = net_radiated(T[i-1])
            dTdt = (Q_diss + Q_solar - q_out) / self.C
            T[i] = T[i-1] + dTdt * dt

        T_min, T_max = float(T.min()), float(T.max())
        T_steady = float(T[-1])

        warnings = []
        if T_max > self.T_max:
            warnings.append(
                f"Peak temp {T_max-273.15:.1f}°C exceeds safe limit {self.T_max-273.15:.1f}°C."
            )

        # Required radiator area for steady state
        Q_in = Q_diss + Q_solar
        if T_steady > ambient_temp:
            A_req = Q_in / (emissivity * SIGMA_SB * (T_steady**4 - ambient_temp**4))
        else:
            A_req = 0.0

        series = [{
            "component": "main_bus",
            "min_temp_k": T_min,
            "max_temp_k": T_max,
            "steady_state_k": T_steady,
            "time_series_t": t.tolist(),
            "time_series_temp_k": T.tolist()
        }]

        return {
            "steady_state_k": T_steady,
            "min_temp_k": T_min,
            "max_temp_k": T_max,
            "radiator_required_m2": float(A_req),
            "heat_rejected_w": Q_in,
            "time_series": series,
            "warnings": warnings,
            "safe": T_max <= self.T_max
        }

    @staticmethod
    def _solve_steady_state(Q_in: float, net_radiated, t_ambient: float,
                            tol: float = 1e-3, t_max_search: float = 1000.0) -> float:
        lo, hi = t_ambient + 0.01, t_ambient + t_max_search
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            q = net_radiated(mid)
            if q < Q_in:
                lo = mid
            else:
                hi = mid
            if (hi - lo) < tol:
                break
        return 0.5 * (lo + hi)
