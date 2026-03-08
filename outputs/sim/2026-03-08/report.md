# Weekly Simulation Report: Growth S-Shape Emergence

**Date:** 2026-03-08
**Sweep Name:** weekly-sim: growth-s-shape-emergence
**Parameter Swept:** `active_curvature` (mapped to `chi_kappa`) from 0 to 15.
**Fixed Parameter:** `anisotropy` = 3.0 (high lateral stiffness)

## What Changed
In this parameter sweep, we scaled up the active sagittal growth (`active_curvature`) from 0 to 15 while holding lateral stiffness anisotropy constant at a relatively high value (`anisotropy = 3.0`) and applying normal gravity. This tests whether simply driving sagittal curvature against gravity with a strong lateral "vector chain" can induce stable S-shaped sagittal profiles without collapsing into 3D scoliosis.

## Emergent Shapes
* **0-1.6:** At baseline/low growth, the spine is relatively compressed but maintains a typical minor curve.
* **1.6-6.6:** Strong S-shaped sagittal profiles begin to emerge and compress down. The vertical tip (`z_tip`) dips negative due to looping/curling.
* **10.0-15.0:** Extreme active curvature results in very tight curling in the sagittal plane (maximum curvature reaches >150). However, the Cobb angle remains exactly 0.0 across all tests.
* The high lateral stiffness (`anisotropy = 3.0`) perfectly suppresses any lateral buckling, meaning all deformation is constrained to the 2D sagittal plane.

## Implications for Scoliosis vs. Normal S-Curve
This result confirms a key aspect of the Biological Counter-Curvature hypothesis: under sufficient lateral stiffness (a strong "vector chain"), massive active growth drives the spine into an S-curve (or deeper curling) in the sagittal plane *without* causing scoliosis. The instability is purely sagittal. It implies that for true 3D scoliosis to occur, there must be either a failure of lateral stiffness (low anisotropy), a symmetry-breaking initial defect, or an active torsion component.

## Next Sweep Suggestion
Combine this high active growth (`active_curvature ~ 10.0`) with a sweep of `torsion_drive` (`chi_tau`). We need to observe if the addition of active torsion causes this tightly wound 2D sagittal curve to violently buckle out-of-plane into a true 3D scoliotic deformity.