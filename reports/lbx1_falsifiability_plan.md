# LBX1 Falsifiability Package
**Target**: LBX1 (Transcription Factor, Scoliosis Driver)
**Hypothesis**: LBX1 acts as a **nuclear mechanosensor** where mechanical stress alters its phase behavior (solubility/binding), coupling spinal growth forces to proprioceptive gene expression.

## Experiment 1: Nuclear Stiffness Rescue
**Hypothesis**: LBX1 dysfunction leads to nuclear softening (via Lamin A/C downregulation or chromatin de-compaction), making proprioceptive neurons hypersensitive to noise.
**Design**:
1.  **Model**: LBX1-knockout or mutant iPSC-derived proprioceptive neurons.
2.  **Intervention**: Overexpress Lamin A (LMNA) to artificially stiffen the nucleus.
3.  **Readout**: neuronal firing rate / adaptation under mechanical ramp stimulation.
**Expected Result**: LBX1-KO neurons are hypersensitive/unstable. LMNA overexpression restores normal firing thresholds.
**Falsification Threshold**: If LMNA overexpression has **no effect** on the firing instability of LBX1-KO neurons, then LBX1's mechanism is **not** mediated by nuclear stiffness.

## Experiment 2: Strain-Dependent Translocation
**Hypothesis**: LBX1 nuclear entry or chromatin binding is gated by mechanical strain on the nucleus (e.g., via nuclear pore opening or phase solubility).
**Design**:
1.  **Model**: Wild-type proprioceptive neurons on a stretchable substrate (10% cyclic strain).
2.  **Tag**: Endogenous GFP-tagged LBX1.
3.  **Readout**: Ratio of Nuclear vs. Cytoplasmic fluorescence intensity under Static vs. Strained conditions.
**Expected Result**: Strain increases Nuclear/Cytoplasmic ratio (mechanically gated entry).
**Falsification Threshold**: If the Nuclear/Cytoplasmic ratio is **unchanged** (< 10% diff) between static and strained conditions, LBX1 is **not** a direct mechanosensor.

## Experiment 3: IDR Phase Disruption
**Hypothesis**: LBX1 transcriptional activity relies on Intrinsically Disordered Region (IDR) driven phase separation (condensates) at super-enhancers.
**Design**:
1.  **Model**: Wild-type proprioceptive neurons.
2.  **Intervention**: Treat with 1,6-hexanediol (dissolves liquid-liquid phase separated droplets) at non-toxic concentrations.
3.  **Readout**: Expression levels of LBX1 target genes (e.g., mechanosensory channels).
**Expected Result**: 1,6-hexanediol treatment mimics the LBX1-KO transcriptional phenotype (downregulation of targets).
**Falsification Threshold**: If 1,6-hexanediol has **no specific effect** on LBX1 targets compared to housekeeping genes, then the **Phase Separation hypothesis is falsified** (LBX1 acts as a standard lock-and-key factor).

## Priority
Start with **Experiment 3** (Chemical probe) as it is the fastest to execute in cell culture.
Follow with **Experiment 2** (Imaging) if Expt 3 suggests phase behavior.
