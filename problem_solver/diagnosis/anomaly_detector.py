import numpy as np
from ..schemas import Anomaly
from .threshold_engine import Thresholds

class AnomalyDetector:
    def __init__(self):
        pass
        
    def detect(self, history: list[dict]) -> list[Anomaly]:
        anomalies = []
        if not history:
            return anomalies
            
        for step in history:
            t = step.get("time", 0.0)
            
            # 1. Thermal check
            thermal = step.get("thermal_k", [])
            for i, temp in enumerate(thermal):
                if temp > Thresholds.THERMAL_MAX_K:
                    anomalies.append(Anomaly(
                        anomaly_type="Thermal",
                        severity="critical",
                        timestamp=t,
                        message=f"Node {i} temperature ({temp:.1f} K) exceeds critical limit {Thresholds.THERMAL_MAX_K} K.",
                        node_id=i
                    ))
                elif temp > Thresholds.THERMAL_WARNING_K:
                    anomalies.append(Anomaly(
                        anomaly_type="Thermal",
                        severity="medium",
                        timestamp=t,
                        message=f"Node {i} temperature ({temp:.1f} K) is in warning range.",
                        node_id=i
                    ))
                elif temp < Thresholds.THERMAL_MIN_K:
                    anomalies.append(Anomaly(
                        anomaly_type="Thermal",
                        severity="medium",
                        timestamp=t,
                        message=f"Node {i} temperature ({temp:.1f} K) is below minimum allowed ({Thresholds.THERMAL_MIN_K} K).",
                        node_id=i
                    ))
            
            # 2. Power check
            soc = step.get("battery_soc", 1.0)
            if soc < Thresholds.BATTERY_CRITICAL_SOC:
                anomalies.append(Anomaly(
                    anomaly_type="Power",
                    severity="critical",
                    timestamp=t,
                    message=f"Battery state of charge ({soc*100:.1f}%) is critical (below {Thresholds.BATTERY_CRITICAL_SOC*100:.1f}%)."
                ))
            elif soc < Thresholds.BATTERY_WARNING_SOC:
                anomalies.append(Anomaly(
                    anomaly_type="Power",
                    severity="low",
                    timestamp=t,
                    message=f"Battery state of charge ({soc*100:.1f}%) is in warning range."
                ))
                
            # 3. Orbit check
            pos = step.get("position_m", [0, 0, 0])
            r_mag = np.linalg.norm(pos)
            alt = r_mag - 6378137.0
            if alt < Thresholds.MIN_LEO_ALTITUDE_M and r_mag > 1.0:
                anomalies.append(Anomaly(
                    anomaly_type="Orbit",
                    severity="critical",
                    timestamp=t,
                    message=f"Spacecraft altitude ({alt/1000:.1f} km) is below re-entry threshold ({Thresholds.MIN_LEO_ALTITUDE_M/1000:.1f} km)."
                ))
                
            # 4. Fuel check
            prop = step.get("propellant_fraction", 1.0)
            if prop <= 1e-4:
                anomalies.append(Anomaly(
                    anomaly_type="Propulsion",
                    severity="high",
                    timestamp=t,
                    message="Propellant completely depleted."
                ))
                
        return anomalies
