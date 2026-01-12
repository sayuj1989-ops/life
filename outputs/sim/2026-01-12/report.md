# Simulation Report: Posture Stability Sweep (2026-01-12)

## Hypothesis
A purely growth-driven S-shape (fixed `chi_kappa`) without active muscle compensation (`chi_M=0`) will exhibit non-linear instability as the load vector rotates from axial (vertical) to transverse (horizontal).

## Setup
- Fixed `chi_kappa = 10.0` (Natural S-shape)
- Swept `Tilt Angle` from 0 to 90 degrees
- Information Field: Sine Wave (Periodic)
- Gravity: 9.81 m/s²

## Results
| Angle (deg) | Tip Sag (m) | Axial Shortening (m) |
|-------------|-------------|----------------------|
| 0 | 0.0301 | 1.2374 |
| 15 | 0.0900 | 1.2319 |
| 30 | 0.1383 | 1.2061 |
| 45 | 0.1810 | 1.1707 |
| 60 | 0.2151 | 1.1264 |
| 75 | 0.2371 | 1.0825 |
| 90 | 0.2501 | 1.0368 |

## Observations
Measured deformation as the spine rotated from vertical to horizontal. Peak sag occurred at 90 degrees.
