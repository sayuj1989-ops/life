# Bolt-BioFold ⚡ Analysis Report
Sources: Mechanotransduction,Proprioception, Somite,Muscle,Proprioception, Mechanotransduction,Hippo,Growth_Plate, Cilia,Centriole, Mechanotransduction,Adhesion, Segmentation,Somite, Mechanotransduction,Hippo, Cytoskeleton,Segmentation

## 1. Results Table
| Identity | Species | Length | pLDDT_mean | pLDDT_frac_low | PAE_mean | PAE_blockiness | Disorder_Proxy | Hinge_Cands | Rg | End_to_End | Curvature | Torsion | Anisotropy | Hotspots | Exposed_Frac | Charged_Patch | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PIEZO2 (Q9H5I5) | Homo sapiens | 709 | 79.4 | 0.21 | 17.0 | 2.8 | 0.14 | 0 | 48.6 | 28.4 | 0.329 | 1.428 | 3.45 | 460:0.38; 239:0.38; 138:0.38 | 0.56 | 0.25 | MultiDomUncert |
| LBX1 (P52954) | Homo sapiens | 281 | 66.9 | 0.61 | 25.1 | 7.35 | 0.26 | 0 | 37.0 | 51.9 | 0.343 | 1.173 | 1.76 | 83:0.39; 37:0.39; 34:0.38 | 0.93 | 0.36 | LowConf, MultiDomUncert |
| YAP1 (P46937) | Homo sapiens | 504 | 57.4 | 0.74 | 27.5 | 9.26 | 0.45 | 2 | 44.9 | 11.4 | 0.321 | 1.628 | 1.54 | 182:0.38; 241:0.38; 257:0.38 | 0.93 | 0.3 | LowConf, MultiDomUncert, IDR_Heavy |
| POC5 (Q8NA72) | Homo sapiens | 575 | 64.0 | 0.61 | 25.6 | 3.51 | 0.49 | 5 | 83.2 | 307.4 | 0.364 | 0.848 | 4.97 | 156:0.38; 247:0.38; 192:0.37 | 1.0 | 0.36 | LowConf, MultiDomUncert, IDR_Heavy |
| ITGB1 (P05556) | Homo sapiens | 798 | 85.9 | 0.11 | 18.2 | 4.9 | 0.03 | 10 | 46.6 | 94.9 | 0.305 | 1.725 | 2.79 | 193:0.39; 474:0.38; 521:0.38 | 0.34 | 0.35 | MultiDomUncert |
| MESP2 (Q0VG99) | Homo sapiens | 397 | 54.2 | 0.82 | 26.9 | 0.0 | 0.58 | 1 | 43.5 | 42.6 | 0.351 | 1.183 | 1.56 | 142:0.38; 85:0.38; 109:0.38 | 0.97 | 0.36 | LowConf, IDR_Heavy |
| WWTR1 (Q9GZV5) | Homo sapiens | 400 | 59.1 | 0.7 | 27.1 | 5.85 | 0.52 | 0 | 41.0 | 52.0 | 0.326 | 1.471 | 1.66 | 135:0.39; 42:0.38; 49:0.38 | 0.97 | 0.29 | LowConf, MultiDomUncert, IDR_Heavy |
| ADGRG6 (Q86SQ4) | Homo sapiens | 1221 | 73.7 | 0.3 | 24.4 | 6.78 | 0.15 | 12 | 55.0 | 50.9 | 0.308 | 1.633 | 2.8 | 57:0.43; 530:0.39; 247:0.39 | 0.44 | 0.25 | MultiDomUncert |
| FLNB (O75369) | Homo sapiens | 2602 | 76.3 | 0.24 | 27.0 | 8.93 | 0.04 | 158 | 55.0 | 35.9 | 0.277 | 2.133 | 2.06 | 1505:0.44; 2595:0.43; 1409:0.42 | 0.28 | 0.41 | MultiDomUncert |

