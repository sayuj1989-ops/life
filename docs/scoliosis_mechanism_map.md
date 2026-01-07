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

## New Pathway: Disc Maintenance (ADGRG6)

**Arc Added**: `ADGRG6` $\rightarrow$ Disc Maintenance $\rightarrow$ Stiffness $\rightarrow$ Stability.

### Evidence
The gene `ADGRG6` (also known as `GPR126`) is an Adhesion GPCR that has been identified as a susceptibility gene for AIS and is essential for intervertebral disc development.

*   **Molecular Actor**: `ADGRG6` is expressed in the cartilage and developing spine.
*   **Process**: It regulates **Disc Maintenance**, specifically the fusion of the annulus fibrosus and the structural integrity of cartilaginous tissues.
*   **Tissue Property**: Loss of this gene compromises the **Stiffness ($EI$)** and structural continuity of the spinal column. The intervertebral discs act as flexible joints; if their material quality degrades or they fail to form correctly, the column's effective stiffness drops, making it susceptible to buckling.
*   **Outcome**: In mouse models, conditional deletion of `ADGRG6` in cartilage causes severe scoliosis and pectus excavatum, confirming its critical role in maintaining spinal linearity against loads.

> **Hypothesis**: `ADGRG6` signaling may couple mechanical load on the disc to metabolic maintenance of the ECM, ensuring the disc remains stiff enough to support the growing column.

**Citation**:
*   *Karner, C. M., et al. (2015). Gpr126/Adgrg6 deletion in cartilage models idiopathic scoliosis and pectus excavatum in mice. Human Molecular Genetics, 24(15), 4365-4376.* https://doi.org/10.1093/hmg/ddv170

---

## Figure

The visual representation of these pathways can be found in `docs/figures/scoliosis_mechanism_map.mmd`.
