# Phase 1, Day 2: Adolescent Idiopathic Scoliosis (AIS) Genetics - GWAS Review

This document provides a comprehensive review of the major Genome-Wide Association Study (GWAS) hits for Adolescent Idiopathic Scoliosis (AIS), focusing on risk alleles, effect sizes, population frequencies, and proposed biological functions. The primary goal is to map these genetic variants to the components of the proprioceptive delay ($\tau$) or the mechanical "plant" (spine/vertebrae) in the derivative gain gap model.

## 1. GPR126 (ADGRG6)
*   **Locus/Gene:** Chromosome 6q24.1 / GPR126 (Adhesion G-protein-coupled receptor G6).
*   **Key Variants:**
    *   rs6570507 (intronic): Originally identified in Japanese populations (Kou et al., 2013, Nat Genet).
    *   rs41289839 (G>A): Affects alternative splicing of exon 6 (decreased inclusion). Associated with cartilage development in Chinese populations.
    *   rs225694, rs7774095, rs2294773: Associated with specific curve types (PUMC classification).
*   **Risk Allele / Frequency:** Risk allele frequencies vary by population but are generally common variants (e.g., MAF 0.3-0.5).
*   **Effect Size:** Modest (Odds Ratio ~ 1.15 to 1.30 per risk allele).
*   **Proposed Biological Function:** GPR126 is critical for Schwann cell development and myelination of peripheral nerves. It is also implicated in cartilage development and endochondral ossification.
*   **Mapping to Model:** Primary candidate for modulating $\tau_{aff}$ (afferent conduction delay) via subtle impairments in myelination efficiency during the adolescent growth spurt. Secondary potential effect on the "plant" via cartilage/disc mechanics.

## 2. LBX1 (Ladybird homeobox 1)
*   **Locus/Gene:** Chromosome 10q24.31 / LBX1.
*   **Key Variants:**
    *   rs11190870 (T>C): Located near LBX1. The strongest and most consistently replicated GWAS signal for AIS across Asian and Caucasian populations (Takahashi et al., 2011, Nat Genet).
*   **Risk Allele / Frequency:** Risk allele 'T'. Highly prevalent (e.g., ~60% in some Asian populations).
*   **Effect Size:** Odds Ratio ~ 1.15 to 1.25.
*   **Proposed Biological Function:** LBX1 is a homeobox transcription factor essential for the specification and migration of dorsal spinal cord interneurons, particularly those involved in proprioceptive and somatosensory relay circuits.
*   **Mapping to Model:** Primary candidate for modulating $\tau_{spin}$ (spinal relay delay) by altering the developmental timing, connectivity, or synaptic efficiency of proprioceptive interneurons in the dorsal horn / Clarke's column.

## 3. PAX1 (Paired box 1)
*   **Locus/Gene:** Chromosome 20p11.2 / PAX1 enhancer locus (PEC7).
*   **Key Variants:**
    *   rs169311: Top SNP, predicted to alter transcription factor binding sites (Sharma et al., 2015, Nat Commun).
*   **Risk Allele / Frequency:** Associated specifically with female susceptibility.
*   **Effect Size:** Modest.
*   **Proposed Biological Function:** PAX1 is a transcription factor crucial for the development of the vertebral column (sclerotome differentiation) and segmentation.
*   **Mapping to Model:** Primarily affects the mechanical "plant" (vertebral geometry, disc wedging) rather than the neural controller ($\tau$). This variant may lower the critical threshold for spinal buckling, making the system more vulnerable to a given derivative gain gap.

## 4. Other Notable Loci
*   **BNC2 (Basonuclin 2):** (Chromosome 9p22.2). Implicated in melanocyte development and potentially connective tissue.
*   **MIR4300HG:** Host gene for microRNA MIR4300. Variant associated with *progression* of AIS rather than just onset.

## Synthesis and Next Steps
The GWAS data cleanly separates into two functional categories relevant to the control-theoretic model:
1.  **Controller Variants (modulating $\tau$):** GPR126 (peripheral myelination $\rightarrow \tau_{aff}$) and LBX1 (spinal circuit development $\rightarrow \tau_{spin}$).
2.  **Plant Variants (modulating structural mechanics):** PAX1 (vertebral development).

The next step is to deeply investigate the biological mechanism of GPR126 to precisely quantify how its variants might perturb afferent conduction velocity during adolescence.
