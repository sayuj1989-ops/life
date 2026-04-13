# Multi-segment Cosserat Rod Modeling of Lenke Curve Types

## Abstract
This document formalizes the theoretical derivation extending the single-link inverted pendulum model to a multi-segment Cosserat rod to predict Lenke curve types (1-6) via a spatially varying generalized eigenvalue problem.

## 1. Introduction
The DDE model for Biological Countercurvature treats the spine as a single-link inverted pendulum, capturing the onset of instability at the Hopf bifurcation. However, it does not explain the distinct Lenke curve types. By modeling the spine as a multi-segment Cosserat rod, regional variations in stiffness, damping, and proprioceptive delay can be integrated to explain the spatial patterning of these curve types.

## 2. Generalized Eigenvalue Problem
The buckling of the multi-segment Cosserat rod can be formulated as a generalized eigenvalue problem:

$$ (B(s) \mathbf{y}'')'' = \lambda Q(s) \mathbf{y} $$

Where:
- $B(s) = E I(s)$ is the spatially varying bending stiffness.
- $Q(s)$ is the effective destabilizing drive (instability parameter), which depends on proprioceptive delay $\tau(s)$, damping $b(s)$, and asymmetric loading $F_{asym}$.
- $\mathbf{y}(s)$ is the lateral deviation at arc length $s$.
- $\lambda$ is the eigenvalue associated with the buckling mode.

## 3. Regional Parameter Variations
The spine is not uniform. The variations in $B(s)$ and $Q(s)$ are as follows:

1.  **Stiffness $B(s)$:**
    *   **Thoracic:** Increased stiffness due to rib cage buttressing.
    *   **Lumbar:** Increased structural bulk due to lordosis.
    *   **Thoracolumbar Junction:** Decreased stiffness (vulnerability zone).

2.  **Instability Drive $Q(s)$:**
    *   Modulated by regional variations in mechanoreceptor density (affecting $\tau$), paraspinal muscle mass (affecting damping $b$), and asymmetric loads.

## 4. Derivation of Lenke Types
By modulating $B(s)$ and $Q(s)$ according to regional physiological parameters, the generalized eigenvalue problem yields dominant eigenmodes corresponding to the six Lenke types:

*   **Type 1 (Main Thoracic):** Dominant instability in the thoracic region.
*   **Type 2 (Double Thoracic):** Instability in both proximal and main thoracic regions.
*   **Type 3 (Double Major):** Simultaneous instability in thoracic and lumbar regions.
*   **Type 4 (Triple Major):** Instability spanning proximal thoracic, main thoracic, and lumbar regions.
*   **Type 5 (Thoracolumbar/Lumbar):** Dominant instability at the thoracolumbar junction and lumbar spine.
*   **Type 6 (Thoracolumbar/Lumbar-Main Thoracic):** Lumbar instability exceeding thoracic instability.

## 5. Conclusion
The multi-segment Cosserat rod model successfully maps the global instability trigger of the biological countercurvature framework to specific spatial curve morphologies, explaining the clinical diversity of Lenke curve types in AIS.
