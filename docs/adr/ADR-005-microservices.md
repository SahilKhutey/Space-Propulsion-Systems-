# ADR-005: Microservices Boundaries

- **Status:** Approved
- **Deciders:** Platform Lead
- **Date:** 2026-06-11

## Context
The platform must support SaaS scaling.

## Decision
Decouple services into: `auth`, `project`, and `simulation`. Use REST for project CRUD and WebSocket for real-time telemetry streaming.
