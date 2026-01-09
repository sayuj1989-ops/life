# Simulation Report: Active Muscle Torque Sweep

**Date**: 2026-01-09

## Overview
Investigated the emergence of S-shaped spinal profiles by sweeping the Active Muscle Torque gain ($\chi_M$) under standard gravity loading. A horizontal rod (cantilever) was subjected to a sinusoidal information field driving distributed internal moments.

## Key Findings
- **Gravity Dominance**: At low $\chi_M$, the rod exhibits a simple C-shape sag due to gravity.
- **Emergence**: As $\chi_M$ increases, the internal active moments counteract gravity.
- **S-Shape**: A distinct S-shape (multiple zero crossings in curvature) emerges at higher gains.

## Results Summary

| chi_M | Tip Z (m) | Zero Crossings |
|-------|-----------|----------------|
| 0.00 | -0.0057 | 0 |
| 4.00 | 0.0232 | 18 |
| 8.00 | -0.0855 | 14 |
| 12.00 | 0.1368 | 23 |
| 16.00 | -0.2382 | 14 |
| 20.00 | 0.0848 | 24 |


## Next Steps
- Investigate coupling with $\chi_E$ (stiffness anisotropy).
- Test vertical initialization with buckling loads.
