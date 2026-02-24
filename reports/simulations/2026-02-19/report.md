# Weekly Simulation Report: Anisotropy Rescue Sweep

**Date:** 2026-02-19
**Sweep Name:** weekly-sim-anisotropy-rescue
**Script:** `scripts/experiments/weekly_sim_anisotropy_rescue.py`

## Goal
To test if increasing **Stiffness Anisotropy** (from 1.0 to 10.0) can suppress the S-shaped instability (lateral buckling) that was hypothesized to emerge under high **Active Curvature** growth conditions (`active_curvature = 3.0`, corresponding to `chi_kappa = 15.0`).

## Setup
- **Model:** Cosserat Rod with Information-Elasticity Coupling (IEC).
- **Sweep Parameter:** Stiffness Anisotropy (Ratio of Lateral to Sagittal Bending Stiffness, 1.0 - 10.0).
- **Fixed Parameters:**
  - `active_curvature`: 3.0 (`chi_kappa` ~ 15.0) - A high growth drive.
  - `gravity`: 9.81 m/s^2.
  - `boundary_condition`: Fixed base.
  - `initial_lateral_defect`: 0.01 (small perturbation).
  - `torsion_drive`: 0.0 (`chi_tau` = 0).

## Results

### Key Findings
1.  **Stability Maintained:** Across the entire range of anisotropy (1.0 to 10.0), the rod remained stable.
2.  **No Lateral Buckling:** The maximum Lateral Deviation (`S_lat`) was consistently **0.00**. No S-shaped profile emerged.
3.  **Negligible Cobb Angle:** The maximum Cobb angle was extremely low (0.04° to 0.17°), indicating the rod remained effectively straight in the coronal plane.
4.  **Sagittal Curvature:** The rod exhibited the expected sagittal kyphosis due to the active curvature drive, but this did not translate into lateral instability.

### Quantitative Summary
| Anisotropy | Cobb Angle (deg) | S_lat (Index) | Outcome |
|:----------:|:----------------:|:-------------:|:-------:|
| 1.00       | 0.04             | 0.00          | Stable  |
| 3.37       | 0.13             | 0.00          | Stable  |
| 5.74       | 0.15             | 0.00          | Stable  |
| 10.00      | 0.17             | 0.00          | Stable  |

*(Full data in `results.csv`)*

## Interpretation
The hypothesis that "high growth triggers lateral instability" was **not supported** under these specific conditions (pure planar curvature drive without torsion).

This suggests that the "S-shaped instability" observed in prior simulations likely requires:
1.  **Torsional Coupling (`chi_tau`):** As seen in `weekly-sim-torsion`, twisting forces are likely the primary driver for breaking planar symmetry and inducing 3D scoliosis.
2.  **Active Moments (`chi_M`):** Direct torque application might be more destabilizing than curvature modulation.
3.  **Lower Critical Stiffness:** The rod might be too stiff relative to the growth drive to buckle.

## Conclusion & Next Steps
- **Conclusion:** Increasing stiffness anisotropy had no "rescue" effect because the baseline isotropic rod (Anisotropy=1.0) was already stable under this specific growth load. The system is robust to pure planar growth drive.
- **Next Sweep Suggestion:** Re-introduce **Torsional Coupling (`chi_tau`)** at a known unstable level (e.g., `chi_tau = 1.0`) and *then* sweep Anisotropy to see if it can rescue the spine from *that* instability.

## Artifacts
- [Results CSV](./results.csv)
- [Params CSV](./params.csv)
- [Plot](./plot_anisotropy_rescue.png)
