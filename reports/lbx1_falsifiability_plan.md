# LBX1 Falsifiability Plan: Testing the "Blocky Scaffold" Hypothesis

## Core Hypothesis
LBX1 functions not just as a transcription factor, but as a load-bearing "blocky scaffold" where its modular domains align under tension to gate nuclear signaling.
**Current Status**: Ambiguous Scaffold (Anisotropy 2.27, pLDDT 66.9). The structure suggests flexibility but lacks the "Tension Rod" geometry of PIEZO2 or LMNA.

## Experiment 1: Domain Linker Perturbation
**Hypothesis**: The specific spacing and flexibility between LBX1 domains (high PAE blockiness) is critical for its mechanical function. Disrupting this spacing will uncouple mechanics from signaling.
**Assay Design**:
- **Model**: Zebrafish *lbx1* knockout rescue.
- **Constructs**:
    1. WT LBX1 (Rescue Control)
    2. LBX1-Flex (Flexible GGGGS linkers inserted between blocks)
    3. LBX1-Rigid (Rigid Proline-rich linkers inserted)
- **Method**: Inject mRNA into *lbx1* mutant embryos. Measure spinal curvature at 21 dpf.
**Quantitative Readout**: Cobb angle (degrees) and percentage of rescued spines.
**Expected Direction**: WT rescues curvature. Flex/Rigid variants fail to rescue if geometry is critical, even if nuclear localization is preserved.
**Falsification Threshold**: If LBX1-Flex or LBX1-Rigid rescues scoliosis as effectively as WT (>80% rescue efficiency), the "specific blocky geometry" hypothesis is falsified. It would imply LBX1 acts solely via biochemical presence, not mechanical geometry.

## Experiment 2: LINC Complex Uncoupling
**Hypothesis**: LBX1 mechanosensation requires physical coupling to the nuclear envelope via the LINC complex (Sun1/2, Lamin A/C).
**Assay Design**:
- **Model**: Human Chondrocytes (or Osteoblasts) in a cyclic stretching device (1Hz, 10% strain).
- **Perturbation**: Expression of Dominant Negative KASH domain (DN-KASH) to disrupt LINC complex, or *LMNA* siRNA.
- **Method**: Apply mechanical strain. Measure LBX1 nuclear vs cytoplasmic fraction and transcriptional activity of target genes (e.g., *VEGFA*).
**Quantitative Readout**: Nuclear/Cytoplasmic ratio of LBX1 (Immunofluorescence intensity).
**Expected Direction**: In WT, strain increases LBX1 nuclear retention/activity. In DN-KASH/siLMNA, strain effect is abolished.
**Falsification Threshold**: If mechanical strain induces LBX1 nuclear translocation/activity *despite* LINC disruption (Delta < 15% between WT and DN-KASH), the "Nuclear Tension" hypothesis is falsified. It would suggest LBX1 responds to soluble signals (e.g. Ca2+), not direct nuclear stress.

## Experiment 3: The "Osteopenic Window" Temporal Degron
**Hypothesis**: LBX1 structural integrity is only critical during the peak growth velocity ("Osteopenic Window"), predicting a specific susceptibility window.
**Assay Design**:
- **Model**: *lbx1*-AID (Auxin Inducible Degron) knock-in mouse or zebrafish.
- **Method**: Degrade LBX1 protein by adding Auxin at different developmental stages:
    1. Pre-growth spurt (Early)
    2. Peak growth velocity (Window)
    3. Post-growth spurt (Late)
**Quantitative Readout**: Spinal deformity index (Cobb angle) at maturity.
**Expected Direction**: Degradation during the "Window" causes severe scoliosis. Degradation "Late" has minimal effect.
**Falsification Threshold**: If degradation *after* the growth spurt (Late) still induces significant scoliosis (>10 degrees), the "Osteopenic Window" hypothesis is falsified. It would imply LBX1 is a constant maintenance factor, not a specific counter-curvature brake during growth.

## Summary of Falsification Criteria
1. **Geometry**: If flexible linkers don't break function, geometry is irrelevant.
2. **Mechanics**: If LINC disruption doesn't block sensing, nuclear tension is irrelevant.
3. **Timing**: If late degradation causes curves, the "growth window" model is incorrect.
