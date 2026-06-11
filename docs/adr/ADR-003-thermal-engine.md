# ADR-003: Thermal Engine Lumped Parameter Solver

- **Status:** Approved
- **Deciders:** Thermal Engineers
- **Date:** 2026-06-11

## Context
FEM analysis is too computationally expensive for real-time mission planning.

## Decision
Use an N-Node Lumped Parameter Network (LPN) model representing spacecraft components (body, solar panels, radiators, battery).

## Consequences
- 1000x faster than FEM.
- Requires calibrated nodal conduction matrices.
