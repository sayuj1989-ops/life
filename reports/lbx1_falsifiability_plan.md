# LBX1 Falsifiability Plan

This plan defines strict falsification criteria for the hypothesized link between LBX1 and mechanical transduction in the context of Biological Countercurvature.

## Core Hypothesis
LBX1 acts as a mechanical sensor or early responder to tissue tension, driving S-shaped growth patterns (countercurvature) in the spine.

## Proposed Experiments

### 1. Nuclear Mechanotransduction Dependence
**Hypothesis:** LBX1 nuclear localization and transcriptional activity are directly modulated by cytoskeletal tension.
**Assay Design:** Subject human primary osteoblasts or chondrocytes to cyclic mechanical stretch (e.g., Flexcell) vs. static control. Apply LINC complex disruptors (e.g., KASH-domain overexpression) to decouple the nucleus from the cytoskeleton.
**Quantitative Readout:** Ratio of nuclear to cytoplasmic LBX1 protein (via quantitative immunofluorescence) and mRNA levels of LBX1 downstream targets (e.g., via RT-qPCR).
**Expected Direction:** Mechanical stretch increases nuclear LBX1 and target gene expression; LINC disruption abolishes this effect.
**Falsification Threshold:** If stretch does not significantly alter nuclear LBX1 localization (p > 0.05) or if LINC disruption fails to blunt the response, the direct mechanotransduction link is falsified.

### 2. Structural Rigidity vs. Flexibility
**Hypothesis:** LBX1 possesses a rigid, load-bearing domain crucial for its hypothesized mechanosensor role, despite low AlphaFold confidence.
**Assay Design:** Perform Small-Angle X-ray Scattering (SAXS) or single-molecule FRET on purified LBX1 protein in solution to assess its conformational ensemble and rigidity.
**Quantitative Readout:** Radius of gyration ($R_g$), maximum dimension ($D_{max}$), and FRET transfer efficiency distributions.
**Expected Direction:** SAXS profile consistent with an extended, rigid rod (high anisotropy). FRET shows a narrow distribution indicating a stable, non-flexible conformation.
**Falsification Threshold:** If SAXS/FRET reveals a highly dynamic, unstructured, or compact globular ensemble, contradicting the "rigid sensor" model, the structural hypothesis is falsified.

### 3. Tension-Dependent Countercurvature in vivo
**Hypothesis:** LBX1 is required for the compensatory S-shaped spinal curve (countercurvature) induced by asymmetrical mechanical loading.
**Assay Design:** Utilize a zebrafish model (e.g., *lbx1* knockout/morpholino vs. wild-type). Induce mechanical asymmetry (e.g., via unilateral muscle ablation or tethering). Monitor spinal curvature over time.
**Quantitative Readout:** Cobb angle (or equivalent curvature metric) of primary and secondary (compensatory) spinal curves.
**Expected Direction:** Wild-type fish develop a compensatory counter-curve. *lbx1* mutants either fail to develop the counter-curve or develop severe, uncompensated primary curves.
**Falsification Threshold:** If *lbx1* mutants develop compensatory counter-curves statistically indistinguishable from wild-type (p > 0.05), LBX1's necessary role in countercurvature is falsified.
