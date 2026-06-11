# Propulsion Simulation Platform (PropSim)

> Professional-Grade Aerospace Digital Engineering & Trajectory Propagation Platform.

PropSim is a modular, high-fidelity spacecraft simulation platform engineered for mission design, trajectory propagation, thermal-network analysis, and digital twin telemetry synchronization. It supports the optimization of low-thrust electric propulsion missions (Hall, Ion, VASIMR, MPD) as well as high-thrust chemical and nuclear systems.

---

## 🛰️ 1. Project Vision

PropSim bridges the gap between early R&D mission planning and real-time operations. It enables aerospace engineers to:
* **Model Thrusters**: Simulates performance (thrust, Isp, efficiency, mass flow, plasma dynamics) across 9 distinct propulsion technologies.
* **Propagate Orbits**: Evaluates orbital trajectories under $J_2$ Earth oblateness and atmospheric drag perturbations using symplectic, energy-preserving integrators.
* **Simulate Subsystems**: Runs coupled simulations modeling multi-node thermal conduction/radiation and solar array power generation.
* **Synchronize Telemetry**: Integrates real-time flight telemetry streams with a simulated Extended Kalman Filter (EKF) to establish an operational digital twin.

---

## 📦 2. Subsystem Architecture

PropSim is built using a decoupled, layered architecture to isolate foundational calculations from application services:

```
                            ┌─────────────────────────┐
                            │    React Frontend /     │
                            │    Three.js Viewports   │
                            └───────────┬─────────────┘
                                        │ REST / WebSockets
                            ┌───────────▼─────────────┐
                            │   FastAPI API Gateway   │
                            │    (SaaS Microservices) │
                            └───────────┬─────────────┘
                                        │
             ┌──────────────────────────┼──────────────────────────┐
             ▼                          ▼                          ▼
      ┌──────────────┐           ┌──────────────┐           ┌──────────────┐
      │ Orbit Engine │           │ Thrust Engine│           │Thermal Engine│
      │   (Verlet)   │           │ (Performance)│           │   (N-Node)   │
      └──────┬───────┘           └──────┬───────┘           └──────┬───────┘
             │                          │                          │
             └──────────────────────────┼──────────────────────────┘
                                        ▼
                            ┌─────────────────────────┐
                            │    Foundational Core    │
                            │   Math, Physics, Consts │
                            └─────────────────────────┘
```

