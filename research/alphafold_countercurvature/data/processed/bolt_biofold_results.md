# Bolt-BioFold ⚡ Analysis Report

Sources: Week6_Gravity_Expansion

## 1. Results Table
| Identity | Species | Length | pLDDT_mean | pLDDT_frac_low | PAE_mean | PAE_blockiness | Disorder_Proxy | Hinge_Cands | Rg | End_to_End | Curvature | Torsion | Anisotropy | Principal_Axis | Hotspots | Exposed_Frac | Charged_Patch | Domains | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EMD (P50402) | Homo sapiens | 254 | 60.3 | 0.72 | 26.5 | 9.13 | 0.48 | 1 | 21.0 | 19.8 | 0.35 | 1.112 | 4.29 | [-0.478, -0.124, 0.870] | 8:0.38; 11:0.38; 34:0.38 | 0.94 | 0.23 | 2 | LowConf, MultiDomUncert |
| STOML3 (Q8TAV4) | Homo sapiens | 291 | 84.3 | 0.18 | 13.6 | 0.0 | 0.1 | 0 | 36.6 | 106.3 | 0.326 | 1.44 | 5.56 | [-0.750, -0.272, 0.602] | 43:0.38; 70:0.38; 64:0.37 | 0.6 | 0.24 | 1 | OK |
| AQP4 (P55087) | Homo sapiens | 323 | 81.0 | 0.25 | 13.9 | 5.21 | 0.2 | 0 | 18.4 | 25.2 | 0.345 | 1.185 | 1.97 | [-0.766, -0.254, 0.590] | 211:0.39; 188:0.38; 95:0.38 | 0.45 | 0.3 | 2 | MultiDomUncert |
| SSPOP (A2VEC9) | Homo sapiens | 1317 | 60.1 | 0.57 | 27.2 | 8.62 | 0.35 | 31 | 44.2 | 33.5 | 0.304 | 1.771 | 1.92 | [-0.549, -0.107, 0.829] | 37:0.39; 82:0.38; 83:0.38 | 0.6 | 0.29 | 20 | LowConf, MultiDomUncert |
| ROCK1 (Q13464) | Homo sapiens | 1354 | 76.1 | 0.28 | 24.3 | 4.95 | 0.1 | 3 | 66.6 | 47.6 | 0.333 | 1.329 | 3.29 | [-0.484, -0.440, 0.757] | 1157:0.39; 1269:0.39; 131:0.38 | 0.71 | 0.45 | 13 | MultiDomUncert |
| DZIP1 (Q86YF9) | Homo sapiens | 867 | 64.4 | 0.51 | 26.7 | 3.83 | 0.44 | 0 | 46.5 | 88.3 | 0.354 | 1.026 | 2.54 | [-0.667, -0.106, 0.738] | 388:0.38; 367:0.38; 605:0.38 | 0.95 | 0.39 | 5 | LowConf, MultiDomUncert |
| MYLK (Q15746) | Homo sapiens | 1914 | 65.8 | 0.39 | 26.6 | 8.29 | 0.35 | 31 | 41.5 | 56.8 | 0.277 | 2.076 | 1.46 | [-0.262, -0.391, 0.882] | 1835:0.42; 59:0.41; 649:0.41 | 0.53 | 0.4 | 28 | LowConf, MultiDomUncert |
| PANX3 (Q96QZ0) | Homo sapiens | 392 | 81.7 | 0.17 | 12.9 | 2.77 | 0.04 | 1 | 33.0 | 12.8 | 0.348 | 1.145 | 5.08 | [-0.676, -0.135, 0.725] | 364:0.38; 305:0.38; 306:0.38 | 0.43 | 0.21 | 7 | MultiDomUncert |
| FBLN5 (Q9UBX5) | Homo sapiens | 448 | 83.3 | 0.15 | 19.0 | 3.55 | 0.13 | 3 | 51.1 | 125.3 | 0.286 | 1.938 | 7.05 | [-0.703, -0.164, 0.692] | 412:0.43; 361:0.42; 322:0.41 | 0.47 | 0.31 | 2 | MultiDomUncert |
| GDF5 (P43026) | Homo sapiens | 501 | 70.0 | 0.42 | 20.2 | 3.5 | 0.31 | 16 | 27.0 | 16.6 | 0.299 | 1.901 | 2.97 | [-0.730, -0.144, 0.668] | 353:0.40; 435:0.39; 420:0.39 | 0.62 | 0.33 | 7 | LowConf, MultiDomUncert |
| CNNM2 (Q9H8M5) | Homo sapiens | 875 | 70.4 | 0.37 | 22.4 | 4.83 | 0.27 | 4 | 61.1 | 22.6 | 0.315 | 1.538 | 8.54 | [-0.676, -0.127, 0.726] | 675:0.39; 445:0.39; 167:0.39 | 0.56 | 0.37 | 8 | MultiDomUncert |
| BNC2 (Q6ZN30) | Homo sapiens | 1099 | 53.5 | 0.71 | 27.9 | 6.97 | 0.64 | 1 | 30.9 | 24.0 | 0.325 | 1.47 | 1.96 | [-0.385, -0.482, -0.787] | 190:0.38; 844:0.38; 171:0.38 | 0.83 | 0.29 | 7 | LowConf, MultiDomUncert |

