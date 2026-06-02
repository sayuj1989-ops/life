# Bio-Gravitational Number Validation Test — Implementation Checklist

**Date:** 2026-05-04  
**Goal:** Execute falsifiable test of $\mathcal{B}_g = 1.0$ critical point hypothesis within 4 weeks

---

## Pre-Flight Checks

### Environment Setup

- [x] PyElastica installed and available
  ```bash
  cd /home/sayuj/life
  source .venv/bin/activate
  python -c "from spinalmodes.countercurvature.pyelastica_bridge import PYELASTICA_AVAILABLE; print(f'PyElastica: {PYELASTICA_AVAILABLE}')"
  ```

- [x] Experiment script is executable
  ```bash
  chmod +x scripts/experiments/experiment_bg_critical_point_validation.py
  python scripts/experiments/experiment_bg_critical_point_validation.py --help
  ```

- [ ] Create output directory
  ```bash
  mkdir -p results/bg_validation
  mkdir -p results/bg_validation_quick
  ```

### Compute Resources

- [ ] Verify GB10 is available (not running other heavy jobs)
  ```bash
  nvidia-smi  # Check GPU not saturated (though this is CPU-only)
  htop        # Check CPU cores available
  df -h       # Check disk space (need ~500MB for full CSVs)
  ```

---

## Week 1: Quick Test & Analysis Script (May 5-11)

### Day 1-2: Quick Test Run

- [ ] **Run quick test** (1 scale, 3 seeds, 20 chi_M → 60 sims, ~30 min)
  ```bash
  cd /home/sayuj/life
  source .venv/bin/activate
  
  python scripts/experiments/experiment_bg_critical_point_validation.py \
      --phase all \
      --scales 1.0 \
      --seeds 3 \
      --chi-M-min 0.1 \
      --chi-M-max 50.0 \
      --n-chi-M 20 \
      --output results/bg_validation_quick/ \
      2>&1 | tee results/bg_validation_quick/run.log
  ```

- [ ] **Verify output CSV**
  ```bash
  head -20 results/bg_validation_quick/bg_validation_results.csv
  wc -l results/bg_validation_quick/bg_validation_results.csv  # Should be 61 lines (1 header + 60 data)
  
  # Check for NaNs or errors
  grep -i "nan\|error\|fail" results/bg_validation_quick/bg_validation_results.csv
  ```

- [ ] **Quick visual check** (manual plot in Python REPL or notebook)
  ```python
  import pandas as pd
  import matplotlib.pyplot as plt
  
  df = pd.read_csv('results/bg_validation_quick/bg_validation_results.csv')
  
  # Plot eta_CC vs Bg (should show sigmoid-like trend)
  plt.figure(figsize=(8, 6))
  for seed in df['seed'].unique():
      data = df[df['seed'] == seed]
      plt.plot(data['Bg'], data['eta_CC'], 'o-', alpha=0.5, label=f'Seed {seed}')
  plt.xlabel('Bio-Gravitational Number (Bg)')
  plt.ylabel('Counter-Curvature Efficiency (eta_CC)')
  plt.axvline(x=1.0, color='r', linestyle='--', label='Bg = 1 (hypothesis)')
  plt.legend()
  plt.grid(True, alpha=0.3)
  plt.title('Quick Test: eta_CC vs Bg')
  plt.savefig('results/bg_validation_quick/quick_plot.png')
  plt.show()
  ```

### Day 3-4: Analysis Script Implementation

- [ ] **Create analysis script directory**
  ```bash
  mkdir -p scripts/analysis
  ```

- [ ] **Implement `scripts/analysis/validate_bg_critical_point.py`**  
  Use template from `QUICKSTART_VALIDATION.md`, implement:
  - Phase 1: Sigmoid fitting (`scipy.optimize.curve_fit`)
  - Phase 2: Robustness test (seed-to-seed variance)
  - Phase 3: Universality test (ANOVA on Bg_star across scales)
  - Plotting functions (phase diagram with error bars)
  - Decision logic (PASS / FAIL / INCONCLUSIVE)

- [ ] **Test analysis script on quick test data**
  ```bash
  python scripts/analysis/validate_bg_critical_point.py \
      --input results/bg_validation_quick/bg_validation_results.csv \
      --output results/bg_validation_quick/analysis/
  ```

