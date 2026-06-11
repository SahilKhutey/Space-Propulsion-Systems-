# PropSim Hall Thruster Demonstration
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "engines", "thrust-engine")))

from thrust_engine import ThrustEngine

def run_demo():
    engine = ThrustEngine()
    print("Initializing Hall Thruster computation...")
    params = {
        "power_w": 4500.0,
        "efficiency": 0.60,
        "isp_s": 1800.0,
        "propellant": "xenon"
    }
    res = engine.compute("hall", params)
    print("Demo Result:")
    for k, v in res.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    run_demo()
