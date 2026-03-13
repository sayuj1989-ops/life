# Evidence Freshness Audit

## Overview
Analyzed 31 runs from 2026-01-06 to 2026-03-05.

## Schema Drifts
The following runs exhibited schema deviations from the canonical (first observed) structure:
- **2026-01-09**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-01-14**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-01-16**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-01-18**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-01-20**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-01-21**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-01-27**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-01-31**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-05**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-06**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-07**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-08**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-09**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-10**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-11**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-12**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-13**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-16**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-17**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-18**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-20**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-02-21**: Missing ['lambda_max', 'n_residues', 'anisotropy_ratio', 'pae_mean', 'source_category', 'uniprot', 'dise_score', 'mean_plddt', 'anisotropy', 'disorder_fraction', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'length', 'PAE_mean', 'disorder_fraction_proxy', 'predicted_domain_segments', 'PAE_domain_blockiness_score', 'species', 'exposed_surface_proxy', 'uniprot_id', 'pLDDT_fraction_low', 'backbone_principal_axis', 'pLDDT_mean', 'anisotropy_index', 'pLDDT_fraction_high']
- **2026-02-22**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'source_category', 'uniprot', 'dise_score', 'mean_plddt', 'anisotropy', 'disorder_fraction', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'priority_score', 'plddt_median', 'plddt_fraction_low', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'plddt_fraction_high', 'exposed_surface_proxy', 'uniprot_id', 'backbone_principal_axis', 'organism', 'anisotropy_index']
- **2026-02-23**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'source_category', 'uniprot', 'dise_score', 'mean_plddt', 'anisotropy', 'disorder_fraction', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'priority_score', 'plddt_median', 'plddt_fraction_low', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'plddt_fraction_high', 'exposed_surface_proxy', 'uniprot_id', 'backbone_principal_axis', 'organism', 'anisotropy_index']
- **2026-02-26**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'source_category', 'uniprot', 'dise_score', 'mean_plddt', 'anisotropy', 'disorder_fraction', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'priority_score', 'plddt_median', 'plddt_fraction_low', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'plddt_fraction_high', 'exposed_surface_proxy', 'uniprot_id', 'backbone_principal_axis', 'organism', 'anisotropy_index']
- **2026-02-28**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'mean_plddt', 'disorder_fraction', 'anisotropy', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'plddt_fraction_low', 'plddt_median', 'plddt_fraction_high', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'exposed_surface_proxy', 'backbone_principal_axis', 'anisotropy_index']
- **2026-03-02**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'source_category', 'uniprot', 'dise_score', 'mean_plddt', 'anisotropy', 'disorder_fraction', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'priority_score', 'plddt_median', 'plddt_fraction_low', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'plddt_fraction_high', 'exposed_surface_proxy', 'uniprot_id', 'backbone_principal_axis', 'organism', 'anisotropy_index']
- **2026-03-04**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'source_category', 'uniprot', 'dise_score', 'mean_plddt', 'anisotropy', 'disorder_fraction', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'priority_score', 'plddt_median', 'plddt_fraction_low', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'plddt_fraction_high', 'exposed_surface_proxy', 'uniprot_id', 'backbone_principal_axis', 'organism', 'anisotropy_index']
- **2026-03-05**: Missing ['lambda_max', 'pae_mean', 'anisotropy_ratio', 'source_category', 'uniprot', 'dise_score', 'mean_plddt', 'anisotropy', 'disorder_fraction', 'lambda_mid', 'fraction_low_plddt', 'likely_idr_heavy', 'pae_blockiness', 'lambda_min', 'exposed_fraction'], Extra ['likely_IDR_heavy', 'PAE_mean', 'plddt_mean', 'disorder_fraction_proxy', 'priority_score', 'plddt_median', 'plddt_fraction_low', 'predicted_domain_segments', 'plddt_fraction_ok', 'PAE_domain_blockiness_score', 'plddt_fraction_high', 'exposed_surface_proxy', 'uniprot_id', 'backbone_principal_axis', 'organism', 'anisotropy_index']

