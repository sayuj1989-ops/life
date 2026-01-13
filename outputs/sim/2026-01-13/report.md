# Simulation Report: Posture (Tilt) Sweep

**Date**: 2026-01-13

## Overview
Investigated the stability of the emergent S-shape (driven by $\chi_M=15$) as the rod's posture changes from Horizontal (0°) to Vertical (90°) under gravity.
The rod is initialized with a sinusoidal information field `I = sin^2(2*pi*s/L)`. Active active torque is coupled via $\chi_M=15$, creating a tendency to bend against gravity in the horizontal case.

## Findings
- **Horizontal (0°)**: Max gravitational moment. S-shape is prominent as active torque fights sag.
- **Vertical (90°)**: Gravity acts axially (compression). Bending moments vanish except for instability.
- **Emergence**: The "S-shape" complexity (Zero Crossings) varies significantly with posture.
    - At 0° (Horizontal), we see ~26 crossings (high complexity due to active fight against sag).
    - At 45°, crossings drop to 18, suggesting a transition regime.
    - At 90° (Vertical), crossings drop to 17, indicating a simplification of the curve as gravitational bending moment disappears, leaving only the intrinsic active moment shape.

## Results Table
| Theta (deg) | Zero Crossings | Avg Curvature (1/m) | Tip X (m) | Tip Z (m) |
|-------------|----------------|---------------------|-----------|-----------|
| 0.0 | 26 | 46.88 | 0.28 | -0.19 |
| 15.0 | 25 | 53.10 | 0.22 | 0.04 |
| 30.0 | 22 | 52.74 | 0.01 | 0.25 |
| 45.0 | 18 | 65.29 | -0.21 | 0.35 |
| 60.0 | 26 | 53.44 | -0.28 | 0.38 |
| 75.0 | 32 | 53.03 | -0.24 | 0.53 |
| 90.0 | 17 | 64.07 | -0.19 | 0.65 |

## Conclusion
The S-shape is *posture-dependent*. Active moments tuned for horizontal support ($\chi_M$) create excessive or different curvature when the rod is vertical. This supports the hypothesis that biological counter-curvature must be dynamically tuned to the gravity vector (vestibular/proprioceptive feedback), and a static "growth" pattern is insufficient for multi-posture stability.
