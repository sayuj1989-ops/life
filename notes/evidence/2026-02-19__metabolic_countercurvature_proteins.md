# Evidence Note: Metabolic Countercurvature Proteins

**Date:** 2026-02-19
**Topic:** Thermodynamic Cost / Metabolic Expansion
**Proteins:** PPARGC1A, IGF1R, GHR, ARNTL, DMD, MYLK

## Context
The "Energy Deficit Window" hypothesis suggests that scoliosis arises when the metabolic cost of maintaining spinal stiffness exceeds the available energy supply during rapid growth. This note documents the addition of 6 key metabolic and structural proteins to the AlphaFold pipeline to quantify their thermodynamic maintenance cost (proxied by Anisotropy and Radius of Gyration).

## Findings: Structural Metrics
The following metrics were computed using the `Metabolic_Expansion` seed list:

| Gene | Role | Anisotropy | Morphology | Rg (Å) | Implication |
|---|---|---|---|---|---|
| **GHR** | Growth Hormone Receptor | **5.13** | Fibrous/Extended | 31.4 | **High Cost:** The receptor driving the adolescent growth spurt is itself highly anisotropic, implying a high entropic cost to maintain its active conformation. This creates a "Scaling Catch-22" where the driver of growth consumes disproportionate energy. |
| **ARNTL** | BMAL1 (Circadian) | **3.32** | Fibrous/Extended | 32.1 | **High Cost:** The core circadian clock factor in the IVD is structurally expensive, linking metabolic timing directly to thermodynamic stability. |
| **PPARGC1A** | PGC-1α (Mito. Biogenesis) | 2.19 | Intermediate | 31.2 | **Supply Regulator:** As the master regulator of mitochondrial biogenesis, its intermediate cost reflects its role as a balanced "hub" for energy supply ($\Gamma_m$). |
| **MYLK** | Myosin Light Chain Kinase | 1.46 | Globular | 41.5 | **Effector:** Regulates tonic contraction. Globular structure suggests stability, but its function drives high-cost ATP consumption in muscles. |
| **IGF1R** | IGF-1 Receptor | 1.43 | Globular | 43.2 | **Signaling:** Key mediator of growth signaling. Lower structural cost compared to GHR suggests GHR is the primary "structural bottleneck" in the growth pathway. |
| **DMD** | Dystrophin | 1.32 | Globular* | 22.8 | **Structural Integrity:** Essential for muscle tone. *Note: Low anisotropy may reflect AlphaFold's prediction of a condensed domain assembly rather than the extended in vivo cytoskeletal state, or domain-specific prediction limitations.* |

## Theoretical Implications
1.  **GHR as a "Buckling Driver":** The high anisotropy of GHR (5.13) supports the theory that rapid growth phases introduce a "Thermodynamic Shock". The receptor itself requires significant negentropy to function, actively competing for ATP with the spinal "Standing Wave".
2.  **Circadian Gating:** ARNTL's high cost (3.32) suggests that circadian disruption (common in adolescents) could destabilize the spine by failing to satisfy the entropy debt of this key clock protein.
3.  **Metabolic Supply:** PPARGC1A represents the "Supply Side" ($\Gamma_m$). Its loss or downregulation (e.g., via inactivity) directly reduces the energy available to pay the "Anisotropy Tax" of proteins like GHR and PIEZO2.

## Next Steps
*   Integrate GHR anisotropy into the $P_{counter}$ calculation in `experiment_energy_deficit_window.py`.
*   Investigate the specific isoform/conformation of DMD to resolve the low anisotropy finding.
