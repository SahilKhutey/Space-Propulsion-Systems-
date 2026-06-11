# Software Architecture

## Layered Design

```
┌────────────────────────────────────────────┐
│ Presentation Layer (React + Three.js)      │
├────────────────────────────────────────────┤
│ Application Layer (FastAPI services)       │
├────────────────────────────────────────────┤
│ Domain Layer (Engines: thrust, thermal...) │
├────────────────────────────────────────────┤
│ Foundation Layer (Core: math, physics)     │
├────────────────────────────────────────────┤
│ Infrastructure (Postgres, Redis, K8s)      │
└────────────────────────────────────────────┘
```

## Module Boundaries

### Foundation (Core)
- Pure-Python, no FastAPI/DB dependency.
- Path: `core/mathematics/`, `core/physics/`, `core/constants/`.
- License: Public, MIT-licensed.

### Domain (Engines)
- Depend on Foundation layer.
- Independent packages: `engines/thrust-engine/`, etc.
- License: Hybrid-licensed (foundation MIT, models proprietary).

### Application (Services)
- Depend on Domain layer.
- FastAPI microservices.
- License: Proprietary.

### Presentation (Apps)
- Depend on Application layer.
- React frontend.
- License: Proprietary.

## Dependency Rules

```
Apps ──> Services ──> Engines ──> Core ──> Datasets
```

Strict Boundaries:
- Core cannot import Engines.
- Engines cannot import Services.
- Services cannot import Apps.
- Apps can import from any layer.
