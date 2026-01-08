# Candidate Registry

**Last Updated:** Week 2 Cycle
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
| 3 | **SOX9** | 94 | **Growth_Plate**: Master regulator of chondrogenesis and vertebral formation. | Expression is upregulated by mechanical compression; master chondrogenic factor. |
| 4 | **FBN1** | 92 | **ECM**: Major structural determinant of spine elasticity. | Microfibrils provide long-range elasticity and sequester TGF-beta, responding to tissue stretch. |
| 5 | **ACAN** | 92 | **ECM**: Primary provider of compressive resistance in the disc. | Provides osmotic swelling pressure to resist compressive gravity loads in spine. |
| 6 | **YAP1** | 90 | **Mechanotransduction**: Central hub of cellular mechanotransduction. | Nuclear translocation is directly regulated by mechanical stiffness and gravity loading forces. |
| 7 | **POC5** | 90 | **Cilia**: Direct genetic cause of scoliosis linked to ciliary geometry. | Ciliary function is critical for detecting fluid flow and potentially gravity vectors (statocysts analogy). |
| 8 | **ITGB1** | 90 | **Mechanotransduction**: Primary gravity sensor at cell-ECM interface. | Integrins are the primary cellular gravity/load sensors via focal adhesions. |
| 9 | **LRP5** | 90 | **Wnt_Signaling**: Critical for bone's adaptive response to load. | Key Wnt co-receptor for osteocyte mechanotransduction (gravity sensing). |
| 10 | **WWTR1** | 88 | **Mechanotransduction**: Key partner of YAP in mechanosensing. | Paralog of YAP, acts as a mechanosensor of matrix stiffness and gravity-derived stress. |
| 11 | **ADGRG6** | 88 | **Mechanotransduction**: Mechanosensitive receptor directly linked to spine integrity. | GPR126 is a mechanosensitive GPCR; essential for intervertebral disc maintenance under mechanical load. |
| 12 | **FLNB** | 88 | **Cytoskeleton**: Structural integrator of stress and segmentation. | Actin cytoskeleton crosslinker, responds to mechanical stress. |
| 13 | **MESP2** | 88 | **Segmentation**: Critical for vertebral segmentation integrity. | Regulates somite boundary formation (the 'clock'), establishing structural units. |
| 14 | **LMNA** | 88 | **Mechanotransduction**: Nuclear mechanosensor essential for structural integrity. | Nuclear lamina stiffness scales with tissue stiffness and gravity load; mutations disrupt mechanotransduction. |
| 15 | **ACTB** | 88 | **Cytoskeleton**: Fundamental cytoskeletal element for cell mechanics. | Primary structural component resisting gravity; remodels under load. |
| 16 | **VANGL2** | 88 | **PCP**: PCP core component partnering with VANGL1. | PCP signaling aligns cells; critical for neural tube closure against stress. |
| 17 | **HES7** | 88 | **Segmentation**: Driver of the segmentation clock. | Oscillatory expression defines somite timing. |
| 18 | **LFNG** | 88 | **Segmentation**: Critical modulator of segmentation timing. | Modulates Notch signaling in the segmentation clock. |
| 19 | **VANGL1** | 85 | **PCP**: PCP pathway is fundamental to body axis linearity. | Planar Cell Polarity (PCP) aligns cells against tissue stress lines (gravity). |
| 20 | **PTK7** | 85 | **PCP**: Core PCP component linked to spinal curvature. | Regulates convergent extension movements, resisting gravity-induced spreading. |
| 21 | **COL2A1** | 85 | **ECM**: Primary gravity-resisting molecule in the spine. | Major structural component resisting compressive gravity loads in spine. |
| 22 | **TBX6** | 85 | **Segmentation**: Fundamental to vertebral segmentation symmetry. | Regulates somite segmentation clock; timing errors lead to hemivertebrae. |
| 23 | **PTK2** | 85 | **Mechanotransduction**: Key signal transducer for gravity sensing. | Central mediator of integrin mechanotransduction and gravity response. |
| 24 | **PKD2** | 85 | **Cilia**: Ciliary mechanosensor linked to asymmetry. | Mechanosensitive ion channel in cilia (flow/bending). |
| 25 | **DLL3** | 85 | **Segmentation**: Notch ligand essential for somite boundaries. | Notch signaling component for segmentation. |
| 26 | **CDH2** | 85 | **Adhesion**: Transmits mechanical information between cells. | Cell-cell adhesion, transmits tension across tissues. |
| 27 | **TLN1** | 85 | **Mechanotransduction**: Direct force transmission link. | Unfolds under force to recruit vinculin; primary cellular mechanosensor. |
| 28 | **SCRIB** | 85 | **PCP**: PCP determinant essential for axis formation. | Basolateral polarity determinant; integrates mechanical cues. |
| 29 | **RIPPLY2** | 85 | **Segmentation**: Terminator of the segmentation clock. | Regulates somite boundaries. |
| 30 | **PIEZO1** | 85 | **Mechanotransduction**: Partner to PIEZO2 in mechanosensing. | Primary mechanosensor in vascular and bone cells. |

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
