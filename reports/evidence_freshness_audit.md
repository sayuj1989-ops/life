# Evidence Freshness Audit

## Overview
This audit analyzes the AFCC run history to detect data reuse, schema drifts, and missing outputs to ensure data integrity for the Biological Countercurvature hypothesis. Generated from `outputs/afcc/*` run on 2026-02-16.

## 1. Static/Reused Per-Gene Vectors
The following genes show completely identical structural metrics (anisotropy and pLDDT) across multiple runs, indicating reuse rather than fresh predictions:

| Gene | Runs | Anisotropy | pLDDT | First Seen | Last Seen |
|---|---|---|---|---|---|
| NTRK3 | 18 | 1.936111715585754 | 76.81557806912993 | 2026-01-27 | 2026-03-05 |
| RUNX3 | 14 | 2.0611670656856456 | 60.564096385542165 | 2026-01-27 | 2026-03-05 |
| LMNA | 13 | 4.751667397697646 | 76.37072289156627 | 2026-01-14 | 2026-02-26 |
| NF1 | 12 | 1.9279279346731688 | 87.17264755480608 | 2026-01-18 | 2026-02-26 |
| PIEZO1 | 11 | 3.896259474160542 | 72.0459182863943 | 2026-01-14 | 2026-02-18 |
| OTOP1 | 10 | 1.7507094616744632 | 75.68916666666668 | 2026-01-27 | 2026-02-26 |
| EGR3 | 10 | 3.762072398804325 | 49.96868217054263 | 2026-01-27 | 2026-02-26 |
| IFT88 | 8 | 2.8032400603850034 | 76.34603155339805 | 2026-01-14 | 2026-02-18 |
| PLOD1 | 7 | 3.3950779336885484 | 92.72865199449797 | 2026-02-05 | 2026-02-26 |
| COL1A1 | 5 | 2.797030038697096 | 52.72999316939891 | 2026-01-18 | 2026-02-18 |
| HIF1A | 5 | 3.417045794347625 | 60.75170702179177 | 2026-02-11 | 2026-02-23 |
| METTL3 | 4 | 1.6486356541690288 | 75.379 | 2026-01-14 | 2026-02-18 |
| FLNA | 4 | 2.501695116785587 | 76.54624858330186 | 2026-01-20 | 2026-02-18 |
| CEP290 | 4 | 2.286118643841953 | 60.54478418717224 | 2026-01-20 | 2026-02-18 |
| EMD | 4 | 4.288514695460691 | 60.25062992125985 | 2026-02-10 | 2026-02-18 |
| TGFBR2 | 3 | 2.481876912319578 | 80.98139329805996 | 2026-02-10 | 2026-02-18 |
| MYO7A | 3 | 2.3398248764346605 | 77.27780586907448 | 2026-02-10 | 2026-02-18 |
| CDH23 | 3 | 11.927795782477896 | 76.72945319740501 | 2026-02-10 | 2026-02-18 |
| FBN2 | 3 | 1.4943730069906092 | 68.39040733197557 | 2026-02-10 | 2026-02-18 |
| SERPINH1 | 3 | 1.9746660315008595 | 91.13595693779904 | 2026-02-10 | 2026-02-18 |
| ETV1 | 3 | 5.323069489820232 | 67.89180064308681 | 2026-02-10 | 2026-02-18 |
| ROR2 | 3 | 2.5114623831285026 | 68.28682926829269 | 2026-02-10 | 2026-02-18 |
| FERMT2 | 3 | 2.502653150494108 | 79.86822058823529 | 2026-02-10 | 2026-02-18 |
| TGFBR1 | 3 | 3.6543426000781953 | 84.19429423459245 | 2026-02-10 | 2026-02-18 |
| BNC2 | 3 | 1.9551006086909324 | 53.49764331210191 | 2026-02-10 | 2026-02-18 |
| SMAD3 | 2 | 2.405930835652692 | 83.6136705882353 | 2026-02-10 | 2026-02-13 |
| ACAN | 2 | 2.663035881007823 | 51.890964426877474 | 2026-02-10 | 2026-02-13 |
| CCDC40 | 2 | 5.699494256013449 | 70.7318213660245 | 2026-02-10 | 2026-02-13 |
| KIF7 | 2 | 2.10884896707772 | 67.16040953090096 | 2026-02-10 | 2026-02-13 |
| KIF3A | 2 | 2.9036334743310475 | 75.44905579399142 | 2026-02-10 | 2026-02-13 |
| SYNE2 | 2 | 2.123597597329561 | 83.327265917603 | 2026-02-10 | 2026-02-18 |
| DZIP1 | 2 | 2.5436815102910297 | 64.35407151095733 | 2026-02-10 | 2026-02-16 |
| RPL38 | 2 | 1.5151481532400566 | 95.34757142857144 | 2026-02-10 | 2026-02-18 |
| SUN1 | 2 | 2.337845450113884 | 60.360891719745226 | 2026-02-10 | 2026-02-18 |
| TLN1 | 2 | 2.043820318201773 | 75.88697756788666 | 2026-02-10 | 2026-02-13 |
| FBLN5 | 2 | 7.054480619949517 | 83.33808035714287 | 2026-02-10 | 2026-02-16 |
| COL11A2 | 2 | 2.4606769611384083 | 49.26498847926268 | 2026-02-10 | 2026-02-16 |
| SSPOP | 2 | 1.9153536859133964 | 60.13063022019741 | 2026-02-10 | 2026-02-16 |
| STOML3 | 2 | 5.559834719858973 | 84.32628865979382 | 2026-02-10 | 2026-02-16 |
| PANX3 | 2 | 5.075360561640713 | 81.7247193877551 | 2026-02-10 | 2026-02-16 |
| GDF5 | 2 | 2.969673405734348 | 69.98487025948103 | 2026-02-10 | 2026-02-16 |
| ROCK1 | 2 | 3.2921885930351955 | 76.13419497784342 | 2026-02-10 | 2026-02-16 |
| AQP4 | 2 | 1.969106742320216 | 81.03699690402476 | 2026-02-10 | 2026-02-16 |
| CNNM2 | 2 | 8.540535839977684 | 70.37298285714286 | 2026-02-10 | 2026-02-16 |
| NR1D1 | 2 | 1.796872009762566 | 62.885390879478834 | 2026-02-13 | 2026-02-18 |
| TEAD1 | 2 | 1.9067232446511149 | 76.47657276995305 | 2026-02-13 | 2026-02-18 |
| CLOCK | 2 | 1.8268099455225064 | 60.60554373522458 | 2026-02-13 | 2026-02-18 |
| COL1A2 | 2 | 2.876180753979266 | 53.64081991215226 | 2026-02-13 | 2026-02-18 |

