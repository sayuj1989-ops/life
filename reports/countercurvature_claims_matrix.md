# Biological Countercurvature Claims Matrix

## Evidence Tiers
- **Confirmed**: Quantitative metrics align with hypothesis (Anisotropy > 3.0, pLDDT > 70).
- **Supported (Uncertain)**: Strong geometric signal but low structural confidence (Anisotropy > 3.0, pLDDT < 70).
- **Refuted/Refined**: Metrics contradict the specific claim (e.g. "Rod" claim for globular protein).
- **Speculative**: Narrative claim without current quantitative backing.

## Claims Matrix

| Claim | Source | Evidence | Tier | Notes |
|---|---|---|---|---|
| **PIEZO2 is a Tension Rod** | `reports/afcc_latest.md` | Anisotropy 4.44, pLDDT 79.4 | **Confirmed** | High confidence extended structure supports force transmission role. |
| **LMNA is a Tension Rod** | `reports/afcc_latest.md` | Anisotropy 4.75, pLDDT 76.4 | **Confirmed** | Consistent high anisotropy and confidence across runs. |
| **LBX1 is a Mechanical Switch** | `reports/structure_clusters` | Anisotropy 2.27, pLDDT 66.9 | **Refined** | Not a "Rod" (Intermediate anisotropy). "Blocky Scaffold" hypothesis is a refinement. Low confidence requires functional validation. |
| **POC5 is a Tension Rod** | `reports/afcc_latest.md` | Anisotropy 24.69, pLDDT 64.0 | **Supported (Uncertain)** | Extreme anisotropy suggests fiber formation, but low pLDDT warns of potential IDR artifact. |
| **GHR is a Tensile Tether** | `H_2026_02_24_Anisotropic_Scaffolds` | Anisotropy 5.13, pLDDT 58.7 | **Supported (Uncertain)** | High anisotropy supports tethering, but low confidence suggests flexibility/disorder. |
| **ADGRG6 is Anisotropic** | `outputs/afcc/2026-02-16` | Anisotropy 3.06, pLDDT 73.7 | **Confirmed** | Meets threshold for fibrous morphology with good confidence. |
| **CNNM2 is a Tension Element** | `outputs/afcc/2026-02-16` | Anisotropy 8.54, pLDDT 70.4 | **Confirmed** | Very strong signal, often overlooked in narrative. |
| **PLOD1 is a Structural Crosslinker** | `reports/afcc_latest.md` | Anisotropy 3.40, pLDDT 92.7 | **Confirmed** | High confidence extended structure (enzyme). |

## Provenance Note
Evidence values derived from `outputs/afcc/confidence_weighted_ranking.csv` (Composite 2026-02-16/18).