- [ ] **Verify analysis outputs**
  - `analysis/phase_diagram.png` exists and shows sigmoid fit
  - `analysis/robustness_test.csv` has Bg_star per seed
  - `analysis/decision.txt` contains preliminary judgment

### Day 5: Documentation & Adjustments

- [ ] **Document any issues found**
  - If simulations didn't converge → increase `final_time`
  - If Bg_star is far from 1.0 → check parameter normalization
  - If seed variance is high → may need more equilibration time

- [ ] **Adjust parameters for full run if needed**
  - Update `--chi-M-min` / `--chi-M-max` if quick test shows critical point outside [0.1, 50]
  - Update `n_chi_M` if transition region is under-sampled
  - Consider adding `--final-time` argument to script if needed

---

## Week 2: Full Protocol Run (May 12-18)

### Day 1: Launch Full Run

- [ ] **Verify compute availability**
  ```bash
  # Check no other heavy jobs running
  htop
  # Consider running in tmux/screen for resilience
  tmux new -s bg_validation
  ```

- [ ] **Run full protocol** (3 scales × 8 seeds × 30 chi_M = 720 sims, ~6 hrs)
  ```bash
  cd /home/sayuj/life
  source .venv/bin/activate
  
  time python scripts/experiments/experiment_bg_critical_point_validation.py \
      --phase all \
      --scales 0.5 1.0 2.0 \
      --seeds 8 \
      --chi-M-min 0.1 \
      --chi-M-max 50.0 \
      --n-chi-M 30 \
      --output results/bg_validation/ \
      2>&1 | tee results/bg_validation/run.log
  ```

- [ ] **Monitor progress** (open second terminal)
  ```bash
  # Watch CSV grow
  watch -n 60 wc -l results/bg_validation/bg_validation_results.csv
  
  # Check for errors
  tail -f results/bg_validation/run.log
  ```

### Day 2-3: Phase 1+2 Analysis

- [ ] **Run analysis on full data**
  ```bash
  python scripts/analysis/validate_bg_critical_point.py \
      --input results/bg_validation/bg_validation_results.csv \
      --output results/bg_validation/analysis/ \
      --phases 1 2
  ```

- [ ] **Inspect Phase 1 results (sigmoid fit)**
  - Check `analysis/phase_diagram.png`
  - Verify `k > 5` (sharp transition) or `k < 2` (gradual)
  - Check if `Bg_star ∈ [0.85, 1.15]` (hypothesis prediction)

- [ ] **Inspect Phase 2 results (robustness)**
  - Check `analysis/robustness_test.csv`
  - Compute `σ(Bg_star) / Bg_star` for each scale
  - If > 0.3 → noise artifact (like consciousness-geometry NULL)
  - If < 0.1 → robust critical point

- [ ] **Generate Phase 1+2 report**
  ```bash
  # analysis script should write analysis/phase1_2_summary.md
  cat results/bg_validation/analysis/phase1_2_summary.md
  ```

### Day 4-5: Plotting & Interpretation

- [ ] **Generate publication-quality plots**
  - Phase diagram: eta_CC vs Bg with sigmoid fit overlay
  - Error bars (std over seeds)
  - Separate panels for each scale
  - Highlight Bg = 1.0 reference line

- [ ] **Check for anomalies**
  - Are there outlier seeds (one seed behaves very differently)?
  - Do any scales fail to converge (high runtime, NaN values)?
  - Is baseline z_tip_passive consistent across seeds?

- [ ] **Write interim interpretation**
  - Based on Phases 1+2, is hypothesis trending toward PASS / FAIL / INCONCLUSIVE?
  - Document any surprises or unexpected patterns

---

## Week 3: Universality Test & Decision (May 19-25)

### Day 1-2: Phase 3 Analysis (Universality)

- [ ] **Run Phase 3 analysis** (ANOVA on Bg_star across scales)
  ```bash
  python scripts/analysis/validate_bg_critical_point.py \
      --input results/bg_validation/bg_validation_results.csv \
      --output results/bg_validation/analysis/ \
      --phases 3
  ```

- [ ] **Inspect universality results**
  - Check `analysis/universality_test.csv`
  - ANOVA p-value: if p > 0.05 → no significant scale dependence (PASS)
  - If p < 0.05 → Bg_star varies across scales (FAIL universality)
  - Check Bg_star range: if < 0.3 → universal; if > 0.5 → non-universal

### Day 3: Decision Logic