### Directory Structure Map
* [apps/web](file:///C:/Users/User/Documents/Space%20Propulsion/propulsion-simulation-platform/apps/web) — React + TypeScript dashboard with Three.js orbit viewer.
* [services/](file:///C:/Users/User/Documents/Space%20Propulsion/propulsion-simulation-platform/services) — FastAPI services for authentication, project management, and simulation workflows.
* [engines/](file:///C:/Users/User/Documents/Space%20Propulsion/propulsion-simulation-platform/engines) — Independent python engines for trajectory propagation, thruster sizing, thermal networks, and mission planning.
* [core/](file:///C:/Users/User/Documents/Space%20Propulsion/propulsion-simulation-platform/core) — Pure mathematical and physical foundations (Runge-Kutta, vector algebra, J2 gravity fields, constants).
* [docs/](file:///C:/Users/User/Documents/Space%20Propulsion/propulsion-simulation-platform/docs) — Layered documentation detailing equations, architectures, and deployment guidelines.
* [standards/](file:///C:/Users/User/Documents/Space%20Propulsion/propulsion-simulation-platform/standards) — Coding guidelines, aerospace standards, and simulation accuracies.
* [validation/](file:///C:/Users/User/Documents/Space%20Propulsion/propulsion-simulation-platform/validation) — daily benchmark runs comparing simulation outputs against analytical solutions and NASA flight data.

---

## 🚀 3. Features

* **Advanced Solvers**: Includes Runge-Kutta 4 (RK4), adaptive-step Dormand-Prince (RK45) for maneuvers, and Symplectic Velocity Verlet for long-duration orbital stability.
* **Low-Thrust Optimization**: Hybrid genetic algorithm (GA) and Sequential Quadratic Programming (SQP) trajectory optimizer.
* **Digital Twin & EKF**: Multi-variable state estimator utilizing an Extended Kalman Filter to process noisy telemetry inputs.
* **Thermal Networks**: N-Node lumped parameter network (LPN) thermal solver accounting for radiation, conduction, and active thruster dissipation.
* **Power Forecasting**: Orbital solar flux modeling (accounting for distance and eclipses) and battery charge/discharge transient solvers.

---

## 📐 4. Mathematical & Physics Foundations

### Hohmann Transfer Delta-V
Computes impulse maneuvers between circular orbits:
$$\Delta v_1 = \sqrt{\frac{\mu}{r_1}} \left( \sqrt{\frac{2 r_2}{r_1 + r_2}} - 1 \right)$$
$$\Delta v_2 = \sqrt{\frac{\mu}{r_2}} \left( 1 - \sqrt{\frac{2 r_1}{r_1 + r_2}} \right)$$

### J2 Perturbation Acceleration
Models the oblateness of Earth:
$$a_{J2} = \frac{3}{2} \frac{J_2 \mu R_E^2}{r^5} \begin{bmatrix} x \left(5\frac{z^2}{r^2} - 1\right) \\ y \left(5\frac{z^2}{r^2} - 1\right) \\ z \left(5\frac{z^2}{r^2} - 3\right) \end{bmatrix}$$

---

## 🛠️ 5. Quick Start & Installation

### Prerequisites
* Python $\ge$ 3.11
* Node.js $\ge$ 20 (for Web UI)
* Docker & Docker Compose (for microservices stack)

### Local Setup
1. Clone the repository and initialize the virtual environment:
   ```bash
   make setup
   ```
2. Activate the virtual environment:
   * **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   * **Linux/macOS**:
     ```bash
     source .venv/bin/activate
     ```

### Running the Test Suite
Verify that all 116 unit, integration, and physics validation tests pass:
```bash
python -m pytest
```

### Running Demos
Evaluate thruster performance and trajectory propagation:
* **Hall Effect Thruster Sizing**:
  ```bash
  python examples/hall_thruster_demo/main.py
  ```
* **Gridded Ion Thruster Simulation**:
  ```bash
  python examples/ion_thruster_demo/main.py
  ```

---

## 🧪 6. Verification and Validation

We validate all physical models against analytical solutions and published NASA data:
* **Orbit Solvers**: Bounded energy drift using symplectic integrators. Tested against Keplerian analytical periods.
* **Thrust and Specific Impulse**: Child-Langmuir space-charge limitations are validated against gridded ion test data.
* **Real-time Performance**: Long-duration runs (72h simulated) are benchmarked to verify memory stability ($<50\text{ MB}$ growth).

---

## 🗺️ 7. Development Roadmap

* [x] **Phase 1: R&D Foundation**: Core orbital propagator, basic thermal node network, and 9 thruster models.
* [ ] **Phase 2: Hybrid Open-Core**: Open-source mathematical foundations and closed-source trajectory optimizer integration.
* [ ] **Phase 3: WebGPU SaaS**: Offload PIC plasma and CFD thermal simulations to client-side WebGPU solvers.

---

## ⚖️ 8. License & Export Controls

* **License**: Open-core components (mathematical solvers, unit transformations, base physics) are under the **MIT License**. The optimization engines, digital twin telemetry pipelines, and advanced thruster models are under the **PropSim Proprietary License**.
* **Export Control Notice**: This repository contains advanced electric spacecraft propulsion modeling algorithms. Distribution and usage must comply with **ITAR (International Traffic in Arms Regulations, Category XV)** and **EAR (Export Administration Regulations)** compliance frameworks.
