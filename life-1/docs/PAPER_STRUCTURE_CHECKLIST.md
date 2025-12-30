# Paper Structure Sanity Check

## Purpose

Before moving to LaTeX/Overleaf, verify that your draft has the complete structure and flow of a publication-ready manuscript.

---

## 1. Introduction

### Required Elements

- [ ] **Motivation** (2–3 paragraphs)
  - [ ] Life vs gravity problem (plants, spines, microgravity)
  - [ ] Why this matters (biological structure maintenance)
  - [ ] Gap in current understanding

- [ ] **Biological countercurvature idea** (1–2 paragraphs)
  - [ ] High-level hypothesis: information reshapes effective geometry
  - [ ] Connection to analog-gravity perspective
  - [ ] Brief mention of IEC + Cosserat rod approach

- [ ] **Scope and contributions** (1 paragraph)
  - [ ] What this paper does
  - [ ] What it doesn't claim (not modifying GR, analog model)
  - [ ] Preview of results (regimes, scoliosis branch)

### Current Status

- [ ] Draft exists: `docs/paper_draft_intro.md` (or equivalent)
- [ ] Length: ~500–800 words
- [ ] Flow: Motivation → Hypothesis → Approach → Preview

---

## 2. Methods

### Required Sections

- [ ] **IEC + Cosserat rod setup** (1–2 pages)
  - [ ] Information field I(s) definition
  - [ ] IEC coupling parameters (χ_κ, χ_E, χ_M)
  - [ ] Cosserat rod mechanics (PyElastica)
  - [ ] Mapping from I(s) to mechanical properties

- [ ] **Countercurvature metric + D̂_geo** (1 page)
  - [ ] Definition of g_eff(s) = exp(2φ(s))
  - [ ] D_geo formula and normalization
  - [ ] Interpretation as Riemannian distance

- [ ] **Experiments** (1 page)
  - [ ] Spine modes experiment (χ_κ sweep)
  - [ ] Plant growth experiment
  - [ ] Microgravity adaptation experiment
  - [ ] Phase diagram generation

- [ ] **Thoracic asymmetry + scoliosis metrics** (1 page)
  - [ ] Gaussian bump perturbation
  - [ ] S_lat and Cobb-like angle definitions
  - [ ] Regime classification thresholds

### Current Status

- [ ] IEC section: `docs/paper_draft_methods_iec.md` (or in main Methods)
- [ ] Countercurvature metric: `docs/mathematical_box_countercurvature.md`
- [ ] Scoliosis methods: `docs/paper_draft_methods_scoliosis.md`
- [ ] All sections have LaTeX-ready equations
- [ ] All parameters are defined with units/ranges

---

## 3. Results

### Required Subsections

- [ ] **Gravity vs information regimes** (2–3 pages)
  - [ ] Spine S-curve results (χ_κ sweep)
  - [ ] Plant growth results
  - [ ] D̂_geo_norm as regime indicator

- [ ] **Microgravity persistence** (1–2 pages)
  - [ ] D̂_geo_norm vs g plot
  - [ ] Comparison to passive energy collapse
  - [ ] Quantitative statement: "D̂_geo_norm changes by <X% while passive energy falls by Y%"

- [ ] **Phase diagram** (1–2 pages)
  - [ ] D̂_geo_norm(χ_κ, g) contour plot
  - [ ] Three regime boundaries
  - [ ] Three anchor points (normal, borderline, scoliotic)

- [ ] **Information-dominated regime & scoliosis branch** (1–2 pages)
  - [ ] Symmetric vs asymmetric comparison
  - [ ] Gravity-dominated: small changes
  - [ ] Information-dominated: large amplification
  - [ ] Quantitative thresholds (S_lat, Cobb-like angles)

### Current Status

- [ ] Results draft: `docs/paper_draft_results_subsection.md`
- [ ] All subsections have quantitative statements
- [ ] All figures are referenced (Fig. X, Panel Y)
- [ ] Placeholder numbers are marked for replacement

---

## 4. Discussion

### Required Elements

- [ ] **Biological interpretation** (1–2 pages)
  - [ ] What does "biological countercurvature" mean in practice?
  - [ ] Connection to neural control, growth programs
  - [ ] Why information-dominated regime might be pathological

- [ ] **Analog-gravity framing** (1 page)
  - [ ] What "analog spacetime" means
  - [ ] Limitations: not modifying GR, effective geometry only
  - [ ] Connection to consciousness (if appropriate)

- [ ] **Scoliosis implications** (1 page)
  - [ ] Unified framework for normal and pathological curvature
  - [ ] Clinical relevance (if any)
  - [ ] Predictions for scoliosis development

- [ ] **Future directions** (1 page)
  - [ ] Experimental tests (microgravity posture, scoliosis data)
  - [ ] Extensions (time-dependent I(s), 3D full spine)
  - [ ] Connections to other biological systems

### Current Status

- [ ] Discussion draft exists (or outline)
- [ ] Limitations section explicitly fences off over-claims
- [ ] Future directions are concrete and testable

---

## 5. Abstract

### Required Elements