## Missing Linked Outputs
The following runs have missing linked outputs (e.g., PDB files not matching metrics count):
- **2026-01-06**: No 'pdb' directory found, but metrics exist.
- **2026-01-07**: No 'pdb' directory found, but metrics exist.
- **2026-01-09**: No 'pdb' directory found, but metrics exist.
- **2026-01-14**: No 'pdb' directory found, but metrics exist.
- **2026-01-16**: No 'pdb' directory found, but metrics exist.
- **2026-01-18**: No 'pdb' directory found, but metrics exist.
- **2026-01-20**: No 'pdb' directory found, but metrics exist.
- **2026-01-21**: No 'pdb' directory found, but metrics exist.
- **2026-01-27**: No 'pdb' directory found, but metrics exist.
- **2026-01-31**: No 'pdb' directory found, but metrics exist.
- **2026-02-05**: No 'pdb' directory found, but metrics exist.
- **2026-02-06**: No 'pdb' directory found, but metrics exist.
- **2026-02-07**: No 'pdb' directory found, but metrics exist.
- **2026-02-08**: No 'pdb' directory found, but metrics exist.
- **2026-02-09**: No 'pdb' directory found, but metrics exist.
- **2026-02-10**: No 'pdb' directory found, but metrics exist.
- **2026-02-11**: No 'pdb' directory found, but metrics exist.
- **2026-02-12**: No 'pdb' directory found, but metrics exist.
- **2026-02-13**: No 'pdb' directory found, but metrics exist.
- **2026-02-16**: No 'pdb' directory found, but metrics exist.
- **2026-02-17**: No 'pdb' directory found, but metrics exist.
- **2026-02-18**: No 'pdb' directory found, but metrics exist.
- **2026-02-20**: No 'pdb' directory found, but metrics exist.
- **2026-02-21**: No 'pdb' directory found, but metrics exist.
- **2026-02-22**: No 'pdb' directory found, but metrics exist.
- **2026-02-23**: No 'pdb' directory found, but metrics exist.
- **2026-02-26**: No 'pdb' directory found, but metrics exist.
- **2026-02-28**: No 'pdb' directory found, but metrics exist.
- **2026-03-02**: No 'pdb' directory found, but metrics exist.
- **2026-03-04**: No 'pdb' directory found, but metrics exist.
- **2026-03-05**: No 'pdb' directory found, but metrics exist.

## Static Metrics Warning
The following proteins show identical structural metrics across multiple historical runs, indicating the underlying AFDB structures have not been updated or are being reused from cache:

