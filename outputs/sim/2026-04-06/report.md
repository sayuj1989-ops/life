# Simulation Report: Natural Kyphosis Sweep

**Date:** 2026-04-06
**Sweep Name:** weekly-sim-posture-kyphosis
**Parameter Swept:** `natural_kyphosis` (Range: 0.0 to 5.0)

## 1. What Changed
We ran a parameter sweep over the `natural_kyphosis` parameter, ranging from 0.0 (straight sagittal profile) to 5.0 (hyper-kyphosis). The simulation was driven by high active curvature (`active_curvature = 10.0`) and included a small initial lateral defect (`initial_lateral_defect = 0.05`) to test for susceptibility to lateral instability (S-shaped scoliosis) under different sagittal baseline curvatures. Stiffness anisotropy was set to 3.0.

## 2. What Emergent Shapes Occurred
- **Lateral Deviation (S_lat):** The lateral deviation increased monotonically with higher natural kyphosis. At `natural_kyphosis = 0.0`, `S_lat` was roughly 0.005. It steadily increased to over 0.009 at `natural_kyphosis = 5.0`.
- **Cobb Angle:** The Cobb angle similarly increased from ~0.30 degrees at flat kyphosis to ~1.43 degrees at extreme kyphosis. While the absolute Cobb angle remained relatively small (due to the stabilizing effect of `anisotropy = 3.0` and absence of torsion), there is a clear destabilizing trend associated with higher kyphosis in the presence of growth.
- **Max Curvature:** Interestingly, the maximum localized curvature slightly decreased from ~155.2 to ~153.0 as kyphosis increased, suggesting the overall bending energy becomes more distributed rather than sharply localized.

## 3. How This Informs Scoliosis vs. Normal S-Curve
The classical model often associates *hypokyphosis* (flattened thoracic spine) with adolescent idiopathic scoliosis (AIS), sometimes viewing it as a permissive factor for lateral rotation.
However, in this purely mechanical model (growth vs. anisotropic resistance, without coupled torsion), *increasing* the natural kyphosis actually amplified the lateral instability triggered by a small defect. This suggests that while physiological kyphosis is normal, excessive pre-existing sagittal curvature (hyper-kyphosis) under high active growth creates a larger moment arm for lateral buckling forces, making the spine *more* sensitive to small lateral defects. The discrepancy with clinical observation (where hypokyphosis is more common in AIS) highlights the critical missing role of torsional coupling in this specific sweep, which we know from previous sweeps can invert these stability relationships.

## 4. Next Sweep Suggestion
**Sweep:** Torsional Coupling (`torsion_drive`) combined with varying `natural_kyphosis`.
**Reasoning:** Since this sweep showed increased lateral instability with hyper-kyphosis (contradicting the clinical hypokyphosis-scoliosis link), we need to re-introduce `torsion_drive`. We should test if torsional coupling specifically destabilizes the *hypokyphotic* spine more than the hyperkyphotic one, which would perfectly bridge the mechanical model with clinical observations.
