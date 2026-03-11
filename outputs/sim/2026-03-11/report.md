# Parameter Sweep: Torsional Coupling (torsion_drive)

- **What changed:** Swept `torsion_drive` from 0.0 to 2.0 under high growth (active_curvature=12.0) and moderate anisotropy (3.0).
- **Emergent shapes:** Increasing torsion transforms a planar sagittal profile into a 3D scoliotic shape, driving the Cobb angle up to a peak of ~101 degrees at `torsion_drive=1.0`. The system exhibits complex, non-monotonic sensitivity to torsion, with resonance peaks and stability valleys.
- **Scoliosis implications:** Torsional coupling acts as the symmetry-breaking mechanism that converts growth energy into lateral deviation. At specific critical values (e.g., 1.0), it dramatically destabilizes the spine even with stabilizing anisotropy present.
- **Next sweep suggestion:** Sweep `initial_lateral_defect` under varying `torsion_drive` to map defect sensitivity and the transition to buckling.