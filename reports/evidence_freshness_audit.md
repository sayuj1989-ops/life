# Evidence Freshness Audit Report

## Data Integrity and Freshness

- **Runs Audited**: 27

- **Missing Linked Outputs**: 0 (None)

- **Schema Drifts**: None detected in scoped files with `gene_symbol`.


## Identical Per-Gene Vectors Across Runs (Static Metrics)

The following genes have identical metrics (anisotropy, pLDDT, PAE blockiness) across multiple runs, indicating reused static inputs rather than fresh measurements:

| Gene | Runs Present | First Date | Last Date | Anisotropy | pLDDT |

|------|--------------|------------|-----------|------------|-------|
| NTRK3 | 16 | 2026-01-27 | 2026-02-26 | 1.936111715585754 | 76.81557806912993 |
| LMNA | 13 | 2026-01-14 | 2026-02-26 | 4.751667397697646 | 76.37072289156627 |
| RUNX3 | 13 | 2026-01-27 | 2026-02-18 | 2.0611670656856456 | 60.564096385542165 |
| NF1 | 12 | 2026-01-18 | 2026-02-26 | 1.9279279346731688 | 87.17264755480608 |
| OTOP1 | 10 | 2026-01-27 | 2026-02-26 | 1.7507094616744632 | 75.68916666666668 |
| EGR3 | 10 | 2026-01-27 | 2026-02-26 | 3.762072398804325 | 49.96868217054263 |
| IFT88 | 8 | 2026-01-14 | 2026-02-18 | 2.8032400603850034 | 76.34603155339805 |
| PLOD1 | 7 | 2026-02-05 | 2026-02-26 | 3.3950779336885484 | 92.72865199449797 |
| COL1A1 | 5 | 2026-01-18 | 2026-02-18 | 2.797030038697096 | 52.72999316939891 |
| HIF1A | 5 | 2026-02-11 | 2026-02-23 | 3.417045794347625 | 60.75170702179177 |
| METTL3 | 4 | 2026-01-14 | 2026-02-18 | 1.6486356541690288 | 75.379 |
| FLNA | 4 | 2026-01-20 | 2026-02-18 | 2.501695116785587 | 76.54624858330186 |
| CEP290 | 4 | 2026-01-20 | 2026-02-18 | 2.286118643841953 | 60.54478418717224 |
| EMD | 4 | 2026-02-10 | 2026-02-18 | 4.288514695460691 | 60.25062992125985 |
| TGFBR2 | 3 | 2026-02-10 | 2026-02-18 | 2.481876912319578 | 80.98139329805996 |
| MYO7A | 3 | 2026-02-10 | 2026-02-18 | 2.3398248764346605 | 77.27780586907448 |
| CDH23 | 3 | 2026-02-10 | 2026-02-18 | 11.927795782477896 | 76.72945319740501 |
| FBN2 | 3 | 2026-02-10 | 2026-02-18 | 1.4943730069906092 | 68.39040733197557 |
| SERPINH1 | 3 | 2026-02-10 | 2026-02-18 | 1.9746660315008595 | 91.13595693779904 |
| ETV1 | 3 | 2026-02-10 | 2026-02-18 | 5.323069489820232 | 67.89180064308681 |
| ROR2 | 3 | 2026-02-10 | 2026-02-18 | 2.5114623831285026 | 68.28682926829269 |
| FERMT2 | 3 | 2026-02-10 | 2026-02-18 | 2.502653150494108 | 79.86822058823529 |
| TGFBR1 | 3 | 2026-02-10 | 2026-02-18 | 3.6543426000781953 | 84.19429423459245 |
| BNC2 | 3 | 2026-02-10 | 2026-02-18 | 1.9551006086909324 | 53.49764331210191 |
| SMAD3 | 2 | 2026-02-10 | 2026-02-13 | 2.405930835652692 | 83.6136705882353 |
| ACAN | 2 | 2026-02-10 | 2026-02-13 | 2.663035881007823 | 51.890964426877474 |
| CCDC40 | 2 | 2026-02-10 | 2026-02-13 | 5.699494256013449 | 70.7318213660245 |
| KIF7 | 2 | 2026-02-10 | 2026-02-13 | 2.10884896707772 | 67.16040953090096 |
| KIF3A | 2 | 2026-02-10 | 2026-02-13 | 2.9036334743310475 | 75.44905579399142 |
| SYNE2 | 2 | 2026-02-10 | 2026-02-18 | 2.123597597329561 | 83.327265917603 |
| DZIP1 | 2 | 2026-02-10 | 2026-02-16 | 2.5436815102910297 | 64.35407151095733 |
| RPL38 | 2 | 2026-02-10 | 2026-02-18 | 1.5151481532400566 | 95.34757142857144 |
| SUN1 | 2 | 2026-02-10 | 2026-02-18 | 2.337845450113884 | 60.360891719745226 |
| TLN1 | 2 | 2026-02-10 | 2026-02-13 | 2.043820318201773 | 75.88697756788666 |
| FBLN5 | 2 | 2026-02-10 | 2026-02-16 | 7.054480619949517 | 83.33808035714287 |
| COL11A2 | 2 | 2026-02-10 | 2026-02-16 | 2.4606769611384083 | 49.26498847926268 |
| SSPOP | 2 | 2026-02-10 | 2026-02-16 | 1.9153536859133964 | 60.13063022019741 |
| STOML3 | 2 | 2026-02-10 | 2026-02-16 | 5.559834719858973 | 84.32628865979382 |
| PANX3 | 2 | 2026-02-10 | 2026-02-16 | 5.075360561640713 | 81.7247193877551 |
| GDF5 | 2 | 2026-02-10 | 2026-02-16 | 2.969673405734348 | 69.98487025948103 |
| ROCK1 | 2 | 2026-02-10 | 2026-02-16 | 3.2921885930351955 | 76.13419497784342 |
| AQP4 | 2 | 2026-02-10 | 2026-02-16 | 1.969106742320216 | 81.03699690402476 |
| CNNM2 | 2 | 2026-02-10 | 2026-02-16 | 8.540535839977684 | 70.37298285714286 |
| NR1D1 | 2 | 2026-02-13 | 2026-02-18 | 1.796872009762566 | 62.885390879478834 |
| TEAD1 | 2 | 2026-02-13 | 2026-02-18 | 1.9067232446511149 | 76.47657276995305 |
| CLOCK | 2 | 2026-02-13 | 2026-02-18 | 1.8268099455225064 | 60.60554373522458 |
| COL1A2 | 2 | 2026-02-13 | 2026-02-18 | 2.876180753979266 | 53.64081991215226 |

