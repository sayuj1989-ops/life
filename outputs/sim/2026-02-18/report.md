# Simulation Report: Stiffness Modulation Sweep (2026-02-18)

## Hypothesis
Increasing stiffness in information-rich regions (simulating bone/vertebrae) while leaving gradients flexible (discs) will reduce gravitational sag while maintaining the S-shape induced by `chi_kappa`.

## Setup
- Fixed `chi_kappa = 5.0` (Geometric Counter-Curvature)
- Swept `chi_E` from 0.0 to 20.0
- Information Field: $I = \sin^2(4\pi s)$, simulating 4 segments.
- Gravity: 9.81 m/s², Rod horizontal.

## Results
| chi_E | Tip Deflection Z (m) | Peak-to-Trough Z (m) |
|-------|----------------------|----------------------|
| 0.0 | -0.0381 | 0.0567 |
| 2.0 | -0.0205 | 0.0347 |
| 4.0 | -0.0050 | 0.0181 |
| 6.0 | -0.0022 | 0.0156 |
| 8.0 | 0.0025 | 0.0161 |
| 10.0 | -0.0119 | 0.0200 |
| 15.0 | -0.0067 | 0.0144 |
| 20.0 | -0.0029 | 0.0093 |

## Observations
- **Stiffness Counteracts Sag:** Increasing `chi_E` generally reduces the downward tip deflection (sag). At `chi_E=8.0`, the rod actually deflects slightly upwards at the tip (+2.5mm), indicating the counter-curvature torque is fully effectively lifting the structure against gravity.
- **Suppression of Curvature:** The Peak-to-Trough Z (an indicator of S-shape amplitude) decreases as `chi_E` increases. This implies that while stiffness modulation helps fight gravity, it also stiffens the mechanism that generates the S-curve itself (since regions of high `I` become rigid).
- **Non-Monotonicity:** An interesting anomaly occurs at `chi_E=10.0`, where sag increases again (-1.19cm) and curvature amplitude increases. This suggests a potential mode buckling or a resonance where the specific stiffness pattern aligns unfavorably with the gravitational moment arm.
- **Optimal Window:** There appears to be an optimal range (around `chi_E \approx 6.0-8.0`) where the rod maintains a near-horizontal posture (minimal tip deflection) without becoming completely rigid (flattened).

## Conclusion
Stiffness inhomogeneity (vertebrae-disc model) effectively complements geometric counter-curvature. Unlike a uniform rod which just sags, the modulated rod can be tuned to hold its shape against gravity. However, excessive stiffness gains suppress the S-curve formation.
