# Bolt-BioFold ⚡ Analysis Report

Sources: Bolt_Seed_List

## 1. Results Table
| Identity | Species | Length | pLDDT_mean | pLDDT_median | pLDDT_frac_high | pLDDT_frac_ok | pLDDT_frac_low | PAE_mean | PAE_blockiness | Disorder_Proxy | Hinge_Cands | Rg | End_to_End | Curvature | Torsion | Anisotropy | Principal_Axis | Hotspots | Exposed_Frac | Charged_Patch | Domains | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PIEZO2 (Q9H5I5) | Homo sapiens | 709 | 79.4 | 88.4 | 0.42 | 0.37 | 0.21 | 17.0 | 2.8 | 0.14 | 0 | 43.4 | 28.4 | 0.329 | 1.428 | 4.44 | [-0.687, -0.068, 0.724] | 460:0.38; 239:0.38; 138:0.38 | 0.56 | 0.25 | 7 | MultiDomUncert |
| LMNA (P02545) | Homo sapiens | 664 | 76.4 | 93.1 | 0.58 | 0.11 | 0.31 | 24.9 | 2.56 | 0.26 | 0 | 71.2 | 278.1 | 0.344 | 1.194 | 4.75 | [-0.668, -0.244, 0.703] | 508:0.40; 519:0.39; 30:0.38 | 0.87 | 0.4 | 3 | MultiDomUncert |
| EGR3 (Q06889) | Homo sapiens | 387 | 50.0 | 37.9 | 0.13 | 0.11 | 0.75 | 25.9 | 0.0 | 0.64 | 2 | 18.5 | 42.9 | 0.331 | 1.631 | 3.76 | [-0.453, -0.341, 0.824] | 226:0.38; 300:0.38; 323:0.38 | 0.87 | 0.54 | 1 | LowConf |
| RUNX3 (Q13761) | Homo sapiens | 415 | 60.6 | 46.3 | 0.28 | 0.04 | 0.68 | 25.6 | 0.0 | 0.56 | 12 | 15.8 | 53.0 | 0.284 | 1.965 | 2.06 | [-0.510, 0.008, 0.860] | 159:0.39; 69:0.38; 54:0.38 | 0.78 | 0.37 | 1 | LowConf |

### CSV Block
```csv
Identity,Species,Length,pLDDT_mean,pLDDT_median,pLDDT_frac_high,pLDDT_frac_ok,pLDDT_frac_low,PAE_mean,PAE_blockiness,Disorder_Proxy,Hinge_Cands,Rg,End_to_End,Curvature,Torsion,Anisotropy,Principal_Axis,Hotspots,Exposed_Frac,Charged_Patch,Domains,Flags
PIEZO2 (Q9H5I5),Homo sapiens,709,79.4,88.4,0.42,0.37,0.21,17.0,2.8,0.14,0,43.4,28.4,0.329,1.428,4.44,"[-0.687, -0.068, 0.724]",460:0.38; 239:0.38; 138:0.38,0.56,0.25,7,MultiDomUncert
LMNA (P02545),Homo sapiens,664,76.4,93.1,0.58,0.11,0.31,24.9,2.56,0.26,0,71.2,278.1,0.344,1.194,4.75,"[-0.668, -0.244, 0.703]",508:0.40; 519:0.39; 30:0.38,0.87,0.4,3,MultiDomUncert
EGR3 (Q06889),Homo sapiens,387,50.0,37.9,0.13,0.11,0.75,25.9,0.0,0.64,2,18.5,42.9,0.331,1.631,3.76,"[-0.453, -0.341, 0.824]",226:0.38; 300:0.38; 323:0.38,0.87,0.54,1,LowConf
RUNX3 (Q13761),Homo sapiens,415,60.6,46.3,0.28,0.04,0.68,25.6,0.0,0.56,12,15.8,53.0,0.284,1.965,2.06,"[-0.510, 0.008, 0.860]",159:0.39; 69:0.38; 54:0.38,0.78,0.37,1,LowConf
```

## 2. Key Plots Summary
- `RUNX3_plddt.png`: pLDDT profile for RUNX3
- `RUNX3_pae.png`: PAE heatmap for RUNX3
- `PIEZO2_plddt.png`: pLDDT profile for PIEZO2
- `PIEZO2_pae.png`: PAE heatmap for PIEZO2
- `LMNA_plddt.png`: pLDDT profile for LMNA
- `LMNA_pae.png`: PAE heatmap for LMNA

## 3. Interpretation
**Family: Bolt_Seed_List**
- **PIEZO2**: PIEZO2: Anisotropy=4.4, pLDDT=79. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **LMNA**: LMNA: Anisotropy=4.8, pLDDT=76. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **EGR3**: EGR3: Anisotropy=3.8, pLDDT=50. Highly extended/fibrous. Warning: Low confidence structure. Detected 2 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.
- **RUNX3**: RUNX3: Anisotropy=2.1, pLDDT=61. Intermediate shape. Warning: Low confidence structure. Detected 12 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.


## 4. Best Next Move
Cluster by geometry and correlate curvature metrics with known phenotype genes.

## 5. Quality & Reproducibility Checklist
- Data Source: AlphaFold DB (fetched via scripts/02_fetch_afdb.py)
- Date/Time: 2026-02-04 19:26:17
- Code Version: 646c850
- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default
- Notes: 4 structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml
