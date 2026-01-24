# Bolt-BioFold ⚡ Analysis Report

Sources: seed_Scoliosis_Drivers, seed_Week6_Expansion, seed_Mechanosensors

## 1. Results Table
| Identity | Species | Length | pLDDT_mean | pLDDT_frac_low | PAE_mean | PAE_blockiness | Disorder_Proxy | Hinge_Cands | Rg | End_to_End | Curvature | Torsion | Anisotropy | Principal_Axis | Hotspots | Exposed_Frac | Charged_Patch | Domains | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADGRG6 (Q86SQ4) | Homo sapiens | 1221 | 73.7 | 0.3 | 24.4 | 6.78 | 0.15 | 12 | 51.3 | 50.9 | 0.308 | 1.633 | 3.06 | [-0.749, -0.252, 0.613] | 57:0.43; 530:0.39; 247:0.39 | 0.44 | 0.25 | 23 | MultiDomUncert |
| AQP4 (P55087) | Homo sapiens | 323 | 81.0 | 0.25 | 13.9 | 5.21 | 0.2 | 0 | 18.4 | 25.2 | 0.345 | 1.185 | 1.97 | [-0.766, -0.254, 0.590] | 211:0.39; 188:0.38; 95:0.38 | 0.45 | 0.3 | 2 | MultiDomUncert |
| STOML3 (Q8TAV4) | Homo sapiens | 291 | 84.3 | 0.18 | 13.6 | 0.0 | 0.1 | 0 | 36.6 | 106.3 | 0.326 | 1.44 | 5.56 | [-0.750, -0.272, 0.602] | 43:0.38; 70:0.38; 64:0.37 | 0.6 | 0.24 | 1 | OK |
| SSPOP (A2VEC9) | Homo sapiens | 1317 | 60.1 | 0.57 | 27.2 | 8.62 | 0.35 | 31 | 44.2 | 33.5 | 0.304 | 1.771 | 1.92 | [-0.549, -0.107, 0.829] | 37:0.39; 82:0.38; 83:0.38 | 0.6 | 0.29 | 20 | LowConf, MultiDomUncert |
| ROCK1 (Q13464) | Homo sapiens | 1354 | 76.1 | 0.28 | 24.3 | 4.95 | 0.1 | 3 | 66.6 | 47.6 | 0.333 | 1.329 | 3.29 | [-0.484, -0.440, 0.757] | 1157:0.39; 1269:0.39; 131:0.38 | 0.71 | 0.45 | 13 | MultiDomUncert |
| PTK7 (Q13308) | Homo sapiens | 1070 | 82.7 | 0.14 | 22.5 | 4.53 | 0.09 | 20 | 62.9 | 72.4 | 0.284 | 1.955 | 7.45 | [-0.582, 0.048, 0.812] | 155:0.42; 869:0.42; 618:0.41 | 0.39 | 0.34 | 9 | MultiDomUncert |
| POC5 (Q8NA72) | Homo sapiens | 575 | 64.0 | 0.61 | 25.6 | 3.51 | 0.49 | 5 | 87.3 | 307.4 | 0.364 | 0.848 | 24.69 | [-0.657, -0.161, 0.737] | 156:0.38; 247:0.38; 192:0.37 | 1.0 | 0.36 | 2 | LowConf, MultiDomUncert |
| PIEZO2 (Q9H5I5) | Homo sapiens | 709 | 79.4 | 0.21 | 17.0 | 2.8 | 0.14 | 0 | 43.4 | 28.4 | 0.329 | 1.428 | 4.44 | [-0.687, -0.068, 0.724] | 460:0.38; 239:0.38; 138:0.38 | 0.56 | 0.25 | 7 | MultiDomUncert |

