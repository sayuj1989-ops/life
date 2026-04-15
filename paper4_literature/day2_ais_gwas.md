# Phase 1, Day 2: AIS Genetics — Comprehensive Review of GWAS Hits

## Overview
This document catalogs the major Genome-Wide Association Study (GWAS) hits associated with Adolescent Idiopathic Scoliosis (AIS). The focus is on linking these genetic loci to the component proprioceptive delays ($\tau$) modeled in the derivative gain gap framework.

## 1. LBX1 (Ladybird Homeobox 1)
* **Locus**: Chromosome 10q24.31 (e.g., rs11190870)
* **Risk Allele**: T (often upregulates transcription)
* **Effect Size**: Strongest AIS signal; Odds Ratio (OR) ~1.56 (Takahashi et al., 2011, DOI: 10.1038/ng.974).
* **Population Frequency**: High in East Asian and Caucasian populations.
* **Proposed Biological Function**: LBX1 is a homeodomain transcription factor critical for the specification of dorsal spinal cord interneurons, including proprioceptive relay neurons (dI4-dI6).
* **Connection to $\tau$**: Variations in LBX1 may alter spinal relay circuit development, potentially increasing $\tau_{spin}$ (spinal relay delay) via suboptimal synaptic routing or interneuron numbers in Clarke's column and dorsal spinocerebellar tracts.

## 2. GPR126 (ADGRG6 - Adhesion G Protein-Coupled Receptor G6)
* **Locus**: Chromosome 6q24.1 (e.g., rs6570507)
* **Risk Allele**: A / G depending on the specific tag SNP
* **Effect Size**: OR ~1.27 to 1.28 (Kou et al., 2013, DOI: 10.1038/ng.2604).
* **Population Frequency**: Common across diverse populations (replicated in Japanese, Han Chinese, and European ancestry).
* **Proposed Biological Function**: GPR126 is highly expressed in Schwann cells and is absolutely essential for the myelination of peripheral nerves. Knockout/knockdown models show severe myelination defects and delayed ossification in the developing spine.
* **Connection to $\tau$**: GPR126 variants likely impact Schwann cell function during the rapid peripheral nerve elongation of the adolescent growth spurt, leading to transiently thinner myelin sheaths or shorter internodes. This decreases nerve conduction velocity (NCV) and directly increases $\tau_{aff}$ (afferent conduction delay).

## 3. PAX1 (Paired Box 1)
* **Locus**: Chromosome 20p11.22 (e.g., rs6137473, rs169311)
* **Risk Allele**: G (for rs6137473), A (for rs169311)
* **Effect Size**: OR ~1.53 (Sharma et al., 2015, DOI: 10.1038/ncomms7452).
* **Population Frequency**: Present in multiple populations (notably studied in females).
* **Proposed Biological Function**: Transcription factor involved in vertebral column development and somite segmentation.
* **Connection to $\tau$**: Primarily structural. PAX1 likely alters vertebral morphology or spinal biomechanics (the "plant" in the PID model) rather than the neural controller ($\tau$). However, altered vertebral geometry could change proprioceptor mechanosensitivity thresholds.

## 4. BNC2 (Basonuclin 2)
* **Locus**: Chromosome 9p22.2 (e.g., rs10738445, rs10756785)
* **Risk Allele**: Varies; associated with higher binding of YY1 transcription factor and increased enhancer activity.
* **Effect Size**: OR ~1.21 (Ogura et al., 2015, DOI: 10.1016/j.ajhg.2015.06.002).
* **Population Frequency**: Replicated in Japanese and Chinese populations.
* **Proposed Biological Function**: Zinc finger transcription factor. Overexpression causes body curvature in developing zebrafish.
* **Connection to $\tau$**: Precise role in neurophysiology is less clear. It may be structural/biomechanical like PAX1, or it could have pleiotropic effects on both bone and neural crest-derived structures.

## Summary Table

| Gene/Locus | Key SNP | Risk Allele | Odds Ratio (OR) | Proposed Function | Target $\tau$ Component |
|---|---|---|---|---|---|
| LBX1 | rs11190870 | T | ~1.56 | Spinal interneuron specification | $\tau_{spin}$ (Spinal relay delay) |
| GPR126 (ADGRG6) | rs6570507 | A/G | ~1.28 | Peripheral nerve myelination | $\tau_{aff}$ (Afferent conduction delay) |
| PAX1 | rs6137473 | G | ~1.53 | Vertebral column development | Structural ("Plant" geometry) |
| BNC2 | rs10756785 | - | ~1.21 | Transcription factor (bone/cartilage) | Structural ("Plant" geometry) |

## Next Steps
The strong connection between GPR126, myelination, and the adolescent growth spurt makes it the prime candidate for driving the transient increase in afferent delay ($\tau_{aff}$). The next phase (Day 3) will dive deeply into GPR126 structural variants using AlphaFold data.
