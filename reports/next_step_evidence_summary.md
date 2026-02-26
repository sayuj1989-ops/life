# Next Step Evidence Summary

**Generated:** 2026-02-26
**Status:** **PIVOT REQUIRED**
**New Direction:** From "Stiff Caliper" to "Condensate Sensor"

## 1. What is Stronger Now
- **Negative Control:** We have definitively **refuted** the idea that LBX1 is a rigid, high-confidence structural rod (`reports/confidence_weighted_structural_evidence.md`). This prevents wasting resources on stiffness assays.
- **Data Integrity:** We have proven that "temporal trends" in AlphaFold metrics were artifacts of data reuse (`reports/evidence_freshness_audit.md`). We now have a clean baseline.
- **New Candidates:** We identified **FBLN5** and **STOML3** as high-confidence, high-anisotropy structural candidates to replace LBX1 in the "Stiffness" arm of the theory.

## 2. What Remains Weak
- **LBX1 Mechanism:** The "Condensate Sensor" hypothesis is plausible (High Blockiness, Low pLDDT) but lacks direct experimental proof.
- **POC5 Reality:** The extreme anisotropy of POC5 (24.7) is paired with low confidence (64.0), making it a high-risk structural bet without TEM/AFM validation.
- **Cross-Species Data:** We still lack the `experiment_cross_species_scaling.py` script and data to validate the evolutionary angle.

## 3. Top 3 Highest-Leverage Next Experiments

1.  **Validate LBX1 Phase Separation (Exp B/C from Plan)**
    - *Why:* If LBX1 does not form condensates, the entire mechanosensory hypothesis for it collapses.
    - *Action:* GFP-LBX1-ΔIDR vs WT in hyper-osmotic stress.

2.  **Test FBLN5/STOML3 as the Real "Stiff Rods"**
    - *Why:* These proteins actually fit the original "Stiff Caliper" structural profile (High Anisotropy + High pLDDT).
    - *Action:* Check expression in paraxial mesoderm; knockdown phenotypes.

3.  **LINC Complex Decoupling (Exp A from Plan)**
    - *Why:* Determines if the sensing is physical (nuclear strain) or biochemical.
    - *Action:* *SUN1/2* knockdown + Cyclic stretch -> LBX1 localization.

## 4. Immediate Actions for Manuscript
- **Rewrite:** Remove all references to LBX1 as a "stiff rod". Replace with "disordered/condensate-forming".
- **Substitute:** Use PIEZO2, LMNA, and FBLN5 as the primary examples of "Molecular Struts".
- **Caveat:** Explicitly label POC5 as a "Putative" fiber requiring validation.
