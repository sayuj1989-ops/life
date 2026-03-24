# LBX1 Falsifiability Plan

This document outlines three concrete, quantitative experiments designed to explicitly falsify the hypothesis that LBX1 acts as a mechanosensor or structural tension rod in the context of biological countercurvature.

## Core Hypothesis
LBX1 possesses an intermediate-anisotropy, modular (blocky) architecture that allows it to transduce mechanical tension into biochemical signals, distinct from classical extended tension rods like PIEZO2 or LMNA.

*If this hypothesis is false, LBX1 will not exhibit tension-dependent localization, conformational changes under physiological stress, or structural integrity under mechanical load.*

**Source Data / Rationale**: Based on `outputs/afcc/2026-02-16/metrics.csv`, LBX1 has an `anisotropy_index` of 2.27, a `plddt_mean` of 66.9 (Low confidence), and a high `PAE_domain_blockiness_score` of 7.35.

---

## Experiment 1: Nuclear Tension-Dependent Localization
**Hypothesis**: If LBX1 responds to mechanical cues, modulating nuclear tension via LMNA/LINC complex disruption will alter LBX1 nuclear localization or chromatin binding affinity.
**Assay Design**:
- Cell line expressing tagged LBX1.
- Perturb nuclear tension using LINC complex dominant-negative constructs (e.g., KASH domain overexpression) or direct LMNA knockdown.
- Measure LBX1 nuclear/cytoplasmic ratio and chromatin-bound fraction via quantitative immunofluorescence and cellular fractionation.
**Quantitative Readout**: Ratio of nuclear to cytoplasmic LBX1 intensity; percentage of chromatin-bound LBX1 relative to total protein.
**Expected Direction (if true)**: Decreased nuclear tension reduces LBX1 chromatin binding or nuclear retention.
**Falsification Threshold**: If the change in LBX1 nuclear/chromatin localization between wild-type and tension-depleted cells is $< 10\%$ (p $> 0.05$), the hypothesis that LBX1 localization is tension-dependent is falsified.

---

## Experiment 2: Single-Molecule Force Spectroscopy (smFS)
**Hypothesis**: If LBX1's "blocky" PAE domains (Score: 7.35, low confidence pLDDT: 66.9 per `outputs/afcc/2026-02-16/metrics.csv`) represent mechanically functional hinges or springs rather than unstructured artifactual IDRs, it will exhibit a characteristic force-extension curve distinct from pure globular or pure fibrous proteins, unfolding at specific, physiologically relevant forces.
**Assay Design**:
- Purify recombinant LBX1 protein.
- Perform Atomic Force Microscopy (AFM) based single-molecule force spectroscopy.
- Pull the protein from N- to C-terminus.
**Quantitative Readout**: Unfolding force peaks (pN) and contour length increments ($\Delta L_c$ in nm) during mechanical unfolding.
**Expected Direction (if true)**: Step-wise unfolding corresponding to the predicted modular blocks, with initial unfolding events occurring at forces comparable to known mechanosensors (e.g., 5-20 pN).
**Falsification Threshold**: If LBX1 unfolds in a single, catastrophic event at high forces ($> 50$ pN) typical of stable globular proteins, or shows no structured resistance (pure disorder), the hypothesis that it acts as a modular mechanical spring is falsified.

---

## Experiment 3: In Vivo Mechanotransduction via Orthogonal Reporter
**Hypothesis**: If LBX1 is a critical upstream mechanotransducer in spinal tissue, its targeted degradation will abolish tension-induced downstream transcriptional responses (e.g., YAP/TAZ target gene expression) under cyclical mechanical loading.
**Assay Design**:
- Engineered 3D somite/myotome tissue culture.
- Inducible degron (AID) tagged LBX1.
- Subject tissue to cyclical mechanical stretch (10% strain, 1 Hz).
- Measure downstream mechanosensitive gene expression (e.g., *CTGF*, *CYR61*) via RT-qPCR.
**Quantitative Readout**: Fold-change in downstream target mRNA expression in stretched vs. static conditions, comparing LBX1-intact vs. LBX1-degraded tissues.
**Expected Direction (if true)**: LBX1 degradation significantly dampens or abolishes the stretch-induced upregulation of mechanosensitive targets.
**Falsification Threshold**: If the stretch-induced fold-change of target genes in LBX1-degraded tissues is $\geq 90\%$ of the response in LBX1-intact tissues, the hypothesis that LBX1 is a required primary mechanotransducer in this pathway is falsified.