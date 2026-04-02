# Confidence-Weighted Structural Evidence

## Baseline Re-ranking
Based on the authoritative metrics snapshot `outputs/afcc/2026-02-16/metrics.csv`, candidates are re-ranked based on their anisotropy index, explicitly weighted by their structural confidence (pLDDT).

### High Anisotropy + Adequate Confidence (pLDDT >= 70, Anisotropy >= 3.0)
These candidates present the strongest structural evidence for extended, load-bearing architecture.

1. **CNNM2**: Anisotropy 8.54, pLDDT 70.4
2. **FBLN5**: Anisotropy 7.05, pLDDT 83.3
3. **STOML3**: Anisotropy 5.56, pLDDT 84.3
4. **PANX3**: Anisotropy 5.08, pLDDT 81.7
5. **PIEZO2**: Anisotropy 4.44, pLDDT 79.4
6. **ROCK1**: Anisotropy 3.29, pLDDT 76.1
7. **ADGRG6**: Anisotropy 3.06, pLDDT 73.7

### High Anisotropy + Low Confidence (Exploratory Only) (pLDDT < 70, Anisotropy >= 3.0)
These candidates appear extended, but their low confidence scores indicate potential flexibility, disorder, or unreliable modeling. Structural inferences should be treated as hypothesis-generating.

1. **POC5**: Anisotropy 24.69, pLDDT 64.0
2. **GHR**: Anisotropy 5.13, pLDDT 58.7
3. **EMD**: Anisotropy 4.29, pLDDT 60.3
4. **MESP2**: Anisotropy 4.03, pLDDT 54.2
5. **ARNTL**: Anisotropy 3.32, pLDDT 65.5

## LBX1 Comparator Analysis
LBX1 is hypothesized to link mechanics with biological countercurvature. We compare its structural metrics against known mechanosensors and related proteins.

| Gene | Anisotropy | pLDDT | PAE Blockiness | Morphology | Confidence Class |
|------|------------|-------|----------------|------------|------------------|
| **LBX1** | 2.27 | 66.9 | 7.35 | Intermediate | Low Confidence |
| **PIEZO2** | 4.44 | 79.4 | 2.80 | Fibrous/Extended | Adequate |
| **ADGRG6** | 3.06 | 73.7 | 6.78 | Fibrous/Extended | Adequate |
| **POC5** | 24.69 | 64.0 | 3.51 | Fibrous/Extended | Low Confidence |
| **GHR** | 5.13 | 58.7 | 5.31 | Fibrous/Extended | Low Confidence |
| **RUNX3** | 2.06 | 63.8 | 3.65 | Intermediate | Low Confidence |

*(Note: LMNA is absent from the 2026-02-16 snapshot.)*

**Conclusion**: LBX1 exhibits intermediate anisotropy (2.27) and low structural confidence (pLDDT 66.9). Unlike high-confidence mechanosensors like PIEZO2 (anisotropy 4.44, pLDDT 79.4), LBX1's current structural model does not provide strong, independent evidence of a fibrous, tension-bearing architecture. Its high PAE blockiness (7.35) suggests a multi-domain or flexible structure rather than a rigid rod.
