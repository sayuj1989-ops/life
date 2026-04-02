# Evidence Freshness and Integrity Audit

## 1. Reused Metrics Analysis
This section flags when 'new' reports reuse unchanged per-gene vectors from previous runs.

| Gene | Total Runs | Unique Anisotropy | Unique pLDDT | Status |
|------|------------|-------------------|--------------|--------|
| ACAN | 2 | 1 | 1 | STATIC REUSE |
| ACVR1 | 4 | 2 | 1 | UPDATED |
| ADGRG6 | 6 | 2 | 2 | UPDATED |
| ALPL | 4 | 2 | 1 | UPDATED |
| AQP4 | 2 | 1 | 1 | STATIC REUSE |
| ARNTL | 17 | 2 | 1 | UPDATED |
| BNC2 | 3 | 1 | 1 | STATIC REUSE |
| CCDC40 | 2 | 1 | 1 | STATIC REUSE |
| CCDC57 | 3 | 2 | 1 | UPDATED |
| CDH23 | 3 | 1 | 1 | STATIC REUSE |
| CEP290 | 4 | 1 | 1 | STATIC REUSE |
| CLOCK | 2 | 1 | 1 | STATIC REUSE |
| CNNM2 | 2 | 1 | 1 | STATIC REUSE |
| COL11A2 | 2 | 1 | 1 | STATIC REUSE |
| COL1A1 | 5 | 1 | 1 | STATIC REUSE |
| COL1A2 | 2 | 1 | 1 | STATIC REUSE |
| COL2A1 | 2 | 1 | 1 | STATIC REUSE |
| DAG1 | 8 | 2 | 1 | UPDATED |
| DMD | 17 | 2 | 1 | UPDATED |
| DZIP1 | 2 | 1 | 1 | STATIC REUSE |
| EGR3 | 10 | 1 | 1 | STATIC REUSE |
| EMD | 4 | 1 | 1 | STATIC REUSE |
| ETV1 | 3 | 1 | 1 | STATIC REUSE |
| FBLN5 | 2 | 1 | 1 | STATIC REUSE |
| FBN2 | 3 | 1 | 1 | STATIC REUSE |
| FERMT2 | 3 | 1 | 1 | STATIC REUSE |
| FLNA | 4 | 1 | 1 | STATIC REUSE |
| FLNB | 3 | 1 | 1 | STATIC REUSE |
| GDF5 | 2 | 1 | 1 | STATIC REUSE |
| GHR | 17 | 2 | 1 | UPDATED |
| HIF1A | 5 | 1 | 1 | STATIC REUSE |
| IFT88 | 8 | 1 | 1 | STATIC REUSE |
| IGF1R | 16 | 2 | 1 | UPDATED |
| ITGB1 | 8 | 1 | 1 | STATIC REUSE |
| JAG1 | 2 | 2 | 1 | UPDATED |
| KIF3A | 2 | 1 | 1 | STATIC REUSE |
| KIF7 | 2 | 1 | 1 | STATIC REUSE |
| LBX1 | 22 | 1 | 1 | STATIC REUSE |
| LMNA | 13 | 1 | 1 | STATIC REUSE |
| MESP2 | 4 | 1 | 1 | STATIC REUSE |
| METTL3 | 4 | 1 | 1 | STATIC REUSE |
| MYLK | 16 | 2 | 1 | UPDATED |
| MYO7A | 3 | 1 | 1 | STATIC REUSE |
| NF1 | 12 | 1 | 1 | STATIC REUSE |
| NR1D1 | 2 | 1 | 1 | STATIC REUSE |
| NTRK3 | 18 | 1 | 1 | STATIC REUSE |
| OTOP1 | 10 | 1 | 1 | STATIC REUSE |
| PANX3 | 2 | 1 | 1 | STATIC REUSE |
| PIEZO1 | 11 | 1 | 1 | STATIC REUSE |
| PIEZO2 | 23 | 1 | 1 | STATIC REUSE |
| PLOD1 | 7 | 1 | 1 | STATIC REUSE |
| POC5 | 10 | 1 | 1 | STATIC REUSE |
| PPARGC1A | 16 | 2 | 1 | UPDATED |
| PTK7 | 2 | 1 | 1 | STATIC REUSE |
| ROCK1 | 2 | 1 | 1 | STATIC REUSE |
| ROR2 | 3 | 1 | 1 | STATIC REUSE |
| RPL38 | 2 | 1 | 1 | STATIC REUSE |
| RUNX3 | 14 | 1 | 1 | STATIC REUSE |
| SERPINH1 | 3 | 1 | 1 | STATIC REUSE |
| SMAD3 | 2 | 1 | 1 | STATIC REUSE |
| SSPOP | 2 | 1 | 1 | STATIC REUSE |
| STOML3 | 2 | 1 | 1 | STATIC REUSE |
| SUN1 | 2 | 1 | 1 | STATIC REUSE |
| SYNE2 | 2 | 1 | 1 | STATIC REUSE |
| TBX6 | 2 | 1 | 1 | STATIC REUSE |
| TEAD1 | 2 | 1 | 1 | STATIC REUSE |
| TGFBR1 | 3 | 1 | 1 | STATIC REUSE |
| TGFBR2 | 3 | 1 | 1 | STATIC REUSE |
| TLN1 | 2 | 1 | 1 | STATIC REUSE |
| VANGL1 | 2 | 1 | 1 | STATIC REUSE |
| WWTR1 | 5 | 1 | 1 | STATIC REUSE |
| YAP1 | 9 | 1 | 1 | STATIC REUSE |

**Summary:** Out of genes tracked across multiple runs, 60 are completely static across key metrics, and 12 have been updated.

## 2. Missing Linked Outputs
Flagging runs where expected outputs are missing.

| Run Date | Missing summary.md | Missing failure.md |
|----------|--------------------|--------------------|
| 2026-01-06 | False | True |
| 2026-01-07 | False | True |
| 2026-01-09 | False | True |
| 2026-01-14 | False | True |
| 2026-01-20 | False | True |
| 2026-01-21 | False | True |
| 2026-01-27 | False | True |
| 2026-01-31 | False | True |
| 2026-02-05 | False | True |
| 2026-02-07 | False | True |
| 2026-02-08 | False | True |
| 2026-02-09 | False | True |
| 2026-02-10 | False | True |
| 2026-02-11 | False | True |
| 2026-02-12 | False | True |
| 2026-02-13 | False | True |
| 2026-02-16 | True | True |
| 2026-02-17 | False | True |
| 2026-02-18 | False | True |
| 2026-02-20 | False | True |
| 2026-02-21 | False | True |
| 2026-02-22 | False | True |
| 2026-02-23 | False | True |
| 2026-02-26 | False | True |
| 2026-02-28 | False | True |
| 2026-03-02 | False | True |
| 2026-03-04 | False | True |
| 2026-03-05 | False | True |

## 3. Schema Drift
Analyzing differences in columns across run dates.

- **2026-01-09 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, plddt_fraction_ok, anisotropy_index, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-01-14 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-01-16 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-01-18 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-01-20 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-01-21 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-01-27 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-01-31 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-05 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-06 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-07 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-08 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-09 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-10 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-11 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-12 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-13 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-16 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-17 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-18 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-20 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-21 Drift:** Missing base columns (dise_score, likely_idr_heavy, pae_blockiness, uniprot, disorder_fraction, lambda_mid, lambda_max, source_category, n_residues, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (uniprot_id, pLDDT_fraction_low, likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, species, predicted_domain_segments, pLDDT_mean, backbone_principal_axis, exposed_surface_proxy, anisotropy_index, length, pLDDT_fraction_high, disorder_fraction_proxy).
- **2026-02-22 Drift:** Missing base columns (dise_score, likely_idr_heavy, pae_blockiness, uniprot, disorder_fraction, lambda_mid, lambda_max, source_category, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (organism, uniprot_id, likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, anisotropy_index, plddt_fraction_ok, priority_score, plddt_mean, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-23 Drift:** Missing base columns (dise_score, likely_idr_heavy, pae_blockiness, uniprot, disorder_fraction, lambda_mid, lambda_max, source_category, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (organism, uniprot_id, likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, anisotropy_index, plddt_fraction_ok, priority_score, plddt_mean, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-26 Drift:** Missing base columns (dise_score, likely_idr_heavy, pae_blockiness, uniprot, disorder_fraction, lambda_mid, lambda_max, source_category, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (organism, uniprot_id, likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, anisotropy_index, plddt_fraction_ok, priority_score, plddt_mean, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-02-28 Drift:** Missing base columns (pae_blockiness, likely_idr_heavy, lambda_mid, disorder_fraction, lambda_max, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, plddt_mean, anisotropy_index, plddt_fraction_ok, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-03-02 Drift:** Missing base columns (dise_score, likely_idr_heavy, pae_blockiness, uniprot, disorder_fraction, lambda_mid, lambda_max, source_category, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (organism, uniprot_id, likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, anisotropy_index, plddt_fraction_ok, priority_score, plddt_mean, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-03-04 Drift:** Missing base columns (dise_score, likely_idr_heavy, pae_blockiness, uniprot, disorder_fraction, lambda_mid, lambda_max, source_category, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (organism, uniprot_id, likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, anisotropy_index, plddt_fraction_ok, priority_score, plddt_mean, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
- **2026-03-05 Drift:** Missing base columns (dise_score, likely_idr_heavy, pae_blockiness, uniprot, disorder_fraction, lambda_mid, lambda_max, source_category, exposed_fraction, lambda_min, mean_plddt, pae_mean, anisotropy, anisotropy_ratio, fraction_low_plddt). Extra columns added (organism, uniprot_id, likely_IDR_heavy, PAE_domain_blockiness_score, PAE_mean, predicted_domain_segments, plddt_median, backbone_principal_axis, exposed_surface_proxy, anisotropy_index, plddt_fraction_ok, priority_score, plddt_mean, plddt_fraction_high, disorder_fraction_proxy, plddt_fraction_low).
