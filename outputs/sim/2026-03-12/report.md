# Simulation Report: Active Curvature Sweep (Constant Anisotropy)

**Date:** 2026-03-12
**Sweep:** `weekly-sim-active-curvature-sweep`

## What Changed
Swept `active_curvature` (growth drive) from 0.0 to 15.0 in 15 steps.
Held `anisotropy` constant at 3.0 to isolate the effect of growth.
`torsion_drive` and `initial_lateral_defect` were both 0.0, ensuring the test evaluated planar sagittal dynamics without explicit symmetry-breaking seeds.

## What Emergent Shapes Occurred
- At `active_curvature = 0`, the spine settled into a naturally lordotic/kyphotic shape under gravity, with an end-to-end distance of `~0.395m`.
- As `active_curvature` increased, the spine significantly contracted and curled further into the sagittal plane, reducing the end-to-end distance to `~0.117m` at `active_curvature = 15.0`.
- The tip z-position (`z_tip`) inverted into negative values around `active_curvature = 12.0`, indicating extreme forward/backward curling.
- **Importantly**, `S_lat` and `cobb_angle` remained precisely `0.0` throughout the entire sweep. No 3D lateral buckling (scoliosis) emerged.

## How This Informs Scoliosis vs Normal S-Curve
- **Strong Sagittal Control:** Under a moderate anisotropy (R=3.0) and zero torsional drive, excessive sagittal growth simply deepens the 2D "S-curve" (hyper-kyphosis/hyper-lordosis) rather than spontaneously breaking symmetry into lateral scoliosis.
- **Symmetry Breaking Required:** This result confirms that while growth is a necessary driving force (creating the "Energy Deficit Window" and high internal strain), planar growth alone in a perfectly symmetric model is insufficient to trigger scoliosis. A symmetry-breaking mechanism—such as a non-zero `torsion_drive`, `initial_lateral_defect`, or tilted gravity—is required to push the system out of the sagittal plane and into 3D collapse.
- In biology, perfect symmetry does not exist. The heart and viscera create natural asymmetries (tilted load vectors or small lateral defects), and torsional coupling often arises. This simulation highlights the difference between pure developmental growth (the energetic driver) and the structural triggers (the symmetry breakers) that cause the scoliotic bifurcation.

## Next Sweep Suggestion
- **Sweep Name:** `weekly-sim-active-curvature-with-torsion`
- **Parameter:** Sweep `active_curvature` exactly as done here (0.0 to 15.0), but set `torsion_drive = 0.5`.
- **Rationale:** To prove that once a small symmetry-breaking torsional coupling is present, the same increase in `active_curvature` will rapidly trigger lateral buckling and non-zero Cobb angles.