# Simulation Report: Growth S-Shape Emergence Sweep

**Date**: 2026-04-10

## Hypothesis
Testing the emergence of an S-shaped spinal profile driven by a growth gradient (chi_kappa) acting under gravity, stabilized by stiffness anisotropy.

## Parameters
- **Growth Gain Sweep**: chi_kappa in [0.0, 15.0, 30.0] (Quick mode)
- **Anisotropy Ratio**: 3.0
- **Gravity**: 9.81
- **Boundary Condition**: Fixed

## Results
See attached `plot_s_shape.png`.

### Quantitative Summary
| Growth Gain (chi_kappa) | Lateral Dev | Sagittal Range | Curvature Inflections | Cobb Angle |
|-------------------------|-------------|----------------|-----------------------|------------|
| 0.0                     | 0.0         | 0.9290         | 1                     | 0.0        |
| 15.0                    | 0.0         | 0.2532         | 2                     | 180.0      |
| 30.0                    | 0.0         | 0.5517         | 12                    | 180.0      |

## Observations
- Increasing the growth gain (chi_kappa) to 15.0 leads to the emergence of 2 curvature inflections, indicating a stable S-shaped profile in the sagittal plane, with significantly reduced sagittal range (0.25m vs 0.93m).
- At an extreme growth gain of 30.0, the rod buckles in the sagittal plane with numerous high-frequency inflections (12) and increased sagittal range (0.55m).
- Due to the absence of torsional coupling or lateral tilt, the lateral deviation remained 0 across all runs.

## Next Steps
- Implement a similar sweep that introduces torsional coupling (`chi_tau > 0`) to investigate lateral instability and 3D scoliosis once the S-shape emerges.
