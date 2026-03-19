# Phase 1, Day 3: GPR126 Deep Dive

## Introduction
GPR126 (Adhesion G Protein-Coupled Receptor G6, encoded by the ADGRG6 gene) is a heavily replicated genetic risk locus for Adolescent Idiopathic Scoliosis (AIS). While often studied in the context of chondrogenesis and bone formation, GPR126 plays a primary and critical role in the peripheral nervous system (PNS).

## Role in Schwann Cell Myelination
According to UniProt (Q86SQ4) and established literature, GPR126 is an adhesion GPCR essential for the differentiation of promyelinating Schwann cells and for the normal myelination of peripheral axons.

*   **Signaling Pathway**: GPR126 binding causes a conformational change that triggers signaling via G proteins, modulating the activity of downstream effectors such as adenylate cyclase. It couples to G(i) and G(q) proteins and elevates intracellular cAMP levels, a critical secondary messenger for upregulating myelin basic protein (MBP) and initiating myelin wrapping.
*   **Knockout Phenotype**: In vertebrate models (e.g., zebrafish and mice), loss of GPR126 results in a complete failure of peripheral nerve myelination. Schwann cells arrest at the promyelinating stage.

## Impact on Nerve Conduction Velocity (NCV) and $\tau_{afferent}$
Myelin acts as an electrical insulator, allowing for rapid saltatory conduction of action potentials along axons.
*   **The $\tau_{afferent}$ Connection**: Group Ia proprioceptive afferents from muscle spindles are among the largest and most heavily myelinated fibers in the body, achieving conduction velocities of 40-60 m/s.
*   **Hypothesis**: Subtle hypomorphic mutations in GPR126 (like those associated with AIS) may not completely arrest myelination but could lead to thinner myelin sheaths (higher g-ratio). A slight reduction in conduction velocity (e.g., from 50 m/s to 40 m/s) over a 1-meter afferent pathway during the adolescent growth spurt would increase $\tau_{afferent}$ by 5 ms. When combined with other delay factors, this pushes the total $\tau$ toward the critical >200 ms instability threshold.

## Structural Insights (AlphaFold Data)
*   **UniProt ID**: Q86SQ4 (Human ADGRG6)
*   **AlphaFold DB**: Structure available for Q86SQ4.
*   **Receptor Structure**: GPR126 possesses a large, alternatively spliced, five-domain extracellular region (ECR), a 7-transmembrane (7TM) domain, and an intracellular tail.
*   **Variant Mapping**: Recent structural studies highlight the functional importance of specific domains, such as the far extracellular CUB domain, in maintaining a compact ECR conformation and regulating signaling (e.g., CUB domain mutant C94Y drastically perturbs ECR conformation). AIS-associated SNPs in regulatory or coding regions of ADGRG6 could similarly alter receptor signaling efficiency, directly impacting the cAMP burst required for optimal adolescent myelin remodeling.

## Conclusion for Paper 4
GPR126 provides the molecular mechanism for the $\tau_{afferent}$ component of the proprioceptive delay model. AIS-associated variations in this gene likely degrade the efficiency of proprioceptive signal transmission from the paraspinal muscles to the spinal cord, predisposing the adolescent to transient postural instability during rapid spinal growth.
