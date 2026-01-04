# Bolt-BioFold ⚡ Analysis Report

## 1. Results Table
| Identity | Species | Length | pLDDT_mean | pLDDT_frac_low | PAE_mean | PAE_blockiness | Disorder_Proxy | Hinge_Cands | Rg | End_to_End | Curvature | Torsion | Anisotropy | Hotspots | Exposed_Frac | Charged_Patch | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ACAN (P16112) | Homo sapiens | 2530 | 51.9 | 0.73 | 26.3 | 5.01 | 0.54 | 26 | 59.8 | 24.4 | 0.288 | 1.909 | 1.33 | 2343:0.42; 2405:0.42; 109:0.41 | 0.56 | 0.41 | LowConf, MultiDomUncert, IDR_Heavy |
| ACTB (P60709) | Homo sapiens | 375 | 95.2 | 0.03 | 5.0 | 1.26 | 0.01 | 1 | 21.6 | 42.7 | 0.318 | 1.551 | 2.16 | 335:0.39; 265:0.39; 258:0.38 | 0.3 | 0.34 | OK |
| BMP4 (P12644) | Homo sapiens | 408 | 78.5 | 0.28 | 13.4 | 1.53 | 0.15 | 12 | 27.8 | 16.4 | 0.297 | 1.901 | 2.69 | 343:0.39; 329:0.38; 352:0.38 | 0.47 | 0.38 | MultiDomUncert |
| CDH2 (P19022) | Homo sapiens | 906 | 79.4 | 0.25 | 22.5 | 6.35 | 0.17 | 22 | 67.3 | 177.2 | 0.287 | 2.02 | 4.52 | 205:0.44; 176:0.43; 315:0.43 | 0.5 | 0.26 | MultiDomUncert |
| COL2A1 (P02458) | Homo sapiens | 1487 | 52.1 | 0.81 | 27.4 | 5.9 | 0.69 | 16 | 61.3 | 45.4 | 0.294 | 1.87 | 1.19 | 1327:0.42; 1454:0.39; 1282:0.38 | 0.87 | 0.28 | LowConf, MultiDomUncert, IDR_Heavy |
| IFT88 (Q13099) | Homo sapiens | 824 | 76.3 | 0.29 | 19.4 | 2.43 | 0.23 | 1 | 44.1 | 92.4 | 0.358 | 1.121 | 2.38 | 315:0.38; 643:0.38; 426:0.38 | 0.51 | 0.44 | MultiDomUncert |
| ITGB1 (P05556) | Homo sapiens | 798 | 85.9 | 0.11 | 18.2 | 4.9 | 0.03 | 10 | 46.6 | 94.9 | 0.305 | 1.725 | 2.79 | 193:0.39; 474:0.38; 521:0.38 | 0.34 | 0.35 | MultiDomUncert |
| KIF3A (Q9Y496) | Homo sapiens | 699 | 75.4 | 0.27 | 20.0 | 4.44 | 0.15 | 4 | 37.7 | 40.6 | 0.328 | 1.461 | 2.43 | 359:0.38; 43:0.38; 88:0.38 | 0.54 | 0.51 | MultiDomUncert |
| PTH1R (Q03431) | Homo sapiens | 593 | 71.0 | 0.41 | 19.5 | 2.87 | 0.3 | 0 | 45.3 | 10.6 | 0.343 | 1.136 | 3.02 | 186:0.38; 33:0.38; 298:0.38 | 0.64 | 0.32 | MultiDomUncert |
| SHH (Q15465) | Homo sapiens | 462 | 78.4 | 0.26 | 17.9 | 6.13 | 0.16 | 6 | 27.4 | 31.2 | 0.303 | 1.81 | 1.94 | 48:0.40; 259:0.39; 174:0.39 | 0.44 | 0.33 | MultiDomUncert |
| SOX9 (P48436) | Homo sapiens | 509 | 56.0 | 0.84 | 27.4 | 0.0 | 0.49 | 2 | 46.6 | 20.7 | 0.341 | 1.288 | 1.3 | 134:0.38; 147:0.38; 116:0.37 | 0.92 | 0.52 | LowConf, IDR_Heavy |
| TUBB (P07437) | Homo sapiens | 444 | 92.1 | 0.04 | 6.3 | 1.26 | 0.02 | 0 | 21.0 | 12.8 | 0.324 | 1.499 | 1.42 | 271:0.39; 61:0.39; 391:0.39 | 0.27 | 0.44 | OK |
| VIM (P08670) | Homo sapiens | 466 | 77.1 | 0.3 | 23.7 | 4.02 | 0.24 | 1 | 71.7 | 208.3 | 0.36 | 0.936 | 5.57 | 404:0.38; 318:0.38; 337:0.37 | 1.0 | 0.38 | MultiDomUncert |
| GAPDH (P04406) | Homo sapiens | 335 | 98.1 | 0.0 | 2.5 | 0.0 | 0.0 | 0 | 19.8 | 11.4 | 0.307 | 1.693 | 1.78 | 17:0.38; 216:0.38; 148:0.38 | 0.25 | 0.37 | OK |


## 2. Key Plots Summary
- Generated `/app/research/alphafold_countercurvature/data/processed/figures/quality_scatter.png`: Scatter plot of Length vs Confidence, sized by Anisotropy.
- Shows clear separation between globular domains (high conf, low aniso) and fibrous tails (often lower conf or very high aniso).

## 3. Interpretation
**Family: control**
- **GAPDH**: GAPDH: Anisotropy=1.8, pLDDT=98. Intermediate shape.  Standard globular domain, likely biochemical role or node in network. (Conf: High). Test: Check expression timing relative to spine straightening.

**Family: seed_Adhesion**
- **CDH2**: CDH2: Anisotropy=4.5, pLDDT=79. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **ITGB1**: ITGB1: Anisotropy=2.8, pLDDT=86. Intermediate shape.  Detected 10 potential flexible hinges; may act as mechanical sensor/switch. (Conf: High). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: seed_Cilia**
- **IFT88**: IFT88: Anisotropy=2.4, pLDDT=76. Intermediate shape.  Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.
- **KIF3A**: KIF3A: Anisotropy=2.4, pLDDT=75. Intermediate shape.  Detected 4 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: seed_Cytoskeleton**
- **ACTB**: ACTB: Anisotropy=2.2, pLDDT=95. Intermediate shape.  Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: High). Test: Mutate hinge region to test effect on mechanosensitivity.
- **TUBB**: TUBB: Anisotropy=1.4, pLDDT=92. Globular/Compact.  Standard globular domain, likely biochemical role or node in network. (Conf: High). Test: Check expression timing relative to spine straightening.
- **VIM**: VIM: Anisotropy=5.6, pLDDT=77. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: seed_ECM**
- **ACAN**: ACAN: Anisotropy=1.3, pLDDT=52. Globular/Compact. Warning: Low confidence structure. Detected 26 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.
- **COL2A1**: COL2A1: Anisotropy=1.2, pLDDT=52. Globular/Compact. Warning: Low confidence structure. Detected 16 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: seed_Growth_Plate**
- **PTH1R**: PTH1R: Anisotropy=3.0, pLDDT=71. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Check expression timing relative to spine straightening.
- **SOX9**: SOX9: Anisotropy=1.3, pLDDT=56. Globular/Compact. Warning: Low confidence structure. Detected 2 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: seed_Morphogens**
- **BMP4**: BMP4: Anisotropy=2.7, pLDDT=79. Intermediate shape.  Detected 12 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.
- **SHH**: SHH: Anisotropy=1.9, pLDDT=78. Intermediate shape.  Detected 6 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.


## 4. Best Next Move
Cluster by geometry and correlate curvature metrics with known phenotype genes.
