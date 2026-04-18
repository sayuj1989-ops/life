# Bolt-BioFold ⚡ Analysis Report

## Mission
Analyze a focused set of proteins derived from our default seed list (ECM, mechanotransducers, and morphogens) relevant to spine morphogenesis and the Biological Countercurvature hypothesis using Google AlphaFold data.

## A) Results Table

Note: Strict explicit true SASA (Solvent Accessible Surface Area) was not computed as to avoid introducing new dependency packages. Surface proxy utilizes internal CA geometry approximations.

## B) Key Plots Summary

Generated output files under `outputs/bolt_biofold/figures/`:

* `*_plddt.png`: Plots showing confidence per residue vs threshold bounds (50, 70).
* `*_pae.png`: Selected expected position error correlation matrices mapping domain isolation and interaction likelihood.

## C) Interpretation

* **COL1A1 (P02452)**: **Confidence level: Low**. What we see: Intermediate shape, 16 potential hinge(s), High local curvature. Why it matters: ECM structural component; anisotropy defines load-bearing axis and tissue stiffness. Next test: Test mechanical gating/unfolding under force.
* **PIEZO2 (Q9H5I5)**: **Confidence level: Low**. What we see: Highly elongated/Fibrous, High local curvature. Why it matters: Mechanosensitive channel; curvature/hinges likely relate to gating mechanics under membrane tension. Next test: Compare with orthologs to check conservation of geometry.
* **YAP1 (P46937)**: **Confidence level: Low**. What we see: Intermediate shape, 2 potential hinge(s), High local curvature. Why it matters: Mechanotransducer; structural disorder likely facilitates binding versatility under stress. Next test: Analyze IDR phase separation potential.
* **PKD2 (Q13563)**: **Confidence level: Low**. What we see: Intermediate shape, 1 potential hinge(s), High local curvature. Why it matters: Structural metrics imply role in mechanical integrity or sensing. Next test: Test mechanical gating/unfolding under force.
* **IGF1R (P08069)**: **Confidence level: Low**. What we see: Globular, 35 potential hinge(s), High local curvature. Why it matters: Structural metrics imply role in mechanical integrity or sensing. Next test: Compare with orthologs to check conservation of geometry.
* **LBX1 (P52954)**: **Confidence level: Low**. What we see: Intermediate shape, High local curvature. Why it matters: Structural metrics imply role in mechanical integrity or sensing. Next test: Compare with orthologs to check conservation of geometry.
* **ADGRG6 (Q7Z2K8)**: **Confidence level: Low**. What we see: Intermediate shape, High local curvature. Why it matters: Structural metrics imply role in mechanical integrity or sensing. Next test: Analyze IDR phase separation potential.
* **DMD (P11532)**: **Confidence level: Low**. What we see: Globular, 1 potential hinge(s), High local curvature. Why it matters: Muscle-ECM linker; massive length and flexibility essential for shock absorption. Next test: Compare with orthologs to check conservation of geometry.
* **PPARGC1A (Q9UBK2)**: **Confidence level: Low**. What we see: Intermediate shape, High local curvature. Why it matters: Structural metrics imply role in mechanical integrity or sensing. Next test: Analyze IDR phase separation potential.
* **GHR (P10912)**: **Confidence level: Low**. What we see: Highly elongated/Fibrous, 54 potential hinge(s), High local curvature. Why it matters: Structural metrics imply role in mechanical integrity or sensing. Next test: Test mechanical gating/unfolding under force.
* **ARNTL (O00327)**: **Confidence level: Low**. What we see: Highly elongated/Fibrous, 6 potential hinge(s), High local curvature. Why it matters: Structural metrics imply role in mechanical integrity or sensing. Next test: Test mechanical gating/unfolding under force.
* **MYLK (Q15746)**: **Confidence level: Low**. What we see: Globular, 31 potential hinge(s), High local curvature. Why it matters: Structural metrics imply role in mechanical integrity or sensing. Next test: Analyze IDR phase separation potential.

## D) Best Next Move
Correlate curvature metrics (especially hinge locations) with known pathogenic variants in these genes to identify if mechanical geometry failure drives scoliosis.

---

## Quality & Reproducibility Checklist
- [x] Data source: AlphaFold DB (fetched dynamically/cached)
- [x] Date/time of run: 2026-04-18 00:12:34
- [x] Code version: Current HEAD
- [x] Parameters: pLDDT >= 70 threshold for structure, discrete curvature computation
- [x] Notes: SASA not computed to strictly adhere to zero new dependency rules.