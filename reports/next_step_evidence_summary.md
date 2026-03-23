# Next-Step Evidence Summary: Biological Countercurvature

## Overview
A rigorous audit of the AlphaFold structural pipeline (AFCC) has refined the evidentiary basis for the Biological Countercurvature hypothesis. By enforcing a strict distinction between measured structural data and generated narrative hypothesis, we have isolated robust mechanical candidates from speculative ones.

## What is Stronger Now Than Baseline
1. **Identification of Bona Fide Structural Rods**: By weighting anisotropy by pLDDT confidence, we have confirmed a reliable set of high-confidence, load-bearing mechanical elements: **FBLN5, STOML3, PANX3, PIEZO2, ROCK1, and ADGRG6**. These are prime candidates for forming the tension network predicted by the countercurvature model.
2. **Data Integrity Discipline**: We implemented an automated freshness audit (`scripts/analysis/evidence_freshness_audit.py`) that successfully caught the repetition of static structural metrics across runs. This prevents the "hallucination" of structural evolution and grounds all future claims in verified data changes.
3. **Falsifiability Framework**: The hypothesis surrounding LBX1's mechanical role is no longer a "just-so" story; it is now bounded by three concrete, quantitative falsification experiments (`reports/lbx1_falsifiability_plan.md`), shifting the project from pure computational mining to testable biophysics.

## What Remains Weak (Evidence AGAINST the Current Hypothesis Narrative)
1. **LBX1's Role as a Direct Mechanosensor**: The baseline narrative strongly implied LBX1 had a unique structural or mechanical geometry. The data confirms this is **weak**: LBX1 has low overall confidence (pLDDT=66.9) and intermediate anisotropy (2.27), lacking the robust structural signatures of known mechanosensors like PIEZO2 or LMNA.
2. **Extreme Anisotropy Outliers**: The extreme anisotropy seen in candidates like POC5 (24.69) and GHR (5.13) is driven primarily by low-confidence (disordered) regions. Treating these as rigid "tension rods" is highly speculative and likely an artifact of the metric calculation on flexible tails.
3. **Temporal Structural "Evolution"**: Previous cluster reports narrated changes or "emergence" of structural classes over time. The audit proved that the underlying per-gene metrics for core candidates (LBX1, PIEZO2, LMNA) were 100% static across January and February. The temporal narrative was an artifact of clustering, not a biological or computational measurement of changing geometry.

## Top 3 Highest-Leverage Next Experiments
To transition from computational generation to physical validation, we must prioritize the following experiments:

1. **Biophysical Profiling of Low-Confidence Outliers (POC5, GHR)**:
   - *Why*: To resolve whether extreme computational anisotropy in low-pLDDT proteins represents rigid mechanical rods or simply highly flexible, disordered chains.
   - *How*: Perform single-molecule Force Spectroscopy (AFM) or Small-Angle X-ray Scattering (SAXS) on purified POC5 and GHR.
2. **LBX1 Domain-Deletion Mechanotransduction Assay**:
   - *Why*: To determine if LBX1's "blocky" architecture actually couples to mechanical forces, testing the core countercurvature claim about its role.
   - *How*: Subject cells expressing WT vs. linker-deleted LBX1 to controlled substrate stretch and quantify nuclear localization and target transcription (e.g., *Atoh1*).
3. **LINC Complex Dependency of Spinal Candidates**:
   - *Why*: The countercurvature model requires continuous force transmission from the extracellular matrix to the nucleus.
   - *How*: Perform Co-IP assays mapping the physical interaction network between high-confidence extracellular/membrane rods (FBLN5, PIEZO2), nuclear envelope mechanotransducers (LMNA), and downstream effectors (LBX1) under varied tension states.
