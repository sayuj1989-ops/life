# Cluster Note: Fibrous Anisotropic Scaffolds (Cluster 0)

**Date:** 2026-01-08
**Cluster ID:** 0
**Method:** K-Means (k=3) on `anisotropy` vs `pae_blockiness` (proxy for multi-domain flexibility).

## Cluster Members
* **PIEZO2** (Mechanotransduction, Proprioception)
* **POC5** (Cilia, Centriole)
* **ITGB1** (Mechanotransduction, Adhesion)
* **ADGRG6** (Mechanotransduction, Adhesion)

## Shared Properties
* **High Anisotropy (> 2.7):** These proteins exhibit extended, non-globular shapes.
* **Moderate Blockiness (~4.5):** They are not monolithic rods nor highly flexible multi-domain beads-on-a-string (compared to Cluster 1's avg blockiness of 7.85). They likely contain stiff structural domains linked by limited flexible regions.
* **Enrichment:** Strongly associated with *Mechanotransduction* and *Adhesion* at the cell periphery.

## Hypothesized Mechanical Role
**"Vectorial Strain Amplifiers"**

The high anisotropy combined with structural rigidity (moderate blockiness) suggests these proteins align with the principal strain vector of the cell. Unlike globular sensors that might detect isotropic pressure, these extended scaffolds likely act as **strain amplifiers**, converting small tissue-level deformations into significant molecular displacements along their long axis. In the context of the spine, their alignment provides the directional information required to distinguish beneficial loading (gravity) from pathological torsion.

## Concrete Test
**Test:** "Anisotropy-Dependent Strain Response"

*   **System:** Human Mesenchymal Stem Cells (hMSCs) or Chondrocytes.
*   **Perturbation:** Compare wild-type response to a truncated mutant of *POC5* or *ADGRG6* where the anisotropic tail is removed but the catalytic/signaling head is intact.
*   **Application:** Apply cyclic uniaxial stretch (10%, 1Hz).
*   **Readout:** Measure nuclear localization of YAP/TAZ (as a proxy for mechanotransduction efficiency).
*   **Prediction:** Truncated (low anisotropy) mutants will show significantly reduced YAP nuclear translocation compared to WT under directional strain, despite having functional signaling domains, verifying the geometric "amplifier" role.
