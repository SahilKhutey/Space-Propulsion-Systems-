class FaultNode:
    def __init__(self, name: str, description: str, children: list = None):
        self.name = name
        self.description = description
        self.children = children if children is not None else []

def build_root_cause_tree() -> FaultNode:
    root = FaultNode("Mission Failure", "Global failure of the mission")
    
    # Subsystems
    prop = FaultNode("Propulsion", "Propulsion subsystem failures", [
        FaultNode("Low ISP", "Thrust specific impulse is below baseline"),
        FaultNode("Low Thrust", "Thrust output is insufficient"),
        FaultNode("Fuel Exhausted", "Propellant depletion before goal achievement")
    ])
    
    thermal = FaultNode("Thermal", "Thermal control subsystem failures", [
        FaultNode("Overheating", "Node temperature exceeds maximum safe limit"),
        FaultNode("Freezing", "Node temperature falls below minimum safe limit"),
        FaultNode("Radiator Failure", "Radiative heat rejection is impaired")
    ])
    
    power = FaultNode("Power", "Electrical power subsystem failures", [
        FaultNode("Battery Depletion", "Battery state of charge falls to critical level"),
        FaultNode("Solar Failure", "Solar array generation is below load requirements"),
        FaultNode("Excess Loads", "Payload or thruster power draw exceeds generation capacity")
    ])
    
    orbit = FaultNode("Orbit", "Orbital mechanics and navigation failures", [
        FaultNode("Transfer Error", "Failed to perform transfer orbit injection"),
        FaultNode("Navigation Error", "Orbit determination error"),
        FaultNode("Escape Failure", "Failed to achieve escape velocity")
    ])
    
    control = FaultNode("Control", "Attitude determination and control failures", [
        FaultNode("Attitude Error", "Pointing error is too high"),
        FaultNode("Sensor Error", "Star tracker or IMU failure"),
        FaultNode("Actuator Failure", "Reaction wheel or RCS failure")
    ])
    
    root.children = [prop, thermal, power, orbit, control]
    return root
