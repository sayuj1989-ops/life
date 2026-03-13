# Load Vector Tilt Sweep Report

**Date:** 2026-03-13
**Author:** Curvature Simulator

## What Changed
A parameter sweep was conducted to evaluate the effect of the **load vector tilt** (i.e., the angle of gravity relative to the spine's primary axis) on spinal geometry. We varied the `tilt_deg` parameter from 0.0 to 30.0 degrees across 20 simulation runs while maintaining a moderate anisotropy (3.0) and high active growth drive (10.0). This was implemented by rotating the gravity vector in the lateral plane within the PyElastica Cosserat rod system.

## Emergent Shapes
As the tilt angle increased, several distinct regimes were observed:
1. **Low Tilt (0-5 degrees):** The spine remains relatively stable in the lateral plane, with Cobb angles below 1 degree, but exhibits minor initial lateral deviations (S_lat ~ 0.3m) due to symmetry breaking.
2. **Moderate Tilt (6-15 degrees):** A steady, near-linear increase in the Cobb angle from ~4 degrees up to ~36 degrees. Lateral deviation decreases in this phase as the spine compensates via increased local curvature.
3. **High Tilt / Critical Transition (15-22 degrees):** A critical instability region where the spine experiences a non-linear buckling transition, with the Cobb angle jumping to a peak of 64.30 degrees at 22.1 degrees of tilt, and lateral deviation jumping to extreme values (S_lat > 0.8m).
4. **Extreme Tilt (>22 degrees):** At very high tilts, the Cobb angle stabilizes slightly and then slightly decreases (dropping from 64 to 54 degrees), while lateral deviation remains high (S_lat ~0.75m), indicating a fully collapsed, post-buckled state lying "flat" relative to the tilted load vector.

## How this informs Scoliosis vs Normal S-Curve
These results highlight that the biological S-curve is highly sensitive to the alignment of the gravitational load vector. When the load vector is perfectly aligned (0 degrees), the system's active curvature and anisotropy successfully maintain a stable planar S-curve (normal spine). However, introducing an asymmetric, tilted load vector breaks this planar symmetry. The metabolic "counter-curvature" system struggles to compensate for the off-axis gravitational torque, forcing the spine into a 3D buckling mode characteristic of severe idiopathic scoliosis (Cobb > 60 degrees). This supports the hypothesis that posture, pelvic tilt, or vestibular imbalances could act as a critical mechanical symmetry-breaker, pushing an otherwise stable growth process into pathological buckling.

## Next Sweep Suggestion
**Coupled Tilt and Torsion Sweep (`tilt_deg` vs `torsion_drive`)**
Given that a tilted load vector induces significant lateral bending, the next logical step is to explore how active torsional coupling (`chi_tau`) interacts with this tilted load. In biological systems, muscles and ligaments may exert active torsional forces to counteract or exacerbate off-axis loads. A 2D sweep (e.g., Tilt: 0-20 deg vs Torsion Drive: 0-2.0) will reveal whether torsion acts as a restorative force or a further destabilizing factor when the spine is already loaded asymmetrically.