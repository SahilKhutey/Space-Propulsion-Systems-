# PropSim Propulsion Simulation Platform

PropSim is a modular, professional-grade aerospace digital engineering and trajectory propagation platform.

## Subsystems Map
- **core/**: Basic coordinate transforms, solvers, and physical constants.
- **engines/**: Physics models for thrust, thermal, orbit propagation, and mission design.
- **services/**: SaaS microservices (auth, project, simulation).
- **docs/**: Comprehensive physics, mathematics, and architectural manuals.

## Quick Start
1. Setup Python Virtual Environment:
   ```bash
   make setup
   ```
2. Run Trajectory Example:
   ```bash
   python examples/hall_thruster_demo/main.py
   ```
