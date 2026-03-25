# Natural Kyphosis Sweep Report
**Date:** 2026-03-25

## 1. Parameter Changed
A parameter sweep was performed over `natural_kyphosis`, ranging from 0.0 to 5.0 in 20 steps.
Other variables were fixed, specifically:
- `active_curvature`: 10.0
- `anisotropy`: 3.0
- `torsion_drive`: 0.0

The goal was to determine if varying the baseline sagittal S-curve (natural kyphosis) alone, in a regime of growth and intermediate anisotropy, could provoke the emergence of lateral S-shapes (scoliosis).

## 2. Emergent Shapes
The primary finding from the sweep is that modifying the natural kyphosis within this range (0.0 to 5.0) **did not** produce lateral deviations or scoliosis in this configuration.
- The `S_lat` (Lateral Scoliosis Index) remained exactly 0.0 across all values.
- The `cobb_angle` remained 0.0 across all values.

However, changes in the sagittal plane were strictly correlated with the natural kyphosis values:
- `end_to_end_distance` monotonically increased from ~0.116m to ~0.165m.
- The sagittal deflection (`z_tip` and `y_tip`) steadily adjusted, indicating the model correctly registered the increasing kyphosis and bent accordingly in the sagittal plane.

## 3. Implications for Scoliosis vs Normal S-curve
The results strongly suggest that simple amplification or reduction of natural kyphosis does not, by itself, break the planar symmetry required to initiate lateral curvature, at least up to an active curvature gain of 10.0 and anisotropy of 3.0 without any initial lateral defect or torsional drive.

This reinforces the conceptual model where "hypokyphosis" or "hyperkyphosis" might be concurrent symptoms of scoliotic progression, but not the direct symmetry-breaking cause unless interacting with a specific threshold of torsional coupling or large structural defect. Planar stability is robust as long as the forces remain cleanly coupled to the sagittal plane.

## 4. Next Sweep Suggestion
Given that natural kyphosis alone failed to break symmetry, a logical next step is to investigate the interaction between **natural kyphosis** and **torsional drive**.
Specifically, sweep `natural_kyphosis` while applying a constant, non-zero `torsion_drive` (e.g., 0.5) to test if different levels of baseline sagittal curvature act as a lever or amplifier for torsionally-induced lateral buckling.
