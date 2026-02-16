# Domain Knowledge Reference

Quick reference for theoretical concepts in biophysics and mathematical modeling.

## Cosserat Rod Theory

### Overview

Models a slender structure as a continuous curve with position $\mathbf{r}(s,t)$ and orientation frame $\{\mathbf{d}_1, \mathbf{d}_2, \mathbf{d}_3\}$.

### Configuration Variables

- **Strain**: $v = \partial\mathbf{r}/\partial s \cdot \mathbf{d}_3$
- **Curvature vector**: $\boldsymbol{\kappa} = (\kappa_1, \kappa_2, \omega)$
  - $\kappa_1$: bending in plane 1
  - $\kappa_2$: bending in plane 2  
  - $\omega$: twist (axial rotation)

### Elastic Energy

$$
U = \frac{1}{2}\int_0^L [B_1\kappa_1^2 + B_2\kappa_2^2 + C\omega^2] \, ds
$$

where $B_i$ are bending stiffnesses, $C$ is torsional stiffness.

### Applications

- Spinal column modeling
- DNA mechanics
- Soft robotics
- Growing biological structures

## Control Theory with Delay

### Standard Feedback Control

$$
u(t) = -K \, e(t)
$$
where $e(t) = x(t) - x_{target}$ is the error.

### Delayed Feedback

$$
u(t) = -K \, e(t - \tau)
$$
where $\tau$ is the feedback delay.

### Stability Criterion

System becomes unstable when:
$$
K \cdot \tau \cdot \omega_0 > \frac{\pi}{2}
$$
where $\omega_0$ is the natural frequency.

### Biological Applications

- Neural feedback loops (proprioception)
- Hormonal regulation
- Immune response
- Developmental timing

## AdS/CFT Correspondence

### Basic Concept

Anti-de Sitter / Conformal Field Theory correspondence: duality between:

- **Bulk**: $(d+1)$-dimensional gravitational theory in AdS space
- **Boundary**: $d$-dimensional quantum field theory

### Holographic Principle

Information in the bulk can be encoded on the boundary:
$$
Z_{bulk}[g_{\mu\nu}] = \langle e^{i S_{CFT}[\mathcal{O}]} \rangle_{boundary}
$$

### Biological Interpretation

- **3D organism shape** (bulk) ↔ **2D epithelial/cortical patterns** (boundary)
- Morphogenesis as holographic reconstruction
- Developmental defects as boundary-bulk mismatch

### Key Result

Bulk geometry $G_{\mu\nu}^{bulk}$ determined by boundary correlation functions.

## General Relativity Applications

### Proper Acceleration

Acceleration required to maintain position at height $h$:
$$
a = \frac{GM}{r^2\sqrt{1-\frac{2GM}{c^2r}}} \approx g
$$

### Geodesic Equation

$$
\frac{d^2x^\mu}{d\tau^2} + \Gamma^\mu_{\rho\sigma}\frac{dx^\rho}{d\tau}\frac{dx^\sigma}{d\tau} = 0
$$

### Biological Countercurvature

Effective metric modification:
$$
g_{\mu\nu}^{eff} = g_{\mu\nu}^{Schwarzschild} + \delta g_{\mu\nu}^{bio}
$$

where $\delta g_{\mu\nu}^{bio}$ represents metabolic stress-energy contribution.

## Standard Notation Conventions

### Greek vs Latin Indices

- **Greek** ($\mu, \nu, \rho, \sigma$): Spacetime indices (0,1,2,3)
- **Latin** ($i, j, k$): Spatial indices (1,2,3)

### Common Symbols

- $\hbar$: Reduced Planck constant
- $k_B$: Boltzmann constant
- $c$: Speed of light
- $G$: Gravitational constant
- $\nabla$: Gradient operator
- $\partial_\mu$: Partial derivative $\partial/\partial x^\mu$

### Tensor Notation

- $T^{\mu\nu}$: Contravariant tensor
- $T_{\mu\nu}$: Covariant tensor
- $T^\mu_{\,\,\nu}$: Mixed tensor
- $\delta^\mu_\nu$: Kronecker delta
- $\epsilon_{\mu\nu\rho\sigma}$: Levi-Civita symbol

## Biomechanics

### Buckling Load (Euler)

Critical load for column buckling:
$$
P_{cr} = \frac{\pi^2 EI}{(KL)^2}
$$

- $E$: Young's modulus
- $I$: Second moment of area
- $K$: End condition factor
- $L$: Column length

### Growth Kinematics

Material point velocity in growing structure:
$$
\frac{D\mathbf{r}}{Dt} = \frac{\partial\mathbf{r}}{\partial t} + \frac{\dot{L}}{L}s\frac{\partial\mathbf{r}}{\partial s}
$$

where $\dot{L}$ is growth rate.

### Stress-Strain Relationships

- **Hooke's Law**: $\sigma = E\epsilon$
- **Viscoelastic**: $\sigma(t) = \int_0^t E(t-t')\dot{\epsilon}(t')dt'$
- **Hyperelastic**: $\sigma = \frac{\partial W}{\partial \epsilon}$ where $W$ is strain energy

## Useful Identities

### Vector Calculus

$$
\nabla \times (\nabla \phi) = 0
$$
$$
\nabla \cdot (\nabla \times \mathbf{A}) = 0
$$

### Differential Geometry

- Frenet-Serret formulas for space curves
- Gauss-Codazzi equations for surfaces
- Riemann curvature tensor

### Special Functions

- Bessel functions: $J_n(x)$, $Y_n(x)$
- Legendre polynomials: $P_n(x)$
- Error function: $\text{erf}(x)$

## Software Tools

### Numerical Simulations

- **PyElastica**: Cosserat rod simulations
- **FEniCS**: Finite element analysis
- **LAMMPS**: Molecular dynamics

### Visualization

- **matplotlib**: 2D plotting
- **Mayavi**: 3D visualization
- **Blender**: 3D rendering

### Symbolic Math

- **SymPy**: Python symbolic mathematics
- **Mathematica**: Symbolic computation
- **Maple**: Computer algebra system
