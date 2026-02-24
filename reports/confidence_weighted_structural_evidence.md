# Confidence-Weighted Structural Evidence

## 1. Methodology
- **Data Source**: Composite snapshot of `2026-02-16` (Baseline) and `2026-02-18` (Comparator Update).
- **Weighting**: Metrics are scaled by `pLDDT / 100` to penalize disordered regions.
- **Classification Criteria**:
  - **Strong Evidence**: Anisotropy >= 3.0, pLDDT >= 70
  - **Exploratory**: Anisotropy >= 3.0, pLDDT < 70

## 2. LBX1 Comparator Analysis
Comparing LBX1 against known mechanosensors and high-anisotropy candidates.

| gene_symbol   |   anisotropy_index |   plddt_mean |   confidence_score |   weighted_anisotropy | classification                             |
|:--------------|-------------------:|-------------:|-------------------:|----------------------:|:-------------------------------------------|
| POC5          |              24.69 |        63.97 |               0.64 |                 15.79 | Exploratory (High Ani + Low Conf)          |
| LMNA          |               4.75 |        76.37 |               0.76 |                  3.63 | Strong Evidence (High Ani + High Conf)     |
| PIEZO2        |               4.44 |        79.44 |               0.79 |                  3.53 | Strong Evidence (High Ani + High Conf)     |
| GHR           |               5.13 |        58.70 |               0.59 |                  3.01 | Exploratory (High Ani + Low Conf)          |
| ADGRG6        |               3.06 |        73.73 |               0.74 |                  2.26 | Strong Evidence (High Ani + High Conf)     |
| LBX1          |               2.27 |        66.87 |               0.67 |                  1.52 | Ambiguous Scaffold (High Block + Low Conf) |
| RUNX3         |               2.06 |        60.56 |               0.61 |                  1.25 | Weak/Globular                              |

### LBX1 Status: Ambiguous Scaffold (High Block + Low Conf)
- Raw Anisotropy: 2.27 (Intermediate)
- Confidence: 66.9%
- Weighted Score: 1.52
- **Conclusion**: LBX1 does NOT meet the criteria for a 'Tension Rod' (Anisotropy > 3.0). Its structural evidence supports a modular/blocky role but confidence is low.

## 3. Top Ranked Candidates (Strong Evidence)
| gene_symbol   |   anisotropy_index |   plddt_mean |   confidence_score |   weighted_anisotropy | classification                         |
|:--------------|-------------------:|-------------:|-------------------:|----------------------:|:---------------------------------------|
| CDH23         |              11.93 |        76.73 |               0.77 |                  9.15 | Strong Evidence (High Ani + High Conf) |
| CNNM2         |               8.54 |        70.37 |               0.70 |                  6.01 | Strong Evidence (High Ani + High Conf) |
| FBLN5         |               7.05 |        83.34 |               0.83 |                  5.88 | Strong Evidence (High Ani + High Conf) |
| STOML3        |               5.56 |        84.33 |               0.84 |                  4.69 | Strong Evidence (High Ani + High Conf) |
| PANX3         |               5.08 |        81.72 |               0.82 |                  4.15 | Strong Evidence (High Ani + High Conf) |
| LMNA          |               4.75 |        76.37 |               0.76 |                  3.63 | Strong Evidence (High Ani + High Conf) |
| PIEZO2        |               4.44 |        79.44 |               0.79 |                  3.53 | Strong Evidence (High Ani + High Conf) |
| DSTYK         |               3.93 |        80.19 |               0.80 |                  3.15 | Strong Evidence (High Ani + High Conf) |
| PLOD1         |               3.40 |        92.73 |               0.93 |                  3.15 | Strong Evidence (High Ani + High Conf) |
| TGFBR1        |               3.65 |        84.19 |               0.84 |                  3.08 | Strong Evidence (High Ani + High Conf) |

## 4. Exploratory High-Anisotropy Signals
Candidates with extreme geometry but low confidence (potential IDRs or fibers).
| gene_symbol   |   anisotropy_index |   plddt_mean |   confidence_score |   weighted_anisotropy | classification                    |
|:--------------|-------------------:|-------------:|-------------------:|----------------------:|:----------------------------------|
| POC5          |              24.69 |        63.97 |               0.64 |                 15.79 | Exploratory (High Ani + Low Conf) |
| ETV1          |               5.32 |        67.89 |               0.68 |                  3.61 | Exploratory (High Ani + Low Conf) |
| GHR           |               5.13 |        58.70 |               0.59 |                  3.01 | Exploratory (High Ani + Low Conf) |
| EMD           |               4.29 |        60.25 |               0.60 |                  2.58 | Exploratory (High Ani + Low Conf) |
| MESP2         |               4.03 |        54.17 |               0.54 |                  2.18 | Exploratory (High Ani + Low Conf) |
| ARNTL         |               3.32 |        65.53 |               0.66 |                  2.18 | Exploratory (High Ani + Low Conf) |
| HIF1A         |               3.42 |        60.75 |               0.61 |                  2.08 | Exploratory (High Ani + Low Conf) |
| EGR3          |               3.76 |        49.97 |               0.50 |                  1.88 | Exploratory (High Ani + Low Conf) |
| ELN           |               4.42 |        35.84 |               0.36 |                  1.58 | Exploratory (High Ani + Low Conf) |