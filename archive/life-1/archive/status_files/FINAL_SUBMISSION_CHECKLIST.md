# Final Submission Checklist for PRX Life

**Status:** ✅ Manuscript polished and ready  
**Version:** v0.1.0  
**Target Journal:** PRX Life

---

## ✅ 1. Build & Eyeball the Final PDF

### Build Command
```bash
cd manuscript
latexmk -pdf main_countercurvature.tex
```

### PDF Checks
- [ ] Title, author, affiliation, email all correct
- [ ] No "TODO", "XX", or placeholder text anywhere
- [ ] All figure references (`Fig. 1`, `Fig. 2`) and section refs compile (no "??")
- [ ] Equations render correctly (metric, D_geo, D̂_geo, etc.)
- [ ] Abstract and Significance read smoothly as a standalone story
- [ ] Page numbers are correct
- [ ] Bibliography compiles correctly

---

## ✅ 2. Cross-Check Claims vs Data

### Spine S-Curve
- [x] One sign change ✔
- [x] max/RMS ≈ 1.81 ✔
- [x] D̂_geo ≈ 0.14 ✔

### Microgravity
- [x] D̂_geo ≈ 0.091, ~0% change between g = 1.0 and g = 0.10 ✔

### Phase Diagram
- [x] Gravity-dominated example: χ_κ = 0.015, g = 9.81, D̂_geo ≈ 0.059 ✔
- [x] Cooperative example: χ_κ = 0.065, g = 9.81, D̂_geo ≈ 0.15 ✔
- [x] Text + Fig. 2 caption both say scoliotic regime is *predicted*, not realized ✔

**Status:** All numbers match extracted anchor values from experiments.

---

## ✅ 3. Repo + Version Sanity

### Check Version Consistency
```bash
# In repo root
git status
git tag -l
```

### Verify Files
- [x] `CITATION.cff` has:
  - [x] Name: Dr. Sayuj Krishnan S, MBBS, DNB (Neurosurgery)
  - [x] Affiliation: Yashoda Hospitals, Malakpet, Hyderabad, India
  - [x] Email: dr.sayujkrishnan@gmail.com
  - [x] ORCID: https://orcid.org/0009-0009-5523-9979
  - [x] Version: 0.1.0
  - [x] Repository: https://github.com/sayujks0071/life

- [x] Tag v0.1.0 exists and is pushed

### Tag Commands (if needed)
```bash
git tag -a v0.1.0 -m "Publication version: Biological Countercurvature of Spacetime"
git push origin v0.1.0
```

---

## ✅ 4. Submission Bundle for PRX Life

### Required Files
- [ ] **main_countercurvature.pdf** – final manuscript (compile and verify)
- [x] **main_countercurvature.tex** – source (ready)
- [x] **Cover letter** – available in `docs/cover_letter_expansion_template.md`
- [x] **CITATION.cff** – software citation metadata

### PRX Life Submission Form

**Article Type:** Regular Article / Original Research

**Code Availability:**
- Repository: https://github.com/sayujks0071/life
- Version: v0.1.0
- Key functions: `compute_countercurvature_metric`, `geodesic_curvature_deviation`, `compute_scoliosis_metrics`, `solve_beam_static`

**Data Availability:**
"All data generated are included in the manuscript and supplementary files, or can be regenerated from the open-source code as described in the Data Availability section. Experiment outputs are written to the `outputs/` directory by scripts in `src/spinalmodes/experiments/countercurvature/`. Running the experiments with default parameters (or `--quick` mode) reproduces all CSV files used by figure-generation scripts."

**Key Claims:** Use bullets from `docs/key_claims_bullets.md` (PRX Life submission-ready version)

---

## ✅ 5. Final Language Polish (Optional)

If desired, use this micro-prompt on the PDF text or LaTeX:

> "Read this final manuscript as a PRX Life referee. Do **not** change equations, symbols, numbers, or claims. Only point out any sentences that read awkwardly, are unclear, or feel repetitive, and suggest minimal rephrasings. Do not alter the scientific content."

---

## Current Title & Abstract

**Title:**
Biological Countercurvature of Spacetime: An Information--Cosserat Framework for Spinal Geometry

**Abstract:**
Living systems routinely generate and maintain structure against gravity, from plant stems that grow upward to vertebrate spines that adopt robust S-shaped profiles. Here we develop a quantitative framework in which such behavior is interpreted as *biological countercurvature*: information-driven modification of the effective geometry experienced by a body in a gravitational field. We combine an information--elasticity coupling (IEC) model of spinal patterning with three-dimensional Cosserat rod mechanics implemented in PyElastica, treating the rod in gravity as an analog spacetime and the IEC information field I(s) as a source of effective countercurvature.

On the body axis s, we define a biological metric dℓ_eff² = g_eff(s) ds², where the conformal factor g_eff(s) depends on the local amplitude and gradient of I(s). Using this countercurvature metric, we introduce a normalized geodesic curvature deviation D̂_geo that measures how far information-shaped equilibrium curvature profiles depart from the corresponding gravity-selected profiles. Across canonical simulations---human-like spinal S-curves, plant-like stems, and microgravity adaptation---we show that D̂_geo cleanly separates gravity-dominated, cooperative, and information-dominated regimes in (χ_κ, g) space, where χ_κ controls information-to-curvature coupling and g denotes gravitational strength.

To probe pathology within the same framework, we introduce a small, localized thoracic asymmetry in the information field or lateral rest curvature and track coronal-plane deformations. In the gravity-dominated regime, this perturbation produces negligible lateral deviation. In contrast, in the information-dominated corner of the phase diagram (at stronger coupling than explored in our current sweep), the same small asymmetry is predicted to be amplified into a scoliosis-like symmetry-broken branch, characterized by increased lateral displacement and Cobb-like angles together with large D̂_geo. These results suggest that normal sagittal curvature and scoliosis-like patterns can emerge from a single IEC--Cosserat model operating in different countercurvature regimes, providing an analog-gravity perspective on how biological information reshapes equilibrium geometry in a gravitational field.

---

## Next Steps

1. **Compile PDF:** Run `latexmk -pdf main_countercurvature.tex` in `manuscript/` directory
2. **Final review:** Check PDF for formatting, references, equations
3. **Submit:** Use PRX Life submission portal with cover letter and files

---

## Status

✅ **Manuscript:** Polished and ready  
✅ **Numbers:** All verified against experiments  
✅ **Version:** v0.1.0 tagged and pushed  
✅ **Cover letter:** Ready in `docs/cover_letter_expansion_template.md`  
✅ **Key claims:** Ready in `docs/key_claims_bullets.md`  
⏳ **Final PDF:** Compile and verify