- [ ] **Compile results from all 3 phases**

  | Phase | Metric | Threshold | Result | Pass/Fail |
  |-------|--------|-----------|--------|-----------|
  | 1. Sharpness | Sigmoid k | k > 5 | k = ? | ? |
  | 2. Robustness | σ(Bg*)/Bg* | < 0.1 | ? | ? |
  | 3. Universality | Bg* range | < 0.3 | ? | ? |
  | | Bg* value | 0.85 - 1.15 | Bg* = ? | ? |

- [ ] **Apply decision criteria**
  - **PASS:** All 3 phases pass + Bg* ∈ [0.85, 1.15]
  - **FAIL:** Phase 1 or 2 fails (no critical point or noise artifact)
  - **INCONCLUSIVE:** Mixed results or parameters out of range

- [ ] **Write `results/bg_validation/DECISION.md`**
  - State verdict: PASS / FAIL / INCONCLUSIVE
  - Cite specific numbers from analysis
  - Compare to consciousness-geometry test (ρ = -0.15, p = 0.53)
  - If FAIL: explain what this means for manuscript claims
  - If PASS: implications for "Allometric Trap" hypothesis

### Day 4-5: Peer Review (Self-Check)

- [ ] **Red-team the analysis**
  - Re-run sigmoid fits with different initial guesses (test robustness of fit)
  - Try alternative functional forms (power law, exponential) — does sigmoid win?
  - Bootstrap confidence intervals on k, Bg_star
  - Check for selection bias (did we cherry-pick seeds or scales?)

- [ ] **Document limitations**
  - Simulation assumptions (quasi-static, 2s equilibration, fixed boundary)
  - Parameter ranges (what if biological chi_M is outside [0.1, 50]?)
  - Observable definition (eta_CC endpoint vs trajectory-averaged)

---

## Week 4: Manuscript Update or Falsification Note (May 26-Jun 1)

### Scenario A: PASS (Hypothesis Supported)

- [ ] **Update manuscript §Results**
  - Add new subsection: "Validation of Bio-Gravitational Number Critical Point"
  - Report sigmoid fit: k = ?, Bg* = ?
  - Show phase diagram (Figure X)
  - Cite robustness (σ/Bg* = ?) and universality (ANOVA p = ?)
  - **Conclusion:** "Computational validation supports Bg = 1 as critical threshold"

- [ ] **Update §Discussion**
  - Strengthen "Allometric Trap" claims (now computationally validated)
  - Note limitations (computational model, need for animal data)
  - Suggest empirical tests (measure chi_M in zebrafish, mouse, human)

- [ ] **Add to supplementary materials**
  - Full validation protocol (link to VALIDATION_TEST_DESIGN.md)
  - Raw data (bg_validation_results.csv)
  - Analysis code (validate_bg_critical_point.py)

### Scenario B: FAIL (Hypothesis Rejected)

- [ ] **Write supplementary falsification note**
  - Title: "Computational Test of Bio-Gravitational Number Critical Point Hypothesis"
  - State null result clearly (k < 2 or noise artifact)
  - Compare to consciousness-geometry Ising test (similar NULL pattern)
  - **Conclusion:** "No critical Bg = 1 threshold detected; counter-curvature scales smoothly"

