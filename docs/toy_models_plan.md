# Toy Models Plan

This document proposes three "Toy Models" to de-risk the theoretical framework and provide simplified, intuitive explanations for the "Metabolic Buckling" mechanism.

## Toy Model A: The 1D Metabolic Spring
**Objective:** Demonstrate that energy-limited stiffness leads to catastrophic collapse.
**Concept:** A simple spring $k$ whose stiffness depends on energy supply $E$.
**Dynamics:**
- $k(E) = k_0 \cdot \frac{E}{E + E_{cost}}$
- Load $F = mg$
- Deflection $x = F / k(E)$
- Energy cost $C(x) = \alpha \cdot x^2$ (cost to maintain position)
- Supply $E_{supply} = S - C(x)$
**Prediction:** As $F$ increases, $x$ increases, $C(x)$ rises, $E_{supply}$ drops, $k(E)$ falls $\rightarrow$ Runaway collapse (Buckling).
**Implementation:** `scripts/experiments/toy_model_metabolic_spring.py`

## Toy Model B: The "Buckling" Supply Chain
**Objective:** Model the lag between transport (supply) and growth rate (demand).
**Concept:** A 1D lattice of "cells" receiving nutrients via diffusion/transport.
**Dynamics:**
- **Demand:** Cells grow at rate $G$, consuming nutrients $N$.
- **Supply:** Nutrients diffuse from the base ($x=0$) with coefficient $D$.
- **Failure:** If $N < N_{crit}$ at tip ($x=L$), growth stops or becomes disordered.
**Prediction:** There exists a critical length $L_{crit} \propto \sqrt{D/G}$. If growth $G$ is too fast, the tip starves before the supply line can extend.
**Relevance:** Explains why rapid growth (high $G$) shrinks the stable length window.

## Toy Model C: The Anisotropic Filter
**Objective:** Test if high anisotropy actually filters high-frequency noise.
**Concept:** A chain of rigid links connected by springs.
**Dynamics:**
- **Input:** Noisy force $F(t) = F_0 + \eta(t)$.
- **Links:** Anisotropic (long, thin) vs Isotropic (spherical).
- **Measure:** Transmission of high-frequency components to the end of the chain.
**Prediction:** Anisotropic links (high rotational inertia) act as a low-pass filter, damping $\eta(t)$. Isotropic links transmit noise, causing "wobble".
**Relevance:** Explains why Vimentin/Piezo2 (high anisotropy) are needed for stability.
