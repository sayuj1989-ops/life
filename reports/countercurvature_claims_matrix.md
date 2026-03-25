# Biological Countercurvature Claims Matrix

## Overview
This matrix categorizes the structural evidence supporting the Biological Countercurvature hypothesis into three explicit tiers of certainty. It strictly maps each claim to exact source rows/files to ensure narrative discipline for manuscript preparation.

## Tier 1: Confirmed by Metrics
*These claims represent direct, reproducible measurements from the current AlphaFold computational pipeline without inferential leaps.*

| Claim ID | Claim Description | Exact Source Row / File | Verification Date |
| :--- | :--- | :--- | :--- |
| **C1.1** | The highest-anisotropy, adequate-confidence candidate (Anisotropy > 4.0, pLDDT > 70) in the latest snapshot is **LMNA**. | `outputs/afcc/confidence_weighted_ranking.csv` (Row 5: LMNA, pulled dynamically from historical runs, Anisotropy: 4.75, pLDDT: 76.4) | 2026-03-25 |
| **C1.2** | **PIEZO2** maintains a high-anisotropy, extended fibrous structure (Anisotropy > 4.0, pLDDT > 70). | `outputs/afcc/2026-02-16/metrics.csv` (Row corresponding to PIEZO2, Anisotropy: 4.44, pLDDT: 79.4) | 2026-02-16 |
| **C1.3** | **LBX1** exhibits intermediate anisotropy (~2.27), low confidence (pLDDT ~66.9), and very high PAE domain blockiness (~7.35). | `outputs/afcc/2026-02-16/metrics.csv` (Row corresponding to LBX1, Anisotropy: 2.27, pLDDT: 66.9, PAE_blockiness: 7.35) | 2026-02-16 |
| **C1.4** | The structural metrics (Anisotropy, pLDDT, Blockiness) for LBX1 and PIEZO2 remained effectively static across available runs in the trend window. | `reports/evidence_freshness_audit.md` (Identified identical vectors for multiple targets across consecutive dates) | 2026-03-25 |

## Tier 2: Supported but Uncertain
*These claims are structurally plausible based on computational geometry but lack direct orthogonal confirmation (e.g., in vivo folding, functional assays) and require confidence caveats.*

| Claim ID | Claim Description | Exact Source Row / File | Verification Date |
| :--- | :--- | :--- | :--- |
| **C2.1** | The rigid rod-like geometries of LMNA and PIEZO2 suggest they function as primary load-bearing "Tension Rods" in mechanotransduction. | `reports/structure_clusters/2026-02-27__tension_rods.md` (Cluster classification based on Anisotropy > 4.0) | 2026-02-27 |
| **C2.2** | The "blocky" architecture of LBX1 (high PAE blockiness) indicates a multi-domain modular topology that may be sensitive to conformational collapse under altered mechanical tension. | `reports/structure_clusters/2026-02-01__blocky_lbx1.md` (H_2026_02_01_Blocky_LBX1 hypothesis based on PAE blockiness > 7.0) | 2026-02-01 |
| **C2.3** | Extremely high anisotropy outliers like **POC5** and **GHR** may represent highly extended structural elements, but their low pLDDT scores (<70) indicate they might be structurally disordered or artefactual string models. | `outputs/afcc/confidence_weighted_ranking.csv` (Rows for POC5 and GHR showing Anisotropy > 5.0 but 'Low-Confidence' tier) | 2026-03-25 |

## Tier 3: Speculative Narrative
*These claims represent theoretical leaps or dynamic interpretations that extend beyond the static structural snapshots provided by the current data.*

| Claim ID | Claim Description | Exact Source Row / File | Verification Date |
| :--- | :--- | :--- | :--- |
| **C3.1** | LBX1 target gene transcription is directly gated by LINC complex-mediated nuclear tension derived from gravity during spinal development. | `reports/structure_clusters/2026-02-01__blocky_lbx1.md` (Hypothesis text linking blockiness to Lamin A/C tension and scoliosis onset) | 2026-02-01 |
| **C3.2** | The divergence in structural blockiness between LBX1 and RUNX3 represents the primary mechanistic driver of proprioceptive drift in Adolescent Idiopathic Scoliosis. | `reports/structure_clusters/2026-02-01__blocky_lbx1.md` (Narrative claiming differential response to nuclear softening drives the disease state) | 2026-02-01 |
| **C3.3** | Repeated cluster note updates describing "evolving" or "shifting" geometries for LBX1 and PIEZO2 over the Jan-Feb window reflect actual structural refinement. | `reports/alphafold_data_assessment_2026-02-16.md` (Identified as a hypothesis inflation flag; underlying data was static) | 2026-02-19 |

