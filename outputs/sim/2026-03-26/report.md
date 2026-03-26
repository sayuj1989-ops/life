# Simulation Report: Active Curvature (Growth) Sweep

**Date**: 2026-03-26
**Sweep Parameter**: `active_curvature`

## What Changed
Swept `active_curvature` from 5.0 to 25.0 under moderate anisotropy (R=3.0), constant lateral defect (0.05), and moderate torsion (0.5).

## Emergent Shapes
The model tests whether an S-shaped spinal profile emerges under gravity-like loading with growth and anisotropic stiffness. At lower active curvatures, the spine remains relatively stable with smaller Cobb angles and lateral deviations. As active curvature increases, simulating a growth spurt, lateral deviation and Cobb angles increase significantly.

## Scoliosis vs Normal S-curve
The results show the bifurcation between a normal S-curve and scoliosis. With higher active curvature representing accelerated spinal growth (growth spurt), the normal S-curve loses stability under gravity and torsional loads and buckels into a 3D scoliotic deformity. The constant moderate anisotropy provides some structural protection but is overwhelmed beyond a certain active curvature threshold.

## Next Sweep Suggestion
Sweep `torsion_drive` at the identified critical active curvature threshold to examine how torsional coupling specifically interacts with the buckling instability.
