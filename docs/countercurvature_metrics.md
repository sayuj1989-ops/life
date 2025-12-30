# Countercurvature Metrics: Mathematical Definitions

This document provides the mathematical definitions and implementation details for the countercurvature metrics implemented in `spinalmodes.countercurvature.validation_and_metrics`.

## 1. Countercurvature Metric g_eff(s)

### Definition

The biological countercurvature metric is a Riemannian metric on the 1D arc-length manifold that encodes how information processing reshapes the effective geometry experienced by the rod:

```
dℓ_eff² = g_eff(s) · ds²
```

where `g_eff(s) = exp(2φ(s))` and `φ(s)` depends on normalized information density `I(s)` and its gradient `∂I/∂s`.

### Construction

1. **Normalize information density** to [0, 1]:
   ```
   Ĩ(s) = (I(s) - I_min) / (I_max - I_min + ε)
   ```

2. **Center the normalized field**:
   ```
   Ĩ_centered = Ĩ - ⟨Ĩ⟩
   ```
   where `⟨Ĩ⟩` is the mean over `s`.

3. **Normalize the gradient**:
   ```
   Ĩ'(s) = (∂I/∂s) / (max|∂I/∂s| + ε)
   ```

4. **Build the field** `φ(s)`:
   ```
   φ(s) = β₁·Ĩ_centered + β₂·Ĩ'
   ```
   where `β₁` and `β₂` are tuning parameters (defaults: `β₁=1.0`, `β₂=0.5`).

5. **Conformal metric factor**:
   ```
   g_eff(s) = exp(2φ(s))
   ```

### Interpretation

- Where `I(s)` and its gradient are high, `φ(s)` is large → local "space" is effectively **stretched** or **weighted** more.
- Where information is low/flat, `g_eff ≈ 1` → recover the ordinary gravitational background.

This implements the "biological countercurvature of spacetime" as a phenomenological Riemannian metric on the rod's arc-length coordinate.

### Usage

```python
from spinalmodes.countercurvature import (
    InfoField1D,
    compute_countercurvature_metric,
)

# Create information field
info = InfoField1D.from_array(s, I)

# Compute metric
g_eff = compute_countercurvature_metric(
    info,
    beta1=1.0,  # Information density coupling
    beta2=0.5,  # Information gradient coupling
)
```

## 2. Geodesic Curvature Deviation D_geo

### Definition

The geodesic curvature deviation measures how far the information-shaped curvature `κ_info(s)` deviates from the gravity-selected curvature `κ_passive(s)`, measured in the Riemannian metric `g_eff(s)`. This is the geodesic distance between the two curvature profiles in the space of curvature functions weighted by the countercurvature metric.

### Formula

**Squared geodesic deviation**:
```
D_geo² = ∫₀ᴸ g_eff(s) · [κ_info(s) - κ_passive(s)]² ds
```

**Geodesic deviation**:
```
D_geo = √(D_geo²)
```

**Normalized version**:
```
D̂_geo = D_geo / (√(∫₀ᴸ g_eff(s) · κ_passive(s)² ds) + ε)
```

### Interpretation

- **D_geo ≈ 0**: Information field is not reshaping the gravitational geodesic.
- **D_geo large**: Information is strongly "bending" curvature away from the gravity-selected mode.
- Regions where information is strong (large `g_eff`) contribute disproportionately to the distance.

### Usage

```python
from spinalmodes.countercurvature import geodesic_curvature_deviation

# Compute deviation
results = geodesic_curvature_deviation(
    s=s,
    kappa_passive=kappa_passive,
    kappa_info=kappa_info,
    g_eff=g_eff,
)

print(f"D_geo = {results['D_geo']:.6f} 1/m")
print(f"D_geo_norm = {results['D_geo_norm']:.6f}")
```

### Return Values

The function returns a dictionary with:
- `"D_geo"`: Geodesic curvature deviation (1/m)
- `"D_geo_sq"`: Squared geodesic deviation (1/m²)
- `"D_geo_norm"`: Normalized geodesic deviation (dimensionless)
- `"base_energy"`: Passive curvature energy in metric (1/m²)

## 3. Applications

The geodesic curvature deviation `D_geo` provides a single scalar that can be compared across:

- **Subjects/individuals**: Compare countercurvature strength across different people
- **Gravity levels**: 1g vs micro-g (see `experiment_microgravity_adaptation.py`)
- **Pathologies**: Scoliosis vs normal spine
- **Developmental stages**: Growth and aging
- **Parameter sweeps**: Vary `χ_κ`, `χ_E`, etc. (see `experiment_spine_modes_vs_gravity.py`)

## 4. Example Workflow

```python
import numpy as np
from spinalmodes.countercurvature import (
    InfoField1D,
    make_uniform_grid,
    compute_countercurvature_metric,
    geodesic_curvature_deviation,
)
from spinalmodes.iec import solve_beam_static

# 1. Create spatial grid and information field
s = make_uniform_grid(length=0.4, n_points=100)
I = 0.5 + 0.3 * np.exp(-((s / s[-1] - 0.3) ** 2) / (2 * 0.1**2))
info = InfoField1D.from_array(s, I)

# 2. Run passive simulation (no info coupling)
kappa_passive = ...  # From solve_beam_static with chi_kappa=0

# 3. Run info-driven simulation (with coupling)
kappa_info = ...  # From solve_beam_static with chi_kappa>0

# 4. Compute countercurvature metric
g_eff = compute_countercurvature_metric(info, beta1=1.0, beta2=0.5)

# 5. Compute geodesic deviation
deviation = geodesic_curvature_deviation(
    s, kappa_passive, kappa_info, g_eff
)

print(f"Geodesic deviation: {deviation['D_geo']:.6f} 1/m")
print(f"Normalized: {deviation['D_geo_norm']:.6f}")
```

## 5. Theory Connection

The countercurvature metric and geodesic deviation provide a **clean bridge** between:

- **PyElastica** → concrete curves & `κ(s)`
- **IEC** → information fields `I(s)`
- **g_eff(s)** → Riemannian language ("countercurvature metric")
- **D_geo** → single number comparable across conditions

This implements the "biological countercurvature of spacetime" hypothesis as a computational tool for exploring how information processing reshapes the effective geometry experienced by living structures.

## References

See `docs/countercurvature_overview.md` for the broader theoretical context and `src/spinalmodes/experiments/countercurvature/example_countercurvature_metrics.py` for a complete working example.

