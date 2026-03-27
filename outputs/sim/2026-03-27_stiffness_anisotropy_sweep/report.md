# Simulation Report: Stiffness Anisotropy Sweep

**Date:** 2026-03-27
**Sweep Name:** weekly-sim: stiffness-anisotropy-protection

## Configuration
- Fixed Active Curvature: 10.0
- Fixed Torsion Drive: 0.5
- Fixed Initial Lateral Defect: 0.05
- Sweep Parameter: `stiffness_anisotropy` from 1.00 to 5.00

## Results Summary
- **What changed:** We systematically varied the lateral stiffness anisotropy (from isotropic 1.0 to highly anisotropic 5.0) under a constant baseline of growth, torsion, and a small symmetry-breaking lateral defect.
- **Emergent Shapes:** At low anisotropy (e.g., R=1.0), the rod bucks laterally, driven by the torsion and initial defect, resulting in high Cobb angles (>60 deg). As anisotropy increases, the lateral bending stiffness resists this buckling, and the Cobb angle decreases significantly, stabilizing the S-curve primarily in the sagittal plane.
- **Scoliosis vs Normal S-curve:** This clearly demonstrates that an underlying structural weakness (loss of anisotropy) can allow normal sagittal growth forces to spill over into the coronal plane, precipitating scoliotic deformity. Normal spines maintain high anisotropy, protecting against lateral deviation despite complex 3D loading.
- **Next Sweep Suggestion:** Investigate how `taper_ratio` (geometric tapering) interacts with localized defects along the spine under high load.
