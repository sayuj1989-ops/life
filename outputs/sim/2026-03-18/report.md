# Simulation Report: Stiffness Anisotropy vs Sagittal Growth

## What Changed
Swept `stiffness_anisotropy` from 0.5 to 5.0 while keeping `active_curvature` constant at a high value (12.0) and `torsion_drive` at 0.0. This tests the interaction between sagittal growth and lateral stiffness anisotropy in the absence of active symmetry-breaking torsion.

## Emergent Shapes
The spine exhibited pure sagittal bending (kyphosis/lordosis profile) across all tested anisotropy values. Crucially, the Cobb angle remained 0.0 degrees throughout the sweep. No lateral buckling or 3D scoliotic deformations emerged.

## Relevance to Scoliosis vs Normal S-Curve
This finding confirms a critical aspect of the biological counter-curvature hypothesis: high sagittal growth alone is insufficient to trigger 3D scoliosis if structural symmetries are preserved. Even at high active curvature (chi_kappa = 60), the S-curve remains stable in the sagittal plane. The varying stiffness anisotropy had no visible effect because the lateral plane was never challenged by a symmetry-breaking force. This emphasizes that scoliosis requires a secondary destabilizing factor, such as torsion (e.g., from PCP defects) or an initial lateral defect, to trigger lateral buckling.

## Next Sweep Suggestion
Introduce a small constant `torsion_drive` (e.g., 0.1) or `initial_lateral_defect` while repeating this `stiffness_anisotropy` sweep to observe how anisotropy protects against (or fails to protect against) buckling when a symmetry-breaking force is present under high growth conditions.