# Full Sweeps + Anchor Number Extraction Guide

## Concrete Plan: Run Full Sweeps and Extract Numbers

This guide provides step-by-step instructions to run full parameter sweeps and extract quantitative anchor numbers for the manuscript.

---

## Step 1: Run Full Parameter Sweeps

**⚠️ Important: Remove `--quick` flags for publication-quality results**

### Commands to Run

```bash
# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# 1) Spine modes vs gravity (sagittal S-curve)
# Expected runtime: 5-10 minutes
python3 -m spinalmodes.experiments.countercurvature.experiment_spine_modes_vs_gravity

# 2) Microgravity adaptation
# Expected runtime: 10-15 minutes
python3 -m spinalmodes.experiments.countercurvature.experiment_microgravity_adaptation

# 3) Phase diagram + scoliosis regime
# Expected runtime: 20-40 minutes (depending on grid size)
python3 -m spinalmodes.experiments.countercurvature.experiment_phase_diagram

# 4) Generate final figure(s)
# Expected runtime: < 1 minute
python3 -m spinalmodes.experiments.countercurvature.generate_countercurvature_figure
```

**Note the output paths** - each script prints where it wrote CSVs and figures. These are your source of truth.

---

## Step 2: Extract Anchor Numbers

### Option A: Automated Extraction Script

**Use the provided script:**

```bash
python3 scripts/extract_anchor_numbers.py
```

This script will:
- Read all experiment CSV files
- Extract key metrics
- Print formatted sentences ready to paste into manuscript
- Calculate ratios and percentage changes

**Output includes:**
- Microgravity persistence numbers
- Phase diagram regime anchor points
- Spine S-curve sine-mode characteristics

### Option B: Manual Extraction (If Script Fails)

#### 1. Microgravity Series

**File:** `outputs/experiments/microgravity/microgravity_summary.csv`

```python
import pandas as pd
import numpy as np

df = pd.read_csv("outputs/experiments/microgravity/microgravity_summary.csv")
print(df.columns)

# Pick canonical g values
interesting_g = [1.0, 0.3, 0.1, 0.01]

rows = df[df["gravity"].isin(interesting_g)].sort_values("gravity")
for _, r in rows.iterrows():
    passive_energy = r.get("passive_energy", r.get("E_passive", np.nan))
    D_geo_norm = r.get("D_geo_norm", np.nan)
    print(
        f"g = {r['gravity']:.2f} | E_passive = {passive_energy:.3e} | "
        f"D_geo_norm = {D_geo_norm:.3f}"
    )

# Calculate ratios
g_high = rows.iloc[0]
g_low = rows.iloc[-1]
energy_ratio = g_low["passive_energy"] / g_high["passive_energy"]
D_geo_ratio = g_low["D_geo_norm"] / g_high["D_geo_norm"]
print(f"\nEnergy collapse: {(1-energy_ratio)*100:.1f}%")
print(f"D_geo persistence: {D_geo_ratio:.2f}×")
```

**Manuscript sentence:**
> "As g decreases from 1.0 to 0.01, passive curvature energy falls by roughly X-fold, while D̂_geo changes by only Y%, indicating that the information-selected 'spinal wave' is largely preserved in microgravity."

#### 2. Phase Diagram Regimes

**File:** `outputs/experiments/phase_diagram/phase_diagram_data.csv`

```python
df = pd.read_csv("outputs/experiments/phase_diagram/phase_diagram_data.csv")

# Thresholds from RegimeThresholds
D_geo_small = 0.1
D_geo_large = 0.3
S_lat_scoliotic = 0.05
cobb_scoliotic = 5.0

# Classify regimes
df["regime"] = "cooperative"
df.loc[df["D_geo_norm"] < D_geo_small, "regime"] = "gravity_dominated"
df.loc[
    (df["D_geo_norm"] > D_geo_large) &
    (df["S_lat_asym"] >= S_lat_scoliotic) &
    (df["cobb_asym_deg"] >= cobb_scoliotic),
    "regime"
] = "scoliotic_regime"

# Find representative points
gdom = df[df["regime"] == "gravity_dominated"].sort_values("D_geo_norm").iloc[0]
coop = df[df["regime"] == "cooperative"].sort_values("D_geo_norm").iloc[len(df[df["regime"] == "cooperative"]) // 2]
scol = df[df["regime"] == "scoliotic_regime"].sort_values("D_geo_norm").iloc[-1]

for label, r in [("gravity", gdom), ("cooperative", coop), ("scoliotic", scol)]:
    print(
        f"[{label}] chi_kappa={r['chi_kappa']:.3f}, g={r['gravity']:.2f}, "
        f"D_geo_norm={r['D_geo_norm']:.3f}, S_lat={r['S_lat_asym']:.3f}, "
        f"Cobb={r['cobb_asym_deg']:.1f}°"
    )
```

