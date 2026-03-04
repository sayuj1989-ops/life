# Protein-to-Geometry Mapping Report

**Date:** 2026-03-03 06:50:28
**Date:** 2026-03-03 15:07:10
**Date:** 2026-03-03 17:09:28
**Date:** 2026-03-03 18:32:24
**Date:** 2026-03-03 14:31:01
**Date:** 2026-03-04 17:25:53
**Source Data:** `results.csv`

## Experiment Summary
This experiment maps biological parameters to mechanical spine outcomes.
- **Anisotropy (FBN1):** Higher values indicate structured ECM (Wild Type), resisting lateral buckling.
- **Active Curvature (Growth):** Higher values indicate rapid growth or high mechanosensory gain.

## Performance Metrics
- **Total Simulations:** 2
- **Average Runtime:** 1.0598 s
- **Peak Memory:** 15.48 MB
- **Average Runtime:** 0.7754 s
- **Average Runtime:** 2.3200 s
- **Average Runtime:** 1.0580 s
- **Average Runtime:** 0.8560 s
- **Peak Memory:** 15.49 MB
- **Average Runtime:** 0.9726 s
- **Peak Memory:** 15.48 MB

## Results Table
| Bio Label | Anisotropy | Active Curv | Cobb Angle (deg) | Max Curvature | Energy (J) | Status |
|---|---|---|---|---|---|---|
| Marfan-like (Degraded ECM) | Homeostatic (Low Gain) | 1.00 | 0.10 | 0.0000 | 0.0018 | 1.6854e-02 | ✅ |
| WildType (Structured ECM) | Homeostatic (Low Gain) | 5.00 | 0.10 | 0.0002 | 0.0018 | 1.6891e-02 | ✅ |

## Interpretation
1. **WildType Stability:** High anisotropy (e.g., 5.0) should maintain low Cobb angles even with some active curvature.
2. **Marfan Instability:** Low anisotropy (e.g., 1.0) makes the spine susceptible to buckling (high Cobb angle) under active growth loads.
3. **Energy Costs:** Higher bending energy typically correlates with higher metabolic cost (U_CC).
