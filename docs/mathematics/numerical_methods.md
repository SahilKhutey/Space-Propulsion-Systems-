# Numerical Methods

## Root-Finding and Equation Solvers

Used to compute thruster mass flow rates, orbital anomalies, and thermal equilibrium temperatures.

### Kepler's Equation Solver
Solving for Eccentric Anomaly ($E$) given Mean Anomaly ($M$) and eccentricity ($e$):
$$f(E) = E - e\sin(E) - M = 0$$
Using Newton-Raphson iteration:
$$E_{k+1} = E_k - \frac{E_k - e\sin(E_k) - M}{1 - e\cos(E_k)}$$
