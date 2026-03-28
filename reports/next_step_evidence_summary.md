# Next Step Evidence Summary: Biological Countercurvature

## 1. What is Stronger Now Than Baseline
- **Data Provenance & Integrity**: We have established a rigorous audit trail (`reports/evidence_freshness_audit.md`) confirming that schema drifts are absent and establishing exactly which candidate metrics are static across runs.
- **Confidence-Weighted Signal Separation**: By filtering out low-confidence predictions (`pLDDT < 70`), we have isolated a robust set of structural anchors (CNNM2, FBLN5, STOML3, PANX3, PIEZO2) that possess both high anisotropy and adequate structural certainty (`reports/confidence_weighted_structural_evidence.md`).
- **Claim Discipline Matrix**: A formal framework (`reports/countercurvature_claims_matrix.md`) now explicitly maps every major claim to its underlying data tier, separating confirmed metrics from unsupported narratives (e.g., the false "evolution" of static LBX1/PIEZO2 metrics in Jan-Feb).
- **LBX1 Characterization**: LBX1's profile as an intermediate-anisotropy, highly blocky, low-confidence candidate is now explicitly defined and separated from high-confidence tension rods like PIEZO2.

## 2. What Remains Weak (Evidence AGAINST / Weakening the Hypothesis)
- **LBX1 Structural Uncertainty**: The low overall pLDDT (66.9) of LBX1 means its proposed "modular spring" architecture (suggested by high PAE blockiness) might simply be an artifact of long, unstructured Intrinsically Disordered Regions (IDRs).
- **Hypothesis Inflation in Historical Reports**: The audit revealed that narratives describing "emerging" or "evolving" structural classes for core genes (LBX1, PIEZO2, LMNA) over the Jan-Feb window were based on repeatedly sampling static, identical metric vectors. This significantly weakens any temporal or causal inferences made during that period.
- **Speculative Extreme Sensors**: Candidates like POC5 and GHR show extreme anisotropy but suffer from low confidence, making them unreliable as primary evidence for a tension-rod architecture without orthogonal biological validation.

## 3. Top 3 Highest-Leverage Next Experiments (Falsifiability)
To definitively test the Biological Countercurvature hypothesis and LBX1's role, the following experiments (`reports/lbx1_falsifiability_plan.md`) must be executed:

1. **Nuclear Tension-Dependent Localization**: Perturb nuclear tension via LMNA/LINC complex disruption and measure LBX1 nuclear/cytoplasmic ratio. *Falsification*: If localization is unchanged under tension depletion, LBX1 is not a mechanosensitive relay.
2. **Single-Molecule Force Spectroscopy (smFS)**: Pull recombinant LBX1 protein via AFM to measure unfolding force peaks and contour length increments. *Falsification*: If LBX1 unfolds as a single catastrophic event at high forces (globular) or shows no resistance (pure disorder), the "modular spring" model is invalid.
3. **In Vivo Mechanotransduction via Orthogonal Reporter**: Degrade LBX1 in 3D somite tissue and measure downstream mechanosensitive gene expression (YAP/TAZ targets) under cyclical stretch. *Falsification*: If target gene expression is preserved despite LBX1 degradation, LBX1 is not a required primary mechanotransducer.
