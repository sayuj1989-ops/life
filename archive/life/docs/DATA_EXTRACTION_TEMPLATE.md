# Data Extraction Template: Anchor Numbers for Paper

## Purpose

This document provides a structured template for extracting specific quantitative values from simulation outputs. These "anchor numbers" will be referenced explicitly in the Abstract, Results, and Discussion sections.

---

## 1. Microgravity Series

### Target Values

For 3–4 representative gravity levels, extract:

| g | Passive Energy | D_geo | D_geo_norm | Notes |
|---|----------------|-------|------------|-------|
| 1.0 | | | | Baseline |
| 0.3 | | | | Moderate reduction |
| 0.1 | | | | Significant reduction |
| 0.01 | | | | Near-zero gravity |

### Extraction Commands

```python
# From microgravity experiment output CSV
import pandas as pd
df = pd.read_csv('outputs/csv/microgravity_summary.csv')

# For each g value:
g_values = [1.0, 0.3, 0.1, 0.01]
for g in g_values:
    row = df[df['g'] == g].iloc[0]
    print(f"g={g}: passive_energy={row['passive_energy']:.4f}, "
          f"D_geo_norm={row['D_geo_norm']:.4f}")
```

### Target Sentences for Paper

> "As g decreased from 1.0 to 0.01, passive curvature energy fell by ~X%, while D̂_geo_norm changed by only Y%."

> "At g = 0.01, passive curvature energy was reduced by [X]% compared to 1g, yet D̂_geo_norm remained at [Y], demonstrating that information-driven structure persists independently of gravitational loading."

### Calculations Needed

- **Percentage change in passive energy**: `(E_passive(g=0.01) - E_passive(g=1.0)) / E_passive(g=1.0) * 100`
- **Percentage change in D_geo_norm**: `(D_geo_norm(g=0.01) - D_geo_norm(g=1.0)) / D_geo_norm(g=1.0) * 100`
- **Ratio**: `D_geo_norm(g=0.01) / D_geo_norm(g=1.0)`

---

## 2. Scoliosis Branch Comparison

### Target Values

For symmetric vs asymmetric runs in two regimes:

#### Gravity-Dominated Regime
(Example: `chi_kappa = 0.01`, `g = 1.0`)

| Metric | Symmetric (ε=0) | Asymmetric (ε=0.05) | Change |
|--------|-----------------|---------------------|--------|
| S_lat | | | |
| Cobb_like_deg | | | |
| D_geo_norm | | | (same for both) |

#### Information-Dominated Regime
(Example: `chi_kappa = 0.05`, `g = 0.1`)

| Metric | Symmetric (ε=0) | Asymmetric (ε=0.05) | Change |
|--------|-----------------|---------------------|--------|
| S_lat | | | |
| Cobb_like_deg | | | |
| D_geo_norm | | | (same for both) |

### Extraction Commands

```python
# From phase diagram or spine experiment output
df = pd.read_csv('outputs/csv/phase_diagram_summary.csv')

# Gravity-dominated case
row_gd = df[(df['chi_kappa'] == 0.01) & (df['g'] == 1.0)].iloc[0]
print(f"Gravity-dominated: S_lat_sym={row_gd['S_lat_sym']:.4f}, "
      f"S_lat_asym={row_gd['S_lat_asym']:.4f}, "
      f"delta_S_lat={row_gd['S_lat_asym'] - row_gd['S_lat_sym']:.4f}")

# Information-dominated case
row_id = df[(df['chi_kappa'] == 0.05) & (df['g'] == 0.1)].iloc[0]
print(f"Information-dominated: S_lat_sym={row_id['S_lat_sym']:.4f}, "
      f"S_lat_asym={row_id['S_lat_asym']:.4f}, "
      f"delta_S_lat={row_id['S_lat_asym'] - row_id['S_lat_sym']:.4f}")
```

### Target Sentences for Paper

> "In the gravity-dominated regime (χ_κ = 0.01, g = 1.0), a 5% thoracic perturbation changes S_lat by <0.01 and Cobb-like angle by <3°. In the information-dominated regime (χ_κ = 0.05, g = 0.1), the same perturbation yields S_lat ≳ 0.05 and Cobb-like angles >10°."

> "The amplification factor (S_lat_asym / S_lat_sym) increases from ~[X] in the gravity-dominated regime to ~[Y] in the information-dominated regime, demonstrating the sensitivity of the system to small asymmetries when information-driven countercurvature dominates."

### Calculations Needed

