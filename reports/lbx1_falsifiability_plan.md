# LBX1 Falsifiability Package

## Goal
Establish rigorous criteria to falsify the hypothesis that LBX1 serves as a direct mechanosensor or acts via a mechanically-sensitive modular block architecture.

## Overview
Current metrics for LBX1 (`outputs/afcc/2026-02-16/metrics.csv`) indicate:
- **Anisotropy:** ~2.27 (Intermediate)
- **pLDDT:** ~66.9 (Low confidence)
- **PAE Blockiness:** ~7.35 (High modularity)
- **Status:** Static across 17 runs in the Jan-Feb 2026 trend window.

Because LBX1 lacks the high anisotropy and adequate confidence of established structural anchors (e.g., PIEZO2, pLDDT ~79.4), attributing direct mechanical tension-sensing to its geometry is risky. We propose three concrete experiments to definitively test—and potentially falsify—the mechanical role of LBX1.

---

### Experiment 1: Nuclear Deformation vs. LBX1 Localization and Activity
**Hypothesis:** If LBX1's high PAE blockiness represents a functional architecture tuned to nuclear tension, then altering the mechanical state of the nucleus will change LBX1 sub-nuclear localization or downstream transcriptional activity.

**Assay Design:**
- **System:** Cultured proprioceptive neuronal precursors (or equivalent relevant lineage).
- **Perturbation:** Alter nuclear tension using a LINC complex disruptor (e.g., KASH domain overexpression) or by plating cells on substrates of varying stiffness (e.g., 1 kPa vs. 50 kPa).
- **Control:** Isogenic cells with intact LINC complexes on standard substrates.

**Quantitative Readout:**
1. Nuclear-to-cytoplasmic ratio of LBX1 (via immunofluorescence/confocal microscopy).
2. Transcriptional output of known LBX1 target genes (via RT-qPCR).

**Expected Direction:** If mechanically linked, decreasing nuclear tension should reduce LBX1 nuclear localization or alter its target gene expression.

**Falsification Threshold:**
- If the nuclear-to-cytoplasmic ratio and target gene expression remain unchanged (p > 0.05, effect size < 10%) across the full range of applied mechanical perturbations (e.g., soft vs. stiff substrates, or LINC disruption), the hypothesis that LBX1 function is governed by cellular/nuclear mechanics is **falsified**.

---

### Experiment 2: Truncation Analysis of "Blocky" Domains
**Hypothesis:** If the high PAE blockiness (score ~7.35) observed in AlphaFold predictions corresponds to distinct mechanosensitive hinges or domains, then deleting inter-domain linker regions will abolish mechanically-induced activity while preserving baseline biochemical function.

**Assay Design:**
- **System:** Cell line expressing wild-type or mutant LBX1 constructs.
- **Perturbation:** Generate LBX1 mutants lacking the specific inter-domain regions predicted by AlphaFold to be hinges or flexible linkers (based on PAE matrices).
- **Control:** Wild-type LBX1.

**Quantitative Readout:**
1. Binding affinity to specific DNA motifs (via EMSA or ChIP-seq).
2. Reporter gene activation under basal vs. mechanically stimulated conditions (e.g., cyclic stretch).

**Expected Direction:** Truncating linkers should decouple LBX1 from mechanical inputs, leading to a loss of stretch-induced changes in activity, while basal binding remains intact.

**Falsification Threshold:**
- If the mutant LBX1 constructs maintain the exact same proportional response to mechanical stimulation as wild-type LBX1 (no significant interaction effect between genotype and mechanical state, p > 0.05), the hypothesis that these specific blocky domains/linkers are the mechanical sensors is **falsified**.

---

### Experiment 3: Orthogonal Structural Validation (In vitro Biophysics)
**Hypothesis:** If the AlphaFold prediction of intermediate anisotropy (2.27) and high blockiness represents the true in vivo physiological ensemble, then purified LBX1 will exhibit an extended, multi-domain conformation in solution rather than a collapsed globular or fully disordered state.

**Assay Design:**
- **System:** Recombinant, purified full-length LBX1 protein in physiological buffer.
- **Perturbation:** N/A (observational baseline).
- **Control:** Well-characterized globular (e.g., BSA) and fully intrinsically disordered (e.g., alpha-synuclein) protein standards.

**Quantitative Readout:**
- Radius of Gyration ($R_g$) and maximum dimension ($D_{max}$) measured via Small-Angle X-ray Scattering (SAXS).

**Expected Direction:** The measured $R_g$ and SAXS envelope should correspond to an extended, multi-domain chain, matching the intermediate anisotropy predicted by AlphaFold, rather than a single compact globule.

**Falsification Threshold:**
- If the SAXS data yields a highly compact globular state ($R_g$ significantly smaller than predicted for an extended chain, matching globular standards) OR a random coil signature (Kratky plot indicating no folded domains), the hypothesis that LBX1 possesses a stable, extended mechanosensitive block architecture is **falsified**. The AlphaFold model would be confirmed as an artifact of low-confidence prediction (pLDDT ~66.9).
