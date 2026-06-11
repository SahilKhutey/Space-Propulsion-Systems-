# State Space Models

## Spacecraft Control & Estimation

The linear dynamics system is defined as:
$$\dot{x}(t) = A x(t) + B u(t) + w(t)$$
$$y(t) = C x(t) + D u(t) + v(t)$$

Where:
- $x(t)$ is the state vector.
- $u(t)$ is the control inputs (thruster firings).
- $w(t), v(t)$ are process and measurement noise respectively.
