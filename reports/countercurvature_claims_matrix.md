# Countercurvature Claims Matrix
**Date:** 2026-02-20
**Purpose:** Provide a disciplined mapping of theoretical claims to evidentiary status.

## Classification Tiers
1.  **Confirmed by Metrics:** Directly supported by quantitative data (Anisotropy > 3.0, pLDDT > 70).
2.  **Supported but Uncertain:** Data exists but relies on interpretation or has caveats (Low confidence).
3.  **Speculative Narrative:** Plausible hypothesis based on limited data or purely theoretical models.

---

## Claims Analysis

| Claim ID | Claim Description | Status | Key Evidence / Source | Caveats |
| :--- | :--- | :--- | :--- | :--- |
| **C1** | **"Tension Rods" exist in the proteome.** | **Confirmed** | **PIEZO2** (Anisotropy 4.44), **LMNA** (Anisotropy 4.75). Source: `outputs/afcc/confidence_weighted_ranking.csv` | Confirmed for key mechanosensors. |
| **C2** | **LBX1 acts as a "Tension Rod".** | **Weak / Falsified** | **LBX1** Anisotropy = 2.27 (Tier 4). Source: `reports/confidence_weighted_structural_evidence.md` | LBX1 is globular/intermediate, not fibrous. |
| **C3** | **LBX1 functions as a "Blocky Switch".** | **Supported** | **LBX1** Blockiness = 7.35 (High domain segregation). Source: `outputs/afcc/2026-02-16/metrics.csv` | Requires experimental validation of functional relevance (Experiment 1). |
| **C4** | **The "Energy Deficit Window" drives scoliosis.** | **Speculative** | Model: `scripts/experiment_energy_deficit_window.py`. Source: `manuscript/sections/theory.tex` | Mathematical derivation only; no direct in vivo measurement yet. |
| **C5** | **Proprioceptive sensors are thermodynamically expensive.** | **Supported** | **PIEZO2**, **GHR** show high anisotropy/surface area. Source: `outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv` | Correlation does not prove causation of failure. |
| **C6** | **"Entropic Rheostat" mechanism filters mechanical noise.** | **Speculative** | Hypothesis `H_2026_02_27_EntropicRheostat`. Source: `notes/hypothesis_register.md` | Purely hypothetical mechanism for IDR function. |
| **C7** | **Microgravity mimics the "Soft Nucleus" state.** | **Speculative** | Analogous to `LMNA` loss-of-function. Source: `reports/structure_clusters/2026-02-01__blocky_lbx1.md` | Indirect inference from spaceflight transcriptomics (Ocy454). |

---

## Action Plan
-   **Prioritize C3:** Validate the "Blocky Switch" hypothesis via proposed experiments.
-   **Refine C4:** Seek clinical growth curve data to correlate with the "Energy Deficit Window".
-   **Abandon C2:** Stop referring to LBX1 as a "rod"; adopt "switch" or "rheostat" terminology.
