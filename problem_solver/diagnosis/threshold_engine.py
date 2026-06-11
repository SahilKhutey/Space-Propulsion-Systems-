class Thresholds:
    # Power
    BATTERY_CRITICAL_SOC = 0.10  # 10%
    BATTERY_WARNING_SOC = 0.20   # 20%
    
    # Thermal
    THERMAL_MAX_K = 343.15       # 70 C
    THERMAL_WARNING_K = 333.15   # 60 C
    THERMAL_MIN_K = 233.15       # -40 C
    
    # Propulsion
    MIN_EFFICIENCY = 0.15
    MAX_ISP = 20000.0            # limit for Hall/Ion thrusters
    
    # Orbit
    MIN_LEO_ALTITUDE_M = 100e3   # Re-entry limit (100km)
