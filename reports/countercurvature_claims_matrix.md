# Counter-Curvature Claims Matrix

## Overview
To enforce manuscript claim discipline and prevent narrative inflation, all structural and geometric statements regarding the Biological Counter-Curvature hypothesis must be stratified into three confidence tiers. This matrix maps exact claims to their definitive source files and rows within the repository.

### Tier Definitions
1. **Confirmed by metrics**: Directly supported by reproducible, adequately confident quantitative data (e.g., `pLDDT >= 70`).
2. **Supported but uncertain**: Derived from measured data but inherently uncertain due to algorithmic confidence limits (e.g., high-anisotropy with `pLDDT < 70`).
3. **Speculative narrative**: Inferential hypotheses without direct empirical support in the current snapshot, including claims of temporal metric drift when vectors are statically cached.

---

## 1. Confirmed by metrics

| Claim | Source File | Source Row / Context | Metric Support |
| :--- | :--- | :--- | :--- |
| **PIEZO2 is a high-confidence, highly anisotropic structure.** | `outputs/afcc/2026-02-16/metrics.csv` | Row matching `PIEZO2` | Anisotropy = 4.44, pLDDT = 79.4 |
| **CNNM2 and FBLN5 exhibit massive geometric elongation with high structural confidence.** | `outputs/afcc/2026-02-16/metrics.csv` | Rows matching `CNNM2`, `FBLN5` | CNNM2 Aniso = 8.54, pLDDT = 70.4. FBLN5 Aniso = 7.05, pLDDT = 83.3 |
| **ADGRG6 possesses an extended structural profile consistent with mechanoreception.** | `outputs/afcc/2026-02-16/metrics.csv` | Row matching `ADGRG6` | Anisotropy = 3.06, pLDDT = 73.7 |
| **LBX1 structure is statically low-confidence across all measured runs since Jan 2026.** | `scripts/analysis/evidence_freshness_audit.py` (Output) | `reports/evidence_freshness_audit.md` | LBX1 pLDDT = 66.9 across 17 identical run vectors. |

---

## 2. Supported but uncertain

| Claim | Source File | Source Row / Context | Caveat / Uncertainty |
| :--- | :--- | :--- | :--- |
| **POC5 possesses extreme structural elongation (Tension Rod).** | `outputs/afcc/2026-02-16/metrics.csv` | Row matching `POC5` | Anisotropy = 24.69, but **pLDDT = 64.0**. High risk of unstructured loop extension artifact. |
| **GHR acts as a highly anisotropic growth sensor.** | `outputs/afcc/2026-02-16/metrics.csv` | Row matching `GHR` | Anisotropy = 5.13, but **pLDDT = 58.7**. Structurally uncertain. |
| **LBX1 has an intermediate, "blocky" architecture.** | `outputs/afcc/2026-02-16/metrics.csv` | Row matching `LBX1` | Anisotropy = 2.27, PAE Blockiness = 7.35. However, model confidence is low (pLDDT = 66.9), meaning the blockiness might be a predictive artifact. |
| **LMNA is a highly anisotropic load-bearing tension rod.** | Historical runs (e.g., `2026-01-20/metrics.csv`) | `reports/alphafold_data_assessment_2026-02-16.md` | Anisotropy = 4.75, pLDDT = 76.4. However, it is missing from the authoritative `2026-02-16` snapshot. |

---

## 3. Speculative narrative

| Claim | Source File / Narrative Location | Context | Reason for Falsification/Demotion |
| :--- | :--- | :--- | :--- |
| **LBX1's geometry is dynamically evolving or reorganizing to support counter-curvature.** | `reports/structure_clusters/*.md` (e.g., `2026-01-20__cluster_note.md`) | Narrative updates describing emerging states. | Audit confirms LBX1 metrics (Aniso 2.27, pLDDT 66.9) have been **mathematically identical and static** for 17 runs. There is zero evidence of temporal metric drift. |
| **High anisotropy in ARNTL, GHR, and MESP2 proves they transmit mechanical force.** | `reports/structure_clusters/*.md` | Clustering assignments | Anisotropy in these genes correlates strictly with poor model quality (pLDDT < 70). Force transmission requires rigidity; AF cannot predict rigidity of IDRs. |
| **The "Blocky Scaffold" class (LBX1, COL1A1) is a definitive mechanical effector category.** | `reports/afcc_latest.md` (e.g., 2026-01-21 entry) | Cluster 1 definition | Both LBX1 (pLDDT 66.9) and COL1A1 (pLDDT 52.7) are low-confidence. Grouping by PAE blockiness on low-confidence models groups prediction uncertainty, not necessarily physiological biology. |
