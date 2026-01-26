# Bolt-BioFold ⚡ Analysis Report

Sources: Mechanotransduction, Proprioception, Somite, Signaling, Muscle, Gravity_Sensing, Cilia

## 1. Results Table
| Identity | Species | Length | pLDDT_mean | pLDDT_frac_low | PAE_mean | PAE_blockiness | Disorder_Proxy | Hinge_Cands | Rg | End_to_End | Curvature | Torsion | Anisotropy | Principal_Axis | Hotspots | Exposed_Frac | Charged_Patch | Domains | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PIEZO2 (Q9H5I5) | Homo sapiens | 709 | 79.4 | 0.21 | 17.0 | 2.8 | 0.14 | 0 | 43.4 | 28.4 | 0.329 | 1.428 | 4.44 | [-0.687, -0.068, 0.724] | 460:0.38; 239:0.38; 138:0.38 | 0.56 | 0.25 | 7 | MultiDomUncert |
| NTRK3 (Q16288) | Homo sapiens | 839 | 76.8 | 0.28 | 22.2 | 6.34 | 0.2 | 9 | 32.5 | 42.5 | 0.303 | 1.829 | 1.94 | [-0.157, -0.071, 0.985] | 328:0.42; 236:0.40; 592:0.39 | 0.41 | 0.32 | 10 | MultiDomUncert |
| RUNX3 (Q13761) | Homo sapiens | 415 | 60.6 | 0.68 | 25.6 | 0.0 | 0.56 | 12 | 15.8 | 53.0 | 0.284 | 1.965 | 2.06 | [-0.510, 0.008, 0.860] | 159:0.39; 69:0.38; 54:0.38 | 0.78 | 0.37 | 1 | LowConf |
| LBX1 (P52954) | Homo sapiens | 281 | 66.9 | 0.61 | 25.1 | 7.35 | 0.26 | 0 | 22.7 | 51.9 | 0.343 | 1.173 | 2.27 | [-0.222, -0.149, 0.964] | 83:0.39; 37:0.39; 34:0.38 | 0.93 | 0.36 | 3 | LowConf, MultiDomUncert |
| NF1 (P21359) | Homo sapiens | 593 | 87.2 | 0.11 | 9.5 | 2.42 | 0.07 | 1 | 26.1 | 40.7 | 0.35 | 1.116 | 1.93 | [-0.387, -0.133, 0.912] | 221:0.38; 178:0.38; 274:0.38 | 0.34 | 0.37 | 6 | OK |
| LMNA (P02545) | Homo sapiens | 664 | 76.4 | 0.31 | 24.9 | 2.56 | 0.26 | 0 | 71.2 | 278.1 | 0.344 | 1.194 | 4.75 | [-0.668, -0.244, 0.703] | 508:0.40; 519:0.39; 30:0.38 | 0.87 | 0.4 | 3 | MultiDomUncert |
| EGR3 (Q06889) | Homo sapiens | 387 | 50.0 | 0.75 | 25.9 | 0.0 | 0.64 | 2 | 18.5 | 42.9 | 0.331 | 1.631 | 3.76 | [-0.453, -0.341, 0.824] | 226:0.38; 300:0.38; 323:0.38 | 0.87 | 0.54 | 1 | LowConf |
| OTOP1 (Q7RTS5) | Homo sapiens | 596 | 76.6 | 0.31 | 14.9 | 1.59 | 0.17 | 1 | 23.0 | 37.5 | 0.354 | 0.956 | 1.82 | [0.163, -0.877, -0.451] | 192:0.38; 117:0.38; 576:0.38 | 0.45 | 0.22 | 6 | MultiDomUncert |
| IFT88 (Q13099) | Homo sapiens | 824 | 76.3 | 0.29 | 19.4 | 2.43 | 0.23 | 1 | 38.3 | 92.4 | 0.358 | 1.121 | 2.8 | [-0.626, -0.157, 0.764] | 315:0.38; 643:0.38; 426:0.38 | 0.51 | 0.44 | 3 | MultiDomUncert |

### CSV Block
```csv
Identity,Species,Length,pLDDT_mean,pLDDT_frac_low,PAE_mean,PAE_blockiness,Disorder_Proxy,Hinge_Cands,Rg,End_to_End,Curvature,Torsion,Anisotropy,Principal_Axis,Hotspots,Exposed_Frac,Charged_Patch,Domains,Flags
PIEZO2 (Q9H5I5),Homo sapiens,709,79.4,0.21,17.0,2.8,0.14,0,43.4,28.4,0.329,1.428,4.44,"[-0.687, -0.068, 0.724]",460:0.38; 239:0.38; 138:0.38,0.56,0.25,7,MultiDomUncert
NTRK3 (Q16288),Homo sapiens,839,76.8,0.28,22.2,6.34,0.2,9,32.5,42.5,0.303,1.829,1.94,"[-0.157, -0.071, 0.985]",328:0.42; 236:0.40; 592:0.39,0.41,0.32,10,MultiDomUncert
RUNX3 (Q13761),Homo sapiens,415,60.6,0.68,25.6,0.0,0.56,12,15.8,53.0,0.284,1.965,2.06,"[-0.510, 0.008, 0.860]",159:0.39; 69:0.38; 54:0.38,0.78,0.37,1,LowConf
LBX1 (P52954),Homo sapiens,281,66.9,0.61,25.1,7.35,0.26,0,22.7,51.9,0.343,1.173,2.27,"[-0.222, -0.149, 0.964]",83:0.39; 37:0.39; 34:0.38,0.93,0.36,3,"LowConf, MultiDomUncert"
NF1 (P21359),Homo sapiens,593,87.2,0.11,9.5,2.42,0.07,1,26.1,40.7,0.35,1.116,1.93,"[-0.387, -0.133, 0.912]",221:0.38; 178:0.38; 274:0.38,0.34,0.37,6,OK
LMNA (P02545),Homo sapiens,664,76.4,0.31,24.9,2.56,0.26,0,71.2,278.1,0.344,1.194,4.75,"[-0.668, -0.244, 0.703]",508:0.40; 519:0.39; 30:0.38,0.87,0.4,3,MultiDomUncert
EGR3 (Q06889),Homo sapiens,387,50.0,0.75,25.9,0.0,0.64,2,18.5,42.9,0.331,1.631,3.76,"[-0.453, -0.341, 0.824]",226:0.38; 300:0.38; 323:0.38,0.87,0.54,1,LowConf
OTOP1 (Q7RTS5),Homo sapiens,596,76.6,0.31,14.9,1.59,0.17,1,23.0,37.5,0.354,0.956,1.82,"[0.163, -0.877, -0.451]",192:0.38; 117:0.38; 576:0.38,0.45,0.22,6,MultiDomUncert
IFT88 (Q13099),Homo sapiens,824,76.3,0.29,19.4,2.43,0.23,1,38.3,92.4,0.358,1.121,2.8,"[-0.626, -0.157, 0.764]",315:0.38; 643:0.38; 426:0.38,0.51,0.44,3,MultiDomUncert
```

## 2. Key Plots Summary
- `PIEZO2_plddt.png`: pLDDT profile for PIEZO2
- `PIEZO2_pae.png`: PAE heatmap for PIEZO2
- `RUNX3_plddt.png`: pLDDT profile for RUNX3
- `RUNX3_pae.png`: PAE heatmap for RUNX3
- `LMNA_plddt.png`: pLDDT profile for LMNA
- `LMNA_pae.png`: PAE heatmap for LMNA

## 3. Interpretation
**Family: Cilia**
- **IFT88**: IFT88: Anisotropy=2.8, pLDDT=76. Intermediate shape.  Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Gravity_Sensing**
- **OTOP1**: OTOP1: Anisotropy=1.8, pLDDT=77. Intermediate shape.  Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Mechanotransduction**
- **PIEZO2**: PIEZO2: Anisotropy=4.4, pLDDT=79. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **LMNA**: LMNA: Anisotropy=4.8, pLDDT=76. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: Muscle**
- **EGR3**: EGR3: Anisotropy=3.8, pLDDT=50. Highly extended/fibrous. Warning: Low confidence structure. Detected 2 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Proprioception**
- **NTRK3**: NTRK3: Anisotropy=1.9, pLDDT=77. Intermediate shape.  Detected 9 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.
- **RUNX3**: RUNX3: Anisotropy=2.1, pLDDT=61. Intermediate shape. Warning: Low confidence structure. Detected 12 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Signaling**
- **NF1**: NF1: Anisotropy=1.9, pLDDT=87. Intermediate shape.  Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: High). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Somite**
- **LBX1**: LBX1: Anisotropy=2.3, pLDDT=67. Intermediate shape. Warning: Low confidence structure. Standard globular domain, likely biochemical role or node in network. (Conf: Low). Test: Check expression timing relative to spine straightening.


## 4. Best Next Move
Cluster by geometry and correlate curvature metrics with known phenotype genes.

## 5. Quality & Reproducibility Checklist
- Data Source: AlphaFold DB (fetched via scripts/02_fetch_afdb.py)
- Date/Time: 2026-01-26 21:39:34
- Code Version: 4690528
- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default
- Notes: 9 structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml
