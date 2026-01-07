# Cluster Note: Anisotropic Strain Sensors (2026-01-06)

## 1. Cluster Identification
*   **Cluster Name:** Fibrous/Intrinsic Anisotropy
*   **Method:** K-Means proxy (Anisotropy > 3.15, Blockiness < 5.9)
*   **Members:** `PTK7` (PCP), `POC5` (Cilia), `PIEZO2` (Mechanotransduction)

## 2. Shared Structural Properties
*   **High Anisotropy:** All members exhibit an elongation ratio > 3.0, significantly higher than the globular baseline (~1.5).
*   **Hinge Presence:** Identified flexible hinge regions (e.g., PTK7 residues 155, 869; POC5 residues 156, 247) suggest these are not rigid rods but articulated levers.
*   **Low Blockiness:** Despite their length, they lack the dense, packed domain architecture of globular multi-domain proteins (like COL2A1 or YAP1), suggesting a more extended, perhaps scaffold-like or repetitive structure.

## 3. Hypothesized Mechanical Role
**"Vectorial Strain Amplifiers"**

The standard model of mechanotransduction often involves globular conformational changes (e.g., integrins) or membrane tension (e.g., channels). This cluster suggests a distinct class of **Directional Sensors**.
*   **PTK7 (PCP):** Its extended ECD/ICD structure may serve to align the cell polarity axis with the principal stress vector of the tissue (gravity/tension lines).
*   **POC5 (Cilia):** As a component of the centriole/cilium, its high anisotropy contributes to the structural stiffness required for the cilium to act as a cantilever beam detecting fluid flow or gravity-induced bending.
*   **PIEZO2:** While a channel, its propeller arms (detected here as anisotropic) extend far into the membrane/cortex to gather tension from a wide area, amplifying small local strains into pore opening.

**Hypothesis Statement:**
These proteins utilize their extreme elongation (Anisotropy > 3) to integrate mechanical signals over long intracellular distances ($>20$ nm), serving as "antennae" that provide the directional vector information (not just scalar magnitude) required for spinal alignment against gravity.

## 4. Proposed Test
**Phenotype:** Directional migration or alignment of fibroblasts/chondrocytes on a cyclically stretched substrate.
**Perturbation:**
1.  Express Wild Type vs. Truncated variants (preserving catalytic/pore function but reducing anisotropy/arm length).
2.  **Prediction:** Truncated variants will maintain scalar mechanosensitivity (e.g., calcium influx upon osmotic shock) but lose **vectorial sensitivity** (failure to align perpendicular to stretch axis).
