# Confidence-Weighted Structural Evidence

## Context
This report re-evaluates the structural candidates from the authoritative snapshot (`outputs/afcc/2026-02-16/metrics.csv`) using explicit confidence weighting to prevent the over-interpretation of poorly predicted architectures.

## Methodology
- **Authoritative Snapshot**: `outputs/afcc/2026-02-16/metrics.csv`
- **Adequate Confidence Threshold**: `plddt_mean >= 70.0`
- **High Anisotropy Threshold**: `anisotropy_index >= 3.0`

## Ranked Evidence Tiers

### Tier 1: High Anisotropy + Adequate Confidence (Strongest Structural Signal)
*These candidates exhibit elongated, potentially load-bearing structures with sufficient AlphaFold prediction confidence to warrant mechanistic interpretation.*

- **CNNM2**: Anisotropy = 8.54, pLDDT = 70.4, PAE Blockiness = 4.83
- **FBLN5**: Anisotropy = 7.05, pLDDT = 83.3, PAE Blockiness = 3.55
- **STOML3**: Anisotropy = 5.56, pLDDT = 84.3, PAE Blockiness = 0.00
- **PANX3**: Anisotropy = 5.08, pLDDT = 81.7, PAE Blockiness = 2.77
- **PIEZO2**: Anisotropy = 4.44, pLDDT = 79.4, PAE Blockiness = 2.80
- **ROCK1**: Anisotropy = 3.29, pLDDT = 76.1, PAE Blockiness = 4.95
- **ADGRG6**: Anisotropy = 3.06, pLDDT = 73.7, PAE Blockiness = 6.78

### Tier 2: High Anisotropy + Low Confidence (Exploratory Only)
*These candidates show high anisotropy, but their structures are poorly predicted (often highly disordered). Their geometry should NOT be used to infer precise mechanosensor architecture without orthogonal validation.*

- **POC5**: Anisotropy = 24.69, pLDDT = 64.0, PAE Blockiness = 3.51
- **GHR**: Anisotropy = 5.13, pLDDT = 58.7, PAE Blockiness = 5.31
- **EMD**: Anisotropy = 4.29, pLDDT = 60.3, PAE Blockiness = 9.13
- **MESP2**: Anisotropy = 4.03, pLDDT = 54.2, PAE Blockiness = 0.00
- **ARNTL**: Anisotropy = 3.32, pLDDT = 65.5, PAE Blockiness = 3.59

## LBX1 Comparator Analysis
Comparing LBX1 to key putative mechanosensors and structural candidates.

| Gene | Anisotropy | pLDDT (Confidence) | PAE Blockiness | Confidence Class |
|---|---|---|---|---|
| LBX1 | 2.27 | 66.9 | 7.35 | Low Confidence |
| PIEZO2 | 4.44 | 79.4 | 2.80 | Adequate Confidence |
| LMNA | N/A | N/A | N/A | Not in 2026-02-16 snapshot |
| ADGRG6 | 3.06 | 73.7 | 6.78 | Adequate Confidence |
| RUNX3 | N/A | N/A | N/A | Not in 2026-02-16 snapshot |
| POC5 | 24.69 | 64.0 | 3.51 | Low Confidence |
| GHR | 5.13 | 58.7 | 5.31 | Low Confidence |

### Observations
- **LBX1 Weakness**: LBX1 remains in the "Low Confidence" tier with intermediate anisotropy (~2.27). Its high PAE blockiness (~7.35) suggests a modular architecture, but the low pLDDT prevents definitive geometric claims about its loaded state.
- **PIEZO2 Strength**: PIEZO2 serves as a positive control, showing both high anisotropy and adequate confidence, supporting its established mechanosensory role.
- **Outlier Caution**: While POC5 and GHR show extreme anisotropy, their low pLDDT scores mark them strictly as exploratory.
