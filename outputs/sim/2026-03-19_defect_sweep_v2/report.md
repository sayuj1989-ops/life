# Simulation Report: Lateral Defect Sweep V2

**Date:** $(date +%Y-%m-%d)

## What Changed
We performed a controlled parameter sweep over the `initial_lateral_defect` (ranging from 0.0 to 0.15) to simulate a structural asymmetry or congenital anomaly. The simulation maintained a constant strong sagittal growth drive (`active_curvature = 12.0`) and moderate lateral stiffness (`anisotropy = 3.0`) using the CounterCurvatureRodSystem.

## What Emergent Shapes Occurred
*   At `defect = 0.0`, the system remained stable with no scoliosis (`S_lat = 0`, `Cobb = 0`).
*   Even minimal defects (`0.007`) triggered sudden lateral buckling (`S_lat ~ 0.16`, `Cobb ~ 15.8 deg`).
*   Interestingly, there was a small stabilizing pocket around `defect ~ 0.015-0.03` where the Cobb angle remained remarkably low (<10 deg), before rising non-linearly.
*   As the defect increased beyond `0.05`, the structure entered a progressive, roughly linear deterioration of its coronal profile, culminating in severe scoliosis (`S_lat > 0.3`, `Cobb > 28 deg`).

## How This Informs Scoliosis vs Normal S-Curve
This result confirms that while proper sagittal active curvature and anisotropy normally interact to produce a stable, physiological S-curve, the presence of even small initial coronal asymmetries can act as critical "seeds" for instability. The strong sagittal drive (energy deficit) amplifies these minor lateral defects into full-blown 3D scoliotic deformities, overcoming the protective anisotropic stiffness.

## Next Sweep Suggestion
Perform a 2D parameter sweep combining `initial_lateral_defect` and `stiffness_modulation` (blockiness) to see if variations in vertebral stiffness can rescue the spine from pre-existing lateral structural defects.
