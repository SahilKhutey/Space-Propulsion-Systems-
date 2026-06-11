# Scaling Architecture

## Horizontal Pod Autoscaler (HPA)

For computational simulation workloads, scaling is based on CPU utilization and Custom Queue Metrics (RabbitMQ/Redis queue size).

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: simulation-service
  namespace: propsim
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: simulation-service
  minReplicas: 3
  maxReplicas: 15
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
  - type: External
    external:
      metric:
        name: cel_simulation_queue_length
      target:
        type: Value
        averageValue: 50
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
```

## Scale-up and Scale-down Cool-down Policies

- **Scale-Up Stabilization Window:** 0 seconds. Ensures that the system spins up extra simulation pods immediately when a large batch of trajectories is queued.
- **Scale-Down Stabilization Window:** 300 seconds (5 minutes). Prevents thrashing (rapid scaling up and down) by waiting for transient queues to clear before deleting warm pods.

## Prometheus Metrics Configuration

Prometheus scrapes custom metrics from the API Gateway and background worker queues.
Metric used: `cel_simulation_queue_length`
PromQL definition:
```promql
sum(rabbitmq_queue_messages{queue="simulations"}) by (queue)
```
