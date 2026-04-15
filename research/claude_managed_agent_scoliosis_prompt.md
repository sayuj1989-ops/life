# Claude Managed Cloud Agent — Scoliosis Research Completion Prompt

**Purpose:** Paste this prompt into Claude's Managed Cloud Agent (with web search, code execution, and file tools) to complete remaining research gaps in the manuscript *"The Allometric Trap: Scaling Laws Predict When Growing Organisms Cannot Afford Their Own Shape"* (branch `claude/strengthen-manuscript-Avo07`).

The manuscript argues that Adolescent Idiopathic Scoliosis (AIS) is the clinical manifestation of a **universal scaling law**: the Bio-Gravitational Number $\mathcal{B}_g = EI/(MgL^2)$ and the $L^4$-vs-$L^2$ energy deficit that opens during the adolescent growth spurt. Scoliosis is framed as *metabolic buckling* driven by a Hopf bifurcation in a delayed proprioceptive control loop (the "Derivative Gain Trap").

---

## ROLE

You are a senior computational biophysicist + scientific editor with deep fluency in:
- Cosserat rod / continuum mechanics and delay differential equations (DDEs)
- Allometric scaling (West–Brown–Enquist, Niklas plant mechanics, vertebrate biomechanics)
- Adolescent Idiopathic Scoliosis (AIS) epidemiology and genetics (LBX1, GPR126, etc.)
- AlphaFold 3 structural prediction and mechanosensory protein biology (PIEZO1/2, Vimentin, Lamin A/C)
- eLife / Nature editorial standards

## MISSION

Close the remaining evidence gaps in the manuscript so that it can withstand reviewer scrutiny at **eLife** (primary target) and a re-submission to **Nature / Nature Communications** (secondary). Do this by (1) sourcing quantitative literature values, (2) validating model predictions against public datasets, (3) hardening the theoretical scaffolding, and (4) identifying the single most fundable experimental validation.

**Hard constraint:** Every numerical claim you add or revise must cite a peer-reviewed source (DOI or PubMed ID). Flag estimates clearly. Do not fabricate references.

---

## REPOSITORY CONTEXT

- Branch: `claude/strengthen-manuscript-Avo07`
- Manuscript root: `manuscript/main.tex` with sections in `manuscript/sections/`
- Species data: `data/species_parameters.csv`
- AlphaFold analysis: `research/alphafold_v6_analysis/`
- Recent strengthening commit: `af47b2e` ("Strengthen manuscript for eLife: reframe as universal scaling law paper")
- Key equations already in text:
  - $\mathcal{B}_g = EI/(MgL^2)$ (passive); $\mathcal{B}_g = \chi_M \langle|\nabla I|\rangle/(\rho A g L^2)$ (active)
  - DDE: $\rho A \ddot{\kappa} + \eta \dot{\kappa} + EI\,\partial_s^4 \kappa + K_P \kappa(s,t-\tau) + K_D \dot{\kappa}(s,t-\tau) = 0$
  - Energy deficit: demand $\propto L^4$, supply $\propto L^2$

---

## WORK PACKAGES (execute in order; deliver each before moving on)

### WP1 — Harden the Cross-Species $\mathcal{B}_g$ Table (HIGH PRIORITY)

**Problem:** `manuscript/sections/tables.tex` lists $\mathcal{B}_g$ for 10 species (mouse → elephant). Several $EI$ values are estimates. Reviewers will demand primary sources.

**Tasks:**
1. For each species in the table (mouse, rat, rabbit, cat, dog, chimpanzee, human child, human adult, horse, elephant), find published measurements or well-justified estimates of:
   - Vertebral column length $L$ (sacrum to atlas, in meters)
   - Body mass $M$ (kg) for the same individuals
   - Flexural stiffness $EI$ (N·m²) — prefer *in vitro* three-point bending of isolated vertebral segments; fall back to $E_\text{bone} \cdot I_\text{area}$ with documented geometry
2. Add **giraffe** and **dolphin** as boundary cases (extreme neck/tail ratios; dolphin is a quadruped-derived marine swimmer whose $\mathcal{B}_g$ tests whether the Allometric Trap is gravity-specific).
3. Recompute $\mathcal{B}_g = EI / (M g L^2)$ with $g = 9.81$ m/s².
4. Fit a power law $\mathcal{B}_g \propto M^\alpha$ across species. Report $\alpha$, 95% CI, and $R^2$. Compare against the claimed exponent $\alpha = -0.282 \pm 0.072$ in `tables.tex`.

