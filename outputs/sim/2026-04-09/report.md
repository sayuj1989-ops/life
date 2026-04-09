# Simulation Report: Growth Gain (chi_kappa) Sweep

## What Changed
Swept the active curvature growth gain (`chi_kappa`) from 0.0 to 30.0 to analyze the emergence of S-shaped spinal profiles under gravitational loading and high lateral stiffness anisotropy (ratio = 3.0).

## Emergent Shapes
*   **Low Growth (0.0):** Sagittal shape collapses into a C-curve under gravity (1 inflection point).
*   **Moderate Growth (5.0 - 20.0):** The simulated spine develops a stable S-shape (2 inflection points) in the sagittal plane. The amplitude (sagittal range) reaches a local minimum around `chi_kappa = 10.0` (0.17m), indicating optimal compensation against gravity.
*   **High Growth (25.0 - 30.0):** Excessive growth leads to buckling. The number of inflection points spikes dramatically (10-12), and the sagittal range increases again, suggesting complex, multi-modal planar buckling instability.
*   **Lateral Stability:** In this perfectly symmetric setup without torsional coupling, the spine remained perfectly stable in the lateral plane (Dev = 0.0) across all growth values, although the reported Cobb angle jumped to 180 deg due to the 2D projection simplifications of the planar buckling.

## Implications for Scoliosis vs. Normal S-Curve
These results demonstrate that a moderate magnitude of differential growth (`chi_kappa`) is essential to counteract gravity and establish a normal, stable sagittal S-curve. However, too much growth forces planar buckling. The absence of 3D lateral deviation here reinforces the hypothesis that true scoliosis requires a symmetry-breaking mechanism (like torsion or a lateral defect) in addition to growth forces; growth alone purely affects the sagittal profile until extreme planar buckling occurs.

## Next Sweep Suggestion
A sweep exploring **torsional coupling (`chi_tau`)** simultaneously with moderate to high growth (`chi_kappa = 15.0`) to observe if the symmetry breaking forces the planar instability to project into true 3D lateral scoliosis.
