# Linear Algebra Foundations

## Coordinate Transformations

Spacecraft simulations require frequent coordinate frame rotations.

### Direction Cosine Matrix (DCM)
Rotates a vector from the Inertial Frame ($I$) to the Spacecraft Frame ($S$):
$$r_S = C_{S/I} \cdot r_I$$

### Quaternion Rotation
Quaternions prevent gimbal lock. A rotation quaternion is defined as:
$$q = \begin{bmatrix} q_0 & q_1 & q_2 & q_3 \end{bmatrix}^T = \begin{bmatrix} \cos(\theta/2) & e_x\sin(\theta/2) & e_y\sin(\theta/2) & e_z\sin(\theta/2) \end{bmatrix}^T$$
Rotation of a vector $v$ is computed as:
$$v' = q \otimes v \otimes q^*$$
