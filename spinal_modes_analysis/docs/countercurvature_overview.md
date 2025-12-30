# Biological Countercurvature of Spacetime: Overview

## Conceptual Framework

We model consciousness and biological intelligence as information flows `I(s, t)` that generate an effective **"biological countercurvature"** of spacetime. Practically, we implement `I(s, t)` as fields that reshape rest curvature, stiffness, and active moments in a Cosserat rod under gravity. The resulting modes (upward growth, stabilized S-shaped spines, microgravity adaptation) are analog models of information-modified curvature.

### Theoretical Context

The hypothesis draws an analogy between:

- **Newtonian mechanics**: Gravity as a force from falling objects
- **Einsteinian relativity**: Gravity as curvature of spacetime
- **Biological systems**: Information processing as a local, information-driven **counter-curvature** that shapes the geometry experienced by the body

Living systems (plants growing upward, vertebrate spines, neural structures in microgravity) systematically generate organized structure against or beyond naive gravitational sag. The **information dynamics** behind life and consciousness modulate an effective curvature field—not literally rewriting General Relativity, but acting like a local, information-driven counter-curvature that shapes the geometry experienced by the body.

### Implementation

We use **Cosserat rod mechanics as an analog spacetime** in which an **information field** modifies:

1. **Rest curvature** `κ_rest(s) = κ_gen(s) + χ_κ · ∂I/∂s`
2. **Effective stiffness** `EI(s) = E₀ · f_E(I(s))`
3. **Active moments** `M_info(s) = χ_M · ∂I/∂s`

This is what we call "biological countercurvature."

## Package Structure

The countercurvature implementation is located in `src/spinalmodes/countercurvature/`:

- **`info_fields.py`**: Data structures for information fields `I(s)` and their gradients
- **`coupling.py`**: Functions that map information to mechanical parameters (rest curvature, stiffness, active moments)
- **`pyelastica_bridge.py`**: PyElastica integration for Cosserat rod simulations
- **`validation_and_metrics.py`**: Metrics quantifying countercurvature effects

### Quickstart (one minute)

- Run the end-to-end demo: `python examples/quickstart.py`
- Fast spine sweep: `python -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity --quick`
- Quick phase map: `python -m spinalmodes.experiments.countercurvature.experiment_phase_diagram --quick`

## Experiments

Three reproducible experiments demonstrate biological countercurvature:

### 1. Plant Upward Growth

**Script**: `src/spinalmodes/experiments/countercurvature/experiment_plant_upward_growth.py`

**Description**: Models a slender rod (plant stem) clamped at the base under gravity.

- **Case A**: No information coupling → rod sags with gravity
- **Case B**: Information-driven countercurvature → rod bends upward, mimicking plant growth

**Run**:
```bash
python -m spinalmodes.experiments.countercurvature.experiment_plant_upward_growth
```

**Outputs**:
- `outputs/experiments/plant_growth/plant_growth_results.csv`
- `outputs/experiments/plant_growth/plant_growth_figure.png`

### 2. Spine Modes vs Gravity

**Script**: `src/spinalmodes/experiments/countercurvature/experiment_spine_modes_vs_gravity.py`

**Description**: Uses IEC-style `κ_gen(s)` approximating a human spine's lordosis/kyphosis profile. Adds an `InfoField1D` representing neural/postural control. Sweeps coupling parameters (`χ_κ`, `χ_E`) and simulates:

- No coupling (control, gravity-selected mode)
- Moderate coupling
- Strong coupling

**Run**:
```bash
python -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity
```

**Outputs**:
- `outputs/experiments/spine_modes/spine_modes_results.csv`
- `outputs/experiments/spine_modes/spine_modes_summary.csv`
- `outputs/experiments/spine_modes/spine_modes_figure.png`

**Metrics computed**:
- Lordosis/kyphosis angles
- Positions of inflection points
- Countercurvature index = deviation from passive gravitational shape

### 3. Microgravity Adaptation

**Script**: `src/spinalmodes/experiments/countercurvature/experiment_microgravity_adaptation.py`

**Description**: Runs the same information field `I(s)` in:

- 1g (Earth)
- 0.1g
- ~0g (microgravity)

**Key finding**: In low gravity, shape is maintained largely by information coupling, not gravity. This is interpreted as "Information-driven structure persists when gravitational curvature is reduced" — an analog to biological countercurvature of spacetime.

**Run**:
```bash
python -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation
```

**Outputs**:
- `outputs/experiments/microgravity/microgravity_results.csv`
- `outputs/experiments/microgravity/microgravity_summary.csv`
- `outputs/experiments/microgravity/microgravity_figure.png`

## Usage Example

```python
from spinalmodes.countercurvature import (
    InfoField1D,
    CounterCurvatureParams,
    make_uniform_grid,
)
from spinalmodes.countercurvature.coupling import (
    compute_rest_curvature,
    compute_effective_stiffness,
    compute_active_moments,
)

# Create information field
s = make_uniform_grid(length=0.5, n_points=100)
I = 1.0 - 0.5 * (s / s[-1])  # Linear gradient
info = InfoField1D.from_array(s, I)

# Set coupling parameters
params = CounterCurvatureParams(
    chi_kappa=0.05,  # Information → rest curvature
    chi_E=0.1,       # Information → stiffness
    chi_M=0.0,       # Information → active moment
)

# Compute countercurvature-modified properties
kappa_gen = np.zeros_like(s)
kappa_rest = compute_rest_curvature(info, params, kappa_gen)
E_eff = compute_effective_stiffness(info, params, E0=1e9)
M_info = compute_active_moments(info, params)

# Use with beam solver or PyElastica
from spinalmodes.iec import solve_beam_static
theta, kappa = solve_beam_static(s, kappa_rest, E_eff, M_info)
```

## Dependencies

### Required
- `numpy >= 1.24.0`
- `scipy >= 1.11.0`
- `matplotlib >= 3.7.0`
- `pandas >= 2.0.0`

### Optional
- `pyelastica`: For full Cosserat rod simulations (install with `pip install pyelastica`)

The experiments work with the existing beam/BVP solver if PyElastica is not available.

## Metrics and Validation

The `validation_and_metrics` module provides:

- **`compute_countercurvature_energy()`**: Energy-like metric quantifying deviation from passive gravitational equilibrium
- **`compute_effective_metric_deviation()`**: L2 norm of curvature deviation, interpreted as metric deviation
- **`compute_shape_preservation_index()`**: How well information preserves shape against gravitational sag
- **`compare_with_beam_solver()`**: Validation against existing beam/BVP solver

## Theory References

The biological countercurvature hypothesis is developed as an analog model connecting:

1. **Information processing** (growth programmes, neural control, consciousness)
2. **Mechanical curvature** (rest curvature, stiffness, active moments)
3. **Spacetime geometry** (effective metric modifications)

This framework provides a computational tool for exploring how biological information processing might reshape the effective geometry experienced by living structures, with applications to:

- Plant growth and gravitropism
- Spinal curvature and postural control
- Neural structure in microgravity
- Consciousness as information-driven geometry

## Future Extensions

- Full 3D Cosserat rod implementation with torsion
- Time-dependent information fields `I(s, t)`
- Coupling to neural activity data
- Validation against experimental biomechanical data
- Extension to full General Relativity analog (beyond scope of current implementation)
