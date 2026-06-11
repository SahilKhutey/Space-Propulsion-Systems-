# Differential Equations & Numerical Solvers

## Astrodynamics and Orbit Propagation

The orbital state of a spacecraft is governed by Newton's laws:
$$\ddot{r} = -\frac{\mu}{r^3}r + a_{perturb}$$

### Runge-Kutta 4th Order (RK4)
Used for fast fixed-step propagation:
$$k_1 = f(t_n, y_n)$$
$$k_2 = f(t_n + \frac{h}{2}, y_n + h\frac{k_1}{2})$$
$$k_3 = f(t_n + \frac{h}{2}, y_n + h\frac{k_2}{2})$$
$$k_4 = f(t_n + h, y_n + h k_3)$$
$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

### Symplectic Integrators (Velocity Verlet)
Preserves energy (Hamiltonian phase space) over millions of orbits:
$$v_{n+1/2} = v_n + a_n \frac{\Delta t}{2}$$
$$r_{n+1} = r_n + v_{n+1/2} \Delta t$$
$$a_{n+1} = f(r_{n+1})$$
$$v_{n+1} = v_{n+1/2} + a_{n+1} \frac{\Delta t}{2}$$
