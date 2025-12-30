# Next Steps Checklist: From Code to Paper

## Status: Implementation Complete → Data Generation Phase

---

## 1. Wire Scoliosis Metrics into Experiment Scripts

### `experiment_spine_modes_vs_gravity.py`
- [ ] For symmetric run: `compute_scoliosis_metrics(z_sym, y_sym)`
- [ ] For asymmetric run: `compute_scoliosis_metrics(z_asym, y_asym)`
- [ ] Use `classify_scoliotic_regime(...)` to get regime flags
- [ ] Save to CSV:
  - `S_lat_sym`, `S_lat_asym`
  - `cobb_sym_deg`, `cobb_asym_deg`
  - `gravity_dominated`, `cooperative`, `scoliotic_regime` (as integers)

### `experiment_phase_diagram.py`
- [ ] Ensure symmetric + asymmetric runs are both executed
- [ ] Compute scoliosis metrics for both cases
- [ ] Overlay scoliotic regime contour on phase diagram
- [ ] Save regime classification flags to summary CSV

### `experiment_scoliosis_bifurcation.py`
- [ ] Verify it uses `apply_info_asymmetry` and `compute_scoliosis_metrics`
- [ ] Check that it sweeps both `chi_kappa` and `epsilon_asym`
- [ ] Ensure output includes amplification factors (asym/sym ratios)

---

## 2. Run the Big Parameter Sweeps

### Microgravity Sweep
- [ ] Extended range: `g ∈ [1.0, 0.9, 0.5, 0.1, 0.05, 0.01, 0.005]`
- [ ] Record `D_geo_norm` at each gravity level
- [ ] Verify persistence of `D_geo_norm` as `g → 0`
- [ ] Check that passive energy collapses while info-driven structure persists

### Phase Diagram
- [ ] Grid over `(chi_kappa, g)`:
  - `chi_kappa ∈ [0, 0.01, 0.02, 0.03, 0.04, 0.05]`
  - `g ∈ [1.0, 0.5, 0.1, 0.05, 0.01]`
- [ ] Run both symmetric (`epsilon_asym = 0`) and asymmetric (`epsilon_asym = 0.05`) for each point
- [ ] Compute `D_geo_norm` for symmetric case
- [ ] Compute `S_lat`, `cobb_like_deg` for both cases
- [ ] Classify regimes using `classify_scoliotic_regime`
- [ ] Generate contour plot with scoliotic regime overlay

### Plant Experiment
- [ ] Vary `I(s)` shape (e.g., different peak locations)
- [ ] Sweep `chi_kappa` from 0 to 0.05
- [ ] Record `D_geo_norm` and compare to plain L2 norm
- [ ] Verify that `D_geo_norm / L2_norm > 1` (metric weighting effect)

---

## 3. Regime Sanity Check

### Hand-Picked Test Cases
- [ ] **Clear "normal" case**: `chi_kappa = 0.01`, `g = 1.0`, `epsilon_asym = 0.05`
  - Should show: `D_geo_norm < 0.1`, `S_lat < 0.05`, `cobb < 5°`
  - Visualize centerline: should be nearly symmetric
  
- [ ] **Clear "scoliotic" case**: `chi_kappa = 0.05`, `g = 0.1`, `epsilon_asym = 0.05`
  - Should show: `D_geo_norm > 0.3`, `S_lat >= 0.05`, `cobb >= 5°`
  - Visualize centerline: should show pronounced lateral deviation
  
- [ ] **Borderline case**: `chi_kappa = 0.03`, `g = 0.5`, `epsilon_asym = 0.05`
  - Should fall in "cooperative" regime
  - Check that metrics are intermediate

### Threshold Tuning
- [ ] Review `RegimeThresholds` defaults:
  - `D_geo_small = 0.1` (gravity/cooperative boundary)
  - `D_geo_large = 0.3` (cooperative/information boundary)
  - `S_lat_scoliotic = 0.05` (dimensionless lateral index)
  - `cobb_scoliotic_deg = 5.0` (Cobb-like angle threshold)
- [ ] Compare thresholds to clinical scoliosis criteria (Cobb angle > 10° is typically considered significant)
- [ ] Adjust if needed based on simulation outputs
- [ ] Document rationale for chosen thresholds

---

## 4. Freeze First Figure Set

### Countercurvature Metrics Figure
- [ ] Run `generate_countercurvature_figure.py` (or equivalent)
- [ ] Generate 4-panel figure:
  - Panel A: Curvature profiles (κ_passive vs κ_info)
  - Panel B: Countercurvature metric g_eff(s)
  - Panel C: D_geo_norm vs χ_κ
  - Panel D: D_geo_norm vs gravity (microgravity adaptation)
- [ ] Save as: `outputs/figs/fig3_countercurvature.png` (and PDF)
- [ ] Update draft to reference `Fig. 3`

### Phase Diagram Figure
- [ ] Generate phase diagram with:
  - Contour plot of `D_geo_norm(chi_kappa, g)`
  - Overlay of scoliotic regime boundary
  - Markers for test cases (normal, borderline, scoliotic)
- [ ] Save as: `outputs/figs/fig4_phase_diagram.png` (and PDF)
- [ ] Update draft to reference `Fig. 4`

### Scoliosis Bifurcation Figure (Optional)
- [ ] If creating dedicated scoliosis figure:
  - Panel A: Symmetric vs asymmetric centerlines (coronal view)
  - Panel B: S_lat vs chi_kappa (bifurcation plot)
  - Panel C: Cobb-like angle vs chi_kappa
- [ ] Save as: `outputs/figs/fig5_scoliosis_bifurcation.png` (and PDF)

---

## 5. Data Extraction for Paper

### Quantitative Values to Extract
- [ ] `D_geo_norm` range for `chi_kappa ∈ [0, 0.05]` at `g = 1.0`
- [ ] `D_geo_norm` at `g = 0.01` (microgravity persistence)
- [ ] Phase boundaries: `D_geo_norm = 0.1` and `0.3` locations in `(chi_kappa, g)` space
- [ ] Plant experiment: `D_geo_norm / L2_norm` ratio
- [ ] Scoliosis amplification: `S_lat_asym / S_lat_sym` in information-dominated regime
- [ ] Bifurcation point: `chi_kappa` value where `S_lat` jumps significantly

### Update Paper Drafts
- [ ] Replace placeholder numbers in `paper_draft_results_subsection.md`
- [ ] Add real values to Abstract if space allows
- [ ] Update Methods with actual parameter ranges used
- [ ] Verify all figure references match generated files

---

## 6. Final Polish

- [ ] Run all experiments end-to-end from scratch
- [ ] Verify reproducibility (same inputs → same outputs)
- [ ] Check that all CSV outputs are complete
- [ ] Ensure all figures are publication-ready (DPI, fonts, labels)
- [ ] Cross-check figure numbers in text match actual files
- [ ] Final proofread of all draft sections

---

## Notes

- **Priority order**: 1 → 2 → 3 → 4 → 5 → 6
- **Time estimate**: Steps 1-2 are the most time-consuming (actual computation)
- **Checkpoint**: After step 3, you should have enough data to write a complete Results section
- **Milestone**: After step 4, you have a complete figure set ready for submission

---

## Quick Commands Reference

```bash
# Run all experiments
./run_experiments.sh all

# Run specific experiment
./run_experiments.sh phase

# Generate figures
python3 -m spinalmodes.experiments.countercurvature.generate_countercurvature_figure

# Check outputs
ls -lh outputs/figs/
ls -lh outputs/csv/
```