### CSV Block
```csv
Identity,Species,Length,pLDDT_mean,pLDDT_frac_low,PAE_mean,PAE_blockiness,Disorder_Proxy,Hinge_Cands,Rg,End_to_End,Curvature,Torsion,Anisotropy,Principal_Axis,Hotspots,Exposed_Frac,Charged_Patch,Domains,Flags
EMD (P50402),Homo sapiens,254,60.3,0.72,26.5,9.13,0.48,1,21.0,19.8,0.35,1.112,4.29,"[-0.478, -0.124, 0.870]",8:0.38; 11:0.38; 34:0.38,0.94,0.23,2,"LowConf, MultiDomUncert"
STOML3 (Q8TAV4),Homo sapiens,291,84.3,0.18,13.6,0.0,0.1,0,36.6,106.3,0.326,1.44,5.56,"[-0.750, -0.272, 0.602]",43:0.38; 70:0.38; 64:0.37,0.6,0.24,1,OK
AQP4 (P55087),Homo sapiens,323,81.0,0.25,13.9,5.21,0.2,0,18.4,25.2,0.345,1.185,1.97,"[-0.766, -0.254, 0.590]",211:0.39; 188:0.38; 95:0.38,0.45,0.3,2,MultiDomUncert
SSPOP (A2VEC9),Homo sapiens,1317,60.1,0.57,27.2,8.62,0.35,31,44.2,33.5,0.304,1.771,1.92,"[-0.549, -0.107, 0.829]",37:0.39; 82:0.38; 83:0.38,0.6,0.29,20,"LowConf, MultiDomUncert"
ROCK1 (Q13464),Homo sapiens,1354,76.1,0.28,24.3,4.95,0.1,3,66.6,47.6,0.333,1.329,3.29,"[-0.484, -0.440, 0.757]",1157:0.39; 1269:0.39; 131:0.38,0.71,0.45,13,MultiDomUncert
DZIP1 (Q86YF9),Homo sapiens,867,64.4,0.51,26.7,3.83,0.44,0,46.5,88.3,0.354,1.026,2.54,"[-0.667, -0.106, 0.738]",388:0.38; 367:0.38; 605:0.38,0.95,0.39,5,"LowConf, MultiDomUncert"
MYLK (Q15746),Homo sapiens,1914,65.8,0.39,26.6,8.29,0.35,31,41.5,56.8,0.277,2.076,1.46,"[-0.262, -0.391, 0.882]",1835:0.42; 59:0.41; 649:0.41,0.53,0.4,28,"LowConf, MultiDomUncert"
PANX3 (Q96QZ0),Homo sapiens,392,81.7,0.17,12.9,2.77,0.04,1,33.0,12.8,0.348,1.145,5.08,"[-0.676, -0.135, 0.725]",364:0.38; 305:0.38; 306:0.38,0.43,0.21,7,MultiDomUncert
FBLN5 (Q9UBX5),Homo sapiens,448,83.3,0.15,19.0,3.55,0.13,3,51.1,125.3,0.286,1.938,7.05,"[-0.703, -0.164, 0.692]",412:0.43; 361:0.42; 322:0.41,0.47,0.31,2,MultiDomUncert
GDF5 (P43026),Homo sapiens,501,70.0,0.42,20.2,3.5,0.31,16,27.0,16.6,0.299,1.901,2.97,"[-0.730, -0.144, 0.668]",353:0.40; 435:0.39; 420:0.39,0.62,0.33,7,"LowConf, MultiDomUncert"
CNNM2 (Q9H8M5),Homo sapiens,875,70.4,0.37,22.4,4.83,0.27,4,61.1,22.6,0.315,1.538,8.54,"[-0.676, -0.127, 0.726]",675:0.39; 445:0.39; 167:0.39,0.56,0.37,8,MultiDomUncert
BNC2 (Q6ZN30),Homo sapiens,1099,53.5,0.71,27.9,6.97,0.64,1,30.9,24.0,0.325,1.47,1.96,"[-0.385, -0.482, -0.787]",190:0.38; 844:0.38; 171:0.38,0.83,0.29,7,"LowConf, MultiDomUncert"
```

## 2. Key Plots Summary
- `SSPOP_plddt.png`: pLDDT profile for SSPOP
- `SSPOP_pae.png`: PAE heatmap for SSPOP
- `CNNM2_plddt.png`: pLDDT profile for CNNM2
- `CNNM2_pae.png`: PAE heatmap for CNNM2
- `FBLN5_plddt.png`: pLDDT profile for FBLN5
- `FBLN5_pae.png`: PAE heatmap for FBLN5

## 3. Interpretation
**Family: Week6_Gravity_Expansion**
- **EMD**: EMD: Anisotropy=4.3, pLDDT=60. Highly extended/fibrous. Warning: Low confidence structure. Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **STOML3**: STOML3: Anisotropy=5.6, pLDDT=84. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **AQP4**: AQP4: Anisotropy=2.0, pLDDT=81. Intermediate shape.  Standard globular domain, likely biochemical role or node in network. (Conf: Medium). Test: Check expression timing relative to spine straightening.
- **SSPOP**: SSPOP: Anisotropy=1.9, pLDDT=60. Intermediate shape. Warning: Low confidence structure. Detected 31 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.
- **ROCK1**: ROCK1: Anisotropy=3.3, pLDDT=76. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.
- **DZIP1**: DZIP1: Anisotropy=2.5, pLDDT=64. Intermediate shape. Warning: Low confidence structure. Standard globular domain, likely biochemical role or node in network. (Conf: Low). Test: Check expression timing relative to spine straightening.
- **MYLK**: MYLK: Anisotropy=1.5, pLDDT=66. Globular/Compact. Warning: Low confidence structure. Detected 31 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.
- **PANX3**: PANX3: Anisotropy=5.1, pLDDT=82. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **FBLN5**: FBLN5: Anisotropy=7.1, pLDDT=83. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **GDF5**: GDF5: Anisotropy=3.0, pLDDT=70. Intermediate shape. Warning: Low confidence structure. Detected 16 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.
- **CNNM2**: CNNM2: Anisotropy=8.5, pLDDT=70. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **BNC2**: BNC2: Anisotropy=2.0, pLDDT=53. Intermediate shape. Warning: Low confidence structure. Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.


## 4. Best Next Move
Cluster by geometry and correlate curvature metrics with known phenotype genes.

## 5. Quality & Reproducibility Checklist
- Data Source: AlphaFold DB (fetched via scripts/02_fetch_afdb.py)
- Date/Time: 2026-01-23 19:31:25
- Code Version: 75af6c4
- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default
- Notes: 12 structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml
