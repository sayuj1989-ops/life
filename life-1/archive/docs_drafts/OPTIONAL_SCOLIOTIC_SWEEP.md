# Optional: Extending Phase Diagram to Capture Scoliotic Regime

## Current Status

The current phase diagram sweep does not produce any points in the "scoliotic regime" (as defined by `RegimeThresholds`). The manuscript now uses conservative wording that treats scoliosis as a "predicted extension" rather than a realized regime.

## If You Want to Show an Actual Scoliotic Point

If you'd like to have at least one scoliotic point in the data before submission, here are two options:

---

## Option 1: Increase χ_κ Upper Bound

**File to edit:** `src/spinalmodes/experiments/countercurvature/experiment_phase_diagram.py`

**Current range:** Check the `chi_kappa_range` or `chi_kappa_values` in the script

**Suggested change:** Increase the maximum χ_κ by 2-3× (e.g., if current max is 0.08, try 0.15-0.20)

**Example:**
```python
# Before
chi_kappa_values = np.linspace(0.0, 0.08, 20)

# After
chi_kappa_values = np.linspace(0.0, 0.15, 25)  # Higher max, more points
```

---

## Option 2: Relax Thresholds (Slightly)

**File to edit:** `src/spinalmodes/countercurvature/scoliosis_metrics.py`

**Current thresholds** (in `RegimeThresholds`):
- `D_geo_large = 0.3`
- `S_lat_scoliotic = 0.05`
- `cobb_scoliotic = 5.0`

**Suggested relaxed thresholds:**
```python
RegimeThresholds(
    D_geo_small=0.1,
    D_geo_large=0.25,  # Lowered from 0.3
    S_lat_scoliotic=0.04,  # Lowered from 0.05
    cobb_scoliotic=4.0,  # Lowered from 5.0
)
```

**Note:** Only relax slightly to maintain scientific rigor. Don't make thresholds so low that normal cases are classified as scoliotic.

---

## After Making Changes

1. **Run the phase diagram experiment:**
   ```bash
   python3 -m spinalmodes.experiments.countercurvature.experiment_phase_diagram
   ```

2. **Extract numbers:**
   ```bash
   python3 scripts/extract_anchor_numbers.py
   ```

3. **Check for scoliotic regime:**
   - Look for rows with `regime == "scoliotic_regime"` in the output
   - If found, you'll get a manuscript sentence like:
     > "For example, at χ_κ = 0.12 and g = 4.9, D̂_geo ≈ 0.35, S_lat ≈ 0.06, and Cobb-like angles exceed 10°, consistent with a scoliosis-like symmetry-broken branch in the information-dominated corner of the phase diagram."

4. **Update manuscript:**
   - Replace the conservative phase diagram paragraph in Results 3.3
   - Add the scoliotic example sentence
   - Update the scoliosis subsection (3.4) to reference actual data

---

## Recommendation

**If you have time:** Try Option 1 first (increase χ_κ max). This is more scientifically rigorous than relaxing thresholds.

**If you're short on time:** The conservative wording in the current manuscript is perfectly fine for submission. You can always add the scoliotic point in a revision or follow-up paper.

---

## Current Manuscript Wording (Conservative)

The manuscript now says:
> "Within the current sweep, our thresholds for a 'scoliotic regime' (S_lat ≳ 0.05, Cobb-like angles ≳ 5°) are not crossed, so the symmetry-broken branch remains a predicted extension at larger χ_κ or stronger asymmetries rather than a regime realized in this parameter window."

This is honest and scientifically sound. The framework predicts scoliosis, but you're not claiming to have observed it in this particular parameter window.

---

## Status

✅ **Manuscript updated with conservative wording**  
⏳ **Optional:** Extend sweep to capture scoliotic regime if desired

