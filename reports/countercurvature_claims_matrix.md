# Biological Countercurvature Claims Matrix

This matrix categorizes current claims regarding the Biological Countercurvature hypothesis based on the strength of supporting evidence from the existing codebase and AlphaFold Structural Clustering (AFCC) data.

## 1. Confirmed by Metrics (Direct Measurement / High Confidence)
Claims in this tier are directly supported by high-confidence quantitative data in the authoritative metrics snapshot.

| Claim | Quantitative Support / Direct Evidence | Exact Source Rows/Files |
|-------|----------------------------------------|-------------------------|
| **Core Mechanosensors are Highly Anisotropic** | PIEZO2 shows extreme extended geometry (Anisotropy 4.44) combined with high structural confidence (pLDDT 79.4). | `outputs/afcc/2026-02-16/metrics.csv` (Row 19) |
| **LBX1 Architecture is Not a Rigid Strut** | LBX1 exhibits intermediate anisotropy (2.27), low confidence (pLDDT 66.9), and high domain blockiness (PAE 7.35). It does not fit the geometric profile of a rigid tension rod. | `outputs/afcc/2026-02-16/metrics.csv` (Row 13) |
| **New Strong Tension Candidates Identified** | CNNM2 (Anis: 8.54, pLDDT: 70.4) and FBLN5 (Anis: 7.05, pLDDT: 83.3) emerge as top high-confidence extended structures, surpassing traditional anchors. | `outputs/afcc/2026-02-16/metrics.csv` (Rows 4, 8) |
| **Static Input Data Reuse** | Core genes (LBX1, PIEZO2, LMNA) have 100% identical metric vectors (Anisotropy, pLDDT) across 13-20 historical AFCC runs spanning Jan-Feb 2026. | `reports/evidence_freshness_audit.md` (Table 1); `outputs/afcc/*/metrics.csv` |

## 2. Supported but Uncertain (Hypothesis / Correlation)
Claims in this tier have some basis in the data but require orthogonal experimental validation due to low structural confidence or reliance on derived proxies.

| Claim | Quantitative Support / Direct Evidence | Exact Source Rows/Files |
|-------|----------------------------------------|-------------------------|
| **GHR acts as a Structural Tension Sensor** | GHR has high anisotropy (5.13) suggesting a fibrous shape, but low structural confidence (pLDDT 58.7) means the "extended" shape may actually be a disordered random coil. | `outputs/afcc/2026-02-16/metrics.csv` (Row 10) |
| **POC5 Extreme Geometry Links to Curvature** | POC5 shows the highest anisotropy (24.69) but very low confidence (pLDDT 64.0). While intriguing for a centriolar scaffold, it is statistically uncertain. | `outputs/afcc/2026-02-16/metrics.csv` (Row 20) |
| **LBX1 Blockiness Implies Multi-Domain Assembly** | LBX1's high PAE domain blockiness (7.35) suggests discrete folding units separated by flexible linkers, but AlphaFold struggles with IDPs, making the "linker" inference uncertain without SAXS/NMR. | `outputs/afcc/2026-02-16/metrics.csv` (Row 13); `reports/lbx1_falsifiability_plan.md` |

## 3. Speculative Narrative (Anecdotal / Over-interpreted)
Claims in this tier are not directly supported by metrics, or they over-interpret static data as dynamic temporal trends. **These must be avoided or explicitly flagged in manuscript drafts.**

| Claim | Quantitative Support / Direct Evidence | Exact Source Rows/Files |
|-------|----------------------------------------|-------------------------|
| **"LBX1 structure is dynamically emerging / shifting"** | **EVIDENCE AGAINST:** LBX1 metrics (2.27 Anis, 66.9 pLDDT) are perfectly static across 20 independent runs from Jan 09 to Feb 28. There is no measurable temporal shift. | `reports/evidence_freshness_audit.md`; `reports/afcc_latest.md` narrative sections |
| **"LBX1 drives curvature via direct cytoskeletal load-bearing"** | **EVIDENCE AGAINST:** LBX1 fails the high-confidence anisotropy threshold (Anis < 3.0). It structurally resembles flexible transcription factors (RUNX3) rather than rigid struts (PIEZO2, LMNA). | `reports/confidence_weighted_structural_evidence.md`; `outputs/afcc/2026-02-16/metrics.csv` |
| **Daily structural "Top Movers" represent biological discovery** | **EVIDENCE AGAINST:** The freshness audit reveals "daily refresh" scripts routinely report unchanged genes (e.g., GHR) as novel findings for the day, which is an artifact of the batch processing script, not a new AlphaFold prediction. | `reports/evidence_freshness_audit.md`; `reports/afcc_latest.md` |
