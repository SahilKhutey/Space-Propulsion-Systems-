# Optimization Algorithms

## Trajectory and Thruster Optimization

### Multi-Objective Optimization
Optimizing propellant mass fraction ($m_f/m_0$) vs. time of flight ($t_f$):
$$\min \mathcal{J} = \omega_1 \left( \frac{m_f}{m_0} \right) + \omega_2 t_f$$

### Genetic Algorithms (GA)
Used for deep space launch window searches. Selects, mutates, and crosses over orbital parameters.

### Physics-Informed Neural Networks (PINN)
Approximates complex orbital perturbation fields directly within the solver loop:
$$\mathcal{L}_{PINN} = \mathcal{L}_{data} + \lambda \mathcal{L}_{physics}$$
