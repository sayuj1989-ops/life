# Protein-to-Geometry Mapping Report

**Date:** 2026-03-13 20:12:41
**Source Data:** `results.csv`

## Experiment Summary
This experiment maps biological parameters to mechanical spine outcomes.
- **Anisotropy (FBN1):** Higher values indicate structured ECM (Wild Type), resisting lateral buckling.
- **Active Curvature (Growth):** Higher values indicate rapid growth or high mechanosensory gain.

## Performance Metrics
- **Total Simulations:** 2
- **Average Runtime:** 0.8616 s
- **Peak Memory:** 15.49 MB

## Results Table
| Bio Label | Anisotropy | Active Curv | Cobb Angle (deg) | Max Curvature | Energy (J) | Status |
|---|---|---|---|---|---|---|
| Marfan-like (Degraded ECM) | Homeostatic (Low Gain) | 1.00 | 0.10 | 0.0000 | 0.0018 | 1.6854e-02 | ✅ |
| WildType (Structured ECM) | Homeostatic (Low Gain) | 5.00 | 0.10 | 0.0002 | 0.0018 | 1.6891e-02 | ✅ |

## Interpretation
1. **WildType Stability:** High anisotropy (e.g., 5.0) should maintain low Cobb angles even with some active curvature.
2. **Marfan Instability:** Low anisotropy (e.g., 1.0) makes the spine susceptible to buckling (high Cobb angle) under active growth loads.
3. **Energy Costs:** Higher bending energy typically correlates with higher metabolic cost (U_CC).
