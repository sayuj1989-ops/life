# Bolt-BioFold ⚡ Analysis Report

Sources: DefaultSeed_Proprioception, DefaultSeed_NuclearStiffness, DefaultSeed_ECM_Gravity, DefaultSeed_Proprioception_Dev
Sources: Top_Priority_Run

## 1. Results Table
| Identity | Species | Length | pLDDT_mean | pLDDT_median | pLDDT_frac_high | pLDDT_frac_ok | pLDDT_frac_low | PAE_mean | PAE_blockiness | Disorder_Proxy | Hinge_Cands | Rg | End_to_End | Curvature | Torsion | Anisotropy | Principal_Axis | Hotspots | Exposed_Frac | Charged_Patch | Domains | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PIEZO2 (Q9H5I5) | Homo sapiens | 709 | 79.4 | 88.4 | 0.42 | 0.37 | 0.21 | 17.0 | 2.8 | 0.14 | 0 | 43.4 | 28.4 | 0.329 | 1.428 | 4.44 | [-0.687, -0.068, 0.724] | 460:0.38; 239:0.38; 138:0.38 | 0.56 | 0.25 | 7 | MultiDomUncert |
| LMNA (P02545) | Homo sapiens | 664 | 76.4 | 93.1 | 0.58 | 0.11 | 0.31 | 24.9 | 2.56 | 0.26 | 0 | 71.2 | 278.1 | 0.344 | 1.194 | 4.75 | [-0.668, -0.244, 0.703] | 508:0.40; 519:0.39; 30:0.38 | 0.87 | 0.4 | 3 | MultiDomUncert |
| COL1A1 (P02452) | Homo sapiens | 1464 | 52.7 | 44.2 | 0.15 | 0.05 | 0.8 | 27.4 | 6.55 | 0.67 | 16 | 23.5 | 49.0 | 0.295 | 1.859 | 2.8 | [-0.475, 0.297, 0.828] | 1315:0.39; 1258:0.38; 1431:0.38 | 0.87 | 0.3 | 3 | LowConf, MultiDomUncert |
| RUNX3 (Q13761) | Homo sapiens | 415 | 60.6 | 46.3 | 0.28 | 0.04 | 0.68 | 25.6 | 0.0 | 0.56 | 12 | 15.8 | 53.0 | 0.284 | 1.965 | 2.06 | [-0.510, 0.008, 0.860] | 159:0.39; 69:0.38; 54:0.38 | 0.78 | 0.37 | 1 | LowConf |
| LBX1 (P52954) | Homo sapiens | 281 | 66.9 | 60.2 | 0.23 | 0.16 | 0.61 | 25.1 | 7.35 | 0.26 | 0 | 22.7 | 51.9 | 0.343 | 1.173 | 2.27 | [-0.222, -0.149, 0.964] | 83:0.39; 37:0.39; 34:0.38 | 0.93 | 0.36 | 3 | LowConf, MultiDomUncert |
| RUNX3 (Q13761) | Homo sapiens | 415 | 60.6 | 46.3 | 0.28 | 0.04 | 0.68 | 25.6 | 0.0 | 0.56 | 12 | 15.8 | 53.0 | 0.284 | 1.965 | 2.06 | [-0.510, 0.008, 0.860] | 159:0.39; 69:0.38; 54:0.38 | 0.78 | 0.37 | 1 | LowConf |
| NTRK3 (Q16288) | Homo sapiens | 839 | 76.8 | 88.8 | 0.47 | 0.25 | 0.28 | 22.2 | 6.34 | 0.2 | 9 | 32.5 | 42.5 | 0.303 | 1.829 | 1.94 | [-0.157, -0.071, 0.985] | 328:0.42; 236:0.40; 592:0.39 | 0.41 | 0.32 | 10 | MultiDomUncert |
| LMNA (P02545) | Homo sapiens | 664 | 76.4 | 93.1 | 0.58 | 0.11 | 0.31 | 24.9 | 2.56 | 0.26 | 0 | 71.2 | 278.1 | 0.344 | 1.194 | 4.75 | [-0.668, -0.244, 0.703] | 508:0.40; 519:0.39; 30:0.38 | 0.87 | 0.4 | 3 | MultiDomUncert |
| KIF3A (Q9Y496) | Homo sapiens | 699 | 75.4 | 83.1 | 0.21 | 0.52 | 0.27 | 20.0 | 4.44 | 0.15 | 4 | 31.6 | 40.6 | 0.328 | 1.461 | 2.9 | [-0.608, -0.163, 0.777] | 359:0.38; 43:0.38; 88:0.38 | 0.54 | 0.51 | 12 | MultiDomUncert |
| COL12A1 (Q99715) | Homo sapiens | 1899 | 75.6 | 84.3 | 0.22 | 0.54 | 0.24 | 25.7 | 6.27 | 0.18 | 41 | 63.1 | 6.0 | 0.279 | 2.024 | 4.14 | [-0.633, -0.197, 0.749] | 1310:0.43; 979:0.39; 1205:0.39 | 0.4 | 0.4 | 29 | MultiDomUncert |
| PCDH15 (Q96QU1) | Homo sapiens | 1955 | 65.8 | 77.6 | 0.09 | 0.5 | 0.41 | 26.5 | 5.35 | 0.31 | 72 | 60.8 | 33.7 | 0.274 | 2.087 | 2.47 | [-0.690, -0.070, 0.721] | 266:0.42; 678:0.41; 296:0.40 | 0.53 | 0.31 | 26 | LowConf, MultiDomUncert |
| USH1C (Q9Y6N9) | Homo sapiens | 552 | 79.4 | 86.8 | 0.37 | 0.46 | 0.17 | 22.3 | 4.21 | 0.13 | 1 | 32.5 | 43.8 | 0.32 | 1.547 | 2.31 | [0.436, 0.587, -0.683] | 82:0.38; 36:0.38; 56:0.38 | 0.52 | 0.46 | 4 | MultiDomUncert |
| TMC1 (Q8TDI8) | Homo sapiens | 760 | 76.9 | 82.8 | 0.12 | 0.67 | 0.21 | 16.3 | 2.89 | 0.09 | 1 | 33.2 | 46.0 | 0.35 | 1.024 | 2.25 | [-0.688, -0.511, 0.516] | 612:0.38; 553:0.38; 599:0.38 | 0.52 | 0.28 | 10 | MultiDomUncert |

