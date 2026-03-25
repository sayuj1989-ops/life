# Day 3: GPR126 (ADGRG6) Deep Dive

## Introduction
GPR126 (Adhesion G protein-coupled receptor G6) is a critical regulator of Schwann cell myelination in the peripheral nervous system. It represents one of the strongest GWAS signals for Adolescent Idiopathic Scoliosis (AIS).

## Role in Myelination
GPR126 is expressed on the surface of Schwann cells. Upon activation by extracellular ligands (such as Laminin-211 or Collagen IV), it signals via $G_{\alpha s}$ to increase intracellular cAMP levels. This cAMP spike is absolutely required for the activation of Oct6 and Krox20 (Egr2), the master transcriptional regulators of myelin basic protein (MBP) and myelin protein zero (MPZ).
- **Knockout Phenotype**: In zebrafish and mice, loss of GPR126 results in amyelinated peripheral nerves (e.g., Mogha et al., 2016, DOI: 10.1523/jneurosci.3854-15.2016). Hypomorphic alleles lead to severe peripheral neuropathy and profoundly reduced nerve conduction velocity (NCV).
- **Conduction Velocity**: NCV is directly proportional to myelin sheath thickness (the $g$-ratio) and internodal length. Thinner myelin (higher $g$-ratio) means higher capacitance and slower saltatory conduction.

## Hypothesis for AIS
We hypothesize that AIS-associated risk variants in GPR126 (such as rs6570507) cause a subtle hypomorphic effect on the receptor's signaling efficiency during the critical pubertal growth window. As long bones rapidly elongate, peripheral nerves are stretched. Schwann cells must continually remodel and extend myelin internodes to maintain optimal NCV. A hypofunctional GPR126 struggles to keep pace, leading to transiently thinner myelin on proprioceptive group Ia/II afferents.

This transient dysmyelination slows afferent conduction velocity, explicitly increasing $\tau_{afferent}$ and $\tau_{efferent}$ during the rapid growth spurt.

## Structural Insight (AlphaFold)
The extracellular domain (ECD) of GPR126 is enormous and contains multiple functional modules (CUB, PTX, HormR, GAIN). The GAIN domain is responsible for autoproteolysis, exposing a tethered "Stachel" sequence that activates the 7TM domain. AIS variants often map to intronic enhancers or subtly alter the ECD, potentially disrupting ligand binding or the mechanical force required to expose the Stachel sequence.
