# Confidence-Weighted Structural Evidence
Date: 2026-02-16 Baseline with explicit confidence segregation.

## High-Anisotropy + Adequate-Confidence (Strong Signal)
Threshold: pLDDT >= 70, ranked by Anisotropy Index.
- **CNNM2**: Anisotropy=8.54, pLDDT=70.4, PAE_blockiness=4.83
- **FBLN5**: Anisotropy=7.05, pLDDT=83.3, PAE_blockiness=3.55
- **STOML3**: Anisotropy=5.56, pLDDT=84.3, PAE_blockiness=0.00
- **PANX3**: Anisotropy=5.08, pLDDT=81.7, PAE_blockiness=2.77
- **LMNA**: Anisotropy=4.75, pLDDT=76.4, PAE_blockiness=2.56
- **PIEZO2**: Anisotropy=4.44, pLDDT=79.4, PAE_blockiness=2.80
- **ROCK1**: Anisotropy=3.29, pLDDT=76.1, PAE_blockiness=4.95
- **ADGRG6**: Anisotropy=3.06, pLDDT=73.7, PAE_blockiness=6.78

## High-Anisotropy + Low-Confidence (Exploratory Only)
Threshold: pLDDT < 70, ranked by Anisotropy Index.
*Caveat: High anisotropy may be an artifact of extended unstructured regions rather than true rigid fibrous geometry.*
- **POC5**: Anisotropy=24.69, pLDDT=64.0, PAE_blockiness=3.51
- **GHR**: Anisotropy=5.13, pLDDT=58.7, PAE_blockiness=5.31
- **EMD**: Anisotropy=4.29, pLDDT=60.3, PAE_blockiness=9.13
- **MESP2**: Anisotropy=4.03, pLDDT=54.2, PAE_blockiness=0.00
- **ARNTL**: Anisotropy=3.32, pLDDT=65.5, PAE_blockiness=3.59

## LBX1 Comparator Analysis
Comparing LBX1 against structurally diverse candidates (PIEZO2, LMNA, ADGRG6, RUNX3, POC5, GHR):
| Gene | Confidence Tier | Anisotropy | pLDDT | PAE Blockiness | Morphology |
|------|-----------------|------------|-------|----------------|------------|
| LBX1 | Low-Confidence | 2.27 | 66.9 | 7.35 | Intermediate |
| POC5 | Low-Confidence | 24.69 | 64.0 | 3.51 | Fibrous/Extended |
| GHR | Low-Confidence | 5.13 | 58.7 | 5.31 | Fibrous/Extended |
| LMNA | Adequate-Confidence | 4.75 | 76.4 | 2.56 | Fibrous/Extended |
| PIEZO2 | Adequate-Confidence | 4.44 | 79.4 | 2.80 | Fibrous/Extended |
| ADGRG6 | Adequate-Confidence | 3.06 | 73.7 | 6.78 | Fibrous/Extended |
| RUNX3 | Low-Confidence | 2.06 | 60.6 | 0.00 | Intermediate |

### Comparator Insights
- **LBX1 vs High-Confidence Effectors (PIEZO2, LMNA, ADGRG6)**: LBX1 exhibits low confidence (pLDDT ~66.9) and intermediate anisotropy (~2.27), unlike the strong rigid-rod fibrous signals of PIEZO2 and LMNA. Its exceptionally high PAE Blockiness (~7.35) supports a multi-domain modular 'beads-on-a-string' topology, making it mechanosensitive to nuclear tension rather than acting as a rigid structural fiber.
- **LBX1 vs Low-Confidence Outliers (POC5, GHR)**: POC5 and GHR show extreme anisotropy (>5.0) but low confidence (<65 pLDDT). This suggests they might be highly extended intrinsically disordered regions (IDRs) or artificial string-like AlphaFold artifacts. LBX1 is less extended and more compact, supporting a functional transcription role.
- **LBX1 vs RUNX3 (Proprioceptive TFs)**: LBX1 has a highly segmented topology (PAE blockiness >7), while RUNX3 is typically monolithic (PAE blockiness ~0). This structural divergence implies differential mechanical sensitivity between the two transcription factors within the proprioceptive axis.