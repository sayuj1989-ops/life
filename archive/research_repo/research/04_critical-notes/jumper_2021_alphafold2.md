---
title: "Highly accurate protein structure prediction with AlphaFold"
authors: "John Jumper, Richard Evans, Alexander Pritzel, et al."
year: "2021"
venue: "Nature"
type: "paper"
tags: [protein structure, AlphaFold, structural biology]
source_file: ""
external_link: "https://doi.org/10.1038/s41586-021-03819-2"
status: "skimmed"
---

# One-paragraph summary

AlphaFold 2 is a deep learning-based system that achieves atomic-level accuracy in predicting protein structures from sequences. It uses an end-to-end neural network architecture that incorporates evolutionary information and physical constraints.

# Key contributions (bullets)

- Significant improvement in the accuracy of protein structure prediction (CASP14).
- Introduction of the "Evoformer" and "Structure Module" components.
- Provision of a platform for biological research at scale (AF Protein Structure Database).

# Methods / assumptions

- Relies on Multiple Sequence Alignments (MSAs).
- Assumes that the folded state is determined by the sequence (Anfinsen's dogma).

# Evidence quality / limitations

- Extremely high evidence quality (validated by experimental structures).
- Limitations: Dynamics, ligands, and multi-protein complexes (partially addressed in later versions).

# My takeaways / how to use

- Use AlphaFold structures to derive local mechanical stiffness and bending properties for the Information-Cosserat model.
- Mapping structural motifs to the IEC framework.

# Related items (internal links)

- [AlphaFold 3 Note](jumper_2024_alphafold3.md)
- [Methods: AlphaFold Analysis](../02_methods/alphafold_analysis/)
