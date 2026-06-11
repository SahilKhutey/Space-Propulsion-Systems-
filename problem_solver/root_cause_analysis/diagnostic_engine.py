import numpy as np
from ..schemas import RootCause, Anomaly
from problem_solver.diagnosis.threshold_engine import Thresholds

class DiagnosticEngine:
    def __init__(self):
        pass
        
    def diagnose(self, history: list[dict], anomalies: list[Anomaly], mission_context: dict = None) -> list[RootCause]:
        diagnoses = []
        if not anomalies:
            return diagnoses
            
        # Group anomalies by type
        types = [a.anomaly_type for a in anomalies]
        
        # 1. Diagnose Power failure
        if "Power" in types:
            # Find the first power anomaly step
            pow_anom = [a for a in anomalies if a.anomaly_type == "Power"][0]
            # Analyze state around that timestamp
            t = pow_anom.timestamp
            matching_steps = [s for s in history if abs(s.get("time", 0) - t) < 60.0]
            step = matching_steps[0] if matching_steps else history[-1]
            
            # Check solar generation vs loads
            p_solar = step.get("power_solar", 0.0)
            p_load = step.get("power_load", 0.0)
            pos = step.get("position_m", [0, 0, 0])
            r_mag = np.linalg.norm(pos)
            dist_au = r_mag / 1.496e11 if r_mag > 1e9 else 1.0
            
            failure_path = ["Battery level dropped below critical threshold"]
            root_cause = "Battery Depleted"
            confidence = 0.8
            
            if dist_au > 1.3:
                # Mars or deep space
                failure_path.append(f"Mission is in deep space (distance: {dist_au:.2f} AU)")
                failure_path.append(f"Solar flux is reduced by {(1/dist_au**2)*100:.1f}% compared to Earth")
                if p_solar < p_load:
                    root_cause = "Solar Array Undersized"
                    failure_path.append("Solar array generation is insufficient to balance the continuous spacecraft load")
                    confidence = 0.95
            elif p_solar == 0.0:
                # Eclipse
                failure_path.append("Spacecraft entered planetary shadow (eclipse)")
                failure_path.append("Solar generation dropped to 0 W")
                # Check if battery was fully charged before eclipse
                root_cause = "Battery Undersized"
                failure_path.append("Battery capacity is insufficient for the shadow duration")
                confidence = 0.9
            elif p_load > p_solar:
                root_cause = "Excessive Load"
                failure_path.append("Continuous system loads exceed solar array generation limits")
                confidence = 0.85
                
            diagnoses.append(RootCause(
                root_cause=root_cause,
                subsystem="Power",
                failure_path=failure_path,
                confidence=confidence
            ))
            
        # 2. Diagnose Thermal failure
        if "Thermal" in types:
            thermal_anom = [a for a in anomalies if a.anomaly_type == "Thermal"][0]
            t = thermal_anom.timestamp
            matching_steps = [s for s in history if abs(s.get("time", 0) - t) < 60.0]
            step = matching_steps[0] if matching_steps else history[-1]
            
            temps = step.get("thermal_k", [250.0])
            max_t = np.max(temps)
            
            failure_path = [f"Component node temperature reached {max_t:.1f} K"]
            
            if max_t > Thresholds.THERMAL_MAX_K:
                root_cause = "Overheating"
                if step.get("thruster_on", False):
                    failure_path.append("Thruster active: generating high heat dissipation")
                    root_cause = "Insufficient Radiator Heat Rejection"
                    failure_path.append("Radiator area or emissivity is undersized for full thruster power thermal dissipation")
                diagnoses.append(RootCause(
                    root_cause=root_cause,
                    subsystem="Thermal",
                    failure_path=failure_path,
                    confidence=0.9
                ))
            elif np.min(temps) < Thresholds.THERMAL_MIN_K:
                diagnoses.append(RootCause(
                    root_cause="Freezing",
                    subsystem="Thermal",
                    failure_path=failure_path + ["Spacecraft entered eclipse or deep space with insufficient heater power"],
                    confidence=0.85
                ))
                
        # 3. Diagnose Propulsion failure
        if "Propulsion" in types:
            prop_anom = [a for a in anomalies if a.anomaly_type == "Propulsion"][0]
            diagnoses.append(RootCause(
                root_cause="Fuel Depleted",
                subsystem="Propulsion",
                failure_path=["Thruster active for long duration", "Propellant mass consumed completely before mission end"],
                confidence=0.95
            ))
            
        return diagnoses