### CSV Block
```csv
Identity,Species,Length,pLDDT_mean,pLDDT_frac_low,PAE_mean,PAE_blockiness,Disorder_Proxy,Hinge_Cands,Rg,End_to_End,Curvature,Torsion,Anisotropy,Hotspots,Exposed_Frac,Charged_Patch,Flags
PIEZO2 (Q9H5I5),Homo sapiens,709,79.4,0.21,17.0,2.8,0.14,0,48.6,28.4,0.329,1.428,3.45,460:0.38; 239:0.38; 138:0.38,0.56,0.25,MultiDomUncert
LBX1 (P52954),Homo sapiens,281,66.9,0.61,25.1,7.35,0.26,0,37.0,51.9,0.343,1.173,1.76,83:0.39; 37:0.39; 34:0.38,0.93,0.36,"LowConf, MultiDomUncert"
YAP1 (P46937),Homo sapiens,504,57.4,0.74,27.5,9.26,0.45,2,44.9,11.4,0.321,1.628,1.54,182:0.38; 241:0.38; 257:0.38,0.93,0.3,"LowConf, MultiDomUncert, IDR_Heavy"
POC5 (Q8NA72),Homo sapiens,575,64.0,0.61,25.6,3.51,0.49,5,83.2,307.4,0.364,0.848,4.97,156:0.38; 247:0.38; 192:0.37,1.0,0.36,"LowConf, MultiDomUncert, IDR_Heavy"
ITGB1 (P05556),Homo sapiens,798,85.9,0.11,18.2,4.9,0.03,10,46.6,94.9,0.305,1.725,2.79,193:0.39; 474:0.38; 521:0.38,0.34,0.35,MultiDomUncert
MESP2 (Q0VG99),Homo sapiens,397,54.2,0.82,26.9,0.0,0.58,1,43.5,42.6,0.351,1.183,1.56,142:0.38; 85:0.38; 109:0.38,0.97,0.36,"LowConf, IDR_Heavy"
WWTR1 (Q9GZV5),Homo sapiens,400,59.1,0.7,27.1,5.85,0.52,0,41.0,52.0,0.326,1.471,1.66,135:0.39; 42:0.38; 49:0.38,0.97,0.29,"LowConf, MultiDomUncert, IDR_Heavy"
ADGRG6 (Q86SQ4),Homo sapiens,1221,73.7,0.3,24.4,6.78,0.15,12,55.0,50.9,0.308,1.633,2.8,57:0.43; 530:0.39; 247:0.39,0.44,0.25,MultiDomUncert
FLNB (O75369),Homo sapiens,2602,76.3,0.24,27.0,8.93,0.04,158,55.0,35.9,0.277,2.133,2.06,1505:0.44; 2595:0.43; 1409:0.42,0.28,0.41,MultiDomUncert

```

## 2. Key Plots Summary
- Generated `/app/research/alphafold_countercurvature/data/processed/figures/quality_scatter.png`: Scatter plot of Length vs Confidence, sized by Anisotropy.
- Shows clear separation between globular domains (high conf, low aniso) and fibrous tails (often lower conf or very high aniso).


## 3. Interpretation
**Family: Cilia,Centriole**
- **POC5**: POC5: Anisotropy=5.0, pLDDT=64. Highly extended/fibrous. Warning: Low confidence structure. Detected 5 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: Cytoskeleton,Segmentation**
- **FLNB**: FLNB: Anisotropy=2.1, pLDDT=76. Intermediate shape.  Detected 158 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Mechanotransduction,Adhesion**
- **ITGB1**: ITGB1: Anisotropy=2.8, pLDDT=86. Intermediate shape.  Detected 10 potential flexible hinges; may act as mechanical sensor/switch. (Conf: High). Test: Mutate hinge region to test effect on mechanosensitivity.
- **ADGRG6**: ADGRG6: Anisotropy=2.8, pLDDT=74. Intermediate shape.  Detected 12 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Mechanotransduction,Hippo**
- **WWTR1**: WWTR1: Anisotropy=1.7, pLDDT=59. Intermediate shape. Warning: Low confidence structure. Standard globular domain, likely biochemical role or node in network. (Conf: Low). Test: Check expression timing relative to spine straightening.

**Family: Mechanotransduction,Hippo,Growth_Plate**
- **YAP1**: YAP1: Anisotropy=1.5, pLDDT=57. Intermediate shape. Warning: Low confidence structure. Detected 2 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Mechanotransduction,Proprioception**
- **PIEZO2**: PIEZO2: Anisotropy=3.5, pLDDT=79. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Check expression timing relative to spine straightening.

**Family: Segmentation,Somite**
- **MESP2**: MESP2: Anisotropy=1.6, pLDDT=54. Intermediate shape. Warning: Low confidence structure. Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Somite,Muscle,Proprioception**
- **LBX1**: LBX1: Anisotropy=1.8, pLDDT=67. Intermediate shape. Warning: Low confidence structure. Standard globular domain, likely biochemical role or node in network. (Conf: Low). Test: Check expression timing relative to spine straightening.

## 4. Best Next Move
Add proteins: Expand search to include more cytoskeletal linkers.

## 5. Quality & Reproducibility Checklist
- Data Source: AlphaFold DB (fetched via scripts/02_fetch_afdb.py)
- Date/Time: 2026-01-08 22:01:27
- Code Version: f9289a2
- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default
- Notes: 9 structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml
