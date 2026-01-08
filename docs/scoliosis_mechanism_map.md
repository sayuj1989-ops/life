# From Molecules to Curvature: A Causal Map of Scoliosis

## Overview

This document serves as an explainer for the **Scoliosis Mechanism Map** (`docs/figures/scoliosis_mechanism_map.mmd`). It links specific molecular actors to macroscopic tissue mechanics, using the theory of **Biological Counter-Curvature** as the central organizing principle.

### The Organizing Principle: Counter-Curvature

In this framework, the spine is not a passive column but an active structure that grows into a specific shape—the "Counter-Curvature" (e.g., Lordosis)—to anticipate and neutralize gravitational moments. Scoliosis is viewed not as a random deformity, but as a failure of this active stabilization system.

The map categorizes the system into four layers:
1.  **Genetics**: The molecular blueprint.
2.  **Processes**: The cellular activities driven by the blueprint.
3.  **Tissue Properties**: The resulting physical parameters (Stiffness, Curvature, Sensitivity).
4.  **Outcomes**: The macroscopic shape and stability.

---

## Key Pathways

### 1. The Geometry Pathway (HOX Genes)
*   **Source**: `HOXA10` (Lumbar), `HOXD11` (Sacral).
*   **Mechanism**: These genes define the "address" of each segment.
*   **Property**: **Rest Curvature ($\kappa_0$)**. This is the target shape the spine *tries* to grow into (e.g., the degree of lordosis).
*   **Role**: Correct $\kappa_0$ ensures the spine "surfs" the gravitational field efficiently.

### 2. The Stiffness Pathway (Collagen)
*   **Source**: `COL2A1` (Type II Collagen).
*   **Mechanism**: Assembly of the Extracellular Matrix (ECM) in the annulus fibrosus and nucleus pulposus.
*   **Property**: **Bending Stiffness ($EI$)**.
*   **Role**: Provides the material rigidity required to resist Euler buckling. Mutations here lead to "soft" spines that buckle under standard loads.

### 3. The Feedback Pathway (Piezo)
*   **Source**: `PIEZO1` (Mechanosensitive Ion Channel).
*   **Mechanism**: Senses mechanical stress and triggers Calcium influx.
*   **Property**: **Feedback Gain ($G_{mech}$)**.
*   **Role**: Allows the spine to reinforce itself where stress is highest (Heuter-Volkmann law). Low gain leads to a failure to adapt, creating a vicious cycle of deformation.

### 4. The Chirality Pathway (Cilia)
*   **Source**: `DNAH5` / `PKD1L1`.
*   **Mechanism**: Motile cilia generate nodal flow, breaking Left-Right symmetry.
*   **Property**: **Chiral Torsion ($\epsilon$)**.
*   **Role**: Establishes the initial subtle twist. Loss of this signal results in randomized symmetry breaking, a high risk factor for scoliosis.

### 5. The Proprioception Pathway (LBX1)
*   **Source**: `LBX1` (Transcription Factor).
*   **Mechanism**: Drives differentiation of somatosensory relay neurons.
*   **Property**: **Muscle Tone Balance**.
*   **Role**: Maintains symmetric active tension ("guy wires") to stabilize the column. `LBX1` deficiency leads to sensor noise and asymmetric pull.

---

### 6. The Disc Maintenance Pathway (ADGRG6)
*   **Source**: `ADGRG6` (GPR126).
*   **Mechanism**: Regulates fusion of the annulus fibrosus and cartilage integrity.
*   **Property**: **Stiffness ($EI$)** and structural continuity.
*   **Role**: Prevents material failure at the "joints" of the spine. Loss leads to severe buckling.

### 7. The Polarity Pathway (PTK7)
*   **Source**: `PTK7` (Planar Cell Polarity).
*   **Mechanism**: Modulates Wnt signaling to orient cells and tissues (PCP).
*   **Property**: **Tissue Anisotropy**.
*   **Role**: Ensures that growth and mechanical properties are directionally ordered. Loss of polarity makes the tissue mechanically isotropic or chaotic, reducing stability against buckling.

---

## New Pathway: Polarity (PTK7)

**Arc Added**: `PTK7` $\rightarrow$ PCP Signaling $\rightarrow$ Anisotropy $\rightarrow$ Stability.

### Evidence
The gene `PTK7` (Protein Tyrosine Kinase 7) is a key regulator of Planar Cell Polarity (PCP) and has been identified as a causative gene for idiopathic scoliosis in zebrafish models.

*   **Molecular Actor**: `PTK7` is conserved across vertebrates and regulates the non-canonical Wnt pathway.
*   **Process**: It drives **PCP Signaling**, which aligns cell polarity perpendicular to the axis of extension (convergence and extension).
*   **Tissue Property**: This alignment creates **Tissue Anisotropy**, ensuring that the spinal column has distinct properties along the longitudinal axis versus the transverse axes.
*   **Outcome**: In zebrafish, `ptk7` mutants develop severe, late-onset spinal curvature that mimics human AIS. This suggests that without the correct "compass" for cell alignment, the macroscopic structure loses its ability to maintain a straight trajectory during rapid growth.

> **Hypothesis**: High-anisotropy proteins like PTK7 act as "Vectorial Strain Amplifiers," translating micro-scale strain into macro-scale alignment cues. Loss of this anisotropy decouples the tissue from the "Information Field," leading to geometric instability.

**Citation**:
*   *Hayes, M., et al. (2014). Ptk7 mutant zebrafish models of congenital and idiopathic scoliosis implicate dysregulated Wnt signalling. Nature Communications, 5, 4726.* https://doi.org/10.1038/ncomms5726

---

## Figure

The visual representation of these pathways can be found in `docs/figures/scoliosis_mechanism_map.mmd`.