- **Delta S_lat**: `S_lat_asym - S_lat_sym`
- **Delta Cobb**: `Cobb_asym - Cobb_sym`
- **Amplification factor**: `S_lat_asym / S_lat_sym` (when S_lat_sym > 0)
- **Relative change**: `(S_lat_asym - S_lat_sym) / S_lat_sym * 100`

---

## 3. Phase Diagram Anchor Points

### Three Representative Points

#### Point 1: "Normally-curved, stable"
(Example: `chi_kappa = 0.01`, `g = 1.0`)

| Parameter | Value |
|-----------|-------|
| χ_κ | |
| g | |
| D_geo_norm | |
| S_lat_asym | |
| Cobb_asym (deg) | |
| Regime | gravity-dominated |

#### Point 2: "Borderline cooperative"
(Example: `chi_kappa = 0.03`, `g = 0.5`)

| Parameter | Value |
|-----------|-------|
| χ_κ | |
| g | |
| D_geo_norm | |
| S_lat_asym | |
| Cobb_asym (deg) | |
| Regime | cooperative |

#### Point 3: "Scoliotic regime"
(Example: `chi_kappa = 0.05`, `g = 0.1`)

| Parameter | Value |
|-----------|-------|
| χ_κ | |
| g | |
| D_geo_norm | |
| S_lat_asym | |
| Cobb_asym (deg) | |
| Regime | scoliotic |

### Extraction Commands

```python
# From phase diagram summary
df = pd.read_csv('outputs/csv/phase_diagram_summary.csv')

points = [
    {'chi_kappa': 0.01, 'g': 1.0, 'label': 'Normal'},
    {'chi_kappa': 0.03, 'g': 0.5, 'label': 'Borderline'},
    {'chi_kappa': 0.05, 'g': 0.1, 'label': 'Scoliotic'},
]

for pt in points:
    row = df[(df['chi_kappa'] == pt['chi_kappa']) & 
             (df['g'] == pt['g'])].iloc[0]
    print(f"{pt['label']}: (χ_κ={pt['chi_kappa']}, g={pt['g']})")
    print(f"  D_geo_norm={row['D_geo_norm']:.4f}")
    print(f"  S_lat_asym={row['S_lat_asym']:.4f}")
    print(f"  Cobb_asym={row['cobb_asym_deg']:.2f}°")
    print(f"  Regime={row['regime']}")
```

### Target Sentences for Paper

> "Three representative points illustrate the phase diagram: (1) Normal curvature (χ_κ = 0.01, g = 1.0) with D̂_geo_norm = [X] and S_lat < 0.01; (2) Borderline cooperative (χ_κ = 0.03, g = 0.5) with D̂_geo_norm = [Y]; and (3) Scoliotic regime (χ_κ = 0.05, g = 0.1) with D̂_geo_norm = [Z] and Cobb-like angles >10°."

---

## 4. Plant Experiment

### Target Values

| Parameter | Value |
|-----------|-------|
| D_geo_norm | |
| L2_norm | |
| Ratio (D_geo_norm / L2_norm) | |

### Target Sentence

> "In the plant growth experiment, D̂_geo_norm = [X] compared to a plain L2 norm of [Y], yielding a ratio of [Z], confirming that information-dense regions contribute disproportionately to curvature deviation."

---

## 5. Spine Modes Sweep

### Target Values

For `chi_kappa` sweep at `g = 1.0`:

| χ_κ | D_geo_norm |
|-----|------------|
| 0.0 | 0.0 (baseline) |
| 0.01 | |
| 0.02 | |
| 0.03 | |
| 0.04 | |
| 0.05 | |

### Target Sentence

> "As χ_κ increased from 0 to 0.05 at 1g, D̂_geo_norm increased from 0 to [X], demonstrating a monotonic relationship between information coupling strength and deviation from gravity-selected curvature."

---

## Usage Instructions

1. **Run experiments** and generate CSV outputs
2. **Extract values** using the commands above (or adapt to your CSV structure)
3. **Fill in tables** in this document
4. **Copy values** into paper drafts, replacing placeholder text
5. **Verify** that all referenced numbers match extracted values

---

## Quality Checks

Before finalizing paper:

- [ ] All numbers in Abstract match extracted values
- [ ] All numbers in Results match extracted values
- [ ] Percentage changes are calculated correctly
- [ ] Units are consistent (degrees for Cobb, dimensionless for S_lat, etc.)
- [ ] Significant figures are appropriate (2-3 decimal places for most metrics)
- [ ] Ranges are specified (e.g., ">10°" not just "10°")

