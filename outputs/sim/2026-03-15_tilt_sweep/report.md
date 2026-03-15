# Load Vector Tilt Sweep

**Date**: 2026-03-15

## Objective
To test whether an S-shaped spinal profile modeled dynamically as an emergent state breaks down or alters its characteristics when the direction of gravitational loading (the load vector tilt) is varied from 0° (vertical) to 90° (horizontal).

## What Changed
- Swept `tilt_deg` from 0.0 to 90.0 degrees.
- Implemented load vector tilting by rotating the rod's initial `base_direction` and `normal` relative to PyElastica's fixed default gravity vector `(0, 0, -9.81)`.
- Maintained constant active coupling `chi_kappa = 10.0` and calculated deviations in the local coordinate frame (longitudinal `Z`, sagittal `X`, lateral `Y`).

## What Emergent Shapes Occurred
- **Lateral Stability**: The rod maintained `max_dev_lateral_y = 0.0` across all tilts. The perturbation did not break symmetry into the lateral plane without a pre-existing lateral defect or torsional coupling (`chi_tau = 0.0`).
- **Sagittal Deviation**: The `max_dev_sagittal_x` (in-plane S-shape depth) increased monotonically from `~0.064 m` at 0° to `~0.171 m` at 90°.
- **Longitudinal Compression**: Tip deflection along the local longitudinal axis (`tip_z_local`) decreased in magnitude (became less compressed) from `-0.237 m` at 0° to `-0.142 m` at 90°, as the axial load diminished and bending moments increased.

## Interpretation: Scoliosis vs. Normal S-Curve
The simulation shows that pure off-axis loading amplifies the depth of the sagittal S-curve but does not inherently trigger 3D lateral scoliosis if perfect symmetry exists and torsional coupling is zero. This reinforces the Biological Counter-Curvature hypothesis that *torsional coupling* or *lateral asymmetric growth* must be present to drive 3D buckling; altered load tilt alone merely deepens the normal 2D curve.

## Next Sweep Suggestion
- Investigate Load Vector Tilt combined with a small lateral defect or Torsional Coupling (`chi_tau > 0`) to see if tilt accelerates the transition from 2D S-curve to 3D scoliosis.