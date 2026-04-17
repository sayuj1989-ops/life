# Spine Submission Roadmap

**Target:** *eLife* (primary) / *Spine Deformity* — Springer (fallback)
**IF:** eLife (IF: 6.4) | Spine Deformity (IF: 2.6)
**Strategy:** "The Allometric Trap" — AIS as a growth-velocity-gated Hopf bifurcation. Unified Active Inference + Cosserat + allometric scaling framework.
**Start Date:** 2026-02-23
**Target Submission Date:** 2026-05-01
**Last Updated:** 2026-04-16

---

## Phase 1: Computational Framework ✅ COMPLETE

- [x] **Core Model:** Energy Deficit model (`experiment_energy_deficit_window.py`)
- [x] **Rescue Cliff:** Validated at Anisotropy ~2.4 (`outputs/sim/2026-02-22/`)
- [x] **Spinal Jetlag:** Circadian modulation simulation (`experiment_spinal_jetlag.py`)
- [x] **Robustness:** Sensitivity analysis across parameter sweeps
- [x] **Active Inference Simulation:** Full PD-precision-collapse simulation (`managed_agent/active_inference_simulation.py`, 687 lines)
  - Confirmed Hopf bifurcation mechanics: `Kd_eff` vs `Kd_crit` dynamics reproduced
  - Figure generated: `managed_agent/active_inference_buckling.png`
  - Healthy vs AIS-susceptible parameter regimes distinguished

## Phase 2: Clinical & Theoretical Validation ✅ COMPLETE

- [x] **Cohort Data:** Weinstein 1983 / Lonstein 1984 curve progression data
- [x] **PHV Timing:** Instability window vs PHV timing validated (sex-stratified; WP8)
- [x] **Sexual Dimorphism:** Female-to-male ratio explained (earlier PHV + prolonged $R > R_{crit}$)
- [x] **Literature Landscape:** WP5 — 35 papers evaluated, 12 Tier-1 citations integrated, defensive responses to Castelein 2005 and Machida 1993 drafted
- [x] **Cross-species Scaling:** WP4 — allometric safety factor computed for 5 species
- [x] **Fundable Experiment Design:** WP6 — NAD+ mouse rescue study (R21, $500K, 18 months) fully specified with power analysis
- [x] **IEC Framework:** Multi-scale cascade (Levels 1–5) with Cosserat integration and vector-mismatch analysis

## Phase 3: Manuscript Preparation ✅ COMPLETE

- [x] **Unified Markdown Draft:** `research/manuscript_allometric_trap.md` (~4,800 words, full IMRaD)
- [x] **LaTeX Manuscript:** `spine_submission/allometric_trap_manuscript.tex` (submission-ready)
- [x] **BibTeX References:** `spine_submission/references.bib` (35 entries, Tier-1 verified)
- [x] **Abstract:** 215 words + Significance Statement
- [x] **Falsifiable Predictions:** Three numbered predictions (H-reflex, NAD+ rescue, cross-species)
- [x] **Relation to Existing Models:** Defensive + integrative framing for RF/CSF, Castelein, melatonin models
- [x] **Supplementary Appendices:** Kd_crit derivation + sensitivity analysis written

## Phase 4: Submission Packaging 🔲 IN PROGRESS

- [ ] **Figure 1:** Copy/polish `managed_agent/active_inference_buckling.png` → `spine_submission/figures/`
- [ ] **Figure 2:** Generate thermodynamic instability windows plot (age-stratified R(t) curves)
- [ ] **Figure 3:** Generate vector-mismatch / alignment-parameter heat map (coronal vs sagittal)
- [ ] **Figure 4:** Multi-scale mechanistic cascade schematic
- [ ] **Cover Letter:** Author cover letter for eLife submission portal
- [ ] **ORCID / Author Declaration:** Complete eLife author information form
- [ ] **LaTeX PDF Compile:** Run `pdflatex allometric_trap_manuscript.tex` → verify output
- [ ] **Reference audit:** Cross-check all [VERIFY] tags in `references.bib` against PubMed
- [ ] **Preprint:** Upload to bioRxiv before submission (eLife requires this)

## Key Files

| File | Description |
|------|-------------|
| `spine_submission/allometric_trap_manuscript.tex` | **Primary submission manuscript** |
| `spine_submission/references.bib` | BibTeX references |
| `research/manuscript_allometric_trap.md` | Markdown version (co-authoring) |
| `managed_agent/active_inference_simulation.py` | Simulation code (687 lines) |
| `managed_agent/active_inference_buckling.png` | Figure 1 raw output |
| `managed_agent/wp5_output.md` | Literature landscape & BibTeX entries |
| `managed_agent/wp6_output.md` | Fundable experiment design (R21 spec) |
| `managed_agent/wp7_output.md` | References database |
| `managed_agent/wp8_output.md` | Active Inference ↔ PID derivation |

## Progress Tracking

**Current Phase:** Phase 4 (Submission Packaging)
**Percent Complete:** 75% (3 of 4 phases complete)
**Status:** Manuscript ready — figures, cover letter, and final audit needed
