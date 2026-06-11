# ADR-002: Orbit Engine Solvers

- **Status:** Approved
- **Deciders:** Orbit Subsystem Leads
- **Date:** 2026-06-11

## Context
Orbit propagation needs to balance computational cost (for batch Monte Carlo) and precision (for flight path validation).

## Decision
Implement a solver factory providing:
1. **Symplectic Velocity Verlet:** Default for long missions.
2. **Dormand-Prince adaptive RK45:** Default for close-proximity maneuvers.
