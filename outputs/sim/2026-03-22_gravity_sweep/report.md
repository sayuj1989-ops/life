# Weekly Simulation: PyElastica Gravity and Anisotropy Sweep

## Overview
This experiment maps the interaction between axial gravity-like loading and biological structural parameters (anisotropy) to emergent spinal metrics via the `run_protein_simulation` PyElastica bridge. It investigates whether an S-shaped spinal profile emerges or worsens under increased gravity-like loading with varying anisotropic stiffness.

## Performance
- **Total Runtime:** 95.76 seconds
- **Peak Memory Usage:** 0.00 MB

## Results Summary
- **Anisotropy = 1.0**: Max Cobb Angle = 87.07 deg
- **Anisotropy = 2.0**: Max Cobb Angle = 39.83 deg
- **Anisotropy = 4.0**: Max Cobb Angle = 8.19 deg

## Biological Interpretation
The results illustrate the complex interaction between mechanical loading (gravity) and internal stabilization (anisotropy). They support the Biological Counter-curvature hypothesis, indicating that spinal alignment stability under gravity depends fundamentally on active, balanced stiffness maintenance. Specifically, the interplay of gravity-like loading with low anisotropic stiffness precipitates lateral deviation (scoliosis) compared to more stable behavior with higher anisotropy.

### Next Sweep Suggestion
Examine the influence of asymmetric growth rates along the length of the beam combined with varied torsional parameters to model adolescent growth spurts more accurately.

## Generated Artifacts
- `results.csv`
- `params.csv`
- `plot_gravity_cobb.png`
- `plot_gravity_slat.png`
