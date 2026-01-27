# Bolt-BioFold ⚡ Analysis Report

Sources: seed_Scoliosis_Drivers, seed_ECM, seed_Segmentation, seed_Mechanosensors

## 1. Results Table
| Identity | Species | Length | pLDDT_mean | pLDDT_median | pLDDT_frac_high | pLDDT_frac_ok | pLDDT_frac_low | PAE_mean | PAE_blockiness | Disorder_Proxy | Hinge_Cands | Rg | End_to_End | Curvature | Torsion | Anisotropy | Principal_Axis | Hotspots | Exposed_Frac | Charged_Patch | Domains | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADGRG6 (Q86SQ4) | Homo sapiens | 1221 | 73.7 | 81.0 | 0.16 | 0.54 | 0.3 | 24.4 | 6.78 | 0.15 | 12 | 51.3 | 50.9 | 0.308 | 1.633 | 3.06 | [-0.749, -0.252, 0.613] | 57:0.43; 530:0.39; 247:0.39 | 0.44 | 0.25 | 23 | MultiDomUncert |
| COL11A2 (P13942) | Homo sapiens | 1736 | 49.3 | 40.2 | 0.12 | 0.09 | 0.8 | 27.2 | 5.25 | 0.74 | 24 | 24.5 | 21.8 | 0.292 | 1.93 | 2.46 | [-0.879, 0.323, 0.350] | 130:0.39; 219:0.38; 166:0.38 | 0.84 | 0.33 | 7 | LowConf, MultiDomUncert |
| HES7 (Q9BYE0) | Homo sapiens | 225 | 73.3 | 72.3 | 0.37 | 0.16 | 0.46 | 22.9 | 4.97 | 0.19 | 0 | 26.1 | 46.5 | 0.35 | 1.077 | 2.25 | [0.047, -0.369, -0.928] | 122:0.38; 46:0.37; 43:0.37 | 0.94 | 0.33 | 2 | MultiDomUncert |
| LBX1 (P52954) | Homo sapiens | 281 | 66.9 | 60.2 | 0.23 | 0.16 | 0.61 | 25.1 | 7.35 | 0.26 | 0 | 22.7 | 51.9 | 0.343 | 1.173 | 2.27 | [-0.222, -0.149, 0.964] | 83:0.39; 37:0.39; 34:0.38 | 0.93 | 0.36 | 3 | LowConf, MultiDomUncert |
| MESP2 (Q0VG99) | Homo sapiens | 397 | 54.2 | 46.7 | 0.12 | 0.07 | 0.82 | 26.9 | 0.0 | 0.58 | 1 | 17.0 | 42.6 | 0.351 | 1.183 | 4.03 | [-0.526, -0.048, 0.849] | 142:0.38; 85:0.38; 109:0.38 | 0.97 | 0.36 | 1 | LowConf |
| PIEZO2 (Q9H5I5) | Homo sapiens | 709 | 79.4 | 88.4 | 0.42 | 0.37 | 0.21 | 17.0 | 2.8 | 0.14 | 0 | 43.4 | 28.4 | 0.329 | 1.428 | 4.44 | [-0.687, -0.068, 0.724] | 460:0.38; 239:0.38; 138:0.38 | 0.56 | 0.25 | 7 | MultiDomUncert |
| POC5 (Q8NA72) | Homo sapiens | 575 | 64.0 | 50.9 | 0.33 | 0.06 | 0.61 | 25.6 | 3.51 | 0.49 | 5 | 87.3 | 307.4 | 0.364 | 0.848 | 24.69 | [-0.657, -0.161, 0.737] | 156:0.38; 247:0.38; 192:0.37 | 1.0 | 0.36 | 2 | LowConf, MultiDomUncert |
| PTK7 (Q13308) | Homo sapiens | 1070 | 82.7 | 89.6 | 0.48 | 0.38 | 0.14 | 22.5 | 4.53 | 0.09 | 20 | 62.9 | 72.4 | 0.284 | 1.955 | 7.45 | [-0.582, 0.048, 0.812] | 155:0.42; 869:0.42; 618:0.41 | 0.39 | 0.34 | 9 | MultiDomUncert |

