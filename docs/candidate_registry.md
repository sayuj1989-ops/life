# Candidate Registry

**Last Updated:** Week 1 Cycle
**Focus:** Gravity, Mechanotransduction, and Spinal Curvature

This registry tracks high-priority gene and protein candidates identified as relevant to the "Biological Counter-Curvature" hypothesis. Candidates are scored based on their relevance to:
1.  **Gravity/Mechanotransduction**: Ability to sense or resist physical forces.
2.  **Spinal Curvature**: Genetic or experimental links to scoliosis or vertebral defects.
3.  **Developmental Role**: Involvement in key spinal formation pathways (Somites, PCP, Cilia).

## Top 30 Priority Candidates

| Rank | Gene Symbol | Score | Mechanism / Rationale | Gravity/Mechano Link |
|:----:|:-----------:|:-----:|:----------------------|:---------------------|
| 1 | **PIEZO2** | 95 | **Mechanotransduction**: Direct link between gravity sensing (proprioception) and spinal alignment. | Essential for proprioception, which provides the gravity reference frame for posture control. |
| 2 | **LBX1** | 95 | **Somite**: Major genetic driver of AIS with clear mechanistic link to postural tone. | Regulates migration of muscle precursors and formation of dorsal horn neurons involved in proprioception/gravity sensing. |
| 3 | **FBN1** | 92 | **ECM**: Major structural determinant of spine elasticity. | Microfibrils provide long-range elasticity and sequester TGF-beta, responding to tissue stretch. |
| 4 | **YAP1** | 90 | **Mechanotransduction**: Central hub of cellular mechanotransduction. | Nuclear translocation is directly regulated by mechanical stiffness and gravity loading forces. |
| 5 | **POC5** | 90 | **Cilia**: Direct genetic cause of scoliosis linked to ciliary geometry. | Ciliary function is critical for detecting fluid flow and potentially gravity vectors (statocysts analogy). |
| 6 | **ITGB1** | 90 | **Mechanotransduction**: Primary gravity sensor at cell-ECM interface. | Integrins are the primary cellular gravity/load sensors via focal adhesions. |
| 7 | **WWTR1** | 88 | **Mechanotransduction**: Key partner of YAP in mechanosensing. | Paralog of YAP, acts as a mechanosensor of matrix stiffness and gravity-derived stress. |
| 8 | **ADGRG6** | 88 | **Mechanotransduction**: Mechanosensitive receptor directly linked to spine integrity. | GPR126 is a mechanosensitive GPCR; essential for intervertebral disc maintenance under mechanical load. |
| 9 | **FBN2** | 88 | **ECM**: Major structural component of early elastic fibers. | Forms early microfibrils regulating elastic fiber assembly and TGF-beta bioavailability. |
| 10 | **CAV1** | 88 | **Mechanotransduction**: Critical membrane tension buffer for notochord integrity. | Caveolae buffer membrane tension; loss compromises ability to handle mechanical stress. |
| 11 | **MESP2** | 88 | **Segmentation**: Critical for vertebral segmentation integrity. | Regulates somite boundary formation (the 'clock'), establishing structural units. |
| 12 | **FLNB** | 88 | **Cytoskeleton**: Structural integrator of stress and segmentation. | Actin cytoskeleton crosslinker, responds to mechanical stress. |
| 13 | **COL11A2** | 85 | **ECM**: Collagen nucleation factor linked to vertebral malformations. | Nucleates collagen fibrils; mutations cause Stickler syndrome type III. |
| 14 | **TTLL11** | 85 | **Cilia**: Ciliary modification enzyme linked to spine straightness. | Polyglutamylase modifying ciliary microtubules, affecting beat and sensory function. |
| 15 | **CDH2** | 85 | **Adhesion**: Transmits mechanical information between cells. | Cell-cell adhesion, transmits tension across tissues. |
| 16 | **DLL3** | 85 | **Segmentation**: Notch ligand essential for somite boundaries. | Notch signaling component for segmentation. |
| 17 | **PKD2** | 85 | **Cilia**: Ciliary mechanosensor linked to asymmetry. | Mechanosensitive ion channel in cilia (flow/bending). |
| 18 | **PAX1** | 85 | **Development**: Key transcription factor for vertebral segmentation. | Essential for sclerotome specification under mechanical guidance. |
| 19 | **PTK2** | 85 | **Mechanotransduction**: Key signal transducer for gravity sensing. | Central mediator of integrin mechanotransduction and gravity response. |
| 20 | **VANGL1** | 85 | **PCP**: PCP pathway is fundamental to body axis linearity. | Planar Cell Polarity (PCP) aligns cells against tissue stress lines (gravity). |
| 21 | **PTK7** | 85 | **PCP**: Core PCP component linked to spinal curvature. | Regulates convergent extension movements, resisting gravity-induced spreading. |
| 22 | **TBX6** | 85 | **Segmentation**: Fundamental to vertebral segmentation symmetry. | Regulates somite segmentation clock; timing errors lead to hemivertebrae. |
| 23 | **COL2A1** | 85 | **ECM**: Primary gravity-resisting molecule in the spine. | Major structural component resisting compressive gravity loads in spine. |
| 24 | **LRP5** | 82 | **Signaling**: Key Wnt co-receptor for bone mechanosensing. | Wnt co-receptor essential for osteocyte mechanotransduction (sensing fluid flow). |
| 25 | **COL11A1** | 82 | **ECM**: Controls collagen fibril mechanics. | Nucleates collagen fibril assembly, determining fiber diameter and mechanical strength. |
| 26 | **PIEZO1** | 82 | **Mechanotransduction**: Major cellular mechanosensor complementing PIEZO2. | Primary non-neuronal mechanosensor; senses shear stress and membrane tension. |
| 27 | **CELSR1** | 82 | **PCP**: PCP determinant of tissue polarity. | PCP pathway component aligning tissues against stress. |
| 28 | **TRPV4** | 82 | **Mechanotransduction**: Direct mechanosensor in chondrocytes. | Mechanosensitive ion channel activated by osmotic and mechanical stress (gravity load). |
| 29 | **KCNJ2** | 80 | **Ion_Channel**: Ion channel controlling muscle excitability and tone. | Sets resting membrane potential, critical for muscle tone and excitability against gravity. |
| 30 | **COMP** | 80 | **ECM**: Critical for matrix integrity under load. | Cartilage Oligomeric Matrix Protein; organizes collagen to resist load. |


## Selection Methodology

Candidates were selected based on a "Gravity x Curvature" cross-referencing strategy:
*   **Seed Categories**: Mechanotransduction, Cilia/PCP, Somite Segmentation, Growth Plate.
*   **Expansion Criteria**: Direct literature evidence connecting the gene to both mechanical sensing/response and spinal alignment defects (Scoliosis, Kyphosis, AIS).
*   **Scoring**:
    *   **90-100**: Proven causative gene for Scoliosis with direct mechanotransduction role.
    *   **80-89**: Strong association with Scoliosis and clear mechanobiological function.
    *   **70-79**: Pathway member with experimental links to spine development or gravity response.

## Next Steps

1.  **AlphaFold Analysis**: Run the "Bolt-BioFold" pipeline on the top 10 candidates to assess structural anisotropy and mechanical robustness.
2.  **Simulation**: Incorporate PIEZO2 and LBX1 related parameters (neuromuscular tone) into `pyelastica` models.
3.  **Literature Review**: Deep dive into the "Proprioception as Gravity Sensing" mechanism for LBX1.
