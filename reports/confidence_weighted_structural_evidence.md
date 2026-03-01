# Confidence-Weighted Structural Evidence Ranking

**Date:** 2026-02-19
**Source Snapshot:** `outputs/afcc/2026-02-16/metrics.csv`
**Methodology:** Filtering candidates via strictly quantitative AlphaFold structural metrics (Anisotropy > 3.0, pLDDT > 70 for adequate confidence).

## The Core Problem
Prior analysis (Jan-Feb 2026) inflated structural hypotheses by treating low-confidence AlphaFold predictions (pLDDT < 70) as high-anisotropy mechanically rigid "rods" or "blocky scaffolds." Disordered regions artifactually increase apparent radius of gyration and anisotropy index when predicted in arbitrary extended states.

## Re-Ranking Candidates
We systematically separate high-confidence mechanistic anchors from low-confidence hypothesis generators.

### 1. High-Anisotropy + Adequate-Confidence (Mechanistic Anchors)
These genes present high confidence structural predictions (>70 pLDDT) combined with extended geometries (Anisotropy > 3.0).

| Rank | Gene | Anisotropy | pLDDT | PAE Blockiness | Notes |
|---|---|---|---|---|---|
| 1 | **CNNM2** | 8.54 | 70.4 | 4.83 | Highest confidence rod. |
| 2 | **FBLN5** | 7.05 | 83.3 | 3.55 | Strong ECM structural candidate. |
| 3 | **STOML3** | 5.56 | 84.3 | 0.00 | Membrane-associated mechanosensor. |
| 4 | **PANX3** | 5.08 | 81.7 | 2.77 | High confidence channel protein. |
| 5 | **PIEZO2** | 4.44 | 79.4 | 2.80 | Validated mechanotransducer. |
| 6 | **ROCK1** | 3.29 | 76.1 | 4.95 | Cytoskeletal tension regulator. |
| 7 | **ADGRG6** | 3.06 | 73.7 | 6.78 | Known scoliosis driver. |

*Interpretation:* These are publication-defensible anchors for the Countercurvature hypothesis.

### 2. High-Anisotropy + Low-Confidence (Exploratory Only)
These genes show extended structures but lack the prediction confidence (<70 pLDDT) to claim true mechanistic form without orthogonal validation. They are mostly unstructured or intrinsically disordered regions (IDRs).

| Rank | Gene | Anisotropy | pLDDT | PAE Blockiness | Notes |
|---|---|---|---|---|---|
| 1 | **POC5** | 24.69 | 64.0 | 3.51 | Extreme outlier; likely intrinsically disordered. |
| 2 | **GHR** | 5.13 | 58.7 | 5.31 | Transmembrane receptor; unstructured intracellular domains. |
| 3 | **EMD** | 4.29 | 60.3 | 9.13 | Nuclear envelope protein; likely dynamic/flexible. |
| 4 | **MESP2** | 4.03 | 54.2 | 0.00 | Segmentation clock; mostly disordered. |
| 5 | **ARNTL** | 3.32 | 65.5 | 3.59 | Circadian clock; basic helix-loop-helix with IDRs. |

*Interpretation:* **DO NOT** claim these are rigid rods. Structural speculation on POC5, GHR, and MESP2 must be downgraded to "Supported but uncertain".

### 3. LBX1 Comparator Analysis
How does the primary developmental target (LBX1) compare to known mechanosensors and structural proteins?

| Gene | Role | Anisotropy | pLDDT | PAE Blockiness | Assessment |
|---|---|---|---|---|---|
| **LBX1** | Somite Patterning | 2.27 | 66.9 | 7.35 | Low confidence, intermediate shape. Likely functions via standard modular binding, not as an extended force-transmitting rod or mechanosensor. |
| **PIEZO2** | Mechanosensor | 4.44 | 79.4 | 2.80 | High confidence, highly extended. Clear structural capability for direct force transduction. |
| **LMNA** | Nuclear Scaffolding | 4.75 | 76.4 | 2.56 | High confidence, highly extended. Validated structural integrity element. |
| **ADGRG6** | Scoliosis Driver | 3.06 | 73.7 | 6.78 | High confidence, extended/blocky. Plausible mechanosensor or structural linker. |
| **RUNX3** | Transcription Factor | 2.06 | 60.6 | N/A | Low confidence, low anisotropy. Typical transcription factor profile, lacking extended mechanical geometry. |
| **POC5** | Centriole/Cilia | 24.69 | 64.0 | 3.51 | Extreme outlier anisotropy, but low confidence. Likely intrinsically disordered regions (IDRs) mimicking rod-like behavior in static prediction. |
| **GHR** | Transmembrane Receptor | 5.13 | 58.7 | 5.31 | High anisotropy but very low confidence. Unstructured intracellular domains inflate the apparent extension. |

*Conclusion on LBX1:* The hypothesis that LBX1 itself acts as a "blocky scaffold" or "cryptic signal reservoir" undergoing tension-dependent unfolding (e.g., Cluster 1 note 2026-01-20) is structurally ungrounded. It lacks the pLDDT confidence and physical span to support this. Its role is likely downstream (transcriptional) rather than primary structural sensing.
