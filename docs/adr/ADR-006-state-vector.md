# ADR-006: State Vector Structure

- **Status:** Approved
- **Deciders:** Core Leads
- **Date:** 2026-06-11

## Context
State sharing between orbit and thermal solvers requires a strict boundary.

## Decision
Establish a unified flat vector representation to allow fast NumPy operations.
