# Protein-to-Geometry Mapping Report

**Date:** 2026-02-19 14:37:44
**Source Data:** `protein_mapping_results.csv`

## Experiment Summary
This experiment maps biological parameters to mechanical spine outcomes.
- **Anisotropy (FBN1):** Higher values indicate structured ECM (Wild Type), resisting lateral buckling.
- **Active Curvature (Growth):** Higher values indicate rapid growth or high mechanosensory gain.

## Performance Metrics
- **Total Simulations:** 4
- **Average Runtime:** 6.4382 s
- **Peak Memory:** 15.52 MB

## Results Table
| Bio Label | Anisotropy | Active Curv | Cobb Angle (deg) | Max Curvature | Energy (J) |
|---|---|---|---|---|---|
| Marfan-like (Degraded ECM) | Homeostatic (Low Gain) | 1.00 | 0.50 | 0.0000 | 36.9156 | 6.4633e-01 |
| Marfan-like (Degraded ECM) | Hyper-Growth (High Gain) | 1.00 | 3.00 | 0.0000 | 51.9630 | 4.2629e-01 |
| WildType (Structured ECM) | Homeostatic (Low Gain) | 5.00 | 0.50 | 0.0000 | 36.9156 | 6.4633e-01 |
| WildType (Structured ECM) | Hyper-Growth (High Gain) | 5.00 | 3.00 | 0.0000 | 51.9630 | 4.2629e-01 |

## Interpretation
1. **WildType Stability:** High anisotropy (e.g., 5.0) should maintain low Cobb angles even with some active curvature.
2. **Marfan Instability:** Low anisotropy (e.g., 1.0) makes the spine susceptible to buckling (high Cobb angle) under active growth loads.