| gene_symbol   |   appearances | first_seen   | last_seen   |   anisotropy |    plddt |
|:--------------|--------------:|:-------------|:------------|-------------:|---------:|
| PIEZO2        |            23 | 2026-01-06   | 2026-02-28  |    nan       | nan      |
| LBX1          |            22 | 2026-01-06   | 2026-02-28  |    nan       | nan      |
| NTRK3         |            18 | 2026-01-27   | 2026-03-05  |      1.93611 |  76.8156 |
| RUNX3         |            14 | 2026-01-27   | 2026-03-05  |      2.06117 |  60.5641 |
| LMNA          |            13 | 2026-01-14   | 2026-02-26  |      4.75167 |  76.3707 |
| NF1           |            12 | 2026-01-18   | 2026-02-26  |      1.92793 |  87.1726 |
| PIEZO1        |            11 | 2026-01-14   | 2026-02-18  |      3.89626 |  72.0459 |
| EGR3          |            10 | 2026-01-27   | 2026-02-26  |      3.76207 |  49.9687 |
| OTOP1         |            10 | 2026-01-27   | 2026-02-26  |      1.75071 |  75.6892 |
| POC5          |            10 | 2026-01-06   | 2026-02-18  |    nan       | nan      |
| YAP1          |             9 | 2026-01-06   | 2026-02-18  |    nan       | nan      |
| ITGB1         |             8 | 2026-01-07   | 2026-02-18  |    nan       | nan      |
| IFT88         |             8 | 2026-01-14   | 2026-02-18  |      2.80324 |  76.346  |
| PLOD1         |             7 | 2026-02-05   | 2026-02-26  |      3.39508 |  92.7287 |
| COL1A1        |             5 | 2026-01-18   | 2026-02-18  |      2.79703 |  52.73   |
| WWTR1         |             5 | 2026-01-06   | 2026-02-13  |    nan       | nan      |
| HIF1A         |             5 | 2026-02-11   | 2026-02-23  |      3.41705 |  60.7517 |
| FLNA          |             4 | 2026-01-20   | 2026-02-18  |      2.5017  |  76.5462 |
| CEP290        |             4 | 2026-01-20   | 2026-02-18  |      2.28612 |  60.5448 |
| METTL3        |             4 | 2026-01-14   | 2026-02-18  |      1.64864 |  75.379  |
| MESP2         |             4 | 2026-01-07   | 2026-02-16  |    nan       | nan      |
| EMD           |             4 | 2026-02-10   | 2026-02-18  |      4.28851 |  60.2506 |
| BNC2          |             3 | 2026-02-10   | 2026-02-18  |      1.9551  |  53.4976 |
| FBN2          |             3 | 2026-02-10   | 2026-02-18  |      1.49437 |  68.3904 |
| ROR2          |             3 | 2026-02-10   | 2026-02-18  |      2.51146 |  68.2868 |
| FERMT2        |             3 | 2026-02-10   | 2026-02-18  |      2.50265 |  79.8682 |
| TGFBR1        |             3 | 2026-02-10   | 2026-02-18  |      3.65434 |  84.1943 |
| SERPINH1      |             3 | 2026-02-10   | 2026-02-18  |      1.97467 |  91.136  |
| ETV1          |             3 | 2026-02-10   | 2026-02-18  |      5.32307 |  67.8918 |
| CDH23         |             3 | 2026-02-10   | 2026-02-18  |     11.9278  |  76.7295 |
| TGFBR2        |             3 | 2026-02-10   | 2026-02-18  |      2.48188 |  80.9814 |
| FLNB          |             3 | 2026-01-07   | 2026-02-10  |    nan       | nan      |
| MYO7A         |             3 | 2026-02-10   | 2026-02-18  |      2.33982 |  77.2778 |
| ROCK1         |             2 | 2026-02-10   | 2026-02-16  |      3.29219 |  76.1342 |
| SSPOP         |             2 | 2026-02-10   | 2026-02-16  |      1.91535 |  60.1306 |
| STOML3        |             2 | 2026-02-10   | 2026-02-16  |      5.55983 |  84.3263 |
| PANX3         |             2 | 2026-02-10   | 2026-02-16  |      5.07536 |  81.7247 |
| GDF5          |             2 | 2026-02-10   | 2026-02-16  |      2.96967 |  69.9849 |
| CNNM2         |             2 | 2026-02-10   | 2026-02-16  |      8.54054 |  70.373  |
| AQP4          |             2 | 2026-02-10   | 2026-02-16  |      1.96911 |  81.037  |
| FBLN5         |             2 | 2026-02-10   | 2026-02-16  |      7.05448 |  83.3381 |
| TBX6          |             2 | 2026-01-06   | 2026-02-10  |    nan       | nan      |
| NR1D1         |             2 | 2026-02-13   | 2026-02-18  |      1.79687 |  62.8854 |
| TEAD1         |             2 | 2026-02-13   | 2026-02-18  |      1.90672 |  76.4766 |
| CLOCK         |             2 | 2026-02-13   | 2026-02-18  |      1.82681 |  60.6055 |
| COL11A2       |             2 | 2026-02-10   | 2026-02-16  |      2.46068 |  49.265  |
| VANGL1        |             2 | 2026-01-06   | 2026-02-10  |    nan       | nan      |
| TLN1          |             2 | 2026-02-10   | 2026-02-13  |      2.04382 |  75.887  |
| SUN1          |             2 | 2026-02-10   | 2026-02-18  |      2.33785 |  60.3609 |
| RPL38         |             2 | 2026-02-10   | 2026-02-18  |      1.51515 |  95.3476 |
| DZIP1         |             2 | 2026-02-10   | 2026-02-16  |      2.54368 |  64.3541 |
| SYNE2         |             2 | 2026-02-10   | 2026-02-18  |      2.1236  |  83.3273 |
| KIF3A         |             2 | 2026-02-10   | 2026-02-13  |      2.90363 |  75.4491 |
| KIF7          |             2 | 2026-02-10   | 2026-02-13  |      2.10885 |  67.1604 |
| CCDC40        |             2 | 2026-02-10   | 2026-02-13  |      5.69949 |  70.7318 |
| ACAN          |             2 | 2026-02-10   | 2026-02-13  |      2.66304 |  51.891  |
| SMAD3         |             2 | 2026-02-10   | 2026-02-13  |      2.40593 |  83.6137 |
| PTK7          |             2 | 2026-01-06   | 2026-02-10  |    nan       | nan      |
| COL2A1        |             2 | 2026-01-06   | 2026-02-10  |    nan       | nan      |
| COL1A2        |             2 | 2026-02-13   | 2026-02-18  |      2.87618 |  53.6408 |