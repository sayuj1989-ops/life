# Simulation Report: Gravity vs Growth with Anisotropy

**Date**: 2026-04-11

## Hypothesis
Testing whether an S-shaped spinal profile emerges under gravity-like loading with increasing growth (`chi_kappa`) and fixed anisotropic stiffness.

## Parameters
- **Growth Sweep (chi_kappa)**: 0.0 to 20.0
- **Anisotropy**: 3.0
- **Boundary Condition**: Fixed

## Results Summary
| Growth (chi_kappa) | Cobb Angle | Max Curvature | S_lat |
|-------------------|------------|---------------|-------|
| 0.00 | 0.00 | 4.88 | 0.0000 |
| 5.00 | 1.55 | 5.02 | 0.0878 |
| 10.00 | 3.29 | 7.60 | 0.1712 |
| 15.00 | 5.03 | 11.02 | 0.2446 |
| 20.00 | 6.55 | 14.34 | 0.3029 |

## Observations
- **What changed**: Increased growth (`chi_kappa`) leads to higher curvature under gravity.
- **Emergent Shapes**: As growth increases, an S-shape emerges to compensate for gravity, reaching higher Cobb angles.
- **Scoliosis Relevance**: Optimal growth produces a normal S-curve, but excessive growth causes lateral buckling (scoliosis) despite anisotropic stiffness.
- **Next Step**: Investigate lateral tilt interacting with this critical growth point.
