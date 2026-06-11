"""
Optimization Sizing Engine
"""
from typing import Literal
import numpy as np
from scipy.optimize import minimize
from core.constants.constants import G0


class OptimizationEngine:
    """Parametric L-BFGS-B optimization & trade study score evaluator."""

    @staticmethod
    def run_trade_study(params: dict) -> dict:
        m_payload = float(params.get("payload_mass_kg", 1000.0))
        dv = float(params.get("delta_v_ms", 3000.0))
        duration = float(params.get("mission_duration_years", 5.0))
        power_budget = params.get("power_budget_w")
        candidates = params.get("candidates", ["chemical_bipropellant", "hall_thruster", "ion_thruster", "VASIMR"])

        tech_specs = {
            "chemical_bipropellant": {"isp": 320.0, "eff": 0.95, "power": 0.0, "maturity": 0.99},
            "chemical_monopropellant": {"isp": 220.0, "eff": 0.95, "power": 0.0, "maturity": 0.98},
            "chemical_LOX_LH2": {"isp": 450.0, "eff": 0.95, "power": 0.0, "maturity": 0.95},
            "chemical_LOX_methane": {"isp": 360.0, "eff": 0.95, "power": 0.0, "maturity": 0.92},
            "hall_thruster": {"isp": 2000.0, "eff": 0.60, "power": 5000.0, "maturity": 0.90},
            "ion_thruster": {"isp": 3500.0, "eff": 0.70, "power": 3200.0, "maturity": 0.92},
            "MPD": {"isp": 5000.0, "eff": 0.50, "power": 100000.0, "maturity": 0.60},
            "VASIMR": {"isp": 8000.0, "eff": 0.65, "power": 200000.0, "maturity": 0.50},
            "NTR": {"isp": 900.0, "eff": 0.85, "power": 10000.0, "maturity": 0.65},
            "resistojet": {"isp": 300.0, "eff": 0.40, "power": 1000.0, "maturity": 0.95},
            "arcjet": {"isp": 600.0, "eff": 0.45, "power": 2000.0, "maturity": 0.90},
            "PPT": {"isp": 1200.0, "eff": 0.15, "power": 100.0, "maturity": 0.90}
        }

        candidates_out = []
        for name in candidates:
            if name not in tech_specs:
                continue
            spec = tech_specs[name]
            isp = spec["isp"]
            eff = spec["eff"]
            power = spec["power"]
            
            if power_budget and power > 0:
                power = min(power, float(power_budget))

            mass_ratio = np.exp(dv / (isp * G0))
            prop_mass = m_payload * (mass_ratio - 1)
            total_mass = m_payload + prop_mass
            ve = isp * G0

            if power > 0:
                thrust = 2.0 * eff * power / ve
                mdot = thrust / ve
                t_burn_s = prop_mass / mdot if mdot > 0 else 0.0
                transfer_days = (t_burn_s / 0.85) / 86400.0
            else:
                thrust = 400.0
                transfer_days = 0.5

            candidates_out.append({
                "thruster_type": name,
                "isp_s": float(isp),
                "thrust_n": float(thrust),
                "propellant_mass_kg": float(prop_mass),
                "total_mass_kg": float(total_mass),
                "power_w": float(power),
                "efficiency": float(eff),
                "transfer_time_days": float(transfer_days),
                "maturity": spec["maturity"]
            })

        # Sizing calculations
        prop_masses = [c["propellant_mass_kg"] for c in candidates_out]
        times = [c["transfer_time_days"] for c in candidates_out]
        min_prop = min(prop_masses)
        max_prop = max(prop_masses)
        min_time = min(times)
        max_time = max(times)

        scored_candidates = []
        for c in candidates_out:
            s_prop = 1.0 - (c["propellant_mass_kg"] - min_prop) / (max_prop - min_prop) if max_prop > min_prop else 1.0
            s_time = 1.0 - (c["transfer_time_days"] - min_time) / (max_time - min_time) if max_time > min_time else 1.0
            s_mat = c["maturity"]
            score = (0.40 * s_prop + 0.40 * s_time + 0.20 * s_mat) * 100.0

            scored_candidates.append({
                "thruster_type": c["thruster_type"],
                "isp_s": c["isp_s"],
                "thrust_n": c["thrust_n"],
                "propellant_mass_kg": c["propellant_mass_kg"],
                "total_mass_kg": c["total_mass_kg"],
                "power_w": c["power_w"],
                "efficiency": c["efficiency"],
                "transfer_time_days": c["transfer_time_days"],
                "score": float(score)
            })

        scored_candidates.sort(key=lambda x: x["score"], reverse=True)
        winner = scored_candidates[0]["thruster_type"]
        best = scored_candidates[0]

        rationale = (
            f"Based on optimization, the {best['thruster_type']} wins "
            f"with {best['score']:.1f}/100, requiring {best['propellant_mass_kg']:.1f} kg prop "
            f"and a transfer time of {best['transfer_time_days']:.1f} days."
        )

        return {
            "mission_summary": {
                "payload_mass_kg": m_payload,
                "delta_v_ms": dv,
                "mission_duration_years": duration,
                "evaluated_candidates_count": len(scored_candidates)
            },
            "candidates": scored_candidates,
            "winner": winner,
            "rationale": rationale
        }

    @staticmethod
    def optimize_thruster(
        thruster_type: str,
        target: Literal["thrust", "isp", "efficiency"],
        power_limit_w: float = 10000.0,
        mass_flow_limit_kg_s: float = 100e-6
    ) -> dict:
        bounds = [
            (100.0, power_limit_w),
            (1e-6, mass_flow_limit_kg_s),
            (0.1, 1.0)
        ]
        x0 = [power_limit_w * 0.5, mass_flow_limit_kg_s * 0.5, 0.5]

        def obj_func(x):
            power, mdot, mag_field = x
            base_eff = 0.65 if thruster_type == "hall_thruster" else 0.70
            ionization_efficiency = base_eff * (1.0 - np.exp(-power / 3000.0)) * mag_field
            nozzle_efficiency = 1.0 - 0.05 * (mdot / mass_flow_limit_kg_s)
            efficiency = float(np.clip(ionization_efficiency * nozzle_efficiency, 0.05, 0.85))

            isp = 1500.0 * np.sqrt(power / (mdot * 1e6)) * (1.0 + mag_field * 0.15)
            isp = float(np.clip(isp, 500.0, 10000.0))
            thrust = mdot * (isp * G0)

            if target == "thrust":
                return -thrust
            elif target == "isp":
                return -isp
            else:
                return -efficiency

        res = minimize(obj_func, x0, method="L-BFGS-B", bounds=bounds)
        opt_power, opt_mdot, opt_mag_field = res.x
        
        # Calculate comparison details
        opt_base_eff = 0.65 if thruster_type == "hall_thruster" else 0.70
        opt_ionization = opt_base_eff * (1.0 - np.exp(-opt_power / 3000.0)) * opt_mag_field
        opt_nozzle = 1.0 - 0.05 * (opt_mdot / mass_flow_limit_kg_s)
        opt_eff = float(np.clip(opt_ionization * opt_nozzle, 0.05, 0.85))
        opt_isp = 1500.0 * np.sqrt(opt_power / (opt_mdot * 1e6)) * (1.0 + opt_mag_field * 0.15)
        opt_isp = float(np.clip(opt_isp, 500.0, 10000.0))
        opt_thrust = opt_mdot * (opt_isp * G0)

        init_power, init_mdot, init_mag = x0
        init_ionization = opt_base_eff * (1.0 - np.exp(-init_power / 3000.0)) * init_mag
        init_nozzle = 1.0 - 0.05 * (init_mdot / mass_flow_limit_kg_s)
        init_eff = float(np.clip(init_ionization * init_nozzle, 0.05, 0.85))
        init_isp = 1500.0 * np.sqrt(init_power / (init_mdot * 1e6)) * (1.0 + init_mag * 0.15)
        init_isp = float(np.clip(init_isp, 500.0, 10000.0))
        init_thrust = init_mdot * (init_isp * G0)

        return {
            "thruster_type": thruster_type,
            "target_optimized": target,
            "success": bool(res.success),
            "iterations": int(res.nit),
            "parameters": {
                "power_w": {"initial": float(init_power), "optimal": float(opt_power)},
                "mass_flow_rate_kg_s": {"initial": float(init_mdot), "optimal": float(opt_mdot)},
                "magnetic_field_strength": {"initial": float(init_mag), "optimal": float(opt_mag_field)}
            },
            "performance": {
                "thrust_n": {
                    "initial": float(init_thrust),
                    "optimal": float(opt_thrust),
                    "improvement_pct": float(((opt_thrust - init_thrust) / init_thrust) * 100.0)
                },
                "isp_s": {
                    "initial": float(init_isp),
                    "optimal": float(opt_isp),
                    "improvement_pct": float(((opt_isp - init_isp) / init_isp) * 100.0)
                },
                "efficiency": {
                    "initial": float(init_eff),
                    "optimal": float(opt_eff),
                    "improvement_pct": float(((opt_eff - init_eff) / init_eff) * 100.0)
                }
            }
        }
