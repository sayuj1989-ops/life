# Evidence Freshness Audit

**Date:** 2026-04-04

## 1. Identical Per-Gene Vectors Across Runs
Many runs appear to simply reuse data from previous runs without computing new structure predictions, resulting in artificial inflation of report counts without new evidence.

- 2026-01-14 completely reuses values from 2026-01-09 for 5 overlapping genes
- 2026-01-16 completely reuses values from 2026-01-14 for 3 overlapping genes
- 2026-01-18 completely reuses values from 2026-01-16 for 2 overlapping genes
- 2026-01-20 completely reuses values from 2026-01-18 for 7 overlapping genes
- 2026-01-21 completely reuses values from 2026-01-20 for 6 overlapping genes
- 2026-01-27 completely reuses values from 2026-01-21 for 5 overlapping genes
- 2026-01-31 completely reuses values from 2026-01-27 for 9 overlapping genes
- 2026-02-05 completely reuses values from 2026-01-31 for 8 overlapping genes
- 2026-02-06 completely reuses values from 2026-02-05 for 9 overlapping genes
- 2026-02-07 completely reuses values from 2026-02-06 for 9 overlapping genes
- 2026-02-08 completely reuses values from 2026-02-07 for 7 overlapping genes
- 2026-02-09 completely reuses values from 2026-02-08 for 4 overlapping genes
- 2026-02-10 completely reuses values from 2026-02-09 for 10 overlapping genes
- 2026-02-11 completely reuses values from 2026-02-10 for 9 overlapping genes
- 2026-02-12 completely reuses values from 2026-02-11 for 10 overlapping genes
- 2026-02-13 completely reuses values from 2026-02-12 for 10 overlapping genes
- 2026-02-16 reuses values from 2026-02-13 for 10 out of 11 overlapping genes
- 2026-02-17 completely reuses values from 2026-02-16 for 6 overlapping genes
- 2026-02-18 completely reuses values from 2026-02-17 for 10 overlapping genes
- 2026-02-20 completely reuses values from 2026-02-18 for 10 overlapping genes
- 2026-02-23 completely reuses values from 2026-02-22 for 7 overlapping genes
- 2026-02-26 completely reuses values from 2026-02-23 for 3 overlapping genes
- 2026-02-28 completely reuses values from 2026-02-26 for 5 overlapping genes
- 2026-03-02 completely reuses values from 2026-02-28 for 6 overlapping genes
- 2026-03-04 completely reuses values from 2026-03-02 for 6 overlapping genes
- 2026-03-05 completely reuses values from 2026-03-04 for 6 overlapping genes

## 2. Missing Linked Outputs
- Missing summary.md for run 2026-02-16
- Missing summary.md for run FOXO3
- Missing summary.md for run KLOTHO
- Missing summary.md for run YAP1
- Missing summary.md for run manual_longevity
- Missing summary.md for run manual_longevity_yap1
- Missing summary.md for run manual_metabolic_update

## 3. Schema Drifts
- Run 2026-01-09:
  - Added: disorder_fraction_proxy, PAE_domain_blockiness_score, backbone_principal_axis, exposed_surface_proxy, plddt_median, plddt_fraction_low, predicted_domain_segments, plddt_mean, PAE_mean, anisotropy_index, plddt_fraction_high, likely_IDR_heavy, plddt_fraction_ok
  - Removed: anisotropy, pae_mean, lambda_min, pae_blockiness, mean_plddt, fraction_low_plddt, anisotropy_ratio, lambda_mid, exposed_fraction, lambda_max, likely_idr_heavy, disorder_fraction
- Run 2026-02-21:
  - Added: uniprot_id, length, pLDDT_fraction_low, species, pLDDT_fraction_high, pLDDT_mean
  - Removed: n_residues, plddt_median, source_category, plddt_fraction_low, plddt_mean, dise_score, plddt_fraction_ok, plddt_fraction_high, uniprot
- Run 2026-02-22:
  - Added: n_residues, plddt_median, plddt_fraction_low, priority_score, plddt_mean, plddt_fraction_ok, plddt_fraction_high, organism
  - Removed: length, pLDDT_fraction_low, species, pLDDT_fraction_high, pLDDT_mean
- Run 2026-02-28:
  - Added: source_category, dise_score, uniprot
  - Removed: uniprot_id, organism, priority_score
- Run 2026-03-02:
  - Added: uniprot_id, organism, priority_score
  - Removed: source_category, dise_score, uniprot
- Run FOXO3:
  - Removed: organism, priority_score
- Run manual_longevity:
  - Added: interpretation, species, uniprot, confidence_level
  - Removed: uniprot_id
- Run manual_metabolic_update:
  - Added: source_category, dise_score
  - Removed: interpretation, species, confidence_level
