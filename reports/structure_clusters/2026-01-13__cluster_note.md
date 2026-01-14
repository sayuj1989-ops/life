# Cluster Note: Anisotropic Patterning Axis (Cluster 2)

**Date:** 2026-01-13
**Cluster ID:** 2
**Method:** K-Means (k=3) on `anisotropy` vs `pae_blockiness`.

## Cluster Members
* **PIEZO2** (Mechanotransduction, Proprioception)
* **POC5** (Cilia, Centriole)
* **MESP2** (Segmentation, Somite)

## Shared Properties
* **High Anisotropy (Avg ~11.0):** Defines this cluster. POC5 is extreme (~24.7), but PIEZO2 and MESP2 are also extended (~4.0 - 4.4).
* **Low Blockiness (Avg ~2.1):** These proteins are relatively continuous or structurally integrated, rather than being composed of many loosely coupled globular domains.
* **Enrichment:** Spans *Ciliary* structures and *Segmentation* regulators.

## Hypothesized Mechanical Role
**"Long-Range Strain Integration"**

The co-clustering of the ciliary protein POC5 and the segmentation factor MESP2 in this high-anisotropy group suggests a direct structural link between cellular strain sensing and tissue patterning. The extended, anisotropic nature of these proteins may allow them to function as "strain antennas," integrating mechanical signals over long distances (relative to molecular scale) to filter out high-frequency noise and detect stable gravitational vectors. This ensures that the segmentation clock (MESP2) remains synchronized with the physical body axis defined by gravity.

## Concrete Test
**Test:** "Anisotropy-Deficient Segmentation"

*   **System:** Zebrafish embryos.
*   **Perturbation:** Overexpression of a truncated POC5 variant (globular, low anisotropy) or an MESP2 variant with its disordered extensions removed, competing with the endogenous anisotropic forms.
*   **Condition:** Standard 1g vs. Simulated Microgravity (Random Positioning Machine).
*   **Readout:** Vertebral segmentation regularity (somite boundaries) and spine linearity.
*   **Prediction:** Loss of anisotropy (truncation) will disrupt segmentation regularity (hemivertebrae) specifically under 1g loading, as the "antenna" function is required to organize the gravity-resisting structure.
