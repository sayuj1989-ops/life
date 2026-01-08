# Scientific Predictions: Testable Statements from Countercurvature Framework

## Overview

The countercurvature metrics framework enables sharp, testable predictions. Here we outline three key predictions and how to test them computationally.

---

## Prediction 1: Information Persistence in Microgravity

### Statement

> As gravitational loading is reduced, passive curvature collapses, but normalized geodesic deviation D̂_geo remains roughly constant or increases. This demonstrates that information-driven structure is maintained independently of gravitational curvature.

### Test

Run `experiment_microgravity_adaptation` with extended gravity range:

```python
gravity_values = [9.81, 4.9, 2.0, 1.0, 0.5, 0.2, 0.1, 0.05, 0.01, 0.005]
```

### Expected Results

- **Passive curvature energy**: Monotonically decreases as g → 0
- **D̂_geo**: Remains > 0.1 even at 0.01g, demonstrating information persistence
- **Ratio D̂_geo / passive_energy**: Increases dramatically as g → 0

### Interpretation

This is the numerical signature of "information maintaining structure when gravitational curvature is reduced"—the core prediction of biological countercurvature.

### Visualization

- Panel A: Passive energy vs g (log scale, decreasing)
- Panel B: D̂_geo vs g (log scale, roughly constant)
- Panel C: Ratio vs g (log scale, increasing)

---

## Prediction 2: Scoliosis as Countercurvature Failure

### Statement

> Small lateral asymmetries in κ_gen or I(s) lead to large lateral deviations when countercurvature strength χ_κ is insufficient. This creates a bifurcation diagram: normal vs scoliosis-like branch, controlled by countercurvature strength.

### Test

Modify `experiment_spine_modes_vs_gravity` to:

1. Add lateral asymmetry to κ_gen:
   ```python
   kappa_gen_lateral = kappa_gen + asymmetry * np.sin(2 * np.pi * s / length)
   ```

2. Sweep both χ_κ and asymmetry:
   ```python
   chi_kappa_values = np.linspace(0.0, 0.08, 20)
   asymmetry_values = np.linspace(0.0, 0.05, 10)
   ```

3. Compute lateral deviation metric:
   ```python
   lateral_deviation = np.max(np.abs(centerline[:, 1]))  # Max y-coordinate
   ```

### Expected Results

- **Low χ_κ + high asymmetry**: Large lateral deviation → scoliosis-like branch
- **High χ_κ + high asymmetry**: Small lateral deviation → normal branch maintained
- **Bifurcation point**: Critical χ_κ where small asymmetry causes large deviation

### Interpretation

Countercurvature strength determines stability against lateral perturbations. Insufficient countercurvature → pathological branch.

### Visualization

- Bifurcation diagram: lateral_deviation(χ_κ, asymmetry)
- Phase boundary separating normal vs scoliosis regimes

---

## Prediction 3: Plant-Like Growth Against Gravity

### Statement

> For certain parameter regions (basal information dominance, moderate χ_κ), information-driven configuration has net upward deflection despite gravity, while passive configuration always sags. The ratio D̂_geo / L2_norm > 1 indicates information-dense regions drive curvature deviation.

### Test

Modify `experiment_plant_upward_growth` to:

1. Vary information field shape:
   ```python
   # Basal dominance
   I_basal = 1.0 - 0.8 * s_norm
   
   # Apical dominance  
   I_apical = 0.2 + 0.8 * s_norm
   
   # Uniform
   I_uniform = 0.5 * np.ones_like(s)
   ```

2. Sweep χ_κ and χ_M:
   ```python
   chi_kappa_values = np.linspace(0.0, 0.1, 20)
   chi_M_values = np.linspace(0.0, 0.05, 10)
   ```

3. Compute upward angle:
   ```python
   tip_angle = np.arctan2(centerline[-1, 1], centerline[-1, 0])
   upward_deflection = tip_angle > 0  # Positive = upward
   ```

### Expected Results

- **Basal dominance + moderate χ_κ**: Upward deflection (tip_angle > 0)
- **Passive case**: Always downward (tip_angle < 0)
- **D̂_geo / L2_norm**: > 1.2 for successful upward growth cases

### Interpretation

Information field shape and coupling strength determine whether structure can grow against gravity—the plant growth paradigm.

### Visualization

- Parameter space map: upward_deflection(χ_κ, I_shape)
- Comparison: D̂_geo vs L2_norm showing information-weighted contribution

---

## Prediction 4: Phase Diagram Regimes

### Statement

> The phase diagram D̂_geo(χ_κ, g) reveals three distinct regimes: gravity-dominated (D̂_geo < 0.05), cooperative (0.05 < D̂_geo < 0.2), and information-dominated (D̂_geo > 0.2). The phase boundary shifts toward lower χ_κ as gravity decreases.

### Test

Run `experiment_phase_diagram` with:

```python
chi_kappa_values = np.linspace(0.0, 0.08, 20)
gravity_values = np.array([9.81, 4.9, 2.0, 1.0, 0.5, 0.2, 0.1, 0.05, 0.01])
```

### Expected Results

- **Phase boundaries**: Clear transitions at D̂_geo ≈ 0.05 and 0.2
- **Boundary shift**: Information-dominated region expands as g → 0
- **Critical point**: (χ_κ ≈ 0.04, g ≈ 0.1) where all three regimes meet

### Interpretation

The phase diagram provides a quantitative map of where "biological countercurvature of spacetime" is weak vs strong, enabling predictions about system behavior across parameter space.

### Visualization

- Contour plot: D̂_geo(χ_κ, g) with regime boundaries
- Overlay: Passive energy vs g showing collapse

---

## Implementation Status

- ✅ Prediction 1: Implemented in `experiment_microgravity_adaptation.py`
- ⏳ Prediction 2: Needs lateral asymmetry extension
- ⏳ Prediction 3: Needs information field shape sweep
- ✅ Prediction 4: Implemented in `experiment_phase_diagram.py`

---

## Next Steps

1. **Run phase diagram experiment** to generate full parameter sweep
2. **Extend microgravity experiment** to lower gravity values (0.005g)
3. **Add lateral asymmetry** to spine experiment for scoliosis prediction
4. **Add information field shape sweep** to plant experiment
5. **Generate all figures** and lock in quantitative values
6. **Write Results section** using these predictions