### CSV Block
```csv
Identity,Species,Length,pLDDT_mean,pLDDT_frac_low,PAE_mean,PAE_blockiness,Disorder_Proxy,Hinge_Cands,Rg,End_to_End,Curvature,Torsion,Anisotropy,Principal_Axis,Hotspots,Exposed_Frac,Charged_Patch,Domains,Flags
ADGRG6 (Q86SQ4),Homo sapiens,1221,73.7,0.3,24.4,6.78,0.15,12,51.3,50.9,0.308,1.633,3.06,"[-0.749, -0.252, 0.613]",57:0.43; 530:0.39; 247:0.39,0.44,0.25,23,MultiDomUncert
AQP4 (P55087),Homo sapiens,323,81.0,0.25,13.9,5.21,0.2,0,18.4,25.2,0.345,1.185,1.97,"[-0.766, -0.254, 0.590]",211:0.39; 188:0.38; 95:0.38,0.45,0.3,2,MultiDomUncert
STOML3 (Q8TAV4),Homo sapiens,291,84.3,0.18,13.6,0.0,0.1,0,36.6,106.3,0.326,1.44,5.56,"[-0.750, -0.272, 0.602]",43:0.38; 70:0.38; 64:0.37,0.6,0.24,1,OK
SSPOP (A2VEC9),Homo sapiens,1317,60.1,0.57,27.2,8.62,0.35,31,44.2,33.5,0.304,1.771,1.92,"[-0.549, -0.107, 0.829]",37:0.39; 82:0.38; 83:0.38,0.6,0.29,20,"LowConf, MultiDomUncert"
ROCK1 (Q13464),Homo sapiens,1354,76.1,0.28,24.3,4.95,0.1,3,66.6,47.6,0.333,1.329,3.29,"[-0.484, -0.440, 0.757]",1157:0.39; 1269:0.39; 131:0.38,0.71,0.45,13,MultiDomUncert
PTK7 (Q13308),Homo sapiens,1070,82.7,0.14,22.5,4.53,0.09,20,62.9,72.4,0.284,1.955,7.45,"[-0.582, 0.048, 0.812]",155:0.42; 869:0.42; 618:0.41,0.39,0.34,9,MultiDomUncert
POC5 (Q8NA72),Homo sapiens,575,64.0,0.61,25.6,3.51,0.49,5,87.3,307.4,0.364,0.848,24.69,"[-0.657, -0.161, 0.737]",156:0.38; 247:0.38; 192:0.37,1.0,0.36,2,"LowConf, MultiDomUncert"
PIEZO2 (Q9H5I5),Homo sapiens,709,79.4,0.21,17.0,2.8,0.14,0,43.4,28.4,0.329,1.428,4.44,"[-0.687, -0.068, 0.724]",460:0.38; 239:0.38; 138:0.38,0.56,0.25,7,MultiDomUncert
```

## 2. Key Plots Summary
- `PTK7_plddt.png`: pLDDT profile for PTK7
- `PTK7_pae.png`: PAE heatmap for PTK7
- `POC5_plddt.png`: pLDDT profile for POC5
- `POC5_pae.png`: PAE heatmap for POC5
- `SSPOP_plddt.png`: pLDDT profile for SSPOP
- `SSPOP_pae.png`: PAE heatmap for SSPOP

## 3. Interpretation
**Family: seed_Mechanosensors**
- **PIEZO2**: PIEZO2: Anisotropy=4.4, pLDDT=79. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: seed_Scoliosis_Drivers**
- **ADGRG6**: ADGRG6: Anisotropy=3.1, pLDDT=74. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.
- **PTK7**: PTK7: Anisotropy=7.4, pLDDT=83. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **POC5**: POC5: Anisotropy=24.7, pLDDT=64. Highly extended/fibrous. Warning: Low confidence structure. Detected 5 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: seed_Week6_Expansion**
- **AQP4**: AQP4: Anisotropy=2.0, pLDDT=81. Intermediate shape.  Standard globular domain, likely biochemical role or node in network. (Conf: Medium). Test: Check expression timing relative to spine straightening.
- **STOML3**: STOML3: Anisotropy=5.6, pLDDT=84. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **SSPOP**: SSPOP: Anisotropy=1.9, pLDDT=60. Intermediate shape. Warning: Low confidence structure. Detected 31 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.
- **ROCK1**: ROCK1: Anisotropy=3.3, pLDDT=76. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.


## 4. Best Next Move
Cluster by geometry and correlate curvature metrics with known phenotype genes.

## 5. Quality & Reproducibility Checklist
- Data Source: AlphaFold DB (fetched via scripts/02_fetch_afdb.py)
- Date/Time: 2026-01-24 21:43:34
- Code Version: 3f22850
- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default
- Notes: 8 structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml
