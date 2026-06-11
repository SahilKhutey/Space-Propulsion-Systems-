# ADR-001: Simulation Engine Design

- **Status:** Approved
- **Deciders:** Core Architecture Team
- **Date:** 2026-06-11

## Context
We need to run high-fidelity orbit propagation, thermal nodes solver, and power simulation simultaneously.

## Decision
We choose a decoupled loop architecture. The main loop runs at a master clock rate of 1 Hz. Orbit propagation and attitude drift run inside a sub-solver loop @ 10 Hz to prevent numerical instabilities.

## Consequences
- High precision.
- Requires strict lock-step synchronization on SpacecraftState.
