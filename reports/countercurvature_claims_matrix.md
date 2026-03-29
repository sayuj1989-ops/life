# Countercurvature Claims Matrix

## Overview
To enforce claim discipline for manuscript preparation, this matrix categorizes current hypotheses regarding the Biological Countercurvature into three distinct tiers of evidence derived strictly from measured AlphaFold structural metrics.

**Source Data Snapshot:** `outputs/afcc/2026-02-16/metrics.csv`

---

## Tier 1: Confirmed by Metrics
*These claims represent direct, robust geometric and confidence readouts replicated across runs.*

| Claim | Supporting Evidence | File Citation |
|---|---|---|
| **High Anisotropy Core:** `PIEZO2` and `ADGRG6` possess highly extended, anisotropic structures with adequate confidence, supporting their role as physical mechanosensors. | PIEZO2 (Anisotropy: 4.44, pLDDT: 79.4, PAE_blockiness: 2.80); ADGRG6 (Anisotropy: 3.06, pLDDT: 73.7, PAE_blockiness: 6.78). | `outputs/afcc/2026-02-16/metrics.csv` |
| **LBX1 Geometry:** `LBX1` is an intermediate-anisotropy, highly modular (blocky) protein with low structural confidence, lacking the continuous rigidity of classic tension rods. | LBX1 (Anisotropy: 2.27, pLDDT: 66.9, PAE_blockiness: 7.35). | `outputs/afcc/2026-02-16/metrics.csv` |
| **Static Inputs:** Structural metrics for core candidates (`LBX1`, `PIEZO2`, `LMNA`, `POC5`) have remained effectively identical across all analysis runs within the Jan-Feb 2026 window. | Freshness audit confirms zero variance across historical run vectors. | `reports/evidence_freshness_audit.md`, `outputs/afcc/2026-02-16/metrics.csv` |

---

## Tier 2: Supported but Uncertain
*These claims are plausible based on AlphaFold geometry but suffer from low structural confidence or require orthogonal biological validation.*

| Claim | Supporting Evidence | File Citation |
|---|---|---|
| **Extreme Outlier Rods:** `POC5` and `GHR` exhibit extreme anisotropy, suggesting massive elongation, but their low pLDDT scores mean the precise coordinates are unreliable. | POC5 (Anisotropy: 24.69, pLDDT: 64.0); GHR (Anisotropy: 5.13, pLDDT: 58.7). | `outputs/afcc/2026-02-16/metrics.csv`, `reports/confidence_weighted_structural_evidence.md` |
| **Blocky Scaffolds:** Proteins like `LBX1` and `COL1A1` may act as flexible multi-domain linkers due to high PAE blockiness, though this could simply reflect intrinsic disorder. | COL1A1 (pLDDT: 52.7, PAE_blockiness: 6.55); LBX1 (PAE_blockiness: 7.35). | `outputs/afcc/2026-02-16/metrics.csv` |

---

## Tier 3: Speculative Narrative
*These claims are derived from qualitative interpretations of clusters or temporal narratives that exceed the measured structural evidence.*

| Claim | Weakness / Falsification Requirement | File Citation |
|---|---|---|
| **LBX1 as a Primary Mechanosensor:** The narrative that LBX1 itself directly bears mechanical load or acts as a "tension rod" equivalent to LMNA. | Weakened by its very low confidence-weighted anisotropy (0.87 vs LMNA's 3.06). Requires direct biophysical testing (see Falsifiability Plan). | Cluster notes (e.g., `reports/structure_clusters/2026-01-20__cluster_note.md`), `reports/lbx1_falsifiability_plan.md` |
| **Evolving Structural Classes:** The implication that AFCC "daily refresh" runs discovered *changing* structural states for these proteins over time. | Audits prove the underlying AlphaFold structural outputs were completely static; the "evolution" was purely human interpretive drift. | `reports/evidence_freshness_audit.md` |
| **POC5 is the primary geometric driver of AIS:** Elevating POC5 above PIEZO2 based purely on raw anisotropy. | Raw anisotropy (24.69) is massively penalized by structural uncertainty (pLDDT: 64.0, PAE: 3.51). Must be validated experimentally before making causal claims. | `reports/confidence_weighted_structural_evidence.md` |
