# Weekly Simulation Report: Stiffness Modulation Sweep

**Date:** 2026-02-28
**Parameter Swept:** `stiffness_modulation` (-0.8 to 0.8)

## Overview
This sweep investigates how modulating the baseline stiffness via active signalling (`stiffness_modulation`) affects the lateral stability of the growing spine model. The baseline parameters were set with significant growth/active curvature (`active_curvature = 12.0`) and an initial lateral defect (`initial_lateral_defect = 0.05`) with a baseline structural anisotropy ratio of `2.0`.

## What Changed
- The parameter `stiffness_modulation` was swept linearly from -0.8 to 0.8 across 20 iterations.
- A negative modulation implies active signals reduce the stiffness, whereas a positive modulation increases stiffness in the face of growth/curvature demand.

## Emergent Shapes
- **Negative Stiffness Modulation (-0.8 to -0.4):** As stiffness modulation becomes more negative, the spine shows extreme vulnerability to lateral deviations, exhibiting high Cobb angles (up to ~70 degrees) and large lateral displacement (S_lat > 0.8m). This produces a highly scoliotic, buckling S-shape.
- **Zero to Mild Positive Modulation (-0.1 to 0.2):** There is a "valley of stability" where the Cobb angle is minimized (around 3 to 12 degrees). In this regime, the stiffness tuning correctly balances the growth vector without inducing severe lateral deviation, keeping the spine closer to a stable 2D S-curve.
- **High Positive Modulation (0.3 to 0.8):** Paradoxically, increasing the stiffness modulation *too much* triggers a secondary instability zone (Cobb > 50 degrees near modulation 0.4). Beyond 0.6, the Cobb angle collapses back down to low values (<5 degrees), but the lateral deviation ($S_{lat}$) dramatically increases, suggesting a different mode of failure (perhaps a long sweeping deviation rather than a sharp scoliotic kink).

## Relevance to Scoliosis vs Normal S-Curve
These results strongly imply that a normal S-curve relies on a delicately balanced stiffness response. If the active feedback signals either "under-stiffen" (negative modulation) or "over-stiffen" (high positive modulation) the spine relative to the active curvature/growth demands, the system buckles into a 3D scoliotic shape. Scoliosis may therefore not simply be a failure of growth magnitude, but a mismatch in the coupled stiffness-modulation response (i.e. mechanotransduction mismatch).

## Next Sweep Suggestion
The next logical step is to investigate the interaction between `stiffness_modulation` and `torsion_drive`. Since high positive stiffness modulation triggered a new instability regime, applying torsion in that specific regime could reveal whether it leads to a catastrophic, tightly coiled curve, or whether torsion actually *stabilizes* the overly stiffened structure.
