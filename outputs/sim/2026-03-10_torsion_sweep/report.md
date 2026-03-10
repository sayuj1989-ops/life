# Weekly Simulation Report: Torsion-Driven Buckling under Protected Growth

**Date**: 2026-03-10
**Agent**: Curvature Simulator

## What Changed
Swept torsional coupling (`torsion_drive`) from 0.0 to 2.0 under a constant high sagittal growth drive (`active_curvature = 15.0`) and moderate structural stiffness (`anisotropy = 3.0`).

## Emergent Shapes
- Without torsional coupling (`torsion_drive = 0`), the `anisotropy = 3.0` protects the rod from lateral buckling, keeping the Cobb angle near zero (maintaining a planar S-curve).
- As `torsion_drive` increases, symmetry is broken and a 3D scoliotic deformity emerges.
- The transition from a stable 2D shape to a 3D buckled state occurs gradually but decisively, demonstrating that even with sufficient structural stiffness against pure lateral bending, active torsional drives can bypass this protection.

## Informing Scoliosis vs Normal S-Curve
This result supports the "Torsional Buckling Model" / "Toy Model E" hypothesis. While a normal S-curve relies on structural stiffness anisotropy to stay planar under high growth loads, uncompensated asymmetric torsional drives (e.g., asymmetric muscle tone or mechanosensor failure) can push the system into a 3D scoliotic collapse path that would otherwise be prevented.

## Next Sweep Suggestion
Sweep active curvature under a fixed, non-zero torsional coupling to map the boundary of the 'Energy Deficit Window' where 3D buckling becomes inevitable.
