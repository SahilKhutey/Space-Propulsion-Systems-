# Uncertainty Quantification

## Statistical Dispersion Models

Aerospace missions must account for thrust errors and thermal fluctuations.

### Covariance Propagation
$$P(t) = \Phi(t, t_0) P(t_0) \Phi^T(t, t_0) + Q$$
Where:
- $P$ is the state covariance matrix.
- $\Phi$ is the State Transition Matrix (STM).
- $Q$ is the process noise covariance matrix.
