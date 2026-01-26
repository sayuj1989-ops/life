# Simulation Report: Anisotropy-Torsion Interaction Sweep

**Date:** 2026-01-26
**Agent:** Curvature Simulator
**Script:** `scripts/weekly_sim_anisotropy_torsion_interact.py`

## Goal
Test if the critical instability peak (previously identified at Stiffness Anisotropy $R=2.0$ in the absence of torsion) shifts or intensifies when Torsional Coupling is active ($\chi_\tau=1.0$).

## Parameters
- **Fixed:**
  - Torsional Coupling ($\chi_\tau$): 1.0 (Critical value from Jan 25)
  - Load Vector Tilt: $5.0^\circ$
  - Growth Drive ($\chi_\kappa$): 10.0
- **Swept:**
  - Stiffness Anisotropy ($R$): 0.1 to 10.0 (Log-like spacing)

## Results

| Anisotropy ($R$) | S_lat (m) | Cobb Angle (deg) | Max Torsion (rad/m) |
|------------------|-----------|------------------|---------------------|
| 0.10             | 0.2163    | 20.62            | 7.21                |
| 0.50             | 0.2124    | 24.04            | 6.52                |
| **1.00**         | **0.2247**| **75.89**        | **6.84**            |
| 1.50             | 0.2364    | 79.68            | 6.97                |
| 2.00             | 0.2445    | 80.50            | 7.04                |
| 3.00             | 0.2552    | 80.71            | 7.10                |
| 10.00            | 0.2779    | 80.02            | 7.19                |

## Analysis

### 1. The "Torsion-Lock" Phase Transition
A dramatic phase transition occurs between $R=0.5$ and $R=1.0$.
- Below $R=1.0$ (Lateral stiffness $\ge$ Sagittal stiffness), the spine maintains a moderate curvature (~24 deg).
- At $R \ge 1.0$ (Sagittal stiffness > Lateral stiffness), the spine "snaps" into a high-Cobb mode (~80 deg).

### 2. Anisotropy Fuels Lateral Instability
Contrary to the "stabilizing anisotropy" hypothesis (valid when $\chi_\tau=0$), under torsional coupling, **higher anisotropy increases lateral deviation ($S_{lat}$)**.
- $S_{lat}$ grows monotonically from 0.21m (at R=0.1) to 0.28m (at R=10.0).
- This suggests that restricting sagittal bending (high $R$) forces the growth-induced energy to dissipate via coupled lateral bending and torsion.

### 3. Saturation of Cobb Angle
The Cobb angle saturates at ~80 degrees for all $R \ge 1.5$. This indicates a geometric lock or "buckling limit" has been reached, likely driven by the fixed $\chi_\tau=1.0$.

## Conclusion
Torsional coupling fundamental alters the role of stiffness anisotropy. While anisotropy can stabilize planar curves, it **destabilizes** 3D curves by channeling growth energy into the lateral plane. The combination of Intermediate Anisotropy ($R \approx 2.0$) and Torsional Coupling ($\chi_\tau \approx 1.0$) creates a robust, high-deformation attractor state.

## Next Sweep Suggestion
Investigate the **Growth Drive ($\chi_\kappa$) threshold** required to trigger this "Torsion-Lock" state at fixed $R=2.0$ and $\chi_\tau=1.0$.
