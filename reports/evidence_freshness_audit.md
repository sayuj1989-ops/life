# Evidence Freshness Audit Report

## 1. Run History & Output Integrity

| Date | Rows | Linked Images | Status |
|---|---|---|---|
| 2026-01-06 | 10 | 0 | ⚠️ Missing |
| 2026-01-07 | 9 | 0 | ⚠️ Missing |
| 2026-01-09 | 9 | 0 | ⚠️ Missing |
| 2026-01-14 | 9 | 0 | ⚠️ Missing |
| 2026-01-16 | 3 | 0 | ⚠️ Missing |
| 2026-01-18 | 9 | 0 | ⚠️ Missing |
| 2026-01-20 | 9 | 0 | ⚠️ Missing |
| 2026-01-21 | 9 | 25 | ✅ Present |
| 2026-01-27 | 9 | 0 | ⚠️ Missing |
| 2026-01-31 | 9 | 0 | ⚠️ Missing |
| 2026-02-05 | 9 | 0 | ⚠️ Missing |
| 2026-02-06 | 9 | 0 | ⚠️ Missing |
| 2026-02-07 | 9 | 0 | ⚠️ Missing |
| 2026-02-08 | 9 | 0 | ⚠️ Missing |
| 2026-02-09 | 10 | 0 | ⚠️ Missing |
| 2026-02-10 | 219 | 0 | ⚠️ Missing |
| 2026-02-11 | 10 | 0 | ⚠️ Missing |
| 2026-02-12 | 10 | 0 | ⚠️ Missing |
| 2026-02-13 | 48 | 0 | ⚠️ Missing |
| 2026-02-16 | 25 | 0 | ⚠️ Missing |
| 2026-02-17 | 10 | 0 | ⚠️ Missing |
| 2026-02-18 | 58 | 0 | ⚠️ Missing |
| 2026-02-20 | 10 | 0 | ⚠️ Missing |
| 2026-02-21 | 10 | 0 | ⚠️ Missing |
| 2026-02-22 | 10 | 0 | ⚠️ Missing |
| 2026-02-23 | 10 | 0 | ⚠️ Missing |
| manual_longevity | 2 | 0 | ⚠️ Missing |
| manual_metabolic_update | 6 | 0 | ⚠️ Missing |

## 2. Schema Drift Analysis

- Baseline (2026-01-06): 27 columns
- 2026-01-09: Drift detected.
  - Added: plddt_mean, anisotropy_index, backbone_principal_axis, PAE_domain_blockiness_score, plddt_fraction_ok, predicted_domain_segments, plddt_median, exposed_surface_proxy, plddt_fraction_low, disorder_fraction_proxy, likely_IDR_heavy, plddt_fraction_high, PAE_mean
  - Removed: anisotropy_ratio, pae_mean, fraction_low_plddt, lambda_mid, likely_idr_heavy, pae_blockiness, lambda_min, anisotropy, mean_plddt, disorder_fraction, lambda_max, exposed_fraction
- 2026-02-21: Drift detected.
  - Added: pLDDT_fraction_low, uniprot_id, length, species, pLDDT_mean, pLDDT_fraction_high
  - Removed: plddt_mean, dise_score, plddt_fraction_ok, plddt_median, uniprot, n_residues, plddt_fraction_low, source_category, plddt_fraction_high
- 2026-02-22: Drift detected.
  - Added: plddt_mean, organism, plddt_fraction_ok, plddt_median, n_residues, plddt_fraction_low, priority_score, plddt_fraction_high
  - Removed: pLDDT_fraction_low, length, species, pLDDT_mean, pLDDT_fraction_high
- manual_longevity: Drift detected.
  - Added: confidence_level, interpretation, uniprot, species
  - Removed: uniprot_id, priority_score, organism
- manual_metabolic_update: Drift detected.
  - Added: source_category, dise_score
  - Removed: confidence_level, interpretation, species

## 3. Data Freshness (Reuse Detection)

Analysis of identical per-gene values across multiple dates.

**Total Multi-Run Genes:** 71
**Static Genes (100% Identical Metrics):** 58
**Dynamic Genes (Changed Values):** 13

### Static Genes (Potential Cache Reuse)
| Gene | Run Count | Date Range |
|---|---|---|
| LBX1 | 21 | 2026-01-06 to 2026-02-22 |
| NTRK3 | 15 | 2026-01-27 to 2026-02-22 |
| RUNX3 | 13 | 2026-01-27 to 2026-02-18 |
| LMNA | 12 | 2026-01-14 to 2026-02-18 |
| NF1 | 11 | 2026-01-18 to 2026-02-18 |
| POC5 | 10 | 2026-01-06 to 2026-02-18 |
| OTOP1 | 9 | 2026-01-27 to 2026-02-18 |
| EGR3 | 9 | 2026-01-27 to 2026-02-18 |
| ITGB1 | 8 | 2026-01-07 to 2026-02-18 |
| IFT88 | 8 | 2026-01-14 to 2026-02-18 |
| PLOD1 | 6 | 2026-02-05 to 2026-02-18 |
| HIF1A | 5 | 2026-02-11 to 2026-02-23 |
| COL1A1 | 5 | 2026-01-18 to 2026-02-18 |
| WWTR1 | 5 | 2026-01-06 to 2026-02-13 |
| MESP2 | 4 | 2026-01-07 to 2026-02-16 |
| EMD | 4 | 2026-02-10 to 2026-02-18 |
| METTL3 | 4 | 2026-01-14 to 2026-02-18 |
| CEP290 | 4 | 2026-01-20 to 2026-02-18 |
| FLNA | 4 | 2026-01-20 to 2026-02-18 |
| FBN2 | 3 | 2026-02-10 to 2026-02-18 |
| ... (38 more) | ... | ... |

### Dynamic Genes (Value Updates)
| Gene | Run Count | Changes Detected |
|---|---|---|
| PIEZO2 | 21 | PAE_domain_blockiness_score |
| MYLK | 13 | anisotropy_index, PAE_domain_blockiness_score |
| IGF1R | 13 | anisotropy_index, PAE_domain_blockiness_score |
| GHR | 13 | anisotropy_index, PAE_domain_blockiness_score |
| DMD | 13 | anisotropy_index, PAE_domain_blockiness_score |
| ARNTL | 13 | anisotropy_index, PAE_domain_blockiness_score |
| PPARGC1A | 13 | anisotropy_index, PAE_domain_blockiness_score |
| PIEZO1 | 11 | PAE_domain_blockiness_score |
| YAP1 | 9 | PAE_domain_blockiness_score |
| DAG1 | 6 | anisotropy_index, PAE_domain_blockiness_score |
| ADGRG6 | 6 | anisotropy_index, plddt_mean, PAE_domain_blockiness_score |
| ALPL | 4 | anisotropy_index |
| ACVR1 | 4 | anisotropy_index, PAE_domain_blockiness_score |

## 4. Audit Conclusion
🟠 **WARNING**: Majority of data is static. Verify cache invalidation policies.
