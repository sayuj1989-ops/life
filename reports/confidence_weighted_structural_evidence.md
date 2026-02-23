# Confidence-Weighted Structural Evidence
**Source Data**: `outputs/afcc/current_metrics.csv`
**Date**: 2026-02-23

## Methodology
- **Confidence Score**: `(pLDDT_mean / 100) * (1 - pLDDT_frac_low)`
- **Tier 1 (High Confidence)**: Anisotropy >= 3.0, pLDDT >= 70, Low Confidence Fraction <= 0.3
- **Tier 2 (Artifact Risk)**: Anisotropy >= 3.0 but fails confidence checks.
- **Tier 3**: All other structures (Comparators, Globular, etc.)

## Tier 1: High Confidence
| Gene   |   Anisotropy |   Confidence_Score |   pLDDT_mean |   pLDDT_frac_low |   PAE_blockiness |
|:-------|-------------:|-------------------:|-------------:|-----------------:|-----------------:|
| PIEZO2 |         4.44 |              0.627 |         79.4 |             0.21 |             2.8  |
| PLOD1  |         3.4  |              0.881 |         92.7 |             0.05 |             2.31 |

## Tier 2: Artifact Risk
| Gene   |   Anisotropy |   Confidence_Score |   pLDDT_mean |   pLDDT_frac_low |   PAE_blockiness |
|:-------|-------------:|-------------------:|-------------:|-----------------:|-----------------:|
| GHR    |         5.13 |              0.194 |        58.7  |             0.67 |             5.31 |
| LMNA   |         4.75 |              0.527 |        76.4  |             0.31 |             2.56 |
| EGR3   |         3.76 |              0.125 |        50    |             0.75 |             0    |
| ARNTL  |         3.32 |              0.308 |        65.53 |             0.53 |             3.59 |

*Warning: High anisotropy in these structures may result from 'spaghetti' artifacts in disordered regions (Low pLDDT).*

## Tier 3: Comparators & Globular Structures (Top 10)
| Gene     |   Anisotropy |   Confidence_Score |   pLDDT_mean |   pLDDT_frac_low |   PAE_blockiness |
|:---------|-------------:|-------------------:|-------------:|-----------------:|-----------------:|
| LBX1     |         2.27 |              0.261 |        66.9  |             0.61 |             7.35 |
| PPARGC1A |         2.19 |              0.111 |        52.74 |             0.79 |             6.56 |
| RUNX3    |         2.06 |              0.194 |        60.6  |             0.68 |             0    |
| NTRK3    |         1.94 |              0.553 |        76.8  |             0.28 |             6.34 |
| NF1      |         1.93 |              0.776 |        87.2  |             0.11 |             2.42 |
| OTOP1    |         1.75 |              0.515 |        75.7  |             0.32 |             1.83 |
| MYLK     |         1.46 |              0.402 |        65.85 |             0.39 |             8.29 |
| IGF1R    |         1.43 |              0.585 |        78.02 |             0.25 |             5.85 |
| DMD      |         1.32 |              0.489 |        76.35 |             0.36 |             6.91 |

## Focused Analysis: LBX1 vs Mechanosensors
| Gene   | Tier                        |   Anisotropy |   Confidence_Score |   pLDDT_mean |   pLDDT_frac_low |   PAE_blockiness |
|:-------|:----------------------------|-------------:|-------------------:|-------------:|-----------------:|-----------------:|
| NF1    | Tier 3: Comparator/Globular |         1.93 |              0.776 |         87.2 |             0.11 |             2.42 |
| PIEZO2 | Tier 1: High Confidence     |         4.44 |              0.627 |         79.4 |             0.21 |             2.8  |
| LMNA   | Tier 2: Artifact Risk       |         4.75 |              0.527 |         76.4 |             0.31 |             2.56 |
| LBX1   | Tier 3: Comparator/Globular |         2.27 |              0.261 |         66.9 |             0.61 |             7.35 |
| RUNX3  | Tier 3: Comparator/Globular |         2.06 |              0.194 |         60.6 |             0.68 |             0    |
| GHR    | Tier 2: Artifact Risk       |         5.13 |              0.194 |         58.7 |             0.67 |             5.31 |

### LBX1 Structural Assessment
- **Confidence Score**: 0.261 (Low)
- **Structural State**: Tier 3: Comparator/Globular
- **Blockiness**: 7.35 (High blockiness suggests distinct domains separated by flexibility)

**Interpretation**: LBX1 fails the criteria for a 'rigid tension rod' (Tier 1). Its moderate anisotropy (2.27) combined with low confidence (pLDDT 66.9) and high blockiness suggests it is a **flexible, multi-domain protein with disordered linkers**. This structure is consistent with a dynamic transcriptional regulator that may use intrinsic disorder for promiscuous binding or phase separation, supporting the 'Disordered Mechanogating' hypothesis over a direct load-bearing role.