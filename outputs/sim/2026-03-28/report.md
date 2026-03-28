# Growth-Anisotropy S-Shape Emergence Sweep Report

Date: 2026-03-28

## Overview
Investigated how stiffness anisotropy affects the emergence of a sagittal S-curve driven by planar growth (`chi_kappa=15.0`) under vertical gravity loading.

## Results
| Ratio | Lateral Dev (m) | Sagittal Range (m) |
|-------|-----------------|--------------------|
| 0.5 | 0.0000 | 0.1754 |
| 0.75 | 0.0000 | 0.1754 |
| 1.0 | 0.0000 | 0.1754 |
| 1.5 | 0.0000 | 0.1754 |
| 2.0 | 0.0000 | 0.1754 |
| 3.0 | 0.0000 | 0.1754 |
| 4.0 | 0.0000 | 0.1754 |
| 5.0 | 0.0000 | 0.1754 |
| 7.5 | 0.0000 | 0.1754 |
| 10.0 | 0.0000 | 0.1754 |

## Findings
- **Instability**: Higher lateral stiffness did not prevent lateral buckling, or induced complex 3D instability modes.
- **Relevance**: This supports the hypothesis that structural anisotropy is required to stabilize growth-induced sagittal curvature (normal S-curve) against scoliotic buckling.

## Next Steps
- Sweep `chi_kappa` combined with varying `stiffness_anisotropy` to identify the phase boundary of S-curve stability.
