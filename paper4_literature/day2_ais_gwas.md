# Paper 4: The Molecular Basis of τ — AIS Genetics

## Overview
This document reviews the major Genome-Wide Association Study (GWAS) hits for Adolescent Idiopathic Scoliosis (AIS) to understand their potential role in modulating the proprioceptive delay ($\tau$). Effect sizes and population frequencies are extracted to inform polygenic modeling.

## Major GWAS Loci

### 1. GPR126 (ADGRG6)
*   **Locus:** Chromosome 6q24.1
*   **Discovery:** Kou et al., 2013, Nature Genetics (DOI: 10.1038/ng.2639). "Genetic variants in GPR126 are associated with adolescent idiopathic scoliosis."
*   **Risk Allele/Variant:** rs6570507
*   **Effect Size:** Odds Ratio (OR) = 1.28 in Japanese; Combined OR = 1.27 across Han Chinese and European-ancestry populations. (P = 1.27 × 10^-14).
*   **Population Frequency:** Common variant.
*   **Proposed Biological Function:** GPR126 (Adhesion G protein-coupled receptor G6) is critical for Schwann cell development and myelination of peripheral nerves. Kou et al. note it is also highly expressed in cartilage and delayed ossification occurs in zebrafish knockouts.
*   **Relevance to $\tau$ Model:** Directly impacts $\tau_{aff}$ (afferent conduction delay) and $\tau_{eff}$ (efferent conduction delay). Impaired myelination would reduce conduction velocity, thereby increasing the delays.

### 2. LBX1 (Ladybird Homeobox 1)
*   **Locus:** Chromosome 10q24.31
*   **Discovery:** Takahashi et al., 2011, Nature Genetics (DOI: 10.1038/ng.974). "A genome-wide association study identifies common variants near LBX1 associated with adolescent idiopathic scoliosis."
*   **Risk Allele/Variant:** rs11190870
*   **Effect Size:** Odds Ratio (OR) = 1.56 (combined P = 1.24 × 10^-19 in Japanese females).
*   **Population Frequency:** Common variant.
*   **Proposed Biological Function:** Transcription factor involved in the specification of dorsal spinal cord interneurons.
*   **Relevance to $\tau$ Model:** May alter the development of proprioceptive relay circuits in the spinal cord, impacting $\tau_{spin}$ (spinal relay delay).

### 3. PAX1 (Paired Box 1)
*   **Locus:** Chromosome 20p11.22
*   **Discovery:** Sharma et al., 2015, Nature Communications (DOI: 10.1038/ncomms7452). "A PAX1 enhancer locus is associated with susceptibility to idiopathic scoliosis in females."
*   **Risk Allele/Variant:** rs6137473
*   **Effect Size:** Odds Ratio (OR) = 1.30 (P = 2.15 × 10^-10 in females, USA and Japan).
*   **Population Frequency:** Common variant.
*   **Proposed Biological Function:** Transcription factor essential for normal vertebral column development.
*   **Relevance to $\tau$ Model:** Likely alters the biomechanical "plant" (vertebral geometry and stiffness) rather than the proprioceptive controller ($\tau$). Important to distinguish from controller variables.

### 4. AJAP1, PAX3/EPHA4, BCL-2 Loci (Zhu et al. 2015)
*   **Discovery:** Zhu et al., 2015, Nature Communications (DOI: 10.1038/ncomms9355). "Genome-wide association study identifies new susceptibility loci for adolescent idiopathic scoliosis in Chinese girls."
*   **Risk Alleles/Variants:**
    *   1p36.32 near AJAP1 (rs241215, P = 2.95 × 10^-9)
    *   2q36.1 between PAX3 and EPHA4 (rs13398147, P = 7.59 × 10^-13)
    *   18q21.33 near BCL-2 (rs4940576, P = 1.43 × 10^-8)
*   **Effect Size:** Moderate (typical for complex trait GWAS).
*   **Population Frequency:** Common variants in Chinese girls cohort.
*   **Proposed Biological Function:** AJAP1 is an adherens junction protein. PAX3/EPHA4 are involved in neurodevelopment and somite formation.
*   **Relevance to $\tau$ Model:** EPHA4 (Ephrin type-A receptor 4) guides axonal pathfinding and could theoretically impact $\tau_{eff}$ or $\tau_{aff}$.

## Synthesis for Model Parameterization
*   **GPR126** is the primary candidate for modulating nerve conduction velocity ($\tau_{aff}$, $\tau_{eff}$) given its role in myelination.
*   **LBX1** is the primary candidate for modulating spinal circuit integration time ($\tau_{spin}$) due to its interneuron specification role.
*   Next steps require deep dives into GPR126 and Piezo2 ($\tau_{trans}$), extracting quantitative bounds on how variants might slow transduction and conduction.
