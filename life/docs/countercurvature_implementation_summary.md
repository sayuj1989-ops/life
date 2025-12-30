# Countercurvature Metrics: Implementation Summary

## Overview

The countercurvature metrics framework is now fully integrated into the codebase. This provides a quantitative bridge between:

1. **Mechanical simulations** (PyElastica/beam solver) → curvature profiles κ(s)
2. **Information fields** (IEC model) → biological information processing I(s)
3. **Riemannian geometry** → countercurvature metric g_eff(s)
4. **Scalar metrics** → geodesic deviation D_geo, D̂_geo

## Implementation Status

### ✅ Core Metrics (Complete)

- **`compute_countercurvature_metric()`**: Computes g_eff(s) from information field
- **`geodesic_curvature_deviation()`**: Computes D_geo, D_geo_norm from curvature profiles

**Location:** `src/spinalmodes/countercurvature/validation_and_metrics.py`

### ✅ Experiment Integration (Complete)

All three experiments now compute and save geodesic deviation metrics:

1. **`experiment_spine_modes_vs_gravity.py`**
   - Computes g_eff(s) once (constant across parameter sweep)
   - Computes D_geo_norm for each χ_κ value
   - Saves to `spine_modes_summary.csv` with columns: `D_geo`, `D_geo_norm`, `base_energy`

2. **`experiment_microgravity_adaptation.py`**
   - Computes g_eff(s) once (constant across gravity levels)
   - Computes D_geo_norm for each gravity level
   - Saves to `microgravity_summary.csv` with columns: `D_geo`, `D_geo_norm`
   - Panel B now shows D_geo_norm vs gravity (log scale)

3. **`experiment_plant_upward_growth.py`**
   - Computes g_eff(s) and geodesic deviation
   - Compares D_geo_norm with plain L2 norm
   - Shows ratio to demonstrate information-weighted contribution
   - Saves g_eff(s) to CSV

### ✅ Figure Generation (Complete)

**`generate_countercurvature_figure.py`**: Creates 4-panel publication figure
- Panel A: Curvature profiles (κ_passive vs κ_info)
- Panel B: Countercurvature metric g_eff(s)
- Panel C: Geodesic deviation vs coupling strength
- Panel D: Microgravity adaptation

**Usage:**
```bash
python -m spinalmodes.experiments.countercurvature.generate_countercurvature_figure
```

### ✅ Documentation (Complete)

1. **`docs/mathematical_box_countercurvature.md`**: Ready-to-use Mathematical Box for papers
   - Plain text version
   - LaTeX source
   - Interpretation notes

2. **`docs/figure_plan_countercurvature.md`**: Figure layout and caption

3. **`docs/countercurvature_metrics.md`**: Technical documentation

## Quick Start

### Run Experiments

```bash
# Spine modes (flagship experiment)
python -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity

# Microgravity adaptation
python -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation

# Plant upward growth
python -m spinalmodes.experiments.countercurvature.experiment_plant_upward_growth
```

### Generate Figure

```bash
# After running experiments above
python -m spinalmodes.experiments.countercurvature.generate_countercurvature_figure
```

### Use Metrics in Code

```python
from spinalmodes.countercurvature import (
    InfoField1D,
    compute_countercurvature_metric,
    geodesic_curvature_deviation,
)

# Create info field
info = InfoField1D.from_array(s, I)

# Compute metric
g_eff = compute_countercurvature_metric(info, beta1=1.0, beta2=0.5)

# Compute geodesic deviation
geo = geodesic_curvature_deviation(
    s, kappa_passive, kappa_info, g_eff
)

print(f"D_geo_norm = {geo['D_geo_norm']:.6f}")
```

## Output Files

### CSV Files

- `outputs/experiments/spine_modes/spine_modes_summary.csv`
  - Columns: `chi_kappa`, `chi_E`, `D_geo`, `D_geo_norm`, `base_energy`, ...
  
- `outputs/experiments/microgravity/microgravity_summary.csv`
  - Columns: `gravity`, `gravity_label`, `D_geo`, `D_geo_norm`, ...

- `outputs/experiments/plant_growth/plant_growth_results.csv`
  - Columns: `s`, `I`, `dIds`, `g_eff`, `kappa_passive`, `kappa_info`, ...

### Figures

- `outputs/figs/fig_countercurvature_metrics.png` (4-panel publication figure)
- Individual experiment figures in respective output directories

## Key Metrics Explained

### D_geo (Geodesic Curvature Deviation)

Absolute measure of how far information-driven curvature deviates from passive curvature, weighted by the countercurvature metric:

```
D_geo² = ∫ g_eff(s) · [κ_info(s) - κ_passive(s)]² ds
```

**Units:** 1/m

### D_geo_norm (Normalized Geodesic Deviation)

Dimensionless version normalized by passive curvature energy:

```
D̂_geo = D_geo / √(∫ g_eff(s) · κ_passive(s)² ds)
```

**Use cases:**
- Compare across subjects/individuals
- Track changes across gravity levels
- Distinguish pathologies
- Study developmental stages
- Validate parameter sweeps

### g_eff(s) (Countercurvature Metric)

Information-weighted conformal factor on the 1D arc-length manifold:

```
g_eff(s) = exp(2φ(s))
φ(s) = β₁·Ĩ_centered + β₂·Ĩ'
```

**Interpretation:**
- High g_eff → strong information processing → larger metric weight
- Low g_eff → baseline gravitational geometry

## Next Steps

1. **Run experiments** to generate data
2. **Generate figure** from CSV outputs
3. **Write Results section** using D_geo_norm as quantitative axis
4. **Include Mathematical Box** in paper/manuscript
5. **Extend to 3D** (full Cosserat rod with torsion)

## Theory Connection

This framework implements the "biological countercurvature of spacetime" hypothesis:

- **Passive solution** κ₀(s) = gravity-selected geodesic
- **Info-driven solution** κ_I(s) = information-selected geodesic in countercurvature metric
- **D_geo** = distance between geodesics in the information-weighted metric

This provides a computational tool for exploring how biological information processing reshapes the effective geometry experienced by living structures.

