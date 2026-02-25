# Biological Countercurvature Claims Matrix
**Date:** 2026-03-12
**Purpose:** Strict categorization of scientific claims based on current AFCC metric evidence.

## Classification Legend
*   **🟢 CONFIRMED:** Directly measured by high-confidence metrics (Tier 1: Anisotropy > 3.0, pLDDT > 70).
*   **🟡 SUPPORTED:** measured by metrics but with significant caveats (Tier 2: Low Confidence) or indirect evidence.
*   **🔴 SPECULATIVE / REFUTED:** Narrative claim not supported by current data, or directly contradicted by it.

## 1. Structural Claims
| Claim | Status | Evidence Source | Notes |
| :--- | :--- | :--- | :--- |
| **"PIEZO2 acts as a curved anisotropic beam."** | 🟢 **CONFIRMED** | `metrics.csv`: Aniso=4.44, pLDDT=79.4 | Classic mechanosensor profile. |
| **"LBX1 acts as a rigid molecular caliper."** | 🔴 **REFUTED** | `metrics.csv`: Aniso=2.27, pLDDT=66.9 | Too flexible/globular. Ranks 18th/25. |
| **"POC5 forms a stiff filamentous tether."** | 🟡 **SUPPORTED** | `metrics.csv`: Aniso=24.7, pLDDT=64.0 | Extreme anisotropy supports filament, but low confidence suggests disorder/artifact risk. |
| **"CNNM2 is a high-priority structural candidate."** | 🟢 **CONFIRMED** | `metrics.csv`: Aniso=8.54, pLDDT=70.4 | **New Finding:** Highest anisotropy with acceptable confidence. |
| **"LBX1 has a modular 'beads-on-a-string' architecture."** | 🟢 **CONFIRMED** | `metrics.csv`: PAE_Blockiness=7.35 | High blockiness score confirms distinct domains separated by flexible linkers. |

## 2. Temporal / Evolutionary Claims
| Claim | Status | Evidence Source | Notes |
| :--- | :--- | :--- | :--- |
| **"LBX1 structure is 'emerging' or 'crystallizing' over time."** | 🔴 **REFUTED** | `evidence_freshness_audit.md` | Metrics are bit-for-bit static across 6 weeks. "Emergence" is a narrative hallucination. |
| **"Candidate pool is expanding with new anisotropic targets."** | 🟢 **CONFIRMED** | `metrics.csv` (Compare Jan vs Feb) | New genes (e.g., FBLN5, STOML3) have been added and validated. |

## 3. Mechanistic Hypotheses
| Claim | Status | Evidence Source | Notes |
| :--- | :--- | :--- | :--- |
| **"LBX1 mechanosensitivity is intrinsic to its geometry."** | 🔴 **SPECULATIVE** | `confidence_weighted_ranking.csv` | Geometry (Tier 3) is insufficient. Requires **Experiment 1 (LINC)** to test extrinsic coupling. |
| **"Scoliosis drivers are enriched for high anisotropy."** | 🟡 **SUPPORTED** | `confidence_weighted_ranking.csv` | Top tier includes known driver ADGRG6 and sensor PIEZO2, but LBX1 (major driver) is an exception. |
| **"Disordered regions (IDRs) drive mechanosensation via condensation."** | 🟡 **SUPPORTED** | `metrics.csv` (Low pLDDT for LBX1/GHR) | Plausible alternative to "Rigid Rod" model, but requires **Experiment 3 (Phase Sep)** validation. |

## Action Items
1.  **Retract:** "LBX1 Stiff Rod" narrative in all future manuscripts. Replace with "Modular Integrator".
2.  **Promote:** CNNM2 and FBLN5 to "Primary Structural Candidates".
3.  **Investigate:** POC5 requires specific validation to rule out AlphaFold artifact (e.g., TEM/AFM).
