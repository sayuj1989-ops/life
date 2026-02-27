# Toy Models Plan

**Purpose:** To de-risk the complex Cosserat simulation and provide intuitive validation for "Metabolic Buckling" and "Active Countercurvature".

**Status:** ✅ Completed (2026-05-25)

## Toy Model A: 1D Thermostatic Column (Thermodynamic)

**Goal:** Demonstrate the "Energy Deficit Bifurcation" in a minimal system without complex geometry.

**Setup:**
- Consider a 1D column of height $L$.
- **Active Curvature Cost:** $C(L) \propto \chi_\kappa^2 L^3$ (Volume $\times$ Curvature Energy).
- **Metabolic Supply:** $S(L) \propto L^2$ (Surface Area / Flux Limit).
- **Deficit:** $D(L) = C(L) - S(L)$.

**Analysis:**
- Plot $D(L)$ vs $L$.
- Identify critical length $L_{crit}$ where $D(L) > 0$.
- Show that for $L < L_{crit}$, the column is stable (Surplus). For $L > L_{crit}$, it is unstable (Deficit).

**Implementation:**
- Script: `scripts/experiments/toy_model_thermostatic.py`
- **Output:** [`outputs/figures/toy_model_thermostatic.png`](../outputs/figures/toy_model_thermostatic.png)
- **Status:** ✅ **Implemented**

## Toy Model B: The "Active" Elastica (Mechanical)

**Goal:** Validate that *intrinsic curvature* can stabilize a column against gravity *without* infinite stiffness. Specifically, link Protein Anisotropy to $L_{crit}$.

**Setup:**
- Equations derived in `docs/theory/toy_model_anisotropy.md`.
- $L_{crit} \propto A^{-0.5}$ (Inverse square root of anisotropy).

**Simulations:**
1.  **Passive:** $\chi_\kappa = 0$. Show buckling under self-weight for large $L$.
2.  **Active:** $\chi_\kappa > 0$. Show stability for the same $L$.

**Implementation:**
- Script: `scripts/toy_model_anisotropy_link.py`
- **Output:** [`outputs/figures/toy_model_anisotropy_bifurcation.png`](../outputs/figures/toy_model_anisotropy_bifurcation.png)
- **Status:** ✅ **Implemented**

## Schedule

| Model | Owner | Effort | Status |
| :--- | :--- | :--- | :--- |
| **Toy A** | PI/Theory | 0.5 day | ✅ **Completed** |
| **Toy B** | Comp Bio | 1 day | ✅ **Completed** |
