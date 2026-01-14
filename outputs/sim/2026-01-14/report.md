# Stiffness Anisotropy Sweep Report

Date: 2026-01-14

## Overview
Investigated how the ratio of Lateral to Sagittal stiffness affects 3D stability under torsional load (chi_tau=0.5).

## Results
| Ratio | Lateral Dev | Sagittal Range |
|-------|-------------|----------------|
| 0.1 | 0.1424 | 0.4732 |
| 0.25 | 0.1521 | 0.4862 |
| 0.5 | 0.1753 | 0.4800 |
| 0.75 | 0.1780 | 0.4724 |
| 1.0 | 0.1721 | 0.4679 |
| 1.25 | 0.1641 | 0.4658 |
| 1.5 | 0.1563 | 0.4649 |
| 2.0 | 0.1440 | 0.4645 |

## Findings
- **Low Anisotropy (<1)**: Reduces lateral stiffness, making the rod more susceptible to lateral buckling or deviation driven by torsion coupling.
- **High Anisotropy (>1)**: Increases lateral stiffness, potentially constraining the rod to the sagittal plane despite torsional inputs.
