# Biological Countercurvature Claims Matrix

**Date**: 2026-02-22
**Purpose**: Map central hypothesis claims to quantitative evidence tiers.

| Claim | Confidence Tier | Evidence Source | Key Metrics | Falsifiability Link |
| :--- | :--- | :--- | :--- | :--- |
| **PIEZO2 is a "Tension Rod" sensor** | **Confirmed** | `confidence_weighted_ranking.csv` | Anisotropy: 4.44, Conf: 0.63 (High) | N/A |
| **LBX1 is a rigid mechanosensor** | **Speculative / Weakened** | `confidence_weighted_structural_evidence.md` | Anisotropy: 2.27, Conf: 0.26 (Low), Blockiness: 7.35 | [Falsifiability Plan](lbx1_falsifiability_plan.md) |
| **LBX1 is a "Disordered/Soft" sensor** | **Supported** | `structure_clusters/2026-02-22__cluster_note.md` | High Blockiness + Low pLDDT | [Exp 1: Nuclear Translocation](lbx1_falsifiability_plan.md#experiment-1-stiffness-dependent-nuclear-translocation) |
| **LMNA is a load-bearing element** | **Uncertain (Artifact Risk)** | `confidence_weighted_ranking.csv` | Anisotropy: 4.75, Conf: 0.53 (Tier 2) | N/A |
| **High Anisotropy = Mechanical Function** | **Mixed** | `evidence_freshness_audit.md` | Many IDPs show high anisotropy (EGR3) but low confidence. | N/A |
| **Thermodynamic Standing Wave drives AIS** | **Speculative Narrative** | `manuscript/resubmission_manuscript.tex` | Theoretical Model Only (No direct bio-data) | Needs Experimental Validation |

## Definitions
*   **Confirmed**: Supported by high-confidence structural metrics (Tier 1) and multiple independent data points.
*   **Supported**: Consistent with data but relies on low-confidence structures (Tier 2/3) or single observations.
*   **Uncertain**: Data exists but has quality warnings (e.g., low pLDDT artifacts).
*   **Speculative Narrative**: Logical inference without direct quantitative backing in the current dataset.

## Key Shifts from Baseline
1.  **LBX1 Re-evaluation**: The baseline assumption of LBX1 as a "rod" is unsupported. The data strongly points to a "beads-on-a-string" disordered structure, necessitating a shift to the "Disordered Mechanogating" hypothesis.
2.  **Artifact Awareness**: The identification of Tier 2 structures (High Anisotropy, Low Confidence) prevents false positives where unfolded regions are mistaken for extended rods.
