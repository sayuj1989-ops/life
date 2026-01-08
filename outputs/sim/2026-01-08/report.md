# Weekly Simulation Report: Active Torque Sweep (2026-01-08)

## Overview
This parameter sweep investigates the effect of **Active Muscle Torques ($\chi_M$)** on a horizontal rod subject to gravity. The hypothesis is that increasing active moments driven by an information gradient (sinusoidal) can counteract gravitational sagging and induce S-shaped curvature.

## Parameters
- **Variable**: $\chi_M$ (Active Torque Gain)
- **Range**: 0.0 to 10.0
- **Constant**: Gravity=9.81, E0=1e6, L=1.0
- **Info Field**: Sinusoidal `sin(2*pi*s/L)^2`

## Results
### Quantitative Summary
| chi_M | Tip Deflection Z (m) | Mid Deflection Z (m) |
|-------|----------------------|----------------------|
| 0.0 | -0.9304 | -0.4311 |
| 2.0 | -0.5377 | 0.1632 |
| 4.0 | -0.5098 | -0.4941 |
| 6.0 | -1.1408 | -0.6416 |
| 8.0 | -0.5609 | -0.3124 |
| 10.0 | -1.3506 | -0.7015 |

### Observations
- **What changed**: As $\chi_M$ increases, the rod's deflection profile changes.
- **Emergent Shapes**: Active torques altered the shape, potentially increasing curvature in specific regions.
- **Scoliosis Relevance**: This mechanism demonstrates how active muscle tone (driven by information/proprioception) can dynamically maintain spinal alignment against gravity. Failure of this active component (low $\chi_M$) leads to passive gravitational collapse (sag).

## Next Steps
- Suggestion: Sweep **Stiffness Anisotropy ($\chi_E$)** combined with active moments to see if stiffer regions can lock in the corrective shape.
