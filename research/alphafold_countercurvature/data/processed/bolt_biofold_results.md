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
| NF1 (P21359) | Homo sapiens | 593 | 87.2 | 93.2 | 0.68 | 0.21 | 0.11 | 9.5 | 2.42 | 0.07 | 1 | 26.1 | 40.7 | 0.35 | 1.116 | 1.93 | [-0.387, -0.133, 0.912] | 221:0.38; 178:0.38; 274:0.38 | 0.34 | 0.37 | 6 | OK |
| EGR3 (Q06889) | Homo sapiens | 387 | 50.0 | 37.9 | 0.13 | 0.11 | 0.75 | 25.9 | 0.0 | 0.64 | 2 | 18.5 | 42.9 | 0.331 | 1.631 | 3.76 | [-0.453, -0.341, 0.824] | 226:0.38; 300:0.38; 323:0.38 | 0.87 | 0.54 | 1 | LowConf |
| OTOP1 (Q7RTM1) | Homo sapiens | 612 | 75.7 | 86.9 | 0.4 | 0.28 | 0.32 | 16.2 | 1.83 | 0.23 | 0 | 22.6 | 10.3 | 0.356 | 0.967 | 1.75 | [0.840, 0.540, 0.055] | 255:0.39; 88:0.38; 554:0.38 | 0.46 | 0.19 | 7 | MultiDomUncert |
| PLOD1 (Q02809) | Homo sapiens | 727 | 92.7 | 96.1 | 0.88 | 0.08 | 0.05 | 7.7 | 2.31 | 0.03 | 1 | 34.7 | 81.0 | 0.309 | 1.683 | 3.4 | [-0.617, -0.153, 0.772] | 685:0.39; 660:0.39; 458:0.38 | 0.3 | 0.43 | 3 | OK |

### CSV Block
```csv
Identity,Species,Length,pLDDT_mean,pLDDT_median,pLDDT_frac_high,pLDDT_frac_ok,pLDDT_frac_low,PAE_mean,PAE_blockiness,Disorder_Proxy,Hinge_Cands,Rg,End_to_End,Curvature,Torsion,Anisotropy,Principal_Axis,Hotspots,Exposed_Frac,Charged_Patch,Domains,Flags
PIEZO2 (Q9H5I5),Homo sapiens,709,79.4,88.4,0.42,0.37,0.21,17.0,2.8,0.14,0,43.4,28.4,0.329,1.428,4.44,"[-0.687, -0.068, 0.724]",460:0.38; 239:0.38; 138:0.38,0.56,0.25,7,MultiDomUncert
LMNA (P02545),Homo sapiens,664,76.4,93.1,0.58,0.11,0.31,24.9,2.56,0.26,0,71.2,278.1,0.344,1.194,4.75,"[-0.668, -0.244, 0.703]",508:0.40; 519:0.39; 30:0.38,0.87,0.4,3,MultiDomUncert
COL1A1 (P02452),Homo sapiens,1464,52.7,44.2,0.15,0.05,0.8,27.4,6.55,0.67,16,23.5,49.0,0.295,1.859,2.8,"[-0.475, 0.297, 0.828]",1315:0.39; 1258:0.38; 1431:0.38,0.87,0.3,3,"LowConf, MultiDomUncert"
RUNX3 (Q13761),Homo sapiens,415,60.6,46.3,0.28,0.04,0.68,25.6,0.0,0.56,12,15.8,53.0,0.284,1.965,2.06,"[-0.510, 0.008, 0.860]",159:0.39; 69:0.38; 54:0.38,0.78,0.37,1,LowConf
```

## 2. Key Plots Summary
- `LMNA_plddt.png`: pLDDT profile for LMNA
- `LMNA_pae.png`: PAE heatmap for LMNA
- `PIEZO2_plddt.png`: pLDDT profile for PIEZO2
- `PIEZO2_pae.png`: PAE heatmap for PIEZO2
- `COL1A1_plddt.png`: pLDDT profile for COL1A1
- `COL1A1_pae.png`: PAE heatmap for COL1A1

## 3. Interpretation
**Family: DefaultSeed_ECM_Gravity**
- **COL1A1**: COL1A1: Anisotropy=2.8, pLDDT=53. Intermediate shape. Warning: Low confidence structure. Detected 16 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: DefaultSeed_NuclearStiffness**
- **LMNA**: LMNA: Anisotropy=4.8, pLDDT=76. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: DefaultSeed_Proprioception**
- **PIEZO2**: PIEZO2: Anisotropy=4.4, pLDDT=79. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: DefaultSeed_Proprioception_Dev**
- **RUNX3**: RUNX3: Anisotropy=2.1, pLDDT=61. Intermediate shape. Warning: Low confidence structure. Detected 12 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.
LBX1 (P52954),Homo sapiens,281,66.9,60.2,0.23,0.16,0.61,25.1,7.35,0.26,0,22.7,51.9,0.343,1.173,2.27,"[-0.222, -0.149, 0.964]",83:0.39; 37:0.39; 34:0.38,0.93,0.36,3,"LowConf, MultiDomUncert"
RUNX3 (Q13761),Homo sapiens,415,60.6,46.3,0.28,0.04,0.68,25.6,0.0,0.56,12,15.8,53.0,0.284,1.965,2.06,"[-0.510, 0.008, 0.860]",159:0.39; 69:0.38; 54:0.38,0.78,0.37,1,LowConf
NTRK3 (Q16288),Homo sapiens,839,76.8,88.8,0.47,0.25,0.28,22.2,6.34,0.2,9,32.5,42.5,0.303,1.829,1.94,"[-0.157, -0.071, 0.985]",328:0.42; 236:0.40; 592:0.39,0.41,0.32,10,MultiDomUncert
LMNA (P02545),Homo sapiens,664,76.4,93.1,0.58,0.11,0.31,24.9,2.56,0.26,0,71.2,278.1,0.344,1.194,4.75,"[-0.668, -0.244, 0.703]",508:0.40; 519:0.39; 30:0.38,0.87,0.4,3,MultiDomUncert
NF1 (P21359),Homo sapiens,593,87.2,93.2,0.68,0.21,0.11,9.5,2.42,0.07,1,26.1,40.7,0.35,1.116,1.93,"[-0.387, -0.133, 0.912]",221:0.38; 178:0.38; 274:0.38,0.34,0.37,6,OK
EGR3 (Q06889),Homo sapiens,387,50.0,37.9,0.13,0.11,0.75,25.9,0.0,0.64,2,18.5,42.9,0.331,1.631,3.76,"[-0.453, -0.341, 0.824]",226:0.38; 300:0.38; 323:0.38,0.87,0.54,1,LowConf
OTOP1 (Q7RTM1),Homo sapiens,612,75.7,86.9,0.4,0.28,0.32,16.2,1.83,0.23,0,22.6,10.3,0.356,0.967,1.75,"[0.840, 0.540, 0.055]",255:0.39; 88:0.38; 554:0.38,0.46,0.19,7,MultiDomUncert
PLOD1 (Q02809),Homo sapiens,727,92.7,96.1,0.88,0.08,0.05,7.7,2.31,0.03,1,34.7,81.0,0.309,1.683,3.4,"[-0.617, -0.153, 0.772]",685:0.39; 660:0.39; 458:0.38,0.3,0.43,3,OK
```

## 2. Key Plots Summary
- `RUNX3_plddt.png`: pLDDT profile for RUNX3
- `RUNX3_pae.png`: PAE heatmap for RUNX3
- `PIEZO2_plddt.png`: pLDDT profile for PIEZO2
- `PIEZO2_pae.png`: PAE heatmap for PIEZO2
- `LMNA_plddt.png`: pLDDT profile for LMNA
- `LMNA_pae.png`: PAE heatmap for LMNA

## 3. Interpretation
**Family: Top_Priority_Run**
- **PIEZO2**: PIEZO2: Anisotropy=4.4, pLDDT=79. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **LBX1**: LBX1: Anisotropy=2.3, pLDDT=67. Intermediate shape. Warning: Low confidence structure. Standard globular domain, likely biochemical role or node in network. (Conf: Low). Test: Check expression timing relative to spine straightening.
- **RUNX3**: RUNX3: Anisotropy=2.1, pLDDT=61. Intermediate shape. Warning: Low confidence structure. Detected 12 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.
- **NTRK3**: NTRK3: Anisotropy=1.9, pLDDT=77. Intermediate shape.  Detected 9 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.
- **LMNA**: LMNA: Anisotropy=4.8, pLDDT=76. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **NF1**: NF1: Anisotropy=1.9, pLDDT=87. Intermediate shape.  Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: High). Test: Mutate hinge region to test effect on mechanosensitivity.
- **EGR3**: EGR3: Anisotropy=3.8, pLDDT=50. Highly extended/fibrous. Warning: Low confidence structure. Detected 2 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.
- **OTOP1**: OTOP1: Anisotropy=1.8, pLDDT=76. Intermediate shape.  Standard globular domain, likely biochemical role or node in network. (Conf: Medium). Test: Check expression timing relative to spine straightening.
- **PLOD1**: PLOD1: Anisotropy=3.4, pLDDT=93. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: High). Test: Mutate hinge region to test effect on mechanosensitivity.


## 4. Best Next Move
Add proteins: Expand search to include more cytoskeletal linkers.

## 5. Quality & Reproducibility Checklist
- Data Source: AlphaFold DB (fetched via scripts/02_fetch_afdb.py)
- Date/Time: 2026-02-05 19:31:50
- Code Version: 646c850
- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default
- Notes: 4 structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml
- Date/Time: 2026-02-05 22:06:21
- Code Version: 646c850
- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default
- Notes: 9 structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml
