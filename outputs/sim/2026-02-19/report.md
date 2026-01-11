# Torsion-Coupled Scoliosis Sweep Report

## Overview
Date: 2026-02-19
Goal: Investigate if torsional coupling (chi_tau) transforms a planar S-curve (chi_kappa) into 3D scoliosis.

## Parameters
- **chi_kappa**: 5.0 (Strong Planar Driver)
- **chi_E**: 0.5
- **chi_tau**: Swept [0.0 - 2.0]
- **Info Field**: Sinusoidal (S-shape)

## Results

| chi_tau | Lateral Dev (m) | Sagittal Range (m) | Avg Torsion (1/m) | Scoliosis Index |
|---------|-----------------|--------------------|-------------------|-----------------|
| 0.0 | 0.0000 | 0.4516 | 0.0000 | 0.0000 |
| 0.2 | 0.1256 | 0.4475 | 1.8124 | 0.2276 |
| 0.4 | 0.1655 | 0.4522 | 2.8268 | 0.4679 |
| 0.6 | 0.1830 | 0.4624 | 3.6499 | 0.6680 |
| 0.8 | 0.1929 | 0.4738 | 4.4233 | 0.8535 |
| 1.0 | 0.1985 | 0.4856 | 5.1769 | 1.0275 |
| 1.5 | 0.2033 | 0.5150 | 7.0071 | 1.4244 |
| 2.0 | 0.1932 | 0.5438 | 8.7958 | 1.6994 |

## Observations
- Increasing `chi_tau` induces significant torsion as expected.
- **Emergent Scoliosis**: Lateral deviation increases with torsion, confirming the coupling mechanism.
- The sagittal S-curve profile (measured by range) remained robust.

## Next Steps
- Sweep `chi_M` (Active Muscle) alongside `chi_tau` to see if active correction can suppress the lateral mode.