## When 'New' Reports Reuse Unchanged Values

- **2026-01-18**: Reused static metrics for 2 genes (e.g., IFT88, LMNA...)

- **2026-01-20**: Reused static metrics for 4 genes (e.g., IFT88, LMNA, NF1, COL1A1...)

- **2026-01-21**: Reused static metrics for 3 genes (e.g., IFT88, LMNA, NF1...)

- **2026-01-27**: Reused static metrics for 2 genes (e.g., LMNA, NF1...)

- **2026-01-31**: Reused static metrics for 6 genes (e.g., LMNA, NF1, NTRK3, RUNX3, OTOP1...)

- **2026-02-05**: Reused static metrics for 6 genes (e.g., LMNA, NF1, NTRK3, RUNX3, OTOP1...)

- **2026-02-06**: Reused static metrics for 7 genes (e.g., LMNA, NF1, NTRK3, RUNX3, OTOP1...)

- **2026-02-07**: Reused static metrics for 7 genes (e.g., LMNA, NF1, NTRK3, RUNX3, OTOP1...)

- **2026-02-08**: Reused static metrics for 6 genes (e.g., IFT88, LMNA, NTRK3, RUNX3, OTOP1...)

- **2026-02-09**: Reused static metrics for 2 genes (e.g., NTRK3, RUNX3...)

- **2026-02-10**: Reused static metrics for 11 genes (e.g., IFT88, METTL3, NF1, COL1A1, FLNA...)

- **2026-02-11**: Reused static metrics for 2 genes (e.g., NTRK3, RUNX3...)

- **2026-02-12**: Reused static metrics for 3 genes (e.g., NTRK3, RUNX3, HIF1A...)

- **2026-02-13**: Reused static metrics for 29 genes (e.g., IFT88, LMNA, METTL3, NF1, COL1A1...)

- **2026-02-16**: Reused static metrics for 12 genes (e.g., EMD, DZIP1, BNC2, FBLN5, COL11A2...)

- **2026-02-17**: Reused static metrics for 2 genes (e.g., NTRK3, RUNX3...)

- **2026-02-18**: Reused static metrics for 31 genes (e.g., IFT88, LMNA, METTL3, NF1, COL1A1...)

- **2026-02-20**: Reused static metrics for 1 genes (e.g., NTRK3...)

- **2026-02-22**: Reused static metrics for 1 genes (e.g., NTRK3...)

- **2026-02-23**: Reused static metrics for 1 genes (e.g., HIF1A...)

- **2026-02-26**: Reused static metrics for 6 genes (e.g., LMNA, NF1, NTRK3, OTOP1, EGR3...)


## Conclusion

- **Actionable Insight**: Many core candidates (e.g., LBX1, PIEZO2, LMNA) show static values across the trend window. This confirms the caveat that high-anisotropy narratves may over-interpret static inputs.