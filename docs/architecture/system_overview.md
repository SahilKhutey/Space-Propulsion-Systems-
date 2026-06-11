# System Overview

## PropSim Platform Architecture

PropSim is a modular aerospace propulsion digital engineering platform designed to evolve from an internal R&D tool to a commercial SaaS.

## High-Level Architecture

```
┌─────────────────────────────────────┐
│           Frontend Layer            │
│    React + TypeScript + Three.js    │
│          CesiumJS + WebGPU          │
└─────────────────┬───────────────────┘
                  │ REST + WebSocket
                  ▼
┌─────────────────────────────────────┐
│          API Gateway Layer          │
│    Auth, Routing, Rate Limiting     │
└─────────────────┬───────────────────┘
                  │
        ┌─────────┼──────────┐
        ▼         ▼          ▼
   ┌────────┐ ┌────────┐ ┌──────────┐
   │  Auth  │ │ Project│ │Simulation│
   │Service │ │Service │ │ Service  │
   └────────┘ └────────┘ └────┬─────┘
                             │
        ┌────────────────────┼────────────┐
        ▼                    ▼            ▼
   ┌─────────┐          ┌─────────┐  ┌─────────┐
   │ Thrust  │          │ Thermal │  │ Mission │
   │ Engine  │          │  Engine │  │ Engine  │
   └─────────┘          └─────────┘  └─────────┘
        │                    │            │
        └────────────────────┼────────────┘
                             ▼
                ┌────────────────────────┐
                │    Real-Time Engine    │
                │  (State + Propagators) │
                └────────────────────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │  Projection & Digital  │
                │       Twin Layer       │
                └────────────────────────┘
```

## Core Principles

1. **Modularity** — Every engine is an independent package.
2. **Physics-first** — All equations documented in `/docs/physics/`.
3. **Validation** — Every result is traceable to a benchmark.
4. **Reproducibility** — Deterministic simulations, version-locked datasets.
5. **Extensibility** — Plugin architecture for new thruster types.

## Subsystems

| Subsystem | Responsibility | Tech Stack |
|-----------|----------------|------------|
| Thrust Engine | 9+ thruster models | NumPy, SciPy |
| Orbit Engine | Kepler, transfers | Poliastro, SPICE |
| Thermal Engine | Multi-node heat | NumPy, planned FEM |
| Mission Engine | End-to-end analysis | All engines |
| Real-Time Engine | Live simulation | NumPy, async |
| Digital Twin | State estimation | KF/EKF/UKF/PINN |
| Frontend | Mission Control UI | React, Three.js, Cesium |
| API Gateway | Routing, auth | FastAPI |

## Data Flow

1. User interacts with Frontend (React).
2. Frontend requests API Gateway (REST + WebSocket).
3. Gateway routes to Services (auth, project, simulation, optimization).
4. Services execute Engines (thrust, thermal, etc.).
5. Engines update Real-Time engine for state evolution.
6. Real-Time engine uses Projection for forecasting.
7. Projection stream updates Frontend via WebSocket.