- [ ] **Revise manuscript claims**
  - §Impact Statement: Remove "critical transition" language
  - Replace with "scaling law" framing (Bg as efficiency metric, not phase boundary)
  - Tone down "Allometric Trap" (it's a scaling mismatch, not a critical phenomenon)
  - Keep Bio-Gravitational Number as useful dimensionless predictor (even without critical point)

- [ ] **Document lessons learned**
  - Why did computational operationalization fail? (noise, simulation artifacts, mis-specified observable)
  - What alternative tests could work? (analytical toy model, animal experiments)
  - Update VALIDATION_TEST_DESIGN.md with "Post-Mortem" section

### Scenario C: INCONCLUSIVE

- [ ] **Write analysis note explaining ambiguity**
  - Some phases pass, others fail (e.g., sharp transition but non-universal)
  - Simulations had convergence issues or numerical artifacts
  - Observable definition is sensitive to arbitrary choices

- [ ] **Design follow-up experiment**
  - Option 1: Analytical toy model (reduced-order ODE, no PyElastica complexity)
  - Option 2: Different observable (frequency of S-curve emergence, not eta_CC)
  - Option 3: Defer to empirical data (measure Bg and spinal metrics in animals)

- [ ] **Add "Further Work Needed" section to manuscript**
  - Acknowledge computational test was not definitive
  - Lay out roadmap for resolving question

### Final Steps (All Scenarios)

- [ ] **Archive validation artifacts**
  ```bash
  # Compress results for archival
  tar -czf results/bg_validation_archive_$(date +%Y%m%d).tar.gz results/bg_validation/
  
  # Commit to git
  git add VALIDATION_*.md scripts/experiments/experiment_bg_critical_point_validation.py
  git add scripts/analysis/validate_bg_critical_point.py
  git add results/bg_validation/DECISION.md
  git commit -m "Bio-Gravitational Number validation test complete"
  ```

- [ ] **Update CLAUDE.md in /home/sayuj/**
  - Add validation test outcome to consciousness-geometry project memory
  - Note whether result was PASS / FAIL / INCONCLUSIVE
  - Document lessons for future validation test design

- [ ] **Write summary for collaborators**
  - Email-ready summary of test outcome
  - Key figure (phase diagram)
  - Next steps (manuscript revision or follow-up experiments)

---

## Troubleshooting Guide

### Issue: Simulations not converging (NaN in output)

**Diagnosis:**
```bash
grep "nan" results/bg_validation/bg_validation_results.csv
```

**Fixes:**
1. Increase `final_time` from 2.0s to 5.0s (allow more equilibration)
2. Decrease `dt` from 1e-5 to 1e-6 (more stable integration)
3. Check if issue is specific to high chi_M → may need adaptive time or damping

### Issue: Baseline z_tip_passive ≈ 0 (no gravitational deflection)

**Diagnosis:**
```bash
grep "chi_M,0.0" results/bg_validation/bg_validation_results.csv | head
```

**Fixes:**
1. Verify rod is initialized horizontally (`base_direction=(1,0,0)`)
2. Check gravity acts in -Z direction (default in PyElastica)
3. Increase rod length or reduce stiffness (make it more flexible)

### Issue: Seed variance is huge (σ/Bg* > 0.5)

**Diagnosis:**
```python
df = pd.read_csv('results/bg_validation/bg_validation_results.csv')
df.groupby(['scale', 'chi_M'])['eta_CC'].std().max()  # Check max std
```

**Fixes:**
1. This may be a real result (noise artifact, like consciousness-geometry)
2. Try increasing `n_elements` from 50 to 100 (reduce spatial discretization error)
3. Check if variance is concentrated at specific chi_M (near critical point) → may be inherent critical slowing down

### Issue: Sigmoid fit fails (scipy.optimize.curve_fit raises error)

**Diagnosis:**
```bash
python scripts/analysis/validate_bg_critical_point.py --debug
```

**Fixes:**
1. Try different initial guesses for `p0=[Bg_star, k]`
2. Add bounds: `bounds=([0.5, 0.1], [2.0, 20.0])`
3. If still fails → data may genuinely not be sigmoid (power law or linear)

---

## Success Metrics Checklist

- [ ] Validation test completes within 4 weeks
- [ ] Clear PASS / FAIL / INCONCLUSIVE decision documented
- [ ] Regardless of outcome: honest reporting (no post-hoc rationalization)
- [ ] Reusable analysis pipeline for future validation tests
- [ ] Lessons learned captured for next experiment design
- [ ] Manuscript updated or falsification note written
- [ ] Results archived and version-controlled

---

## References

- Design doc: `/home/sayuj/life/VALIDATION_TEST_DESIGN.md`
- Summary: `/home/sayuj/life/VALIDATION_SUMMARY.md`
- Quick-start: `/home/sayuj/life/QUICKSTART_VALIDATION.md`
- Experiment script: `/home/sayuj/life/scripts/experiments/experiment_bg_critical_point_validation.py`
- Analysis script (to be created): `/home/sayuj/life/scripts/analysis/validate_bg_critical_point.py`

---

## Completion Status

**Week 1:** [ ] Quick test, [ ] Analysis script, [ ] Output validation  
**Week 2:** [ ] Full run, [ ] Phase 1+2 analysis, [ ] Interim report  
**Week 3:** [ ] Phase 3 universality, [ ] Decision, [ ] Self-review  
**Week 4:** [ ] Manuscript update or falsification note, [ ] Archive

**Overall:** [ ] COMPLETE
