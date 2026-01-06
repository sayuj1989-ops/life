# Hypothesis Register

This register tracks testable predictions derived from synthesis and analysis.

## Format
- **ID:** `H_YYYY_WW_NN` (Year, Week, Number)
- **Statement:** The core hypothesis.
- **Rationale:** Brief mechanistic justification.
- **Verification:** How to test it (experiment or simulation).
- **Status:** `Open`, `Verified`, `Falsified`, `Deprecated`.

---

| ID | Statement | Rationale | Verification | Status |
| :--- | :--- | :--- | :--- | :--- |
| **H_2026_02_01** | **YAP/TAZ Nuclear Enforcement Rescues Unloading Degeneration.**<br>Enforcing YAP nuclear entry (e.g., LATS inhibition) will prevent disc degeneration/stiffness in microgravity. | YAP/TAZ is the fast-response mechanotransducer. Unloading causes cytoplasmic retention, halting ECM maintenance. Forcing it back should mimic "loading" signals. | **In Vitro/In Silico:** Treat unloaded disc organoids with LATS inhibitors and measure ECM gene expression (ACAN, COL2A1) vs untreated. | Open |
| **H_2026_02_02** | **Gravity Threshold for Curvature Consolidation.**<br>Spinal curvature (lordosis) will fail to consolidate below a specific gravity threshold (e.g., <0.16G). | Curvature development relies on asymmetric loading to drive differential growth (Heuter-Volkmann). Without sufficient load, symmetry breaking fails. | **In Silico:** Run PyElastica developmental simulations with varying `g` vectors. Measure final curvature vs `g`. | Open |
