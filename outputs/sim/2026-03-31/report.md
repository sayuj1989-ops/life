# Weekly Sim: Anisotropy Torsion Rescue Sweep

## What Changed
Swept stiffness anisotropy from 0.5 to 3.5 under a constant active curvature (growth = 0.5) and torsion drive (0.1).
Config and random seed were explicitly set and saved. Simulation generates stable, reproducible results.

## What Emergent Shapes Occurred
- Reduced forcing parameters yielded a stable structural response mapping.
- As lateral stiffness anisotropy (A) increases, the lateral deviation ($S_{lat}$) and Cobb Angle are progressively suppressed.
- Lower anisotropy values ($A < 1.0$) allow the torsion to manifest as a higher-magnitude lateral scoliotic curve.

## How this informs scoliosis vs normal S-curve
This provides direct evidence for the "anisotropy rescue" hypothesis. Torsion acting on a growing spine causes severe scoliosis only when lateral stiffness (anisotropy) is too low relative to sagittal stiffness. Normal high-anisotropy development suppresses this out-of-plane buckling, maintaining the normal 2D S-curve.

## Next Sweep Suggestion
Sweep `active_curvature` (growth magnitude) against `torsion_drive` at a fixed critical anisotropy (e.g., A=1.5) to map the phase space of growth-induced instability.