**Deliverables:**
- Updated `data/species_parameters.csv` with a `source_doi` column
- A markdown report `research/bg_cross_species_audit.md` with the fit, residual plot, and species-by-species citations
- A recommended revised Table 1 (LaTeX snippet ready to paste)

**Useful search terms:** "vertebral flexural stiffness mammal", "three-point bending vertebra [species]", "spinal column bending modulus in vivo", "allometric scaling vertebral bone elastic modulus", "Niklas biomechanics plant animal comparison".

---

### WP2 — Validate the Hopf Bifurcation Prediction Against AIS Epidemiology

**Claim in manuscript:** Scoliosis onset coincides with the developmental window where neural delay $\tau(t)$ crosses $\tau_c$ (derivative gain trap). Model predicts:
- Peak incidence at **peak height velocity (PHV)**, not at peak height
- Girls affected ~5–8× more than boys (earlier, shorter PHV → narrower buffer against trap)
- Curve magnitude correlates with growth velocity $dL/dt$, not $L$ alone

**Tasks:**
1. Find 3–5 published AIS cohort studies (2010–2026) with longitudinal height velocity + Cobb angle data. Priority sources: Little et al., Charles et al., Skaggs, Sanders; UK Biobank; BrAIST trial.
2. Extract or digitize the incidence-vs-age curve and PHV-vs-Cobb curve.
3. Run a statistical test of the prediction "$|dL/dt|$ predicts Cobb progression better than $L$ or chronological age." Use logistic regression or Cox proportional hazards where data allow.
4. Identify any datasets that **contradict** the prediction and document them honestly.

**Deliverables:**
- `research/ais_epidemiology_validation.md` with the extracted data, analysis script (Python + scipy), and a verdict: "supported / mixed / refuted"
- A revised paragraph for `sections/results.tex` (subsection: "Clinical epidemiology mirrors the bifurcation boundary")
- A clearly-labeled figure (`figures/ais_phv_validation.pdf`) if data permit

**Useful sources:** PubMed, ClinicalTrials.gov, SRS (Scoliosis Research Society) proceedings, medRxiv, Cochrane AIS reviews.

---

### WP3 — Validate the DDE/Derivative-Gain-Trap Framework Against Postural Control Literature

**Claim:** The spine's active control obeys a PD-DDE with time delay $\tau$ that grows during the adolescent spurt because nerve conduction velocity does not scale with height. Hopf bifurcation at $\tau_c$.

**Tasks:**
1. Find the best modern references for:
   - Upright postural control as a delayed PD/PDA system (Milton, Insperger, Stepan, Kiemel, Loram, Collins)
   - Age-dependence of H-reflex / stretch reflex latency in children vs adolescents vs adults
   - Nerve conduction velocity (NCV) scaling with limb length (Lang 1985, Robinson 2001 already cited — find newer)
2. Compute a plausible $\tau_c$ for the spine given published $K_P$, $K_D$ estimates, and spinal $\rho A$ / $EI$. Compare to the observed adolescent $\tau$.
3. Check whether the Hopf predicts the correct dominant spatial mode (thoracic right-convex, apex near T8). This is a specific falsifiable prediction — the eigenvector structure of the linearized DDE with clamped-free boundaries should peak around $s/L \approx 0.6$.

**Deliverables:**
- `research/dde_hopf_validation.md` with the parameter table, calculated $\tau_c$, and eigenmode analysis
- A short appendix section (LaTeX) justifying the DDE parameters

---

### WP4 — Strengthen the Molecular (AlphaFold) Evidence

**Current claim:** Demand-side mechanosensors (anisotropy $3.08 \pm 1.44$) are more anisotropic than supply-side regulators ($1.79 \pm 0.56$); $p = 0.011$, Cohen's $d = 1.19$.

**Tasks:**
1. Re-download full-length structures from **AlphaFold Database (latest version) and AlphaFold 3 server** for:
   - PIEZO2 (Q9H5I5) — full 2822 residues, currently truncated to 709 in our table
   - PIEZO1 (Q92508) — full 2521 residues
   - TRPV4 (Q9HBA0), ASIC3 (Q9UHC3), TREK-1 (O95069), TMC1 (Q8TDI8) — additional mechanosensors not yet included
   - DPYSL4, SCUBE3, HSPG2 — AIS GWAS hits (check)
2. Recompute anisotropy (principal moments of inertia ratio), radius of gyration, pLDDT, and IDR fraction.
3. Redo the Mann–Whitney U test with the expanded sample. Report whether the 72% gap holds.
4. Check known AIS GWAS loci (LBX1, GPR126/ADGRG6, PAX1, BNC2, SOX9) for anisotropy — is the "Demand" signature enriched in AIS-associated genes?

