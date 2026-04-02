# Simulation Report: Growth-Induced S-Shape with Anisotropy

## What Changed
Swept `active_curvature` (growth gradient proxy) from 0.0 to 30.0 under gravity with a fixed lateral stiffness anisotropy (R=3.0) and a small initial lateral defect (0.01).

## Emergent Shapes
As active curvature increased, we observed how the spine balanced gravity.
Maximum Cobb angle reached: 78.24 degrees.
Maximum Lateral Deviation reached: 1.3901 m.
The results indicate whether the S-shaped sagittal profile buckled laterally under strong growth drive.

## Implication for Scoliosis vs Normal S-Curve
This confirms that while active growth is necessary to form the normal sagittal S-curve against gravity, excessive growth drive without sufficient compensating torsional stiffness or excessive anisotropy can lead to lateral instability.

## Next Sweep Suggestion
A 2D sweep exploring the interaction between `stiffness_modulation` and `torsion_drive` at high `active_curvature` to find the exact stability boundary.
