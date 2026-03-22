# Confidence-Weighted Structural Evidence

## Overview
Re-ranking AlphaFold structural outputs utilizing explicit confidence gating (adequate: pLDDT >= 70, high anisotropy: >= 3.0) refines the Biological Countercurvature evidence base. This approach separates measured structural signals from low-confidence model hallucinations, providing a rigorous filter for hypothesis generation. Data from latest snapshot `outputs/afcc/2026-02-16/metrics.csv`.

## 1) High Anisotropy + Adequate Confidence (Strong Structural Signal)
These targets exhibit extended geometries robustly supported by AFCC metrics.

1. **CNNM2**: Anisotropy 8.54, pLDDT 70.37
2. **FBLN5**: Anisotropy 7.05, pLDDT 83.34
3. **STOML3**: Anisotropy 5.56, pLDDT 84.33
4. **PANX3**: Anisotropy 5.08, pLDDT 81.72
5. **PIEZO2**: Anisotropy 4.44, pLDDT 79.44
6. **ROCK1**: Anisotropy 3.29, pLDDT 76.13
7. **ADGRG6**: Anisotropy 3.06, pLDDT 73.73

*Conclusion*: PIEZO2 and ADGRG6 demonstrate strong confidence scores alongside their elongated architecture. This firmly grounds the concept of mechanosensory 'Tension Rods' in structural data, distinguishing it from purely hypothetical models.

## 2) High Anisotropy + Low Confidence (Exploratory Only)
These targets exhibit extended geometries but lack the high pLDDT scores required for firm structural conclusions. High anisotropy here often correlates with large intrinsically disordered regions (IDRs) or isolated segments stretched due to missing inter-domain contacts.

1. **POC5**: Anisotropy 24.69, pLDDT 63.97
2. **GHR**: Anisotropy 5.13, pLDDT 58.70
3. **EMD**: Anisotropy 4.29, pLDDT 60.25
4. **MESP2**: Anisotropy 4.03, pLDDT 54.17
5. **ARNTL**: Anisotropy 3.32, pLDDT 65.53

*Conclusion*: POC5 and GHR possess extremely high anisotropy metrics but cannot be treated as verified tension rods without orthogonal validation. Their 'extendedness' may reflect modeling artifacts of flexible linkers rather than native rigid architecture.

## 3) LBX1 Comparator Panel Analysis
Contextualizing LBX1 against other key proteins.

| Gene | Anisotropy | pLDDT | Category |
|------|------------|-------|----------|
| PIEZO2 | 4.44 | 79.44 | 1) high-anisotropy + adequate-confidence |
| ADGRG6 | 3.06 | 73.73 | 1) high-anisotropy + adequate-confidence |
| POC5 | 24.69 | 63.97 | 2) high-anisotropy + low-confidence (exploratory only) |
| GHR | 5.13 | 58.70 | 2) high-anisotropy + low-confidence (exploratory only) |
| **LBX1** | **2.27** | **66.87** | **3) intermediate/low-anisotropy** |

*(Note: LMNA and RUNX3 are not present in the 2026-02-16 snapshot but historically present in earlier runs).*

### LBX1 Structural Diagnosis
LBX1 exhibits an **Intermediate Anisotropy (2.27)** and **Low Confidence (66.87 pLDDT)** with a high PAE blockiness (7.35).
* **Interpretation**: LBX1 does *not* structurally resemble verified tension rods like PIEZO2. Its low confidence and intermediate anisotropy suggest it is not a primary load-bearing structural element or rigid tension sensor.
* **Caveat**: The high blockiness and intermediate anisotropy previously led to narratives characterizing it as a 'Cryptic Signal Reservoir' or a 'Blocky Integrator'. However, due to its low pLDDT, these are purely speculative structural interpretations. LBX1's mechanism must be verified via alternative means rather than assumed through its AlphaFold geometry.
