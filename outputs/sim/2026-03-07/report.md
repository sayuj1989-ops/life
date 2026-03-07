# Simulation Report: Torsion Drive Sweep under Moderate Growth

**Date:** 2026-03-07
**Sweep Name:** weekly-sim-torsion-stiffness

## What Changed
We swept the torsional coupling parameter (`torsion_drive`) linearly from 0.0 to 2.0 under a baseline condition of moderate active sagittal growth (`active_curvature = 10.0`) and moderate lateral stiffness protection (`anisotropy = 2.0`). This tests the hypothesis that symmetry-breaking torsion triggers scoliotic deformation only when an underlying energy deficit (from growth) exists, and examines how intermediate stiffness modulates this. The initial lateral defect was kept tiny (0.01).

## Emergent Shapes
The emergent shapes exhibit a highly nonlinear, resonant response to torsion:
- At `torsion_drive = 0.0`, the system shows a baseline planar lateral deformation (Cobb ~ 29°, S_lat ~ 0.25m).
- As torsion increases, we see regions of extreme 3D scoliotic buckling (e.g., Cobb ~ 90° at `torsion_drive = 0.57`, and Cobb ~ 87° at `torsion_drive = 1.71`).
- Notably, there are "valleys" of relative planar stability where Cobb angles plummet, yet lateral deviations (`S_lat`) peak (e.g., at `torsion_drive = 0.71`, Cobb is ~ 5° but `S_lat` reaches ~ 0.90m). This suggests the rod undergoes large sweeping planar or low-torsion curves without developing tight helical coils.

## How this Informs Scoliosis vs Normal S-Curve
This result underscores that isolated structural traits (like moderate anisotropy) cannot prevent scoliosis when rotational/torsional forces couple with active growth. The alternating peaks and valleys of Cobb angle vs. `S_lat` imply that certain combinations of torsion and growth resonate with the mechanical modes of the spine, transforming an initial S-curve instability into a fully 3D scoliotic spiral. This maps well to biological "vector mismatch" where mismatched planar cell polarity or rotational stresses bypass the stabilizing effect of ECM anisotropy.

## Next Sweep Suggestion
**Bivariate Torsion and Anisotropy Rescue Sweep:** To see if higher anisotropy (e.g., R=5.0 to 10.0) can "rescue" the spine from the resonant peaks observed here, sweeping both `torsion_drive` and `stiffness_anisotropy` simultaneously over a fine grid would clarify the phase boundary of stability.
