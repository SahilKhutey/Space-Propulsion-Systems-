# Simulation Architecture

## Real-Time Engine

```
┌──────────────┐
│ SpacecraftState│ <── Single source of truth
└──────┬───────┘
       │
  ┌────┴────┐
  ▼         ▼
┌───────┐ ┌─────────┐
│ Orbit │ │ Thermal │
│ Loop  │ │ Loop    │
└───┬───┘ └────┬────┘
    │          │
    └────┬─────┘
         ▼
  ┌──────────────┐
  │   Mission    │ <── Master loop @ 1 Hz
  │   Loop       │
  └──────┬───────┘
         ▼
  ┌──────────────┐
  │  Projection  │
  │  Engine      │
  └──────────────┘
```

## Solver Selection

| Subsystem | Solver | Method |
|-----------|--------|--------|
| Orbit | RK4 (fixed) | Velocity Verlet (symplectic) |
| Orbit (high precision) | RK45 | Dormand-Prince adaptive |
| Orbit (long duration) | Gauss-Jackson | Multistep predictor-corrector |
| Thermal | RK4 | Lumped parameter |
| Power | Forward Euler | Energy balance |
| Mission | Subordinate | Composes other loops |

## State Vector

The system state vector $X$ is defined as:
```python
X = [
    pos_x, pos_y, pos_z,       # position (m)
    vel_x, vel_y, vel_z,       # velocity (m/s)
    mass,                      # total mass (kg)
    propellant_mass,           # remaining fuel (kg)
    q0, q1, q2, q3,            # attitude quaternion
    omega_x, omega_y, omega_z, # angular velocity (rad/s)
    temp_1, ..., temp_8,       # thermal node temperatures (K)
    battery_charge,            # battery state of charge (Wh)
    solar_power_in,            # solar array input (W)
    payload_power_out          # spacecraft power load (W)
]
```
