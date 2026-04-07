# Weekly Simulation: Anisotropy Sweep under Off-Axis Load

## Experiment Overview
Sweeping `stiffness_anisotropy` to observe how directional stiffness constraints rescue the spine from an off-axis gravitational load (mimicked via initial lateral defect) combined with active sagittal growth.

## Changes
- Parameter family swept: `stiffness_anisotropy`
- 15 runs from 1.0 to 10.0
- Fixed active growth (`chi_kappa` = 10.0) and lateral defect (0.05)

## Emergent Shapes
Varying anisotropy reveals a transition in structural stability. Low anisotropy permits large lateral deviations (Cobb peaking ~87.1 deg), while high anisotropy constrains the S-shape primarily to the sagittal plane (Cobb reduced to ~3.7 deg).

## Relevance to Scoliosis
Normal S-curves require high dorso-ventral compliance but lateral rigidity (high anisotropy). A loss of this anisotropy (e.g., fibrillin microfibril defects) under active growth and slight off-axis loads triggers buckling into a 3D scoliotic profile.

## Next Sweep Suggestion
Perform a 2D parameter sweep of `stiffness_anisotropy` vs `torsion_drive` under tilt to map the complete transition boundary.
