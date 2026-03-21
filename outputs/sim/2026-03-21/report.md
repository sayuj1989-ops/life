# Simulation Report: S-Shape Emergence

**Date:** 2026-03-21
**Parameter Sweep:** Growth Gain (`chi_kappa`)

## 1. What Changed
We swept the growth gain (`chi_kappa`) from 0.0 to 30.0 under gravity and an anisotropic stiffness ratio of 3.0. The goal was to test whether an S-shaped spinal profile emerges under gravity-like loading with active growth and anisotropic stiffness.

## 2. Emergent Shapes
- At lower growth gains (`chi_kappa=0.0`), the system exhibits a simple C-shape (1 inflection point).
- Between `chi_kappa=5.0` and `chi_kappa=20.0`, an optimal S-shape emerges, characterized by 2 inflection points and minimized sagittal range.
- At extreme growth gains (`chi_kappa >= 25.0`), the system experiences higher instability, exhibiting a dramatic increase in inflection points (10 to 12) and increased sagittal range. The Cobb angle jumps to 180 degrees.

## 3. Scoliosis vs. Normal S-Curve
This informs the delicate balance required for a normal S-curve. Moderate growth gain combined with structural anisotropy is sufficient to stabilize a double-curve (normal S-curve) against gravity. However, excessive growth gain overpowers the anisotropic constraints, leading to hyper-buckling modes (multi-inflection points) indicative of pathologically complex scoliotic shapes, even without an explicit torsional drive. The planar instability suggests that a primary sagittal overgrowth can precede 3D lateral buckling if coupled with even minute symmetry-breaking.

## 4. Next Sweep Suggestion
The next logical sweep is to maintain `chi_kappa` in the pathological range (e.g., 25.0) and introduce a small `torsion_drive` or `initial_lateral_defect` to observe how this planar hyper-buckling transitions into full 3D scoliosis.
