# LBX1 Falsifiability Plan: Mechanosensor vs. Transcription Factor

## 1. Core Hypothesis Under Test
**Hypothesis H_LBX1_Mechanics**: The LBX1 protein structure itself acts as a mechanical sensor (e.g., a "tension rod" or "caliper") that directly transduces cellular strain into biochemical activity, rather than functioning solely as a chemically-gated transcription factor.

**Counter-Hypothesis**: LBX1 is a standard transcription factor with extensive Intrinsically Disordered Regions (IDRs) that create a false signal of "anisotropy" in AlphaFold predictions. Its link to scoliosis is purely through transcriptional regulation of downstream mechanical effectors, not its own structural mechanics.

## 2. Experiment A: The "Rigid-Linker" Rescue (Structural Mechanics)
**Objective**: Determine if the specific elongated geometry of LBX1 is required for its function.

*   **Rationale**: If LBX1 functions as a mechanical caliper/rod, altering its stiffness or length should disrupt its sensing capability. If it is merely a DNA-binder with a floppy tail, replacing the "rod" with a synthetic linker of different stiffness shouldn't matter as long as the DNA-binding domain is intact.
*   **Assay Design**:
    1.  Create LBX1 variants:
        *   `LBX1-WT`: Wild Type.
        *   `LBX1-Flex`: Replace the predicted anisotropic region (likely the IDR/low-confidence tail) with a flexible Gly-Ser linker.
        *   `LBX1-Rigid`: Replace the region with a rigid alpha-helical spacer (e.g., EAAAK repeats).
    2.  Express in *lbx1* null zebrafish or myoblast cell lines.
    3.  Assess rescue of muscle migration defects (zebrafish) or target gene expression (cells).
*   **Quantitative Readout**: Percentage of successful muscle precursor migration events (in vivo) or fold-change of target genes (e.g., *MESP2*, *Tbx6*) via qPCR.
*   **Expected Direction (If Hypothesis H holds)**: `LBX1-WT` rescues. `LBX1-Flex` fails (too floppy to transmit force). `LBX1-Rigid` might hyper-activate or fail (wrong stiffness match).
*   **Falsification Threshold**: If `LBX1-Flex` rescues the phenotype as effectively as `LBX1-WT`, then the specific anisotropic "structure" is irrelevant, and the mechanical sensor hypothesis is **FALSIFIED**.

## 3. Experiment B: Nuclear Strain Translocation (Direct Mechanosensing)
**Objective**: Test if LBX1 localization responds directly to mechanical load, independent of upstream signaling cascades.

*   **Rationale**: Many mechanosensors (YAP/TAZ, MKL1) translocate to the nucleus under strain. If LBX1 is a sensor, it should show similar dynamics.
*   **Assay Design**:
    1.  Culture C2C12 myoblasts expressing GFP-LBX1 on substrates of varying stiffness (1 kPa vs 50 kPa) or subject them to cyclic stretch (10%).
    2.  Block canonical mechanotransduction pathways (e.g., Verteporfin for YAP, Latrunculin A for Actin) to isolate LBX1's intrinsic response.
    3.  Measure Nuclear/Cytoplasmic (N/C) ratio of GFP-LBX1.
*   **Quantitative Readout**: N/C Fluorescence Ratio.
*   **Expected Direction (If Hypothesis H holds)**: N/C ratio increases significantly with stiffness/stretch, even with pathway inhibitors.
*   **Falsification Threshold**: If N/C ratio is invariant across stiffness/stretch conditions (Change < 10% or p > 0.05), or if it is fully blocked by generic pathway inhibitors (indicating it's just a passenger), the intrinsic mechanosensor hypothesis is **FALSIFIED**.

## 4. Experiment C: The "Decoy Rod" Competition (Molecular Crowding)
**Objective**: Test if free-floating "rods" (LBX1 anisotropic domain without DNA binding) inhibit native LBX1 function by saturating mechanical binding sites.

*   **Rationale**: If LBX1 interacts with a cytoskeletal partner via its "rod" domain, overexpression of just that domain should act as a dominant negative.
*   **Assay Design**:
    1.  Overexpress the LBX1 "rod/tail" domain (residues 100-281, high anisotropy region) in wild-type embryos.
    2.  Observe for scoliosis/muscle defects similar to *lbx1* loss-of-function.
*   **Quantitative Readout**: Cobb angle (or equivalent curvature metric) in developing zebrafish/mice.
*   **Expected Direction (If Hypothesis H holds)**: "Decoy Rod" expression induces curvature defects (Dominant Negative effect).
*   **Falsification Threshold**: If "Decoy Rod" expression has **NO phenotypic effect** (indistinguishable from vector control), it suggests the "rod" domain does not engage in critical mechanical protein-protein interactions.

## 5. Summary of Falsification Logic

| Experiment | Outcome supporting Narrative | Outcome FALSIFYING Narrative |
| :--- | :--- | :--- |
| **A. Rigid-Linker** | Geometry/Stiffness is essential for function. | Flexible linker works fine (IDR is just a linker). |
| **B. Strain Translocation** | LBX1 moves/activates by strain alone. | LBX1 is strain-insensitive or purely downstream. |
| **C. Decoy Rod** | Isolated rod domain acts as dominant negative. | Isolated rod is inert. |

**Conclusion**: If Experiment A (Flex Linker) works and Experiment B (Strain) fails, we must conclude LBX1 is **not** a structural mechanosensor. Its "anisotropy" is likely an artifact of displaying an unfolded IDR in a static PDB frame.
