# PROPSIM Validation & Reasoning Engine Test Suite

This directory contains the 3-Level Validation Suite and automated Engineering Reasoning Engine tests for **PROPSIM**.

## Validation Hierarchy

1. **Level 1 → Mathematical Validation** (`test_01_mathematics.py`)
   - Verifies the vector algebra, matrix rotation transforms, quaternions, and numerical integrators (RK4, adaptive Dopri45, Euler).
2. **Level 2 → Physics Validation** (`test_02_propulsion.py`, `test_03_orbital.py`, `test_05_thermal.py`, `test_06_power.py`)
   - Validates the thruster thrust, mass flow, specific impulse, orbital kinematics, escape velocities, radiative cooling (Stefan-Boltzmann), eclipses, and battery state-of-charge.
3. **Level 3 → Mission Validation** (`test_04_mission.py`, `test_07_realtime.py`, `test_08_projection.py`, `test_09_digital_twin.py`, `test_10_ai_optimization.py`, `test_11_end_to_end.py`)
   - Tests rocket equation calculations, multi-burn propellant budgets, real-time loops, forecasting, Kalman filter telemetry synchronization, and the integrated root cause analysis (RCA) pipeline.

## Running the Tests

To execute the entire test suite:

```bash
cd propulsion-simulation-platform
pytest test-suite/
```

To run a specific category of tests, use the registered markers:

```bash
pytest test-suite/ -m math
pytest test-suite/ -m propulsion
pytest test-suite/ -m orbital
pytest test-suite/ -m mission
pytest test-suite/ -m thermal
pytest test-suite/ -m power
pytest test-suite/ -m realtime
pytest test-suite/ -m projection
pytest test-suite/ -m digital_twin
pytest test-suite/ -m ai
pytest test-suite/ -m e2e
```