**Manuscript paragraph:**
> "In the gravity-dominated regime (e.g., χ_κ = ..., g = ...), we find D̂_geo ≈ 0.0X, S_lat < 0.01, and Cobb-like angles < 3°. In contrast, in the information-dominated corner (χ_κ = ..., g = ...), D̂_geo > 0.3, S_lat ≳ 0.05, and Cobb-like angles exceed 10°, indicating a scoliosis-like symmetry-broken branch."

#### 3. Spine S-Curve Sine-Mode

**File:** `outputs/experiments/spine_modes/spine_modes_results.csv`

```python
df = pd.read_csv("outputs/experiments/spine_modes/spine_modes_results.csv")

# Get info-driven case (highest chi_kappa)
max_chi_k = df["chi_kappa"].max()
info_case = df[df["chi_kappa"] == max_chi_k].sort_values("s")

kappa_info = info_case["kappa"].values

# Count sign changes
sign_changes = np.sum(np.diff(np.sign(kappa_info)) != 0)

# Max/RMS ratio
max_kappa = np.max(np.abs(kappa_info))
rms_kappa = np.sqrt(np.mean(kappa_info**2))
ratio = max_kappa / (rms_kappa + 1e-9)

print(f"Sign changes: {sign_changes}")
print(f"Max/RMS ratio: {ratio:.2f}")

# Get D_geo_norm from summary
summary_df = pd.read_csv("outputs/experiments/spine_modes/spine_modes_summary.csv")
D_geo_norm = summary_df[summary_df["chi_kappa"] == max_chi_k].iloc[0]["D_geo_norm"]
print(f"D̂_geo: {D_geo_norm:.3f}")
```

**Manuscript sentence:**
> "The stabilized sagittal S-curve is dominated by a single smooth sign-changing mode: κ_I(s) exhibits only one sign change along the axis and a max-to-RMS ratio of ≈R, consistent with a sine-like counter-curvature profile against gravity."

---

## Step 3: Update Manuscript with Numbers

### Files to Update

1. **Abstract**: Add 1-2 quantitative statements
2. **Results Section**: Replace vague language with numbers
3. **Cover Letter**: Update key claims bullets
4. **Key Claims**: Update `docs/key_claims_bullets.md`

### Example Replacements

| Before | After (with numbers) |
|--------|---------------------|
| "small asymmetries produce large deviations" | "5% asymmetry (ε_asym = 0.05) produces S_lat ≈ 0.12 and Cobb-like angles > 10°" |
| "D̂_geo increases with coupling" | "D̂_geo increases from 0.05 to 0.35 as χ_κ increases from 0 to 0.08" |
| "information persists in microgravity" | "D̂_geo remains ≈0.25 while passive energy collapses by 95% as g → 0.01" |

---

## Step 4: Verify Output Files

After running sweeps, verify these files exist:

- [ ] `outputs/experiments/spine_modes/spine_modes_results.csv`
- [ ] `outputs/experiments/spine_modes/spine_modes_summary.csv`
- [ ] `outputs/experiments/microgravity/microgravity_summary.csv`
- [ ] `outputs/experiments/phase_diagram/phase_diagram_data.csv`
- [ ] `outputs/figs/fig_countercurvature_metrics.png`
- [ ] `outputs/experiments/phase_diagram/phase_diagram.png`

---

## Troubleshooting

### Script Fails to Find CSV Files

- **Check paths**: Scripts print output paths - verify they match
- **Run experiments first**: Make sure you've run the full sweeps (without `--quick`)
- **Check column names**: CSV columns may vary - adjust script if needed

### Numbers Look Unusual

- **Check parameter ranges**: Verify chi_kappa and g values are in expected ranges
- **Check thresholds**: Regime thresholds (0.1, 0.3) should match `RegimeThresholds`
- **Check sign changes**: Should be 1 for single-mode S-curve

### Runtime Too Long

- **Reduce grid size**: Edit experiment scripts to use fewer points
- **Use `--quick` for testing**: But remember to run full sweeps for final numbers

---

## Expected Runtime

- **Spine modes**: 5-10 minutes
- **Microgravity**: 10-15 minutes
- **Phase diagram**: 20-40 minutes (largest grid)
- **Figure generation**: < 1 minute
- **Number extraction**: < 1 minute

**Total**: ~40-70 minutes for full sweeps

---

## Next Steps After Extraction

1. **Copy extracted sentences** into manuscript
2. **Replace placeholder numbers** with actual values
3. **Update cover letter** key claims bullets
4. **Final manuscript polish** with quantitative language

---

## Status

✅ **Script created**: `scripts/extract_anchor_numbers.py`  
✅ **Manuscript updated**: Results and Discussion sections with sine-wave narrative  
⏳ **Next**: Run full sweeps → Extract numbers → Update manuscript

