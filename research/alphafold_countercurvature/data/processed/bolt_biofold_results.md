# Bolt-BioFold ⚡ Analysis Report

Sources: Mechanotransduction, Proprioception, Nucleus, Cilia, ECM

## 1. Results Table
| Identity | Species | Length | pLDDT_mean | pLDDT_median | pLDDT_frac_high | pLDDT_frac_ok | pLDDT_frac_low | PAE_mean | PAE_blockiness | Disorder_Proxy | Hinge_Cands | Rg | End_to_End | Curvature | Torsion | Anisotropy | Principal_Axis | Hotspots | Exposed_Frac | Charged_Patch | Domains | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PIEZO2 (Q9H5I5) | Homo sapiens | 709 | 79.4 | 88.4 | 0.42 | 0.37 | 0.21 | 17.0 | 2.8 | 0.14 | 0 | 43.4 | 28.4 | 0.329 | 1.428 | 4.44 | [-0.687, -0.068, 0.724] | 460:0.38; 239:0.38; 138:0.38 | 0.56 | 0.25 | 7 | MultiDomUncert |
| LBX1 (P52954) | Homo sapiens | 281 | 66.9 | 60.2 | 0.23 | 0.16 | 0.61 | 25.1 | 7.35 | 0.26 | 0 | 22.7 | 51.9 | 0.343 | 1.173 | 2.27 | [-0.222, -0.149, 0.964] | 83:0.39; 37:0.39; 34:0.38 | 0.93 | 0.36 | 3 | LowConf, MultiDomUncert |
| LMNA (P02545) | Homo sapiens | 664 | 76.4 | 93.1 | 0.58 | 0.11 | 0.31 | 24.9 | 2.56 | 0.26 | 0 | 71.2 | 278.1 | 0.344 | 1.194 | 4.75 | [-0.668, -0.244, 0.703] | 508:0.40; 519:0.39; 30:0.38 | 0.87 | 0.4 | 3 | MultiDomUncert |
| KIF3A (Q9Y496) | Homo sapiens | 699 | 75.4 | 83.1 | 0.21 | 0.52 | 0.27 | 20.0 | 4.44 | 0.15 | 4 | 31.6 | 40.6 | 0.328 | 1.461 | 2.9 | [-0.608, -0.163, 0.777] | 359:0.38; 43:0.38; 88:0.38 | 0.54 | 0.51 | 12 | MultiDomUncert |
| COL12A1 (Q99715) | Homo sapiens | 1899 | 75.6 | 84.3 | 0.22 | 0.54 | 0.24 | 25.7 | 6.27 | 0.18 | 41 | 63.1 | 6.0 | 0.279 | 2.024 | 4.14 | [-0.633, -0.197, 0.749] | 1310:0.43; 979:0.39; 1205:0.39 | 0.4 | 0.4 | 29 | MultiDomUncert |

### CSV Block
```csv
Identity,Species,Length,pLDDT_mean,pLDDT_median,pLDDT_frac_high,pLDDT_frac_ok,pLDDT_frac_low,PAE_mean,PAE_blockiness,Disorder_Proxy,Hinge_Cands,Rg,End_to_End,Curvature,Torsion,Anisotropy,Principal_Axis,Hotspots,Exposed_Frac,Charged_Patch,Domains,Flags
PIEZO2 (Q9H5I5),Homo sapiens,709,79.4,88.4,0.42,0.37,0.21,17.0,2.8,0.14,0,43.4,28.4,0.329,1.428,4.44,"[-0.687, -0.068, 0.724]",460:0.38; 239:0.38; 138:0.38,0.56,0.25,7,MultiDomUncert
LBX1 (P52954),Homo sapiens,281,66.9,60.2,0.23,0.16,0.61,25.1,7.35,0.26,0,22.7,51.9,0.343,1.173,2.27,"[-0.222, -0.149, 0.964]",83:0.39; 37:0.39; 34:0.38,0.93,0.36,3,"LowConf, MultiDomUncert"
LMNA (P02545),Homo sapiens,664,76.4,93.1,0.58,0.11,0.31,24.9,2.56,0.26,0,71.2,278.1,0.344,1.194,4.75,"[-0.668, -0.244, 0.703]",508:0.40; 519:0.39; 30:0.38,0.87,0.4,3,MultiDomUncert
KIF3A (Q9Y496),Homo sapiens,699,75.4,83.1,0.21,0.52,0.27,20.0,4.44,0.15,4,31.6,40.6,0.328,1.461,2.9,"[-0.608, -0.163, 0.777]",359:0.38; 43:0.38; 88:0.38,0.54,0.51,12,MultiDomUncert
COL12A1 (Q99715),Homo sapiens,1899,75.6,84.3,0.22,0.54,0.24,25.7,6.27,0.18,41,63.1,6.0,0.279,2.024,4.14,"[-0.633, -0.197, 0.749]",1310:0.43; 979:0.39; 1205:0.39,0.4,0.4,29,MultiDomUncert
```

## 2. Key Plots Summary
- `LMNA_plddt.png`: pLDDT profile for LMNA
- `LMNA_pae.png`: PAE heatmap for LMNA
- `COL12A1_plddt.png`: pLDDT profile for COL12A1
- `COL12A1_pae.png`: PAE heatmap for COL12A1
- `PIEZO2_plddt.png`: pLDDT profile for PIEZO2
- `PIEZO2_pae.png`: PAE heatmap for PIEZO2

## 3. Interpretation
**Family: Cilia**
- **KIF3A**: KIF3A: Anisotropy=2.9, pLDDT=75. Intermediate shape.  Detected 4 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: ECM**
- **COL12A1**: COL12A1: Anisotropy=4.1, pLDDT=76. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: Mechanotransduction**
- **PIEZO2**: PIEZO2: Anisotropy=4.4, pLDDT=79. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: Nucleus**
- **LMNA**: LMNA: Anisotropy=4.8, pLDDT=76. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: Proprioception**
- **LBX1**: LBX1: Anisotropy=2.3, pLDDT=67. Intermediate shape. Warning: Low confidence structure. Standard globular domain, likely biochemical role or node in network. (Conf: Low). Test: Check expression timing relative to spine straightening.


## 4. Best Next Move
Cluster by geometry and correlate curvature metrics with known phenotype genes.

## 5. Quality & Reproducibility Checklist
- Data Source: AlphaFold DB (fetched via scripts/02_fetch_afdb.py)
- Date/Time: 2026-02-03 19:23:38
- Code Version: 646c850
- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default
- Notes: 5 structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml
