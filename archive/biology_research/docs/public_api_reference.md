# Public API Reference

## Core Countercurvature API

The `spinalmodes.countercurvature` package provides a stable public API for biological countercurvature simulations. This API is suitable for:

- **Methods sections**: Reference specific functions in papers
- **Future notebooks**: Use as a library
- **Student projects**: Build on top of the framework
- **Version stability**: API will be maintained across minor version bumps

---

## Import Pattern

```python
from spinalmodes.countercurvature import (
    InfoField1D,
    CounterCurvatureParams,
    compute_rest_curvature,
    compute_countercurvature_metric,
    geodesic_curvature_deviation,
    CounterCurvatureRodSystem,
    compute_scoliosis_metrics,
    classify_scoliotic_regime,
)
from spinalmodes import solve_beam_static  # Re-exported from spinalmodes.iec
```

---

## Core Data Structures

### `InfoField1D`

1D information field container with arc-length coordinate, information density, and gradient.

```python
from spinalmodes.countercurvature import InfoField1D, make_uniform_grid

s = make_uniform_grid(length=0.4, n_points=100)
I = 0.5 + 0.3 * np.exp(-((s - 0.2)**2) / (2 * 0.1**2))
info = InfoField1D.from_array(s, I)
```

**Attributes:**
- `s`: Arc-length coordinates (m)
- `I`: Information density (dimensionless)
- `dIds`: Gradient ∂I/∂s (1/m)
- `n_points`: Number of points

---

### `CounterCurvatureParams`

Coupling parameters for information-to-mechanics mapping.

```python
from spinalmodes.countercurvature import CounterCurvatureParams

params = CounterCurvatureParams(
    chi_kappa=0.03,  # Information-to-curvature coupling
    chi_E=0.1,      # Information-to-stiffness coupling
    chi_M=0.0,      # Information-to-active-moment coupling
    scale_length=0.4  # Rod length for normalization
)
```

**Attributes:**
- `chi_kappa`: Curvature coupling strength (1/m)
- `chi_E`: Stiffness coupling strength (dimensionless)
- `chi_M`: Active moment coupling strength (N·m per unit gradient)
- `scale_length`: Length scale for normalization (m)

---

## Coupling Functions

### `compute_rest_curvature`

Maps information field to rest curvature via IEC-1 coupling.

```python
from spinalmodes.countercurvature.coupling import compute_rest_curvature

kappa_rest = compute_rest_curvature(
    info_field, params, kappa_gen=np.zeros_like(s)
)
```

**Formula**: κ_rest(s) = κ_gen(s) + χ_κ · ∂I/∂s

---

### `compute_effective_stiffness`

Maps information field to effective stiffness via IEC-2 coupling.

```python
from spinalmodes.countercurvature.coupling import compute_effective_stiffness

E_eff = compute_effective_stiffness(
    info_field, params, E0=1e9, model="linear"
)
```

**Formula**: E_eff(s) = E₀ · (1 + χ_E · I(s))

---

### `compute_active_moments`

Maps information gradient to active moments via IEC-3 coupling.

```python
from spinalmodes.countercurvature.coupling import compute_active_moments

M_info = compute_active_moments(info_field, params)
```

**Formula**: M_info(s) = χ_M · ∂I/∂s

---

## Countercurvature Metrics

### `compute_countercurvature_metric`

Computes the biological countercurvature metric g_eff(s).

```python
from spinalmodes.countercurvature import compute_countercurvature_metric

g_eff = compute_countercurvature_metric(
    info_field, beta1=1.0, beta2=0.5
)
```

**Formula**: g_eff(s) = exp(2φ(s)) where φ(s) = β₁·Ĩ_centered + β₂·Ĩ'

**Returns**: Array of g_eff(s) values, shape (n_points,)

---

### `geodesic_curvature_deviation`

Measures information-driven deviation from gravity-selected curvature.

```python
from spinalmodes.countercurvature import geodesic_curvature_deviation

metrics = geodesic_curvature_deviation(
    s, kappa_passive, kappa_info, g_eff
)
# Returns: {"D_geo": float, "D_geo_sq": float, "D_geo_norm": float, "base_energy": float}
```

**Formula**: D_geo² = ∫ g_eff(s) [κ_info(s) - κ_passive(s)]² ds

**Returns**: Dictionary with D_geo, D_geo_sq, D_geo_norm, base_energy

---

## PyElastica Integration

### `CounterCurvatureRodSystem`

PyElastica Cosserat rod system with information-driven countercurvature.

```python
from spinalmodes.countercurvature import CounterCurvatureRodSystem

rod_system = CounterCurvatureRodSystem.from_iec(
    info=info_field,
    params=params,
    length=0.4,
    n_elements=50,
    E0=1e9,
    rho=1000.0,
    radius=0.01,
    gravity=9.81,
)

result = rod_system.run_simulation(
    final_time=2.0,
    dt=1e-4,
    save_every=100,
    gravity=9.81,
)
```

**Returns**: `SimulationResult` with `time`, `centerline`, `curvature`, `info_field`

---

## Scoliosis Metrics

### `compute_scoliosis_metrics`

Computes lateral scoliosis index and Cobb-like angle from coronal-plane coordinates.

```python
from spinalmodes.countercurvature import compute_scoliosis_metrics

metrics = compute_scoliosis_metrics(z, y, frac=0.2)
# Returns: ScoliosisMetrics(S_lat, y_tip, lat_dev_max, cobb_like_deg)
```

**Inputs:**
- `z`: Longitudinal (cranio-caudal) coordinates
- `y`: Lateral (left-right) coordinates
- `frac`: Fraction of points for Cobb-like angle (default 0.2)

**Returns**: `ScoliosisMetrics` dataclass

---

### `classify_scoliotic_regime`

Classifies gravity-dominated, cooperative, and scoliotic regimes.

```python
from spinalmodes.countercurvature import (
    classify_scoliotic_regime,
    RegimeThresholds,
)

flags = classify_scoliotic_regime(
    D_geo_norm_sym=0.25,
    metrics_sym=metrics_sym,
    metrics_asym=metrics_asym,
    thresholds=RegimeThresholds(),  # Optional: use defaults
)
# Returns: {"gravity_dominated": bool, "cooperative": bool, "scoliotic_regime": bool}
```

---

## Beam Solver

### `solve_beam_static`

Solves static beam equilibrium with IEC couplings (re-exported from `spinalmodes.iec`).

```python
from spinalmodes import solve_beam_static

theta, kappa = solve_beam_static(
    s,
    kappa_target,
    E_field,
    M_active,
    I_moment=1e-8,
    P_load=0.0,
    distributed_load=100.0,
)
```

**Returns**: Tuple of (theta, kappa) where theta is deflection angle and kappa is curvature

---

## Version Information

```python
from spinalmodes import __version__
print(__version__)  # "0.1.0"
```

---

## Usage in Methods Section

When writing the Methods section, you can reference:

> "All simulations were implemented in the `spinalmodes` package (version 0.1.0). Information fields I(s) were constructed using `InfoField1D`, and countercurvature-modified mechanical properties were computed via `compute_rest_curvature`, `compute_effective_stiffness`, and `compute_active_moments`. The countercurvature metric g_eff(s) was computed using `compute_countercurvature_metric`, and geodesic curvature deviation D̂_geo was measured using `geodesic_curvature_deviation`. Scoliosis metrics (S_lat, Cobb-like angles) were computed using `compute_scoliosis_metrics` from coronal-plane centerline coordinates."

---

## Stability Guarantees

- **Version 0.1.x**: API is stable; functions will not be removed or have breaking signature changes
- **Version 0.2.x**: May add new optional parameters, but existing calls will continue to work
- **Version 1.0.0+**: Full semantic versioning applies

---

## See Also

- `examples/quickstart.py` - Minimal working example
- `examples/quickstart.ipynb` - Jupyter notebook version
- `src/spinalmodes/experiments/countercurvature/` - Full experiment scripts
- `docs/` - Detailed documentation

