# Toy Models Plan

**Purpose:** To de-risk the complex Cosserat simulation and provide intuitive validation for "Metabolic Buckling" and "Active Countercurvature".

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
- Simple Python script or even a spreadsheet.
- **Output:** Plot of Energy Deficit vs Length.

## Toy Model B: The "Active" Elastica (Mechanical)

**Goal:** Validate that *intrinsic curvature* can stabilize a column against gravity *without* infinite stiffness.

**Setup:**
- Use `scipy.integrate.solve_bvp`.
- Equation: $EI \theta'' + P \sin(\theta) = M_{active}'$.
- $M_{active} = EI \cdot \kappa_{active}$.
- $\kappa_{active}(s) = \chi_\kappa \cdot \nabla I(s)$.

**Simulations:**
1.  **Passive:** $\chi_\kappa = 0$. Show buckling under self-weight for large $L$.
2.  **Active:** $\chi_\kappa > 0$. Show stability for the same $L$.
3.  **Perturbation:** Add small lateral force. Show Active recovers, Passive collapses.

**Implementation:**
- Python script using `scipy`.
- **Output:** Comparison plot of deflection $\delta$ vs Load $P$ (or Length $L$) for Passive vs Active.

## Schedule

| Model | Owner | Effort | Status |
| :--- | :--- | :--- | :--- |
| **Toy A** | PI/Theory | 0.5 day | ⚪ **Planned** |
| **Toy B** | Comp Bio | 1 day | ⚪ **Planned** |
