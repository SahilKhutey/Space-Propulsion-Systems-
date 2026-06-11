# Data Architecture

## Storage Stack

| Data | Store | Justification |
|------|-------|---------------|
| User accounts | PostgreSQL | ACID, relational integrity |
| Projects/missions | PostgreSQL | Relational integrity |
| Simulation runs | PostgreSQL + JSONB | Structured + flexible payload |
| Time-series telemetry | TimescaleDB | High-write time-series rate |
| Cached results | Redis | Sub-ms latency caching |
| Large binary (reports, exports) | S3 / MinIO | Object storage |
| Reference datasets | Versioned JSON | Reproducibility & portability |

## Schema (PostgreSQL & TimescaleDB)

```sql
-- Core PostgreSQL Tables
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'user',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  owner_id INT REFERENCES users(id),
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- TimescaleDB Time-Series Table
CREATE TABLE telemetry (
  time TIMESTAMPTZ NOT NULL,
  mission_id INT NOT NULL,
  metric VARCHAR(50) NOT NULL,
  value DOUBLE PRECISION NOT NULL
);
SELECT create_hypertable('telemetry', 'time');
```

## Data Retention

- **Hot (PostgreSQL & Redis):** Active cache and relational project tables (90 days).
- **Warm (TimescaleDB):** Real-time telemetry history (1 year).
- **Cold (S3/MinIO):** Parquet-compressed telemetry logs, archived indefinitely for analytical audits.
