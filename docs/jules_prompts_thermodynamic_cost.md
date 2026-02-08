# Google Jules Prompts for Incremental Research Completion

## Overview

These 4 prompts are designed for Google Jules AI to execute sequentially on the repository `sayujks0071/life` (branch: `main` after PR #489 is merged). Each prompt is a self-contained, incremental task that builds on prior work.

---

## Prompt 1: Complete Empty Manuscript Theory Subsections and Add Thermodynamic Cost Table

**Branch name:** `jules/manuscript-theory-completion`

```
You are working on the repository sayujks0071/life, a research manuscript on "Biological Countercurvature of Spacetime" — a framework proposing that developmental information acts as biological countercurvature against gravity, formalized via Information-Elasticity Coupling (IEC).

TASK: Complete two empty subsections in manuscript/sections/theory.tex and add a new table for thermodynamic cost proteins.

### 1. Fill in "Rod Geometry and Kinematic Parameterization" (line 5)

This subsection should define the Cosserat rod parameterization used throughout the paper. Content to include:
- The spine centerline r(s) parameterized by arc length s ∈ [0, L]
- The local material frame {d1(s), d2(s), d3(s)} attached to each cross-section
- Curvature vector κ(s) and twist τ(s) defined via the Darboux vector
- Strain measure ε(s) for extensibility
- Physical interpretation: s=0 is sacrum (clamped), s=L is cranium (free)
- Keep it concise (15-20 lines of LaTeX). Reference Goriely 2017 and Gazzola 2018 which are already in references.bib.

### 2. Fill in "Developmental Information Fields from Morphogenetic Patterning" (line 7)

This subsection should define the scalar information field I(s). Content to include:
- I(s) as a coarse-grained representation of the HOX gene expression pattern along the spine
- The bimodal Gaussian parameterization (already defined in methods.tex Eq. 3): cervical peak (A_c=0.5, s_c=0.80) and lumbar peak (A_l=0.7, s_l=0.25)
- Physical interpretation: peaks correspond to regions of high vertebral identity specification
- The gradient ∂I/∂s as the "curvature generator" that drives rest curvature
- Brief mention that AlphaFold analysis of HOX proteins (HOXC8, HOXB13) confirms structural specificity (already mentioned later in theory.tex line 10, so just introduce the concept here)
- Keep it concise (15-20 lines of LaTeX).

### 3. Add a new Table 2 to manuscript/sections/tables.tex

Add a table summarizing the 16 thermodynamic cost proteins mapped to the three dissipation terms. The data is in outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv. Table columns should be:
- Gene | UniProt | Dissipation Term (η_p / η_a / Γ_m) | Anisotropy | Morphology | pLDDT | Residues | L-Scaling

Group rows by dissipation term. Add a caption referencing the free energy dissipation functional (Eq. \ref{eq:dissipation}).

Also add \ref to this table from the AlphaFold paragraph in theory.tex (line 110, the paragraph starting "The three dissipation terms are not abstract").

### CONSTRAINTS:
- Follow existing LaTeX style conventions in the manuscript (use \mathrm{} for subscript text, \emph{} for emphasis, \cite{} for references)
- Only use references already in references.bib
- Do not modify any existing content — only fill empty subsections and add the new table
- Commit with message: "feat: complete theory subsections and add thermodynamic cost protein table"
- Create a PR to main
```

---

## Prompt 2: Simulate P_counter(L) Energy Deficit Window and Add Results to Manuscript

**Branch name:** `jules/energy-deficit-simulation`

```
You are working on the repository sayujks0071/life, a research project on biological countercurvature of spacetime. The manuscript formalizes a "thermodynamic cost of countercurvature" with a metabolic scaling equation:

P_counter ~ η_a * ρ * A * g * L² * <|κ_IEC - κ_passive|²>

TASK: Create a simulation that computes P_counter as a function of spinal length L, identifying the critical L where the Energy Deficit Window opens, and add the results to the manuscript.

### Step 1: Create scripts/experiment_energy_deficit_window.py

Write a Python script that:

1. Uses the existing IEC beam solver in src/spinalmodes/model/solvers/euler_bernoulli.py (or the simpler src/spinalmodes/iec.py) to compute equilibrium curvature profiles κ_IEC(s) and κ_passive(s) for varying rod lengths L.

2. Parameter sweep:
   - L from 0.25 to 0.55 m in 30 steps (covering pre-adolescent through adult)
   - Use the standard IEC parameters from manuscript/sections/methods.tex (χ_κ=0.05, E0=1.0 GPa, ρ=1100 kg/m³, A=0.001 m²)
   - Information field: bimodal Gaussian (A_c=0.5, s_c=0.80, σ_c=0.08, A_l=0.7, s_l=0.25, σ_l=0.10, I_0=0.3)

3. For each L, compute:
   - κ_IEC(s) from the full IEC model
   - κ_passive(s) from the same model with χ_κ = 0 (gravity only)
   - P_counter(L) = η_a * ρ * A * g * L² * mean(|κ_IEC - κ_passive|²)
   - Use η_a = 1.0 (normalized units, we care about the scaling shape)

4. Also compute a "proprioceptive supply capacity" curve:
   - S_proprio(L) = S_0 * (L / L_0)^α where α ∈ {0.5, 1.0} (sublinear maturation)
   - L_0 = 0.35 m (pre-adolescent reference), S_0 = P_counter(L_0)
   - The intersection P_counter(L) = S_proprio(L) defines L_crit

5. Save results to outputs/thermodynamic_cost/energy_deficit_window.csv with columns: L, P_counter, S_proprio_alpha05, S_proprio_alpha10, Cobb_angle, D_geo

6. Generate a figure (matplotlib) showing:
   - P_counter(L) curve (red, solid)
   - S_proprio(L) curves for both α values (blue, dashed)
   - Shaded "Energy Deficit Window" between the crossings
   - Save to outputs/figures/energy_deficit_window.png

### Step 2: Add results to manuscript/sections/results.tex

Add a new paragraph at the end of section 4.6 (Growth Dynamics) presenting:
- The P_counter(L) scaling result (confirm it matches L² or L³)
- The critical length L_crit where the energy deficit window opens
- Reference the new figure

### Step 3: Add figure caption to manuscript/sections/figures.tex

Add a Figure 6 entry for the energy deficit window plot.

### CONSTRAINTS:
- Check existing code in src/spinalmodes/ before writing new solvers — reuse existing infrastructure
- If the existing solvers don't work directly, write a self-contained minimal beam solver in the script
- Run the script and verify it produces output before committing
- Commit message: "feat: simulate P_counter(L) energy deficit window with figure"
- Create a PR to main
```

---

## Prompt 3: Expand AlphaFold Pipeline with Missing Metabolic Proteins

**Branch name:** `jules/afcc-metabolic-expansion`

```
You are working on the repository sayujks0071/life, which includes an AlphaFold Countercurvature (AFCC) analysis pipeline in research/alphafold_countercurvature/. The pipeline fetches AlphaFold-predicted protein structures and computes structural metrics (anisotropy, radius of gyration, pLDDT, hinge candidates).

TASK: Add 6 missing metabolic proteins to the AFCC pipeline that are critical for the "supply side" (Γ_m term) of the thermodynamic cost framework but are currently absent from data/candidates_master.csv.

### Missing proteins to add:

1. PPARGC1A (Q9UBK2) — PGC-1α; mitochondrial biogenesis master regulator; determines energy SUPPLY capacity
2. IGF1R (P08069) — Insulin-like growth factor 1 receptor; mediates growth plate signaling
3. GHR (P10912) — Growth hormone receptor; master regulator of adolescent growth spurt rate
4. ARNTL (O00327) — BMAL1; circadian clock TF in intervertebral disc
5. DMD (P11532) — Dystrophin; cytoskeleton-ECM linker in paraspinal muscle (η_a term)
6. MYLK (Q15746) — Myosin light chain kinase; tonic contraction regulator (η_a term)

### Steps:

1. Add these 6 proteins to data/candidates_master.csv following the existing CSV format. Look at the existing entries to understand the column structure (gene, uniprot, category, etc.). Assign category "Thermodynamic_Cost".

2. Run the AFCC fetch pipeline to download their AlphaFold structures:
   - The fetch script is at research/alphafold_countercurvature/scripts/01_fetch_structures.py
   - Read its code to understand how to invoke it, or call the AlphaFoldFetcher class from research/alphafold_countercurvature/src/afcc/afdb.py directly
   - If the fetch script requires configuration, check research/alphafold_countercurvature/config/

3. Run the metrics computation pipeline:
   - The metrics script is at research/alphafold_countercurvature/scripts/02_compute_metrics.py
   - This computes anisotropy, Rg, pLDDT stats, hinge candidates, curvature, etc.
   - Output goes to outputs/afcc/YYYY-MM-DD/metrics.csv

4. Update outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv to include the 6 new proteins with their computed metrics.

5. Update the evidence note notes/evidence/2026-02-07__thermodynamic_cost_proteins.md:
   - Add the new proteins to the appropriate tables (DMD and MYLK to η_a; the rest to Γ_m)
   - Update the structural summary statistics (mean anisotropy per term)

6. Run scripts/regenerate_candidate_docs.py to update docs/candidate_registry.md

### CONSTRAINTS:
- The AlphaFold API is at https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id} — no auth needed
- Rate limit: max 5 requests/second
- If any protein fails to fetch, log it and continue with the rest
- Commit message: "feat: add 6 metabolic proteins to AFCC pipeline for thermodynamic cost analysis"
- Create a PR to main
```

---

## Prompt 4: Add Weekly Simulation Script for Energy Deficit Bifurcation Parameter Sweep

**Branch name:** `jules/weekly-sim-energy-deficit`

```
You are working on the repository sayujks0071/life, a research project modeling biological countercurvature of spacetime. The project includes weekly simulation scripts in scripts/ that perform parameter sweeps for the IEC (Information-Elasticity Coupling) spinal model.

TASK: Create a weekly simulation that performs a 2D parameter sweep of the Energy Deficit Window across (χ_κ, L) space, generating a phase diagram showing where AIS vulnerability is highest, and register the key finding as a new hypothesis.

### Step 1: Create scripts/weekly_sim_energy_deficit_bifurcation.py

Perform a 2D parameter sweep:
- χ_κ (IEC coupling strength): 0.01 to 0.10 in 20 steps
- L (spinal length): 0.25 to 0.55 m in 20 steps
- Fixed parameters: ρ=1100, A=0.001, g=9.81, E0=1.0 GPa

For each (χ_κ, L) pair, compute:
1. P_counter(χ_κ, L) — metabolic power required for countercurvature (from IEC energy functional)
2. Cobb angle from lateral asymmetry perturbation (ε_asym = 0.03)
3. D_geo (geodesic deviation metric)
4. The ratio R_deficit = P_counter / S_proprio where S_proprio = S_0 * (L/L_0)^0.7

Use the existing IEC solvers in src/spinalmodes/ — check src/spinalmodes/iec.py and src/spinalmodes/countercurvature/api.py for the high-level API. If they don't support direct P_counter computation, implement it using the energy functional from the theory section.

Generate three output files:
- outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv — full sweep data
- outputs/figures/phase_diagram_energy_deficit.png — 2D heatmap of R_deficit in (χ_κ, L) space, with contour lines marking R_deficit = 1 (the Energy Deficit boundary)
- outputs/figures/phase_diagram_energy_deficit_cobb.png — 2D heatmap of Cobb angle, showing where scoliosis emerges

### Step 2: Add hypothesis to notes/hypothesis_register.md

Append a new row:

| **H_2026_02_08_EnergyPhase** | The Energy Deficit Window in (χ_κ, L) parameter space forms a wedge-shaped instability region: high χ_κ patients enter the window at shorter L (earlier in adolescence) and exit later, experiencing a wider vulnerability window. Low χ_κ patients may never enter the window. | The P_counter scaling (L^{2-3}) combined with the information-coupling strength χ_κ creates a multiplicative effect: high χ_κ means higher curvature deviation from passive, thus higher P_counter at any L. | Compute the 2D phase diagram; validate by correlating pre-treatment χ_κ estimates (from initial radiographs) with age-at-onset in a retrospective AIS cohort. | Proposed |

### Step 3: Add a brief entry to notes/synthesis/ as a new weekly synthesis note

Create notes/synthesis/2026-02__energy_deficit_phase.md summarizing:
- The 2D phase diagram result
- The wedge-shaped instability region finding
- How this connects to clinical risk stratification (high χ_κ patients = earlier onset, wider window)

### CONSTRAINTS:
- Follow existing script patterns (look at scripts/weekly_sim_critical_anisotropy.py for style)
- Use matplotlib for figures, save with plt.savefig() and plt.close()
- All output paths should use Path objects
- Run the script and verify it produces output
- Commit message: "feat: weekly simulation — energy deficit bifurcation phase diagram in (χ_κ, L) space"
- Create a PR to main
```

---

## Execution Order

1. **Prompt 1** (Manuscript completion) — no code dependencies, can run first
2. **Prompt 3** (AFCC expansion) — no code dependencies, can run in parallel with Prompt 1
3. **Prompt 2** (P_counter simulation) — depends on existing IEC solvers, benefits from Prompt 1 context
4. **Prompt 4** (2D phase diagram) — builds on Prompt 2's solver approach, should run last
