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
| 4 | **PIEZO1** | 92 | **Mechanotransduction**: Direct mechanistic link to growth plate asymmetry in scoliosis. | Senses mechanical overload; expression upregulates in compressed regions. |
| 5 | **YAP1** | 90 | **Mechanotransduction**: Central hub of cellular mechanotransduction. | Nuclear translocation is directly regulated by mechanical stiffness and gravity loading forces. |
| 6 | **POC5** | 90 | **Cilia**: Direct genetic cause of scoliosis linked to ciliary geometry. | Ciliary function is critical for detecting fluid flow and potentially gravity vectors (statocysts analogy). |
| 7 | **ITGB1** | 90 | **Mechanotransduction**: Primary gravity sensor at cell-ECM interface. | Integrins are the primary cellular gravity/load sensors via focal adhesions. |
| 8 | **WWTR1** | 88 | **Mechanotransduction**: Key partner of YAP in mechanosensing. | Paralog of YAP, acts as a mechanosensor of matrix stiffness and gravity-derived stress. |
| 9 | **ADGRG6** | 88 | **Mechanotransduction**: Mechanosensitive receptor directly linked to spine integrity. | GPR126 is a mechanosensitive GPCR; essential for intervertebral disc maintenance under mechanical load. |
| 10 | **FLNB** | 88 | **Cytoskeleton**: Structural integrator of stress and segmentation. | Actin cytoskeleton crosslinker, responds to mechanical stress. |
| 11 | **MESP2** | 88 | **Segmentation**: Critical for vertebral segmentation integrity. | Regulates somite boundary formation (the 'clock'), establishing structural units. |
| 12 | **UTS2R** | 88 | **Cilia**: Strong genetic link involving the CSF flow pathway. | Ciliary function detects fluid flow (gravity proxy). |
| 13 | **VANGL1** | 85 | **PCP**: PCP pathway is fundamental to body axis linearity. | Planar Cell Polarity (PCP) aligns cells against tissue stress lines (gravity). |
| 14 | **PTK7** | 85 | **PCP**: Core PCP component linked to spinal curvature. | Regulates convergent extension movements, resisting gravity-induced spreading. |
| 15 | **COL2A1** | 85 | **ECM**: Primary gravity-resisting molecule in the spine. | Major structural component resisting compressive gravity loads in spine. |
| 16 | **TBX6** | 85 | **Segmentation**: Fundamental to vertebral segmentation symmetry. | Regulates somite segmentation clock; timing errors lead to hemivertebrae. |
| 17 | **PTK2** | 85 | **Mechanotransduction**: Key signal transducer for gravity sensing. | Central mediator of integrin mechanotransduction and gravity response. |
| 18 | **PKD2** | 85 | **Cilia**: Ciliary mechanosensor linked to asymmetry. | Mechanosensitive ion channel in cilia (flow/bending). |
| 19 | **DLL3** | 85 | **Segmentation**: Notch ligand essential for somite boundaries. | Notch signaling component for segmentation. |
| 20 | **CDH2** | 85 | **Adhesion**: Transmits mechanical information between cells. | Cell-cell adhesion, transmits tension across tissues. |
| 21 | **FGFR1** | 85 | **Signaling**: Key growth factor receptor linked to congenital spinal defects. | Regulates osteogenesis and limb development under load. |
| 22 | **HES7** | 85 | **Segmentation**: Proven segmentation defect link to spinal malformation. | Establishes structural units (somites) resisting gravity. |
| 23 | **TRPV4** | 82 | **Mechanotransduction**: Direct mechanosensor in chondrocytes. | Mechanosensitive ion channel activated by osmotic and mechanical stress (gravity load). |
| 24 | **CELSR1** | 82 | **PCP**: PCP determinant of tissue polarity. | PCP pathway component aligning tissues against stress. |
| 25 | **COL11A1** | 82 | **ECM**: Controls collagen fibril mechanics. | Nucleates collagen fibril assembly, determining fiber diameter and mechanical strength. |
| 26 | **LAMA2** | 82 | **ECM**: Critical for muscle-matrix coupling; loss leads to severe curvature. | Essential for muscle cell adhesion to ECM, resisting gravity load. |
| 27 | **COMP** | 80 | **ECM**: Critical for matrix integrity under load. | Cartilage Oligomeric Matrix Protein; organizes collagen to resist load. |
| 28 | **PKD1L1** | 80 | **Cilia**: Links CSF flow sensing to spine straightness. | Detects cerebrospinal fluid flow in central canal; flow dynamics are gravity-influenced. |
| 29 | **SHH** | 80 | **Development**: Morphogen establishing the gravity axis. | Notochord (hydrostatic skeleton) secretion; provides initial gravity resistance. |
| 30 | **RUNX2** | 80 | **Bone**: Master regulator of bone response to load. | Master osteogenic factor; expression is upregulated by mechanical load (gravity). |

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
