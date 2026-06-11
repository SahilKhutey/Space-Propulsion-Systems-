# Gridded Ion Thruster Simulation Example
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "engines", "thrust-engine")))

from thrust_engine import ThrustEngine

def run_demo():
    engine = ThrustEngine()
    print("Running Gridded Ion Thruster model...")
    params = {
        "power_w": 3200.0,
        "efficiency": 0.70,
        "isp_s": 3500.0,
        "propellant": "xenon"
    }
    res = engine.compute("ion", params)
    print("Demo Result:")
    for k, v in res.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    run_demo()
