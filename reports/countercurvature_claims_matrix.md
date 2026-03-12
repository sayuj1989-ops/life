# Biological Counter-Curvature Claims Matrix

*Generated to enforce claim discipline for manuscript submission.*
*Data grounded in `outputs/afcc/2026-02-16/metrics.csv` and historical audit.*

## 1. Confirmed by Metrics (High Confidence)
*Claims directly supported by quantitative measurements or high-confidence structural data.*

| Claim | Evidence / Metric | Source File / Rows |
| :--- | :--- | :--- |
| **PIEZO2 and LMNA possess highly extended, anisotropic structures.** | PIEZO2 (Anisotropy=4.44, pLDDT=79.4); LMNA (historical high anisotropy >4.0, adequate pLDDT). | `outputs/afcc/2026-02-16/metrics.csv` (PIEZO2 row); Historical AFCC metrics. |
| **LBX1 is structurally an intermediate-anisotropy, low-confidence protein.** | LBX1 Anisotropy=2.27, pLDDT=66.9, PAE Blockiness=7.35. | `outputs/afcc/2026-02-16/metrics.csv` (LBX1 row). |
| **Core gene structural metrics (LBX1, PIEZO2, LMNA) have remained static across recent AFCC runs.** | Metrics identical across runs from 2026-01-09 to 2026-02-16. | `reports/evidence_freshness_audit.md`. |
| **Certain top-ranked anisotropic candidates are low confidence.** | e.g., POC5 (Anisotropy=24.69, pLDDT=64.0), GHR (Anisotropy=5.13, pLDDT=58.7). | `outputs/afcc/2026-02-16/metrics.csv` (POC5, GHR rows). |

## 2. Supported but Uncertain (Medium Confidence)
*Claims with plausible mechanistic basis but requiring orthogonal validation or relying on moderately confident inferences.*

| Claim | Evidence / Metric | Source File / Rows |
| :--- | :--- | :--- |
| **High-anisotropy/low-confidence proteins (like POC5, GHR) may represent novel mechanosensors or structural tethers.** | Their high anisotropy scores suggest extended geometries, but low pLDDT indicates possible disorder or context-dependence (e.g., needing binding partners). | `outputs/afcc/2026-02-16/metrics.csv`; `reports/confidence_weighted_structural_evidence.md`. |
| **LBX1's "blocky" PAE profile suggests a modular architecture.** | LBX1 PAE Blockiness=7.35. However, low pLDDT means this could be an artifact of poor prediction rather than true modularity. | `outputs/afcc/2026-02-16/metrics.csv` (LBX1 row). |

## 3. Speculative Narrative (Low Confidence / Hypothesis-Generating)
*Claims that infer causality, dynamic changes, or strong structural roles from static or low-confidence data. These must be explicitly labeled as hypotheses.*

| Claim | Evidence / Metric | Source File / Rows |
| :--- | :--- | :--- |
| **LBX1 acts as a primary "Tension Rod" or mechanosensor anchor.** | Speculative. Conflicts with its low anisotropy (2.27) and low pLDDT (66.9). | Contradicts `outputs/afcc/2026-02-16/metrics.csv`. |
| **LBX1 geometry changed or "emerged" into a new structural class during Jan-Feb 2026.** | Falsified by audit. Metrics were static. Any narrative of "emergence" is an over-interpretation of static data. | `reports/evidence_freshness_audit.md`. |
| **Metabolic Buckling is directly caused by energy deficits in specific high-anisotropy proteins.** | Speculative linkage. While energy deficits correlate with scoliosis models, the specific energetic cost of individual proteins like POC5/GHR vs their structural role is not directly measured here. | Conceptual framework; requires further energetic assays. |
