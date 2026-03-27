# Next Step Evidence Summary

This document synthesizes the updated evidence base for the Biological Countercurvature hypothesis, carefully distinguishing data-grounded measurement from speculative narrative and identifying critical next steps.

## What is Stronger Now Than Baseline
1. **High-Confidence Structural Mechanosensors**: The confidence-weighted analysis (`reports/confidence_weighted_structural_evidence.md`) has isolated `CNNM2` (anisotropy 8.54, pLDDT 70.4), `FBLN5` (anisotropy 7.05, pLDDT 83.3), and `PIEZO2` (anisotropy 4.44, pLDDT 79.4) as the most reliable, robust candidates for structurally extended, anisotropic load-bearing elements.
2. **Methodological Rigor**: The creation of a dedicated Evidence Freshness Audit (`reports/evidence_freshness_audit.md`) systematically detected reused, static metric vectors (e.g., LBX1, PIEZO2, LMNA identical across 10+ runs), preventing the hallucination of temporal structural "trends" and enforcing data integrity.
3. **Claim Stratification**: The `reports/countercurvature_claims_matrix.md` rigorously bins all current claims into confirmed, supported, and speculative tiers, directly tying them to the authoritative February 16, 2026 snapshot.

## What Remains Weak (Evidence Against the Current Hypothesis)
1. **LBX1 Structural Role is Weakly Supported**: As identified in the baseline report and confirmed by our `outputs/afcc/confidence_weighted_ranking.csv` snapshot, LBX1 possesses low structural confidence (pLDDT 66.9), intermediate anisotropy (2.27), and high PAE blockiness (7.35). Current structural data alone is insufficient to conclude LBX1 functions as an extended mechanical "tension rod."
2. **Exploratory Outliers Lack Reliability**: Proteins with extreme anisotropy like `POC5` (24.69) and `GHR` (5.13) suffer from very low confidence (pLDDT 64.0 and 58.7, respectively). Their "extended" geometries are highly likely to be AlphaFold modeling artifacts of intrinsically disordered regions (IDRs), rather than true rigid structures.
3. **Narrative Inflation**: Narrative reports and cluster notes (`reports/structure_clusters/`) have repeatedly interpreted static inputs as evolving or emergent structural classes without underlying metric drift, threatening the hypothesis's objective credibility.

## Top 3 Highest-Leverage Next Experiments
To defend this framework in high-impact publication, experimental falsification must replace narrative speculation. Based on the `reports/lbx1_falsifiability_plan.md`, the critical next steps are:

1. **In Vitro Nuclear Tension Perturbation (LBX1 Falsification)**: Subject somite-derived cells expressing tagged LBX1 to cyclic stretch and LINC complex disruption (LMNA knockdown). *Falsification criteria*: If LBX1 localization/activity fails to change under varying tension, its direct mechanosensory role is falsified.
2. **Biophysical Stiffness Measurement via Single-Molecule AFM**: Perform atomic force microscopy (AFM) on purified full-length LBX1 to empirically measure unfolding force and contour length extension, comparing its behavior to validated mechanosensors like Talin. *Falsification criteria*: If it behaves as a simple globular protein without blocky/stepwise unfolding, the extended tension rod hypothesis is falsified.
3. **Orthogonal Validation of Low-Confidence Outliers**: Before relying on `POC5` or `GHR` geometry, perform cross-linking mass spectrometry (XL-MS) or limited proteolysis to determine if these predicted highly extended states exist in vivo or are purely computational artifacts of intrinsically disordered domains.
