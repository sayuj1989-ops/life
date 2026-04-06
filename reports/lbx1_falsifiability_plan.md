# LBX1 Falsifiability Plan: Testing the Mechanics Link

This document establishes strict, testable criteria to falsify the hypothesis that LBX1 acts as a geometry-driven or mechanical load-sensing participant in the Biological Countercurvature framework. Based on current evidence (e.g., `outputs/afcc/2026-02-16/metrics.csv` showing LBX1 with intermediate anisotropy ~2.27, low pLDDT ~66.9, and static properties), we must rigorously test its mechanical responsiveness.

## Core Hypothesis
LBX1 expression, nuclear localization, or transcriptional activity is directly modulated by mechanical tissue tension, thereby integrating metabolic and mechanical growth signals.

## Falsifying Experiments

### Experiment 1: LINC Complex Uncoupling (Nuclear Tension Isolation)
**Hypothesis:** LBX1 localization or activation depends on physical force transmitted to the nucleus via the LINC complex (involving proteins like LMNA or EMD).
**Assay Design:**
- In vitro culture of patient-derived or generic osteoblast/chondrocyte lineages.
- Treat cells with a targeted disruption of the LINC complex (e.g., KASH domain overexpression or dominant-negative SUN/nesprin constructs).
- Apply a standardized cyclic mechanical stretch.
**Quantitative Readout:** Ratio of nuclear to cytoplasmic LBX1 protein (via quantitative immunofluorescence) and LBX1 target gene mRNA expression levels.
**Expected Direction (if hypothesis is true):** LINC disruption abolishes the stretch-induced nuclear accumulation/activation of LBX1.
**Falsification Threshold:** If LINC-disrupted cells still show >80% of the stretch-induced LBX1 activation/localization response seen in wild-type cells, the mechanical-nuclear linkage hypothesis for LBX1 is falsified.

### Experiment 2: Modulating Tissue Stiffness (Matrix Elasticity)
**Hypothesis:** LBX1 expression scales with the mechanical stiffness (elastic modulus) of the surrounding extracellular matrix, functioning as a continuous strain/stiffness sensor.
**Assay Design:**
- Plate cells on synthetic hydrogels of precisely tuned stiffnesses ranging from soft (brain-like, ~1 kPa) to stiff (pre-calcified cartilage/bone, ~50 kPa).
- Maintain constant metabolic/nutrient conditions.
**Quantitative Readout:** Total LBX1 protein levels (Western blot) and transcriptional reporter activity (fluorescence intensity).
**Expected Direction (if hypothesis is true):** LBX1 levels correlate positively with matrix stiffness.
**Falsification Threshold:** If the correlation coefficient (Pearson $r$) between matrix stiffness and LBX1 expression is not statistically significant or $|r| < 0.3$, the continuous stiffness sensor hypothesis is falsified.

### Experiment 3: Isometric Tension vs. Cell Shape Confinement
**Hypothesis:** LBX1 activity is governed by cytoskeletal tension rather than mere cellular geometry/spreading area.
**Assay Design:**
- Micropatterning of cells to distinct geometries (e.g., small circles vs. large stars) to decouple cell area from internal tension.
- Use pharmacological inhibitors of cytoskeletal contractility (e.g., Blebbistatin, Y-27632) to ablate internal tension while maintaining shape constraints.
**Quantitative Readout:** Subcellular distribution of LBX1 and downstream target expression.
**Expected Direction (if hypothesis is true):** Blebbistatin treatment rapidly reverses LBX1 activation regardless of the patterned cell shape.
**Falsification Threshold:** If cell shape (e.g., spreading area) solely dictates LBX1 activity and tension inhibitors fail to reduce LBX1 activation by at least 50% in spread cells, the specific cytoskeletal tension hypothesis is falsified.
