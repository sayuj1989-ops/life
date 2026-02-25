# LBX1 Falsifiability Plan
**Date:** 2026-03-12
**Objective:** Define rigorous failure criteria for the "LBX1 Mechanosensor" hypothesis.

## Context
Structural analysis (Tier 3: Low Anisotropy/Low Confidence) has **falsified** the simple "Stiff Rod" model for LBX1. The remaining viable hypothesis is that LBX1 acts as a **"Condensate Sensor"** or **"Nuclear Shuttling Integrator"** driven by its modular/disordered architecture (High PAE Blockiness, Low pLDDT).

## Experiment 1: The "Nuclear Tether" Test (LINC Perturbation)
**Hypothesis:** LBX1 transcriptional activity depends on mechanical coupling between the cytoskeleton and nucleus via the LINC complex.
**Assay:**
1.  Culture paraspinal myoblasts on stiff (20 kPa) vs. soft (1 kPa) substrates.
2.  Transfect with Dominant-Negative KASH domain (disrupts LINC) or Control.
3.  Measure *LBX1* nuclear localization (IF) and downstream target expression (qPCR of *GDF5*, *FBLN5*).
**Readout:** Ratio of Nuclear/Cytoplasmic LBX1; Fold-change in targets.
**Expected Result (Support):** LINC disruption abolishes stiffness-dependent LBX1 nuclear accumulation.
**Falsification Threshold:**
*   If LBX1 nuclear levels remain unchanged by LINC disruption despite stiffness changes.
*   **AND** Target gene expression is unaffected by LINC state.
*   **Implication:** LBX1 is not mechanically coupled to nuclear tension; it is purely biochemical.

## Experiment 2: The "Blocky Domain" Deletion Series
**Hypothesis:** The high PAE Blockiness (7.35) indicates functional modularity. One specific domain confers mechanosensitivity (e.g., an IDR that collapses under pressure).
**Assay:**
1.  Generate GFP-tagged LBX1 variants: Full-Length, N-term only, C-term only, IDR-deletion.
2.  Subject cells to cyclic stretch (10%, 1Hz, 24h).
3.  Quantify nuclear entry and aggregate formation.
**Readout:** Nuclear/Cytoplasmic ratio; number of nuclear foci.
**Expected Result (Support):** Only Full-Length LBX1 responds to stretch; deletion of the IDR abolishes response.
**Falsification Threshold:**
*   If IDR-deletion mutant responds identically to Full-Length.
*   **OR** If no variant (including Full-Length) shows >1.5x change in localization/foci under stretch.
*   **Implication:** The "Blocky" architecture is structurally irrelevant to mechanics.

## Experiment 3: In Vitro Phase Separation (Condensation)
**Hypothesis:** LBX1's low confidence (pLDDT ~66) and modularity reflect an ability to undergo Liquid-Liquid Phase Separation (LLPS) in response to crowding (a proxy for compressive stress).
**Assay:**
1.  Purify recombinant LBX1-GFP.
2.  Titrate crowding agent (PEG-8000: 0%, 5%, 10%, 20%).
3.  Measure droplet formation via microscopy and FRAP (Fluorescence Recovery After Photobleaching).
**Readout:** Saturation concentration ($C_{sat}$); Diffusion coefficient ($D$).
**Expected Result (Support):** LBX1 forms droplets at physiological concentrations; $C_{sat}$ decreases with increased crowding (pressure sensor).
**Falsification Threshold:**
*   If LBX1 does not form droplets ($C_{sat} > 50 \mu M$).
*   **OR** If droplets are solid aggregates (no FRAP recovery) rather than liquid.
*   **Implication:** LBX1 is not a dynamic condensate; low pLDDT is just disorder, not function.

## Go/No-Go Decision Matrix
| Result Combination | Conclusion | Action |
| :--- | :--- | :--- |
| **Exp 1 Fail + Exp 3 Fail** | **LBX1 is NOT a mechanosensor.** | **DROP LBX1** as a primary candidate. Focus on PIEZO2/ADGRG6. |
| **Exp 1 Pass + Exp 3 Fail** | LBX1 is a LINC-dependent TF. | Reclassify as "Nuclear Responder" (not sensor). |
| **Exp 1 Fail + Exp 3 Pass** | LBX1 is a Crowding Sensor. | Reframe hypothesis around "Metabolic Crowding". |
| **Exp 1 Pass + Exp 3 Pass** | **Strong Confirmation.** | Proceed to *in vivo* Scoliosis models. |
