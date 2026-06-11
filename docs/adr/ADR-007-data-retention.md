# ADR-007: Telemetry Data Retention

- **Status:** Approved
- **Deciders:** Data Leads
- **Date:** 2026-06-11

## Context
High rate websocket telemetry consumes database storage rapidly.

## Decision
Configure TimescaleDB with a retention policy of 1 year. Offload historical runs to S3 in compressed Parquet files.
