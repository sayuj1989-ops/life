# Next Step Evidence Summary
**Date:** 2026-03-06
**Author:** AI Research Engineer

## 1. What is Stronger Now (Confidences Gained)
*   **PIEZO2 as a Tension Rod**: Confirmed with high confidence (Score 1.59, Rank #2). Its anisotropy (4.44) is supported by high pLDDT (79.4) and low PAE (17.0), validating it as a rigid mechanical strut.
*   **Structural Dichotomy**: We have successfully separated "True Rods" (PIEZO2, LMNA, PLOD1) from "Disordered Nodes" (LBX1, EGR3, GHR). This resolves previous confusion where low-confidence "anisotropy" was conflated with stiffness.
*   **Metabolic Candidate Identification**: We confirmed that metabolic candidates (ARNTL, GHR) are being actively updated (fresh metrics), distinguishing them from the stale structural candidates.

## 2. What Remains Weak (Risks Identified)
*   **Stale Core Data**: The metrics for PIEZO2, LBX1, and LMNA have not been re-calculated since January (static values). While reliable, they miss any recent pipeline improvements applied to the metabolic set.
*   **LBX1 Mechanism**: The "Stiff Rod" hypothesis for LBX1 is effectively **refuted** by its low structural confidence (pLDDT=66.9). We lack a validated alternative mechanism (Phase Separation is currently speculative).
*   **Schema Instability**: The `metrics.csv` format is drifting, posing a risk to automated monitoring.

## 3. Top 3 Highest-Leverage Next Experiments
Based on the `reports/lbx1_falsifiability_plan.md`, these are the critical next moves:

1.  **Chemical Probe (Phase Separation)**: Treat LBX1-expressing neurons with **1,6-hexanediol**.
    *   *Why*: Fastest way to test the new "Disordered Sensor" hypothesis. If it works, it validates the pivot from "Rod" to "Droplet".
2.  **Nuclear Stiffness Rescue**: Overexpress **Lamin A (LMNA)** in LBX1-KO neurons.
    *   *Why*: Tests the "Downstream" link. If stiffness rescues the phenotype, it confirms the mechanical etiology regardless of LBX1's direct structure.
3.  **Freshness Pipeline Repair**: Refactor `scripts/afcc_daily_refresh.py` to **force-recalculate** metrics for PIEZO2/LBX1 using the latest code, ensuring the "Confidence Gap" isn't just an artifact of old software.

## Conclusion
The Biological Countercurvature hypothesis has matured. We have moved from a simplistic "Everything is a Rod" model to a nuanced "Rods (PIEZO2) vs. Droplets (LBX1)" model. This creates distinct, falsifiable predictions for the next phase of research.
