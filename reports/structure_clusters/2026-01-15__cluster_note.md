# Cluster Note: Anisotropic Cilio-Nuclear Tethers (Cluster 0)

**Date:** 2026-01-15
**Cluster ID:** 0
**Method:** K-Means (k=3) on `anisotropy` vs `pae_blockiness`.

## Cluster Members
*   **PIEZO2** (Mechanotransduction, Proprioception)
*   **IFT88** (Cilia, Mechanotransduction)
*   **LMNA** (Mechanotransduction, Nucleus, Cytoskeleton)
*   **POC5** (Cilia, Centriole)

## Shared Properties
*   **High Anisotropy (Avg ~9.17):** This cluster is defined by extreme structural elongation. All members (PIEZO2, IFT88, LMNA, POC5) possess extended geometries or filamentous repeating units.
*   **Low/Moderate Blockiness (Avg ~2.82):** These proteins act as continuous structural cables rather than isolated domain islands.
*   **Enrichment:** Spanning from **Cilia** (IFT88, POC5) to the **Nucleus** (LMNA), with **Membrane** sensing (PIEZO2).

## Hypothesized Mechanical Role
**"Anisotropic Cilio-Nuclear Tethers"**

The co-clustering of ciliary structural components (IFT88, POC5) with the nuclear lamina (LMNA) in this high-anisotropy group suggests a direct physical pathway for "Vectorial Mechanotransduction." Unlike scalar pressure sensing, detecting gravity's direction requires a reference vector. These elongated proteins likely align to form a trans-cellular "tether" that couples ciliary bending (fluid flow/gravity) directly to nuclear deformation, bypassing slower biochemical cascades. This anisotropy ensures that the *direction* of ciliary deflection is preserved and mapped onto the nuclear envelope to regulate gene expression spatially.

## Concrete Test
**Test:** "Ciliary-Nuclear Mechanical Decoupling"

*   **System:** RPE1 cells (ciliated) or Tenocytes (mechanosensitive) in 3D culture.
*   **Perturbation:** Overexpression of a "Blocky" mutant of IFT88 or POC5 (repeats removed or disordered linkers rigidified) to disrupt the anisotropic transmission chain, while preserving chemical function.
*   **Condition:** Laminar fluid flow (simulating gravitational shear) vs. Static.
*   **Readout:** Nuclear envelope deformation (Lamin A/C strain) and translocation of mechanosensitive factors (e.g., YAP).
*   **Prediction:** Cells with "Blocky" ciliary proteins will show reduced nuclear deformation and blunted YAP response specifically to *directional* shear, despite intact ciliary structure, proving anisotropy is required for force transmission.
