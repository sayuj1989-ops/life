# Cluster Report: Anisotropic Ciliary Relays

**Date:** 2026-05-25
**Cluster Name:** Anisotropic Ciliary Relays (The "Cantilevers")
**Source Data:** Bolt-BioFold Analysis (2026-01-27)

## 1. Cluster Members
This cluster was identified by filtering for **High Anisotropy Index (> 7.0)** and **Ciliary/PCP Localization**.

| Protein | Gene | Anisotropy | Length | pLDDT | Hinge Candidates | Localization |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **POC5** | *POC5* | **24.69** | 575 | 64.0 | 5 | Centriole/Cilia |
| **PTK7** | *PTK7* | **7.45** | 1070 | 82.7 | 20 | Cilia/PCP |

**Outliers/Related:**
- **PIEZO2** (Anisotropy 4.44): Mechanosensor, but less extreme geometry. Likely the "Transducer" coupled to these "Cantilevers".
- **MESP2** (Anisotropy 4.03): Segmentation, also extended but distinct pathway.

## 2. Shared Properties
1.  **Extreme Anisotropy:** POC5 is effectively a 1D line (Anisotropy ~25). PTK7 is also highly elongated.
2.  **Structural "Hinges":** Both contain flexible linker regions (detected by PAE blockiness drops) separating rigid domains. POC5 has 5, PTK7 has 20.
3.  **Localization:** Both are essential for ciliary function or Planar Cell Polarity (PCP), the systems responsible for spatial orientation.
4.  **Phenotype:** Loss of either gene causes scoliosis in zebrafish and is linked to AIS in humans.

## 3. Hypothesized Mechanical Role: The "Molecular Cantilever"
We propose that these proteins do not merely "scaffold" the cilium but act as **active mechanical lever arms (Cantilevers)**.

*   **Mechanism:** The extreme length ($L$) of the rigid rod domain provides a mechanical advantage, amplifying small displacements ($\delta x$) at the tip (e.g., from fluid flow or gravity-induced settling) into larger torque ($\tau = F \times L$) at the base.
*   **The Hinge:** The "Hinge Candidates" identified in the PAE plots act as the **fulcrum** or the **transduction site**, where mechanical stress triggers a conformational change (e.g., exposing a cryptic binding site or gating an ion channel like PIEZO2).
*   **Gain Control:** The length of the anisotropic domain sets the **Proprioceptive Gain ($\gamma$)**. A shorter rod (truncation) reduces $\gamma$, causing the system to underestimate the error signal and fail to correct spinal curvature (Bastien instability).

## 4. Proposed Test: The "Cantilever Ablation"
**Hypothesis:** The mechanical sensitivity (Gain) of the system is proportional to the Anisotropy (Length) of the relay protein.

**Experiment:**
1.  **Model:** Ciliated epithelial cells (e.g., MDCK) or Zebrafish lateral line.
2.  **Perturbation:** Express a series of POC5 or PTK7 truncation mutants where the rigid "rod" domains are progressively shortened, but the signaling domains (kinase/binding) are preserved.
3.  **Readout:** Measure the Calcium response (via GCaMP) to a defined fluid shear stress.
4.  **Prediction:** There will be a linear relationship between **Rod Length (Anisotropy)** and **Calcium Peak Amplitude (Gain)**. Below a critical length, the signal will vanish, mimicking the microgravity state.

## 5. Connection to Scoliosis
Scoliosis in this framework is a failure of **Geometric Amplification**. If the "antenna" is too short (mutation) or the force is too weak (microgravity), the error signal drops below the noise floor, and the spine drifts into a buckle mode.
