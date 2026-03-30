# Simulation Report: Growth Sweep under Gravity

## What Changed
Swept `active_curvature` (representing biological growth gradient) from 0.0 to 30.0 under constant `gravity=9.81` and `anisotropy=3.0` with a small torsion drive (0.1).

## Emergent Shapes
As active curvature increased, the system initially accommodated the growth by forming a planar S-shape. However, beyond a critical threshold (around `active_curvature=22.0`), symmetry breaks and torsional coupling drives the spine into a 3D scoliotic shape (Max Cobb ~ 68.2 deg).

## Implications for Scoliosis vs Normal S-curve
The results strongly support the Biological Countercurvature hypothesis: normal growth yields a stable 2D S-curve up to a critical point. If growth exceeds the restorative capacity of tissue anisotropy, or if torsional defects are present, the planar curve transforms into a full 3D scoliotic deformity.

## Next Sweep Suggestion
Sweep `torsion_drive` at the critical active curvature threshold to map the exact boundary of 2D to 3D transition.