### CSV Block
```csv
Identity,Species,Length,pLDDT_mean,pLDDT_median,pLDDT_frac_high,pLDDT_frac_ok,pLDDT_frac_low,PAE_mean,PAE_blockiness,Disorder_Proxy,Hinge_Cands,Rg,End_to_End,Curvature,Torsion,Anisotropy,Principal_Axis,Hotspots,Exposed_Frac,Charged_Patch,Domains,Flags
PIEZO2 (Q9H5I5),Homo sapiens,709,79.4,88.4,0.42,0.37,0.21,17.0,2.8,0.14,0,43.4,28.4,0.329,1.428,4.44,"[-0.687, -0.068, 0.724]",460:0.38; 239:0.38; 138:0.38,0.56,0.25,7,MultiDomUncert
LMNA (P02545),Homo sapiens,664,76.4,93.1,0.58,0.11,0.31,24.9,2.56,0.26,0,71.2,278.1,0.344,1.194,4.75,"[-0.668, -0.244, 0.703]",508:0.40; 519:0.39; 30:0.38,0.87,0.4,3,MultiDomUncert
KIF3A (Q9Y496),Homo sapiens,699,75.4,83.1,0.21,0.52,0.27,20.0,4.44,0.15,4,31.6,40.6,0.328,1.461,2.9,"[-0.608, -0.163, 0.777]",359:0.38; 43:0.38; 88:0.38,0.54,0.51,12,MultiDomUncert
COL12A1 (Q99715),Homo sapiens,1899,75.6,84.3,0.22,0.54,0.24,25.7,6.27,0.18,41,63.1,6.0,0.279,2.024,4.14,"[-0.633, -0.197, 0.749]",1310:0.43; 979:0.39; 1205:0.39,0.4,0.4,29,MultiDomUncert
PCDH15 (Q96QU1),Homo sapiens,1955,65.8,77.6,0.09,0.5,0.41,26.5,5.35,0.31,72,60.8,33.7,0.274,2.087,2.47,"[-0.690, -0.070, 0.721]",266:0.42; 678:0.41; 296:0.40,0.53,0.31,26,"LowConf, MultiDomUncert"
USH1C (Q9Y6N9),Homo sapiens,552,79.4,86.8,0.37,0.46,0.17,22.3,4.21,0.13,1,32.5,43.8,0.32,1.547,2.31,"[0.436, 0.587, -0.683]",82:0.38; 36:0.38; 56:0.38,0.52,0.46,4,MultiDomUncert
TMC1 (Q8TDI8),Homo sapiens,760,76.9,82.8,0.12,0.67,0.21,16.3,2.89,0.09,1,33.2,46.0,0.35,1.024,2.25,"[-0.688, -0.511, 0.516]",612:0.38; 553:0.38; 599:0.38,0.52,0.28,10,MultiDomUncert
```

## 2. Key Plots Summary
- `LMNA_plddt.png`: pLDDT profile for LMNA
- `LMNA_pae.png`: PAE heatmap for LMNA
- `PCDH15_plddt.png`: pLDDT profile for PCDH15
- `PCDH15_pae.png`: PAE heatmap for PCDH15

## 3. Interpretation
**Family: Cilia**
- **KIF3A**: Anisotropy=2.9, pLDDT=75. Intermediate shape.  Detected 4 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: ECM**
- **COL12A1**: Anisotropy=4.1, pLDDT=76. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: Mechanotransduction**
- **PIEZO2**: Anisotropy=4.4, pLDDT=79. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **PCDH15**: Anisotropy=2.5, pLDDT=66. Intermediate shape. Warning: Low confidence structure. Detected 72 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.
- **USH1C**: Anisotropy=2.3, pLDDT=79. Intermediate shape.  Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.
- **TMC1**: Anisotropy=2.2, pLDDT=77. Intermediate shape.  Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Nucleus**
- **LMNA**: Anisotropy=4.8, pLDDT=76. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: Proprioception**
- **LBX1**: Anisotropy=2.3, pLDDT=67. Intermediate shape. Warning: Low confidence structure. Standard globular domain, likely biochemical role or node in network. (Conf: Low). Test: Check expression timing relative to spine straightening.


## 4. Best Next Move
Add proteins: Expand search to include more cytoskeletal linkers.

## 5. Quality & Reproducibility Checklist
- Data Source: AlphaFold DB (fetched via scripts/02_fetch_afdb.py)
- Date/Time: 2026-02-07 19:37:28
- Code Version: b127d49
- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default
- Notes: 8 structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml
