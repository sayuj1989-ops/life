# AlphaFold Structure to Mechanics Map

This document links genetic identity to protein structure (via AlphaFold) and finally to macroscopic mechanical parameters in the biological counter-curvature theory.

| Gene | Protein (Uniprot) | AlphaFold Structural Features | Cellular Function | Mechanical Role / Parameter | Potential Defect Effect |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DNAH5** | Dynein heavy chain | Motor head domain, ATP-binding stalk, Microtubule-binding domain | Ciliary motility, Nodal flow generation | **Symmetry Parameter ($\epsilon$):** Initial Left-Right torque breaking. | Loss of motility $\to$ $\epsilon \approx 0$ $\to$ Random L-R symmetry $\to$ Situs Inversus / Scoliosis Risk |
| **HOXA10** | Homeobox protein | Homeodomain (Helix-Turn-Helix), N-terminal disorder | DNA binding, Segment identity (Lumbar) | **Rest Curvature ($\kappa_0^{lumbar}$):** Defines target lordosis magnitude. | Shift in expression boundary $\to$ Transitional vertebrae, Hypolordosis |
| **HOXD11** | Homeobox protein | Homeodomain, Poly-Alanine tracts | DNA binding, Segment identity (Sacral) | **Stiffness ($EI_{sacral}$):** Sacral rigidity and fusion timing. | Altered pelvic incidence constraints |
| **COL2A1** | Collagen Type II | Triple Helix (Gly-X-Y repeats), Fibril assembly domains | Cartilage ECM structure (Nucleus Pulposus) | **Bulk Modulus ($K_{disc}$):** Hydrostatic pressure capability in disc. | Soft discs $\to$ Load transfer failure $\to$ Wedging |
| **ACAN** | Aggrecan | GAG attachment regions, Hyaluronan binding loop | Water retention, Osmotic swelling | **Growth/Swelling Tensor ($g_{vol}$):** Disc height maintenance under load. | Disc desiccation $\to$ Loss of height $\to$ Kyphosis |
| **PIEZO1** | Piezo-type mechanosensitive channel | Propeller-like trimer, Transmembrane levers | Mechanotransduction (calcium influx) | **Feedback Gain ($G_{mech}$):** Sensitivity of growth to local stress. | Weak feedback $\to$ Failure to reinforce concave side $\to$ Curve progression |

## Quantitative Parameter Mapping (Generated from `alphafold_analysis/map_structure_to_param.py`)

The following mechanical parameters are derived from AlphaFold structural metrics (Helicity, Disorder, Asymmetry):

| Gene | Protein | $EI_{norm}$ (Stiffness) | $\epsilon$ (Torsion/Chirality) | $G_{vol}$ (Growth/Swelling) |
| :--- | :--- | :--- | :--- | :--- |
| **COL2A1** | Collagen II | **0.900** (High) | 0.01 | 0.22 |
| **ACAN** | Aggrecan | 0.133 | 0.05 | **1.60** (Very High) |
| **DNAH5** | Dynein HC | 0.500 | **0.95** (Dominant) | 0.40 |
| **HOXA10** | HOX A10 | 0.600 | 0.10 | 0.70 |
| **PIEZO1** | Piezo1 | 0.633 | 0.40 | 0.65 |

### Parameter Definitions
*   **$EI_{norm}$**: Normalized Bending Stiffness. Derived from Helicity (~Triple helix content) and Packing Density.
*   **$\epsilon$**: Symmetry Breaking Force. Derived from molecular Asymmetry.
*   **$G_{vol}$**: Volumetric Growth Potential. Derived from Intrinsic Disorder (swelling capacity/hydration).

## Structural Hypothesis vs. Mechanics

### 1. The Dynein Motor & Chirality
*   **Structure:** The dynein arm's power stroke has a specific chirality defined by the heavy chain structure.
*   **Mechanics:** This molecular chirality translates to a macroscopic fluid vorticity (Nodal flow), which translates to a chemical gradient, which eventually translates to a slight **pre-twist** ($\tau_0$) in the developing spine.
*   **Model Input:** $\tau(0) = \epsilon_{molecular}$.

### 2. The Collagen Triple Helix & Stiffness
*   **Structure:** The tight winding of the Gly-X-Y triple helix provides immense tensile strength per weight.
*   **Mechanics:** This defines the $EI(s)$ (Bending Stiffness) of the annulus fibrosus. Mutations in glycine repeats (Osteogenesis Imperfecta types) destroy this stiffness.
*   **Model Input:** $EI_{effective} \propto \rho_{collagen} \cdot S_{helix}$.

### 3. Homeodomains & Boundary Precision
*   **Structure:** The affinity of the HOX homeodomain determines how strictly gene expression boundaries are maintained.
*   **Mechanics:** Sharp boundaries create distinct "step functions" in material properties ($EI(s)$). "Fuzzy" binding could lead to gradual transitions, altering the buckling modes.
