# Next Step Evidence Summary

*Generated Date: 2026-02-19*

## 1. What is Stronger Now Than Baseline
- **Clarification of "Tension Rods"**: We have cleanly separated high-confidence anisotropic structures (e.g., `CNNM2`, `FBLN5`, `STOML3`, `PIEZO2`) from low-confidence ones (e.g., `POC5`, `GHR`). This prevents the model from relying on disordered regions as rigid structural pillars (supported by `reports/confidence_weighted_structural_evidence.md`).
- **Audit Traceability**: The implementation of `scripts/analysis/evidence_freshness_audit.py` revealed that narrative updates in cluster reports were often based on identically reused AlphaFold metric vectors (`reports/evidence_freshness_audit.md`). This enforces stricter claim discipline.
- **LBX1 De-risking**: We have explicitly bounded the LBX1 structural claim. It is an intermediate-anisotropy, low-confidence prediction (`outputs/afcc/2026-02-16/metrics.csv`). We now have a concrete falsifiability plan (`reports/lbx1_falsifiability_plan.md`) to test its mechanics experimentally rather than computationally.

## 2. What Remains Weak (Evidence Against Current Hypothesis Iterations)
- **Over-reliance on Static AlphaFold Data**: AlphaFold provides a single, often static ground-state prediction. Inferring dynamic mechanosensing cycles from a static structural snapshot (especially for low-confidence proteins like LBX1) is intrinsically underdetermined and currently weakly supported (`reports/evidence_freshness_audit.md`).
- **Low-Confidence Outliers**: Previous narratives heavily indexed on `POC5` and `GHR` as massive structural sensors due to extreme anisotropy. Confidence-weighting reveals these are low-pLDDT predictions, likely representing unstructured loops rather than rigid rods (`outputs/afcc/2026-02-16/metrics.csv`).
- **LBX1 as a Primary Mechanosensor**: The direct computational evidence for LBX1 acting as a load-bearing tension rod is poor (Anisotropy = 2.27). If it is involved in mechanotransduction, it is likely via network/transcriptional rewiring rather than direct load-bearing.

## 3. Top 3 Highest-Leverage Next Experiments
1. **Magnetic Tweezers on LBX1 (Falsification Experiment 1)**: Directly test whether LBX1 undergoes force-dependent conformational changes at physiological tensions (5-15 pN). This moves the claim from *in-silico* inference to *in-vitro* measurement (`reports/lbx1_falsifiability_plan.md`).
2. **Substrate Strain Assays for POC5/GHR**: Culturing cells on tunable stiffness matrices (1 kPa vs 20 kPa) and measuring localization/expression of POC5 and GHR to confirm if their high computational anisotropy correlates with actual mechanosensitivity.
3. **Cross-Linking Mass Spectrometry (XL-MS) on PIEZO2 and LMNA**: To validate the "Tension Rod" hypothesis for the high-confidence candidates, perform XL-MS under varying mechanical loads to map their dynamic interactomes and confirm rigid vs flexible hinge regions in a biological context.
