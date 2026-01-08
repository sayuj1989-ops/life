# Figure Plan: Biological Countercurvature Metrics

This document outlines the figure layout for publication-ready visualization of countercurvature metrics.

## Figure Layout (4 Panels)

### Panel A: Curvature Profiles

**Content:**
- x-axis: `s/L` (normalized arc-length)
- y-axis: κ(s) (1/m or normalized)
- Curves:
  - `κ_passive(s)` (gravity-only, blue)
  - `κ_info(s)` (info-coupled, red)
- Annotations:
  - Mark inflection points
  - Label lordosis/kyphosis peaks (for spine experiments)

**Interpretation:**
Shows the raw curvature profiles that will be compared in the metric.

**Data source:**
From `experiment_spine_modes_vs_gravity.py` or `experiment_plant_upward_growth.py`

---

### Panel B: Countercurvature Metric

**Content:**
- x-axis: `s/L` (normalized arc-length)
- y-axis: `g_eff(s)` (log scale)
- Curves:
  - `g_eff(s)` (purple, main axis)
  - `I(s)` (green, secondary axis, optional)
  - `∂I/∂s` (orange, secondary axis, optional)
- Reference line: `g_eff = 1` (flat metric, dashed)

**Interpretation:**
Shows where information processing is most active (high `g_eff`). These regions contribute disproportionately to geodesic deviation.

**Data source:**
From `compute_countercurvature_metric()` output

---

### Panel C: Geodesic Deviation vs Coupling Strength

**Content:**
- x-axis: χ_κ (coupling strength)
- y-axis: `D_geo_norm` (normalized geodesic deviation)
- Curve: `D_geo_norm(χ_κ)` (green line with markers)
- Optional overlays:
  - Different gravity levels (different colors)
  - Normal vs pathology (different line styles)

**Interpretation:**
Quantitative measure of how strongly information coupling reshapes curvature away from gravity-selected mode.

**Data source:**
From `experiment_spine_modes_vs_gravity.py` summary CSV

---

### Panel D: Microgravity Adaptation

**Content:**
- x-axis: Gravity (m/s², log scale)
- y-axis: `D_geo_norm`
- Curve: `D_geo_norm(g)` (orange line with markers)
- Annotation: Text box "Info-driven structure persists as g → 0"

**Interpretation:**
Demonstrates that information-driven structure persists even when gravitational loading is reduced. This is the key signature of "biological countercurvature of spacetime."

**Data source:**
From `experiment_microgravity_adaptation.py` summary CSV

---

## Implementation

The figure can be generated using:

```bash
python -m spinalmodes.experiments.countercurvature.generate_countercurvature_figure
```

This script:
1. Loads CSV data from the experiments
2. Generates all 4 panels
3. Saves to `outputs/figs/fig_countercurvature_metrics.png`

## Figure Caption (Draft)

> **Figure X: Biological Countercurvature Metrics**
>
> (A) Curvature profiles for passive (gravity-only) and information-coupled configurations. (B) Countercurvature metric `g_eff(s)` encoding information-driven geometry modifications. Regions with high information density or gradients have larger metric weight. (C) Normalized geodesic deviation `D̂_geo` as a function of coupling strength χ_κ. (D) Geodesic deviation persists as gravity is reduced, demonstrating that information-driven structure is maintained independently of gravitational loading—a signature of biological countercurvature of spacetime.

## Paper Integration

This figure supports the narrative:

1. **Information fields** (IEC model) create spatially varying geometry (`g_eff(s)`)
2. **Curvature profiles** deviate from gravity-selected modes in information-weighted metric
3. **Geodesic deviation** (`D_geo_norm`) quantifies this deviation as a single scalar
4. **Microgravity persistence** shows information-driven structure is independent of gravitational curvature

This provides a computational bridge between:
- Mechanical simulations (PyElastica)
- Information processing (IEC)
- Riemannian geometry (countercurvature metric)
- Quantitative metrics (geodesic deviation)

