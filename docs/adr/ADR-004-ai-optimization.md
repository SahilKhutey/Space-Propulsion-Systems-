# ADR-004: Trajectory AI Optimization Engine

- **Status:** Approved
- **Deciders:** ML Architects
- **Date:** 2026-06-11

## Context
High-thrust trajectory optimization has multiple local minima.

## Decision
Use a hybrid optimizer: Genetic Algorithms (GA) locate the global optimal region, followed by a gradient-based sequential quadratic programming (SQP) local solver for convergence.
