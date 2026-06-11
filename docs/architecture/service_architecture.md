# Service Architecture

## Microservices Map

| Service | Port | Responsibility |
|---------|------|----------------|
| api-gateway | 8000 | Single entry, auth, routing |
| auth-service | 8001 | JWT, OAuth2, users |
| project-service | 8002 | Project CRUD, persistence |
| simulation-service | 8003 | Thrust/thermal/power/mission |
| optimization-service | 8004 | AI-driven optimization |
| reporting-service | 8005 | PDF/JSON engineering reports |
| notification-service | 8006 | WebSocket, email, alerts |

## Inter-Service Communication

- **Synchronous:** REST over HTTP (FastAPI clients).
- **Asynchronous:** Redis pub/sub for events.
- **Streaming:** WebSocket for real-time telemetry.

## Service Boundaries

Each service:
- Owns its own database schema.
- Exposes a versioned REST API.
- Logs to a centralized ELK stack.
- Reports metrics to Prometheus.

## Scaling Strategy

| Service | Replicas | Resources |
|---------|----------|-----------|
| api-gateway | 3 | 0.5 CPU, 512MB |
| auth-service | 2 | 0.5 CPU, 512MB |
| simulation-service | 3-10 (HPA) | 1-4 CPU, 1-8GB |
| optimization-service | 1-5 (HPA) | 2-8 CPU, 4-16GB (GPU opt.) |
| reporting-service | 2 | 1 CPU, 1GB |