- [ ] **Problem** (1 sentence): Life vs gravity
- [ ] **Hypothesis** (1–2 sentences): Biological countercurvature
- [ ] **Method** (2–3 sentences): IEC + Cosserat + metric
- [ ] **Results** (3–4 sentences): Regimes, microgravity, scoliosis
- [ ] **Conclusion** (1–2 sentences): Unified framework

### Current Status

- [ ] Main abstract: `docs/paper_draft_abstract.md` (~275 words)
- [ ] Short abstract: `docs/paper_draft_abstract.md` (~180 words)
- [ ] Contains 1–2 specific numerical contrasts
- [ ] No vague phrases ("pronounced", "large", etc.)

---

## 6. Figures

### Required Figures

- [ ] **Figure 1**: Conceptual diagram (optional)
  - [ ] Information field I(s) → mechanical properties
  - [ ] Countercurvature metric visualization

- [ ] **Figure 2**: Countercurvature metrics (4 panels)
  - [ ] Panel A: Curvature profiles (κ_passive vs κ_info)
  - [ ] Panel B: g_eff(s) along rod
  - [ ] Panel C: D_geo_norm vs χ_κ
  - [ ] Panel D: D_geo_norm vs g (microgravity)

- [ ] **Figure 3**: Phase diagram
  - [ ] Contour plot of D_geo_norm(χ_κ, g)
  - [ ] Regime boundaries
  - [ ] Scoliotic regime overlay
  - [ ] Three anchor points marked

- [ ] **Figure 4**: Scoliosis bifurcation (optional)
  - [ ] Symmetric vs asymmetric centerlines (coronal view)
  - [ ] S_lat vs χ_κ
  - [ ] Cobb-like angle vs χ_κ

### Current Status

- [ ] All figures generated: `outputs/figs/`
- [ ] Fixed filenames: `fig2_countercurvature.png`, `fig3_phase_diagram.png`, etc.
- [ ] All figures referenced in text with correct numbers
- [ ] Figure captions are complete and informative

---

## 7. Supporting Information

### Optional but Recommended

- [ ] **Mathematical Box**: Countercurvature metric definition
  - [ ] Status: `docs/mathematical_box_countercurvature.md`

- [ ] **Supplementary Methods**: Detailed parameter tables
  - [ ] All parameter values used in simulations
  - [ ] Regime threshold values

- [ ] **Supplementary Figures**: Additional plots
  - [ ] Extended parameter sweeps
  - [ ] Sensitivity analyses

---

## 8. Transitions and Flow

### Check Between Sections

- [ ] **Introduction → Methods**: Clear statement of approach
- [ ] **Methods → Results**: "We now present results from..."
- [ ] **Results → Discussion**: "These results suggest..."
- [ ] **Discussion → Conclusion**: Summary of contributions

### Check Within Sections

- [ ] Each Results subsection has a clear topic sentence
- [ ] Each paragraph flows logically to the next
- [ ] Quantitative statements are supported by data
- [ ] Figures are introduced before being discussed

---

## 9. Quantitative Completeness

### Verify All Numbers Are Present

- [ ] Microgravity: Percentage changes for D_geo_norm and passive energy
- [ ] Scoliosis: S_lat and Cobb-like angles for both regimes
- [ ] Phase diagram: Three anchor points with all metrics
- [ ] Thresholds: All regime boundaries are numerical
- [ ] Amplification factors: Where relevant (scoliosis branch)

### Verify All Numbers Are Correct

- [ ] Cross-check extracted values against CSV outputs
- [ ] Verify percentage calculations
- [ ] Check significant figures (2–3 decimal places appropriate)
- [ ] Ensure units are consistent

---

## 10. Language and Style

### Final Pass

- [ ] No vague phrases ("pronounced", "large", "small")
- [ ] All comparisons are quantitative
- [ ] All thresholds are explicit
- [ ] Technical terms are defined on first use
- [ ] Analog-gravity language is precise (not claiming GR modification)

---

## Pre-LaTeX Checklist

Before moving to LaTeX/Overleaf:

- [ ] All sections exist in draft form
- [ ] All figures are generated and saved
- [ ] All numbers are extracted and inserted
- [ ] All vague language is replaced with quantitative statements
- [ ] Structure follows standard scientific paper format
- [ ] Transitions are smooth
- [ ] Abstract is complete and quantitative
- [ ] Methods are reproducible
- [ ] Results are supported by data
- [ ] Discussion is balanced (claims + limitations)

---

## Estimated Word Counts

- **Abstract**: 180–300 words
- **Introduction**: 500–800 words
- **Methods**: 2000–3000 words
- **Results**: 2000–3000 words
- **Discussion**: 1500–2000 words
- **Total**: ~6000–9000 words (typical for PRX Life / Nat Comms)

---

## Next Steps After This Check

1. If structure is complete → Move to LaTeX
2. If numbers are missing → Run data extraction (`DATA_EXTRACTION_TEMPLATE.md`)
3. If language is vague → Apply tightening guide (`PAPER_TIGHTENING_GUIDE.md`)
4. If sections are missing → Draft missing pieces
5. If flow is rough → Revise transitions

