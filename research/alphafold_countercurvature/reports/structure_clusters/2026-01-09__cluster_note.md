# Structure Cluster Note: The "Strain Antenna" Complex
**Date:** 2026-01-09
**Cluster ID:** 2026-01-09_Cluster_0
**Method:** K-Means (k=3) on AFCC Metrics (Anisotropy, PAE_Blockiness)

## 1. Cluster Members
| Gene | Anisotropy | Blockiness | Source | Role |
|---|---|---|---|---|
| **POC5** | 4.97 | 3.51 | Cilia | Centriolar structure, extended fiber |
| **PIEZO2** | 3.45 | 2.80 | Mechanotransduction | Ion channel, force sensor |
| **ADGRG6** | 2.80 | 6.78 | Mechanotransduction | Adhesion GPCR, scoliosis associated |
| **ITGB1** | 2.79 | 4.90 | Mechanotransduction | Integrin, ECM adhesion |

## 2. Shared Properties
- **High Anisotropy (> 2.5):** All members exhibit significant structural elongation, exceeding the typical globular range.
- **Moderate Domain Blockiness:** Unlike the "beads-on-a-string" transcription factors (Cluster 1), these proteins appear to be fibrous or extended structural components with integrated domains.
- **Mechanotransduction Nexus:** The cluster brings together the primary force sensors (PIEZO2, ITGB1) with the ciliary base (POC5), suggesting a structural coupling.

## 3. Hypothesized Mechanical Role: The "Strain Antenna"
**Statement:**
High-anisotropy proteins at the cell periphery (Adhesion/Membrane) and the ciliary base (Centriole) function as a unified **"Strain Antenna"**. Their physical elongation is not merely a packing feature but a functional requirement to bridge the spatial gap between the extracellular matrix (ITGB1, ADGRG6) and the intracellular polarity centers (POC5).

**Mechanism:**
We propose that the "anisotropy match" allows these proteins to transmit shear stress vectors faithfully. Disruption of this elongation (e.g., via POC5 truncation or ADGRG6 ECD cleavage) decouples the membrane strain field from the ciliary orientation response, blinding the cell to gravity/fluid flow directionality.

## 4. Proposed Test
**Experiment:** "Anisotropy Rescue Assay"
1. **Model:** Ciliated epithelial cells (e.g., MDCK or osteocytes) under fluid shear.
2. **Perturbation:** Express a truncated POC5 mutant (maintaining centriolar localization but reducing anisotropy) or a flexible-linker ADGRG6 variant.
3. **Readout:** Measure the alignment of the primary cilium relative to flow vector.
4. **Prediction:** Cells with reduced-anisotropy variants will fail to align cilia with flow, despite having functional ion channels/GPCR domains, proving that *shape* drives *directionality*.
