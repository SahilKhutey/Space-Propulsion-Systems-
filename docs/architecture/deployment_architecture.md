# Deployment Architecture

## Production Stack

```
             ┌──────────────┐
             │ CloudFront / │
             │   CDN        │
             └──────┬───────┘
                    │
   ┌────────────────┼────────────────┐
   ▼                ▼                ▼
┌─────────┐   ┌──────────┐     ┌──────────┐
│  Web    │   │  API GW  │     │ WebSocket│
│ (S3+CF) │   │  (ALB)   │     │  (ALB)   │
└─────────┘   └────┬─────┘     └────┬─────┘
                   │                │
   ┌───────────────┼────────────────┼──────────────┐
   ▼               ▼                ▼              ▼
┌─────────┐  ┌──────────┐     ┌──────────┐   ┌──────────┐
│  Auth   │  │Simulation│     │Optimize  │   │ Reporting│
│ Service │  │ Service  │     │ Service  │   │ Service  │
└─────────┘  └──────────┘     └──────────┘   └──────────┘
      │            │                │              │
      └────────────┼────────────────┴──────────────┘
                   ▼
         ┌──────────────────┐
         │  RDS PostgreSQL  │
         │  + TimescaleDB   │
         │  ElastiCache     │
         │  S3 / MinIO      │
         └──────────────────┘
```

## Environments

| Environment | Purpose | Deploy Trigger |
|-------------|---------|----------------|
| dev | Developer staging & preview | PR open / merge to develop |
| staging | Pre-production validation | Merge to develop / release branch |
| production | Live SaaS deployment | Tag v* (release pipeline) |

## CI/CD Pipeline

The integration pipeline uses GitHub Actions to build Docker containers, which are published to ECR/GHCR. ArgoCD monitors the Helm charts under `infrastructure/kubernetes/` to update the Kubernetes clusters automatically.