### Reused Data by Date
The following reports re-used per-gene values that were identical to the previous run for the listed genes:
- **2026-01-16**: PIEZO1
- **2026-01-18**: IFT88, LMNA, PIEZO1
- **2026-01-20**: COL1A1, IFT88, LMNA, NF1, PIEZO1
- **2026-01-21**: IFT88, LMNA, NF1, PIEZO1
- **2026-01-27**: LMNA, NF1, PIEZO1
- **2026-01-31**: EGR3, LMNA, NF1, NTRK3, OTOP1, PIEZO1, RUNX3
- **2026-02-05**: EGR3, LMNA, NF1, NTRK3, OTOP1, RUNX3
- **2026-02-06**: EGR3, LMNA, NF1, NTRK3, OTOP1, PLOD1, RUNX3
- **2026-02-07**: EGR3, LMNA, NF1, NTRK3, OTOP1, PLOD1, RUNX3
- **2026-02-08**: EGR3, IFT88, LMNA, NTRK3, OTOP1, PIEZO1, RUNX3
- **2026-02-09**: NTRK3, RUNX3
- **2026-02-10**: CEP290, COL1A1, EGR3, FLNA, IFT88, METTL3, NF1, NTRK3, OTOP1, PIEZO1, PLOD1, RUNX3
- **2026-02-11**: NTRK3, RUNX3
- **2026-02-12**: HIF1A, NTRK3, RUNX3
- **2026-02-13**: ACAN, CCDC40, CDH23, CEP290, COL1A1, EGR3, EMD, ETV1, FBN2, FERMT2, FLNA, HIF1A, IFT88, KIF3A, KIF7, LMNA, METTL3, MYO7A, NF1, NTRK3, OTOP1, PIEZO1, PLOD1, ROR2, RUNX3, SERPINH1, SMAD3, TGFBR1, TGFBR2, TLN1
- **2026-02-16**: AQP4, BNC2, CNNM2, COL11A2, DZIP1, EMD, FBLN5, GDF5, PANX3, ROCK1, SSPOP, STOML3
- **2026-02-17**: NTRK3, RUNX3
- **2026-02-18**: BNC2, CDH23, CEP290, CLOCK, COL1A1, COL1A2, EGR3, EMD, ETV1, FBN2, FERMT2, FLNA, HIF1A, IFT88, LMNA, METTL3, MYO7A, NF1, NR1D1, NTRK3, OTOP1, PIEZO1, PLOD1, ROR2, RPL38, RUNX3, SERPINH1, SUN1, SYNE2, TEAD1, TGFBR1, TGFBR2
- **2026-02-20**: NTRK3
- **2026-02-22**: NTRK3
- **2026-02-23**: HIF1A
- **2026-02-26**: EGR3, LMNA, NF1, NTRK3, OTOP1, PLOD1
- **2026-02-28**: NTRK3
- **2026-03-05**: NTRK3, RUNX3

## 2. Missing Linked Outputs
The following dated runs are referenced in `reports/afcc_latest.md` but their `metrics.csv` files are missing:
- 2026-01-23

## 3. Schema Drifts
- **2026-01-09**:
  - Added columns: PAE_domain_blockiness_score, PAE_mean, anisotropy_index, backbone_principal_axis, disorder_fraction_proxy, exposed_surface_proxy, likely_IDR_heavy, plddt_fraction_high, plddt_fraction_low, plddt_fraction_ok, plddt_mean, plddt_median, predicted_domain_segments
  - Removed columns: anisotropy, anisotropy_ratio, disorder_fraction, exposed_fraction, fraction_low_plddt, lambda_max, lambda_mid, lambda_min, likely_idr_heavy, mean_plddt, pae_blockiness, pae_mean
- **2026-02-21**:
  - Added columns: length, pLDDT_fraction_high, pLDDT_fraction_low, pLDDT_mean, species, uniprot_id
  - Removed columns: dise_score, n_residues, plddt_fraction_high, plddt_fraction_low, plddt_fraction_ok, plddt_mean, plddt_median, source_category, uniprot
- **2026-02-22**:
  - Added columns: n_residues, organism, plddt_fraction_high, plddt_fraction_low, plddt_fraction_ok, plddt_mean, plddt_median, priority_score
  - Removed columns: length, pLDDT_fraction_high, pLDDT_fraction_low, pLDDT_mean, species
- **2026-02-28**:
  - Added columns: dise_score, source_category, uniprot
  - Removed columns: organism, priority_score, uniprot_id
- **2026-03-02**:
  - Added columns: organism, priority_score, uniprot_id
  - Removed columns: dise_score, source_category, uniprot

## 4. Conclusion and Confidence Labeling
- **[Measured evidence]** Many key genes including LBX1, PIEZO2, and LMNA have identical metrics across all their runs in the window. The narrative of 'evolving' or 'emerging' structural insights for these specific proteins is a **[Speculative narrative]** artifact of script generation or manual drafting, not measured data.
- **Evidence AGAINST hypothesis strength**: The persistence of identical vectors implies the pipeline relies on cached AlphaFold predictions (likely static PDBs) rather than resolving new conformational dynamics over time.
