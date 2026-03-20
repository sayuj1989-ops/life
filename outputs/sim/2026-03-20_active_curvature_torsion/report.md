# Simulation Report: Active Curvature Sweep with Torsion

**Date:** 2026-03-20
**Sweep:** `weekly-sim-active-curvature-torsion-sweep`

## What Changed
Swept `active_curvature` (growth drive) from 0.0 to 15.0 over 16 increments, while keeping `anisotropy = 3.0` constant. Unlike the previous sweep which kept the system perfectly symmetric, this sweep introduced a small, persistent symmetry-breaking torsional force (`torsion_drive = 0.5`).

## What Emergent Shapes Occurred
- The introduction of even a small torsional drive profoundly altered the system dynamics. Instead of simply curling tightly in the sagittal plane, the system exhibited dramatic lateral buckling across the entire range of growth parameters.
- At `active_curvature = 0`, the small torsional coupling alone coupled with natural kyphosis produced a massive scoliotic deformation (`Cobb ~ 107 deg`).
- As `active_curvature` increased up to `8.0`, the interplay between planar sagittal growth and the torsional breaking of symmetry led to complex, non-monotonic 3D buckling behavior (Cobb angles fluctuating between 8 deg and 76 deg).
- For very high growth rates (`active_curvature >= 13.0`), the system consistently locked into a regime of extreme 3D collapse, with Cobb angles rapidly climbing back to ~86-101 degrees.

## How This Informs Scoliosis vs Normal S-Curve
- **Symmetry Breaking is the Key:** This result starkly contrasts with the perfectly symmetric simulation (where Cobb angle remained precisely 0.0 regardless of growth). It confirms that while the energetic driver of the curve is rapid planar growth (an "Energy Deficit"), the actual emergence of Adolescent Idiopathic Scoliosis (AIS) requires a trigger that breaks sagittal symmetry.
- **Torsion as the Instigator:** The presence of a mild torsional force (possibly biological chiral packing, imbalanced muscle tone, or natural handedness) serves as a potent symmetry breaker. Once broken, the rapidly growing spine escapes the sagittal plane, converting sagittal potential energy into catastrophic lateral/torsional buckling.

## Next Sweep Suggestion
- **Sweep Name:** `weekly-sim-anisotropy-torsion-threshold`
- **Parameter:** Sweep `anisotropy` from 1.0 to 10.0 while holding `active_curvature = 10.0` and `torsion_drive = 0.5`.
- **Rationale:** To identify if there exists a structural "rescue window" where extremely high ECM anisotropy can restabilize the spine and prevent this 3D collapse, even in the presence of symmetry-breaking torsion and high growth.