### CSV Block
```csv
Identity,Species,Length,pLDDT_mean,pLDDT_median,pLDDT_frac_high,pLDDT_frac_ok,pLDDT_frac_low,PAE_mean,PAE_blockiness,Disorder_Proxy,Hinge_Cands,Rg,End_to_End,Curvature,Torsion,Anisotropy,Principal_Axis,Hotspots,Exposed_Frac,Charged_Patch,Domains,Flags
ADGRG6 (Q86SQ4),Homo sapiens,1221,73.7,81.0,0.16,0.54,0.3,24.4,6.78,0.15,12,51.3,50.9,0.308,1.633,3.06,"[-0.749, -0.252, 0.613]",57:0.43; 530:0.39; 247:0.39,0.44,0.25,23,MultiDomUncert
COL11A2 (P13942),Homo sapiens,1736,49.3,40.2,0.12,0.09,0.8,27.2,5.25,0.74,24,24.5,21.8,0.292,1.93,2.46,"[-0.879, 0.323, 0.350]",130:0.39; 219:0.38; 166:0.38,0.84,0.33,7,"LowConf, MultiDomUncert"
HES7 (Q9BYE0),Homo sapiens,225,73.3,72.3,0.37,0.16,0.46,22.9,4.97,0.19,0,26.1,46.5,0.35,1.077,2.25,"[0.047, -0.369, -0.928]",122:0.38; 46:0.37; 43:0.37,0.94,0.33,2,MultiDomUncert
LBX1 (P52954),Homo sapiens,281,66.9,60.2,0.23,0.16,0.61,25.1,7.35,0.26,0,22.7,51.9,0.343,1.173,2.27,"[-0.222, -0.149, 0.964]",83:0.39; 37:0.39; 34:0.38,0.93,0.36,3,"LowConf, MultiDomUncert"
MESP2 (Q0VG99),Homo sapiens,397,54.2,46.7,0.12,0.07,0.82,26.9,0.0,0.58,1,17.0,42.6,0.351,1.183,4.03,"[-0.526, -0.048, 0.849]",142:0.38; 85:0.38; 109:0.38,0.97,0.36,1,LowConf
PIEZO2 (Q9H5I5),Homo sapiens,709,79.4,88.4,0.42,0.37,0.21,17.0,2.8,0.14,0,43.4,28.4,0.329,1.428,4.44,"[-0.687, -0.068, 0.724]",460:0.38; 239:0.38; 138:0.38,0.56,0.25,7,MultiDomUncert
POC5 (Q8NA72),Homo sapiens,575,64.0,50.9,0.33,0.06,0.61,25.6,3.51,0.49,5,87.3,307.4,0.364,0.848,24.69,"[-0.657, -0.161, 0.737]",156:0.38; 247:0.38; 192:0.37,1.0,0.36,2,"LowConf, MultiDomUncert"
PTK7 (Q13308),Homo sapiens,1070,82.7,89.6,0.48,0.38,0.14,22.5,4.53,0.09,20,62.9,72.4,0.284,1.955,7.45,"[-0.582, 0.048, 0.812]",155:0.42; 869:0.42; 618:0.41,0.39,0.34,9,MultiDomUncert
```

## 2. Key Plots Summary
- `POC5_plddt.png`: pLDDT profile for POC5
- `POC5_pae.png`: PAE heatmap for POC5
- `PTK7_plddt.png`: pLDDT profile for PTK7
- `PTK7_pae.png`: PAE heatmap for PTK7
- `COL11A2_plddt.png`: pLDDT profile for COL11A2
- `COL11A2_pae.png`: PAE heatmap for COL11A2

## 3. Interpretation
**Family: seed_ECM**
- **COL11A2**: COL11A2: Anisotropy=2.5, pLDDT=49. Intermediate shape. Warning: Low confidence structure. Detected 24 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: seed_Mechanosensors**
- **PIEZO2**: PIEZO2: Anisotropy=4.4, pLDDT=79. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: seed_Scoliosis_Drivers**
- **ADGRG6**: ADGRG6: Anisotropy=3.1, pLDDT=74. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.
- **LBX1**: LBX1: Anisotropy=2.3, pLDDT=67. Intermediate shape. Warning: Low confidence structure. Standard globular domain, likely biochemical role or node in network. (Conf: Low). Test: Check expression timing relative to spine straightening.
- **POC5**: POC5: Anisotropy=24.7, pLDDT=64. Highly extended/fibrous. Warning: Low confidence structure. Detected 5 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **PTK7**: PTK7: Anisotropy=7.4, pLDDT=83. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: seed_Segmentation**
- **HES7**: HES7: Anisotropy=2.2, pLDDT=73. Intermediate shape.  Standard globular domain, likely biochemical role or node in network. (Conf: Medium). Test: Check expression timing relative to spine straightening.
- **MESP2**: MESP2: Anisotropy=4.0, pLDDT=54. Highly extended/fibrous. Warning: Low confidence structure. Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Verify fiber formation in vivo; test mechanical stiffness.


## 4. Best Next Move
Cluster by geometry and correlate curvature metrics with known phenotype genes.

## 5. Quality & Reproducibility Checklist
- Data Source: AlphaFold DB (fetched via scripts/02_fetch_afdb.py)
- Date/Time: 2026-01-27 19:27:28
- Code Version: b3f2832
- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default
- Notes: 8 structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml
