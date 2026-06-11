import numpy as np
from core.constants.constants import G, M_EARTH, R_EARTH
from ..state.state_manager import StateManager

class OrbitLoop:
    def __init__(self, state_manager: StateManager, dt: float = 1.0, include_j2: bool = True):
        self.sm = state_manager
        self.dt = dt
        self.mu = G * M_EARTH
        self.R_body = R_EARTH
        self.J2 = 1.08263e-3 if include_j2 else 0.0

    def step(self):
        st = self.sm.spacecraft.state
        r = st.position
        v = st.velocity
        r_mag = np.linalg.norm(r)
        if r_mag < 1e-6:
            return

        a = -self.mu * r / r_mag**3
        if self.J2 > 0:
            z = r[2]
            factor = 1.5 * self.J2 * self.mu * self.R_body**2 / r_mag**5
            a += factor * np.array([
                r[0] * (5 * (z/r_mag)**2 - 1),
                r[1] * (5 * (z/r_mag)**2 - 1),
                r[2] * (5 * (z/r_mag)**2 - 3),
            ])

        # Symplectic Velocity Verlet
        v_half = v + 0.5 * a * self.dt
        r_new = r + v_half * self.dt
        r_new_mag = np.linalg.norm(r_new)
        a_new = -self.mu * r_new / r_new_mag**3
        v_new = v_half + 0.5 * a_new * self.dt

        st.position = r_new
        st.velocity = v_new
