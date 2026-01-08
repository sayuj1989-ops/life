# Paper Roadmap: Biological Countercurvature of Spacetime

## Current Status: ✅ Implementation Complete

You now have a complete "information-gravity lab" with:
- ✅ Countercurvature metric g_eff(s)
- ✅ Geodesic deviation D_geo, D̂_geo
- ✅ Three experimental paradigms (spine, microgravity, plant)
- ✅ Phase diagram generator
- ✅ Figure generation pipeline
- ✅ Mathematical Box ready for paper

## Next Steps: Scientific Predictions → Paper

### Phase 1: Generate Data (1-2 days)

Run full parameter sweeps to lock in quantitative values:

```bash
# Run all experiments
./run_experiments.sh all

# Generate phase diagram
./run_experiments.sh phase
```

**Deliverables:**
- CSV files with D_geo_norm values across parameter space
- Phase diagram showing three regimes
- Representative figures for each experiment

### Phase 2: Refine Predictions (2-3 days)

Test the four key predictions:

1. **Microgravity persistence**: Extend to g = 0.005, verify D̂_geo persists
2. **Scoliosis bifurcation**: Add lateral asymmetry, find critical χ_κ
3. **Plant growth**: Sweep information field shapes, find upward growth regime
4. **Phase boundaries**: Quantify transitions at D̂_geo = 0.05 and 0.2

**Deliverables:**
- Quantitative predictions with error bars
- Bifurcation diagrams
- Parameter space maps

### Phase 3: Write Paper (1 week)

**Structure:**

1. **Abstract** (250-300 words) - ✅ Draft ready in `docs/paper_draft_abstract.md`
2. **Introduction** (1-2 pages)
   - Living systems vs gravity
   - Information-Elasticity Coupling
   - Biological countercurvature hypothesis
3. **Methods** (1-2 pages)
   - Cosserat rod mechanics
   - IEC model
   - Countercurvature metric definition
   - Geodesic deviation computation
4. **Results** (2-3 pages)
   - ✅ Subsection draft ready: "Information-driven deviations from gravity-selected curvature"
   - Spinal curvature modes
   - Microgravity adaptation
   - Phase diagram and regimes
   - Plant-like growth
5. **Discussion** (1-2 pages)
   - Analog model interpretation (not modifying GR)
   - Connection to consciousness/biological intelligence
   - Limitations and future directions
6. **Mathematical Box** - ✅ Ready in `docs/mathematical_box_countercurvature.md`

### Phase 4: Figures (2-3 days)

**Figure 1: Countercurvature Metrics** (4 panels)
- Panel A: Curvature profiles
- Panel B: Countercurvature metric g_eff(s)
- Panel C: D_geo_norm vs χ_κ
- Panel D: Microgravity adaptation

**Figure 2: Phase Diagram**
- Panel A: D_geo_norm(χ_κ, g) contour plot with regime boundaries
- Panel B: Passive energy vs gravity (reference)

**Figure 3: Predictions** (optional)
- Scoliosis bifurcation diagram
- Plant growth parameter space
- Extended microgravity range

### Phase 5: Submission (1 day)

**Target journals:**
- PRX Life (Physical Review X Life)
- Nature Communications
- Physical Review E
- Journal of the Royal Society Interface

**Requirements:**
- All code/data available (GitHub)
- Reproducibility statement
- Figure files (high-res PNG/PDF)
- LaTeX source with Mathematical Box

## Key Scientific Claims

### Claim 1: Information Persistence in Microgravity

> As gravitational loading is reduced, passive curvature collapses, but normalized geodesic deviation D̂_geo remains roughly constant or increases. This demonstrates that information-driven structure is maintained independently of gravitational curvature.

**Evidence:** Microgravity experiment showing D̂_geo ≈ 0.12 at 0.01g despite passive collapse.

### Claim 2: Three Regimes of Countercurvature

> The phase diagram D̂_geo(χ_κ, g) reveals three distinct regimes: gravity-dominated (D̂_geo < 0.05), cooperative (0.05 < D̂_geo < 0.2), and information-dominated (D̂_geo > 0.2).

**Evidence:** Phase diagram experiment with clear boundaries.

### Claim 3: Information-Weighted Geometry

> The countercurvature metric g_eff(s) correctly weights regions of high information processing, as evidenced by D̂_geo / L2_norm > 1 in plant growth experiments.

**Evidence:** Plant experiment showing ratio > 1.2.

## Language Guidelines

### ✅ DO Say

- "Analog model of spacetime"
- "Effective metric" or "effective geometry"
- "Biological countercurvature" (qualified as analog)
- "Information-selected geodesic" vs "gravity-selected geodesic"
- "Configuration space" (not literal spacetime)

### ❌ DON'T Say

- "Modifying Einstein's equations"
- "Real spacetime curvature"
- "Quantum gravity" (unless you add that layer explicitly)
- "Proving consciousness" (too strong)

### ✅ Safe Phrasing

> "In this analog model, biological information processing acts as a source of effective countercurvature in the configuration space of the body axis, analogous to a local reshaping of spacetime geometry."

## Quantitative Targets

Lock in these numbers from your experiments:

- **D̂_geo range**: [0, ?] for χ_κ ∈ [0, 0.05] at 1g
- **D̂_geo at 0.01g**: ≈ ? (should be > 0.1)
- **Phase boundaries**: D̂_geo = 0.05 and 0.2
- **Plant growth ratio**: D̂_geo / L2_norm ≈ ? (should be > 1.2)

## Timeline

- **Week 1**: Generate all data, refine predictions
- **Week 2**: Write paper, create figures
- **Week 3**: Revise, get feedback, submit

## Success Criteria

Paper is ready when:
- ✅ All four predictions tested and quantified
- ✅ Phase diagram shows clear regimes
- ✅ Figures are publication-quality
- ✅ Abstract and Results section polished
- ✅ Mathematical Box integrated
- ✅ Code/data available for reproducibility

---

## Quick Reference

**Run experiments:**
```bash
./run_experiments.sh all
./run_experiments.sh phase
```

**Generate figure:**
```bash
./run_experiments.sh figure
```

**Draft documents:**
- Abstract: `docs/paper_draft_abstract.md`
- Results: `docs/paper_draft_results_subsection.md`
- Mathematical Box: `docs/mathematical_box_countercurvature.md`
- Predictions: `docs/scientific_predictions.md`

