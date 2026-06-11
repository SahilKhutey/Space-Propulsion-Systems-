# Orbital Mechanics

## Two-Body and N-Body Dynamics

### Vis-Viva Equation
Computes spacecraft orbital speed ($v$):
$$v^2 = \mu \left( \frac{2}{r} - \frac{1}{a} \right)$$

### Perturbations
- **J2 Earth Oblateness:**
  $$a_{J2} = -\frac{3}{2} J_2 \left( \frac{\mu R_E^2}{r^4} \right) \begin{bmatrix} (1 - 5\sin^2(i)\sin^2(u)) \frac{x}{r} \\ (1 - 5\sin^2(i)\sin^2(u)) \frac{y}{r} \\ (3 - 5\sin^2(i)\sin^2(u)) \frac{z}{r} \end{bmatrix}$$
- **Atmospheric Drag:**
  $$a_{drag} = -\frac{1}{2} C_d \frac{A}{m} \rho v_{rel}^2 \hat{v}_{rel}$$
