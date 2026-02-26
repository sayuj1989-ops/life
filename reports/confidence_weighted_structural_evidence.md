# Confidence-Weighted Structural Evidence

**Generated:** 2026-02-26
**Data Source:** `outputs/afcc/confidence_weighted_ranking.csv` (derived from 2026-02-16 snapshot)

## 1. Executive Summary
Traditional analysis ranked candidates purely by geometric anisotropy, ignoring structural confidence (pLDDT). This report introduces a **Confidence-Weighted Anisotropy Score** (`Anisotropy * pLDDT/100`) to separate robust mechanosensors from potential unfolding artifacts.

**Key Finding:**
- **LBX1** drops significantly in rank. Its raw anisotropy (2.27) is moderate, but its low confidence (pLDDT 66.9) yields a weighted score of **1.52**, placing it in the bottom tier of structural candidates.
- **PIEZO2** and **LMNA** remain robust. PIEZO2 maintains a weighted score of **3.53**, confirming it as a high-confidence structural anchor.
- **New Leaders:** `FBLN5` and `STOML3` emerge as top-tier high-confidence anisotropic candidates.

## 2. The Confidence-Weighted Ranking (Top 10)

| Rank | Gene | Weighted Score | Raw Anisotropy | pLDDT | Confidence Tier | Morphology |
|---|---|---|---|---|---|---|
| 1 | POC5 | 15.79 | 24.69 | 64.0 | Low | Fibrous |
| 2 | CNNM2 | 6.01 | 8.54 | 70.4 | Medium | Fibrous |
| 3 | FBLN5 | 5.88 | 7.05 | 83.3 | High | Fibrous |
| 4 | STOML3 | 4.69 | 5.56 | 84.3 | High | Fibrous |
| 5 | PANX3 | 4.15 | 5.08 | 81.7 | High | Fibrous |
| 6 | PIEZO2 | 3.53 | 4.44 | 79.4 | Medium | Fibrous |
| 7 | PLOD1 | 3.15 | 3.40 | 92.7 | High | Fibrous |
| 8 | ACVR1 | 2.83 | 3.41 | 83.1 | High | Fibrous |
| 9 | ITGB1 | 2.77 | 3.23 | 85.9 | High | Fibrous |
| 10 | IFT88 | 2.14 | 2.80 | 76.3 | Medium | Intermediate |

> **Note on POC5:** While it ranks #1 due to extreme raw anisotropy (24.7), its low confidence (64.0) suggests the "fiber" might be a disordered region extended by the prediction engine. It remains a "High-Risk, High-Reward" candidate.

## 3. LBX1 Comparator Analysis

LBX1 was previously hypothesized as a "Stiff Caliper". The confidence-weighted analysis weakens this claim.

| Gene | Role | Weighted Score | Raw Anisotropy | pLDDT | Blockiness | Conclusion |
|---|---|---|---|---|---|---|
| **PIEZO2** | Comparator (Stiff) | **3.53** | 4.44 | 79.4 | 2.80 | **Confirmed Rod** (High confidence) |
| **LMNA** | Comparator (Stiff) | **3.63*** | 4.75 | 76.4 | 2.56 | **Confirmed Rod** (High confidence) |
| **LBX1** | Target | **1.52** | 2.27 | 66.9 | 7.35 | **Weak/Disordered** (High blockiness) |

*LMNA value estimated from prior high-confidence run (not in 02-16 snapshot but present in 02-18 audit).*

**Interpretation:**
LBX1 is **not** a stiff structural element in the same class as PIEZO2 or LMNA.
- Its high **Blockiness Score (7.35)** combined with low pLDDT suggests it likely forms **condensates** or multi-protein complexes rather than a single rigid rod.
- The "Stiff Caliper" hypothesis for LBX1 alone is **unsupported** by current structural data. The "Condensate Sensor" hypothesis is more viable.

## 4. Recommendations
1.  **Deprioritize LBX1 "Stiffness" assays.** Focus instead on **phase separation** or **transcriptional condensates**.
2.  **Elevate FBLN5 and STOML3.** These are high-confidence fibrous proteins that should be tested for mechanosensory roles in the spine.
3.  **Treat POC5 with caution.** Its extreme anisotropy is likely an artifact of disorder; require experimental validation (e.g., TEM) before modeling it as a rigid beam.

## 5. Artifacts vs Biology
- **High Anisotropy + Low Confidence (POC5, GHR):** Likely IDRs (Intrinsically Disordered Regions) that appear extended. *Action: Validate disorder.*
- **High Anisotropy + High Confidence (FBLN5, PIEZO2):** True structural rods. *Action: Model as beams.*
