# Phase 1, Day 2: Literature Review — AIS genetics (GWAS Review)

This document provides a comprehensive review of the major Genome-Wide Association Study (GWAS) hits associated with Adolescent Idiopathic Scoliosis (AIS). We map these hits to proposed biological functions, with a specific focus on evaluating their potential impact on proprioceptive delay ($\tau$) versus biomechanical/structural ("plant") alterations.

## Key GWAS Loci and Associated Genes

### 1. LBX1 (Ladybird Homeobox 1)
*   **Locus:** Chromosome 10q24.31
*   **Top SNP:** rs11190870 (most significant in many replication studies)
*   **Risk Allele / Frequency:** T allele is generally the risk allele in East Asian and Caucasian populations. The minor allele frequency (MAF) is often relatively high (e.g., >30-40%).
*   **Effect Size (Odds Ratio):** ~1.56 (combined P = 1.24 × 10^-19 in initial Japanese female cohort; Takahashi et al., 2011).
*   **Proposed Biological Function:** Transcription factor essential for the specification of dorsal spinal cord interneurons, including those critical for proprioceptive and somatosensory relay. It also plays a role in myogenic precursor specification during somite development.
*   **Relevance to $\tau$ model:** Highly relevant. LBX1 could influence $\tau_{spin}$ (spinal relay delay) by altering the architecture or synaptic efficiency of proprioceptive interneuronal circuits in the dorsal spinal cord.

### 2. GPR126 / ADGRG6 (Adhesion G Protein-Coupled Receptor G6)
*   **Locus:** Chromosome 6q24.1
*   **Top SNP:** e.g., rs6570507, rs7774095
*   **Risk Allele / Frequency:** Varies by population; common variants.
*   **Effect Size (Odds Ratio):** ~1.1 to 1.3 depending on the cohort.
*   **Proposed Biological Function:** GPR126 is critical for Schwann cell development and peripheral nerve myelination. Mutations in the gene cause severe myelination defects in model organisms. It is also implicated in chondrogenesis and osteogenesis.
*   **Relevance to $\tau$ model:** Highly relevant. Polymorphisms could subtly impair myelination efficiency of Group Ia/II proprioceptive afferents. Thinner myelin sheaths or altered nodal spacing would reduce nerve conduction velocity (NCV), directly increasing $\tau_{aff}$ (afferent conduction delay).

### 3. PAX1 (Paired Box 1)
*   **Locus:** Chromosome 20p11.22
*   **Top SNP:** rs12946942 (enhancer region locus)
*   **Risk Allele / Frequency:** T allele; common variant (often MAF ~40% depending on population).
*   **Effect Size (Odds Ratio):** Significant association in female AIS cohorts (OR ~1.2, Sharma et al., 2015).
*   **Proposed Biological Function:** Transcription factor critical for early vertebral column development, specifically the patterning and differentiation of the sclerotome (the embryonic source of vertebrae and ribs).
*   **Relevance to $\tau$ model:** Likely *not* a controller ($\tau$) parameter. PAX1 variants are more likely to influence vertebral geometry or disc biomechanics. In the PID inverted pendulum model, PAX1 modifies the "plant" (e.g., stiffness $K$, or introducing initial geometric asymmetry) rather than the proprioceptive delay $\tau$.

### 4. BNC2 (Basonuclin 2)
*   **Locus:** Chromosome 9p22.2
*   **Top SNP:** rs3904778
*   **Risk Allele / Frequency:** C allele; common variant (MAF often >20%).
*   **Effect Size (Odds Ratio):** 1.19 (combined P = 3.28 × 10^-18 in international meta-analysis; Ogura et al., 2015).
*   **Proposed Biological Function:** Zinc finger protein implicated in multiplication of epithelial cells and potentially osteoblast differentiation or function.
*   **Relevance to $\tau$ model:** Likely modifies the "plant" via bone/cartilage matrix properties, similar to PAX1, rather than altering neural processing delays.

### 5. CHL1 (Cell Adhesion Molecule L1 Like)
*   **Locus:** Chromosome 3p26.3
*   **Top SNP:** rs1400180 (first GWAS Caucasian population, though replication in Asian populations is mixed).
*   **Risk Allele / Frequency:** G allele; MAF varies by population, highly frequent in Caucasians.
*   **Effect Size (Odds Ratio):** Initial report OR ~1.3 (Sharma et al., 2011), but often lacks significance in meta-analyses.
*   **Proposed Biological Function:** Cell adhesion molecule belonging to the L1 family, involved in nervous system development, including neurite outgrowth, neuronal migration, and survival.
*   **Relevance to $\tau$ model:** Potentially relevant to central or peripheral axonal pathfinding or synaptic integrity, possibly affecting $\tau_{spin}$ or $\tau_{cereb}$, though evidence is weaker than for LBX1 or GPR126.

## Summary Table

| Gene | Proposed Primary Function | Pathway / Tissue | Hypothesized Impact on PID Model | Target $\tau$ Component |
| :--- | :--- | :--- | :--- | :--- |
| **LBX1** | Dorsal interneuron specification | Neural development (Spinal cord) | Controller degradation | $\tau_{spin}$ (Spinal Relay) |
| **GPR126** | Schwann cell myelination | Peripheral nervous system | Controller degradation | $\tau_{aff}$ (Afferent Conduction) |
| **PAX1** | Sclerotome differentiation | Skeletal development (Vertebrae) | Plant / Structural asymmetry | N/A (Alters plant geometry) |
| **BNC2** | Osteoblast/epithelial function | Skeletal development | Plant / Structural integrity | N/A (Alters plant stiffness) |
| **CHL1** | Axonal guidance / Cell adhesion| Central/Peripheral nervous system | Controller degradation | $\tau_{spin}$ / $\tau_{cereb}$ |

## Conclusion
The AIS genetic architecture supports a dual-mechanism etiology: variants affecting spinal/vertebral development (PAX1, BNC2) modify the biomechanical load (the "plant"), while variants affecting neural circuit development and conduction velocity (LBX1, GPR126) degrade the feedback controller by increasing components of $\tau$. Paper 4 will focus specifically on the latter class.
