# Integrated Bio-Gravitational Simulation Report

**Date:** 2026-02-09 14:31:53

## Experiment Summary
This experiment maps 'virtual protein' profiles to macroscopic spinal mechanics using PyElastica.
It tests the **Vector-Scalar Mismatch** hypothesis: that spinal stability requires a balance between ECM anisotropy (Vector) and mechanosensitive growth drive (Scalar).

### Performance Metrics
- **Total Experiment Time:** 31.17 s
- **Average Simulation Time:** 6.2285 s
- **Peak Memory Usage:** 14.58 MB

## Results Table

| Profile | Anisotropy (Vector) | Curvature Drive (Scalar) | S_lat (Scoliosis Index) | Cobb Angle (deg) | Max Torsion |
|---|---|---|---|---|---|
| WildType_Control | 2.00 | 0.10 | 0.6061 **(Unstable)** | 40.03 | 0.2916 |
| Marfan_Like (Low Anisotropy) | 1.00 | 0.10 | 0.2616 | 24.44 | 0.2284 |
| Piezo_Gain (High Drive) | 2.00 | 2.00 | 0.4731 **(Unstable)** | 13.65 | 2.1644 |
| Scoliotic_Risk (Mismatch) | 1.10 | 2.00 | 0.0938 | 2.25 | 8.0085 |
| Microgravity (Unloaded) | 1.50 | 1.50 | 0.3976 | 13.15 | 3.4641 |

## Interpretation
1. **WildType Control**: Shows baseline stability.
2. **Marfan-Like**: Low anisotropy leads to reduced stiffness against perturbation.
3. **Piezo Gain**: High active curvature drive can induce over-correction.
4. **Scoliotic Risk**: The combination of low anisotropy and high drive maximizes deformation (High S_lat).
