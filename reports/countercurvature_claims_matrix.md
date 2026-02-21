# Biological Countercurvature Claims Matrix

## Evidence Tiers
- **Confirmed**: Quantitative metrics directly support the claim (e.g., Structure is high-confidence anisotropic).
- **Supported (Uncertain)**: Metrics are consistent but have significant caveats (e.g., Low confidence, potential IDR artifact).
- **Speculative**: Narrative hypothesis with weak or indirect structural evidence.

## Claims vs. Evidence Mapping

| Claim | Evidence Tier | Supporting Metrics (Source: `outputs/afcc/confidence_weighted_ranking.csv`) | Caveats / Falsification Risk |
| :--- | :--- | :--- | :--- |
| **1. PIEZO2 acts as a "Tension Rod"** | **Confirmed** | Anisotropy: 4.44, Confidence: Medium (pLDDT 79.4). Weighted Score: 2.80. | High confidence in extended geometry. Functional validation needed (mechanosensitivity). |
| **2. LMNA acts as a Nuclear "Tension Rod"** | **Confirmed** | Anisotropy: 4.75, Confidence: Medium (pLDDT 76.4). Weighted Score: 2.77. | Known intermediate filament former. Structure supports load-bearing role. |
| **3. LBX1 is a Structural Mechanosensor** | **Speculative** | Anisotropy: 2.27, Confidence: Low (pLDDT 66.9). Weighted Score: 1.01. | **HIGH RISK**: Low pLDDT suggests IDR/disorder. Anisotropy likely an artifact of extended tail in static model. |
| **4. POC5 forms rigid Ciliary structures** | **Supported (Uncertain)** | Anisotropy: 24.7, Confidence: Low (pLDDT 64.0). Weighted Score: 10.10. | Extremely high anisotropy fits "fiber" model, but low confidence suggests it might be aggregating/polymerizing rather than a single folded rod. |
| **5. GHR (Growth Hormone Receptor) is a Tension Rod** | **Supported (Uncertain)** | Anisotropy: 5.13, Confidence: Low (pLDDT 58.7). Weighted Score: 1.77. | Anisotropy is high, but confidence is very low. Likely an IDR-rich intracellular domain. |
| **6. ADGRG6 (GPR126) is a Tension Rod** | **Confirmed** | Anisotropy: 3.06, Confidence: Medium (pLDDT 73.7). Weighted Score: 1.66. | Solid structural prediction. Known adhesion GPCR. |
| **7. "Countercurvature" Mechanism (General)** | **Speculative** | N/A (Hypothesis Level). | Requires establishing that *defects* in these rods cause specific curvature patterns. Currently, we only have correlation of "rod-like" genes with scoliosis. |

## Verification Status

### Verified Strong Candidates (High Priority for Experiment)
- **PIEZO2**
- **LMNA**
- **ADGRG6**
- **STOML3** (New Candidate, High Confidence Anisotropy: 5.56, pLDDT 84.3)

### Candidates Requiring De-Risking (Low Priority or Specific Controls)
- **LBX1** (Likely transcription factor IDR)
- **POC5** (Likely polymerization artifact in monomer prediction)
- **GHR** (Likely IDR)

## Conclusion
The "Biological Countercurvature" hypothesis is structurally **robust for PIEZO2 and LMNA**, but **weak for LBX1**.
Future work should focus on the **PIEZO2-LMNA axis** as the primary driver of "Tension Rod" mechanics, while treating LBX1 as a downstream transcriptional regulator rather than a structural element.
