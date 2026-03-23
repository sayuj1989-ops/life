# Phase 1, Day 3: GPR126 (ADGRG6) Deep Dive

## Protein Overview
**GPR126 (ADGRG6)** is an adhesion G-protein-coupled receptor. It consists of a large extracellular domain (ECD) which mediates adhesion, a GPCR autoproteolysis-inducing (GAIN) domain, a seven-transmembrane domain (7TM), and an intracellular domain.

## Role in Peripheral Nerve Myelination
The most relevant functional role of GPR126 with respect to proprioceptive delay is its obligate role in Schwann cell myelination. During peripheral nerve development, Schwann cells must transition from a proliferative state to a myelinating state. GPR126 signaling via cAMP pathways is strictly required to drive this differentiation and to maintain the myelin sheath structure.
*   **Knockout Phenotypes:** Loss of Gpr126 in animal models leads to profound deficits in peripheral nerve myelination. This directly impacts the conduction velocity of action potentials.
*   **Relevance to $\tau_{aff}$:** Myelination thickness and integrity directly determine saltatory conduction speed. A hypomorphic variant in GPR126 that modestly reduces its signaling efficiency could result in thinner myelin sheaths (reduced g-ratio) or delayed myelination specifically during the rapid axon elongation of the pubertal growth spurt. This translates directly to a slower afferent conduction velocity and a larger $\tau_{aff}$.

## Structural Considerations and Variant Mapping (AlphaFold Anticipation)
AIS-associated variants often map to intronic regions (affecting expression levels) or specific functional domains. If an AIS risk variant falls in the extracellular adhesion domain, it may weaken the interaction with the extracellular matrix (e.g., laminin or collagen), which provides the mechanical cue for myelination. If it falls in the GAIN or transmembrane domains, it could alter the baseline signaling tone. The upcoming structural analysis using AlphaFold will focus on mapping these specific SNPs onto the 3D structure to predict the functional consequence on receptor activation.

## References

```bibtex
@article{Montigny_2025,
  title={Schwann cells in the inner ear: development, disease, and regeneration},
  volume={19},
  ISSN={1662-5102},
  url={http://dx.doi.org/10.3389/fncel.2025.1662274},
  DOI={10.3389/fncel.2025.1662274},
  journal={Frontiers in Cellular Neuroscience},
  publisher={Frontiers Media SA},
  author={Montigny, Drew J. and Kempfle, Judith S.},
  year={2025},
  month=sep
}

@article{Srivastava_2026,
  title={Adgrg6/Gpr126 is required for compact wall integrity and establishing trabecular identity during cardiac trabeculation},
  volume={17},
  ISSN={2041-1723},
  url={http://dx.doi.org/10.1038/s41467-026-69292-5},
  DOI={10.1038/s41467-026-69292-5},
  number={1},
  journal={Nature Communications},
  publisher={Springer Science and Business Media LLC},
  author={Srivastava, Swati and Gunawan, Felix and Vergarajauregui, Silvia and Gentile, Alessandra and Angeloni, Miriam and Petersen, Sarah C. and Günther, Stefan and Ferrazzi, Fulvia and Stainier, Didier Y. R. and Engel, Felix B.},
  year={2026},
  month=feb
}

@article{El_Hage_2025,
  title={Schwann cells have a limited window of time in which to initiate myelination signaling during early migration in vivo},
  volume={181},
  ISSN={2667-2901},
  url={http://dx.doi.org/10.1016/j.cdev.2024.203993},
  DOI={10.1016/j.cdev.2024.203993},
  journal={Cells & Development},
  publisher={Elsevier BV},
  author={El-Hage, Océane and Mikdache, Aya and Boueid, Marie-José and Degerny, Cindy and Tawk, Marcel},
  year={2025},
  month=mar,
  pages={203993}
}
```