**Deliverables:**
- Updated `research/alphafold_v6_analysis/anisotropy_summary_v7.csv`
- Revised `sections/tables.tex` Table 3 (thermodynamic cost proteins)
- `research/alphafold_ais_gwas_overlap.md` with enrichment test (Fisher's exact)

---

### WP5 — Literature Landscape: Competing and Complementary 2024–2026 Work

**Tasks:**
1. Search for recent (2024–2026) theoretical / computational work on:
   - Scoliosis etiology (especially zebrafish urotensin/reissner's fiber work, cilia models)
   - Scaling laws in vertebrate biomechanics
   - Active matter / active rods / morphogenesis under gravity
   - Delay-induced instabilities in biology
2. For each relevant paper, write 2–3 sentences on (a) what they found, (b) how it relates to the Allometric Trap, (c) whether it supports, complements, or competes with our framework.
3. Identify 3–5 citations to **add** to the Discussion section and 0–2 that require a **defensive** response in the revised manuscript.

**Deliverables:**
- `research/literature_landscape_2024_2026.md`
- BibTeX entries appended to `manuscript/references.bib`
- A revised "Relation to existing models" paragraph for `sections/discussion.tex`

---

### WP6 — The Single Most Fundable Experiment

**Tasks:**
1. Propose ONE experiment that would decisively validate (or falsify) the Allometric Trap / Derivative Gain Trap hypothesis, feasible within a standard R01 / Wellcome budget.
2. Criteria:
   - Directly tests a quantitative prediction of the model (e.g., $\tau_c$, $dL/dt$-dependence, NAD+ rescue, pulsatile loading circadian prediction)
   - Uses an existing, validated model system (zebrafish *ptk7*, mouse *Lbx1*, ferret, organoid)
   - Produces a binary outcome within 18 months
3. Sketch the experimental design, required N, primary endpoint, and go/no-go criterion.

**Deliverables:**
- `research/fundable_experiment_proposal.md` (2–3 pages, grant-ready language)

---

### WP7 — Editorial and Reference Audit

**Tasks:**
1. Run a full reference audit on `manuscript/references.bib`:
   - Every `\cite{}` key in `manuscript/sections/*.tex` resolves
   - Every bib entry has a DOI or URL
   - No Wikipedia, no predatory journals
2. Check every numerical claim in abstract, introduction, and results against its source.
3. Verify equation numbering, figure numbering, and table numbering are consistent after the reframe.
4. Check `cover_letter.tex` matches the current title and the target journal the user is submitting to.

**Deliverables:**
- `research/editorial_audit_report.md` with a red/yellow/green table of every citation
- A patch file or list of Edit-tool operations ready to apply

---

## OPERATING RULES

1. **Cite or flag.** Any number you write down without a source must be wrapped in `\todo{SOURCE NEEDED}`.
2. **Show your work.** Every statistical test includes the raw data, code, and seed.
3. **Prefer primary sources.** Use review articles only for orientation.
4. **Respect the frame.** The paper's headline is the *universal scaling law*. Scoliosis is the validation case, not the subject. Do not let WP2 drift into a clinical paper.
5. **Report honestly.** If a prediction is not supported by the data you find, say so and propose a revision or a caveat — do not hide it.
6. **Keep commits clean.** Make one commit per work package on branch `claude/strengthen-manuscript-Avo07` with messages of the form `WP<n>: <summary>`.
7. **Do not alter** the DDE / Hopf bifurcation / Derivative Gain Trap / Polygenic Threshold content added by the user post-commit `af47b2e` unless explicitly improving it — the user considers those edits intentional.

## FINAL DELIVERABLE

At the end, produce `research/strengthening_report_final.md` containing:
- Executive summary (1 page): what was validated, what was revised, what remains open
- Updated abstract (~200 words) reflecting any new findings
- A reviewer-response-style table: "anticipated reviewer critique → our evidence"
- A go/no-go recommendation: submit to eLife as-is, or hold for experiment X?

## SUCCESS CRITERIA

- Every $\mathcal{B}_g$ row in Table 1 has a DOI
- At least one public dataset tested the $dL/dt$-vs-Cobb prediction
- The AlphaFold anisotropy gap either survives expansion to n≥30 proteins or is honestly retracted
- The manuscript compiles cleanly (`pdflatex main.tex` + `bibtex`) with no undefined references
- All changes pushed to `claude/strengthen-manuscript-Avo07`

---

**Begin with WP1. Confirm your plan in one paragraph, then execute.**
