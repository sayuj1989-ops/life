[Output for brevity]

sts load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Mechanotransduction,Hippo,Growth_Plate**
- **YAP1**: YAP1: Anisotropy=2.0, pLDDT=57. Intermediate shape. Warning: Low confidence structure. Detected 2 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Mechanotransduction,Nucleus,Cytoskeleton**
- **LMNA**: LMNA: Anisotropy=4.8, pLDDT=76. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: Mechanotransduction,Proprioception**
- **PIEZO2**: PIEZO2: Anisotropy=4.4, pLDDT=79. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: Somite,Muscle,Proprioception**
- **LBX1**: LBX1: Anisotropy=2.3, pLDDT=67. Intermediate shape. Warning: Low confidence structure. Standard globular domain, likely biochemical role or node in network. (Conf: Low). Test: Check expression timing relative to spine straightening.


## 4. Best Next Move
Cluster by geometry and correlate curvature metrics with known phenotype genes.

## 5. Quality & Reproducibility Checklist
- Data Source: AlphaFold DB (fetched via scripts/02_fetch_afdb.py)
- Date/Time: 2026-01-14 21:36:09
- Code Version: 4e77d57
- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default
- Notes: 9 structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml

## 2026-01-16
- Processed 3/10 candidates.
- Top candidate for anisotropy: **PIEZO2** (4.44)
- Average pLDDT: 69.6
- 7 candidates missing from local archive.
# Bolt-BioFold ⚡ Analysis Report

Sources: Mechanotransduction, Somite, Cilia, Signaling, ECM

## 1. Results Table
| Identity | Species | Length | pLDDT_mean | pLDDT_frac_low | PAE_mean | PAE_blockiness | Disorder_Proxy | Hinge_Cands | Rg | End_to_End | Curvature | Torsion | Anisotropy | Principal_Axis | Hotspots | Exposed_Frac | Charged_Patch | Domains | Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PIEZO2 (Q9H5I5) | Homo sapiens | 709 | 79.4 | 0.21 | 17.0 | 2.8 | 0.14 | 0 | 43.4 | 28.4 | 0.329 | 1.428 | 4.44 | [-0.687, -0.068, 0.724] | 460:0.38; 239:0.38; 138:0.38 | 0.56 | 0.25 | 7 | MultiDomUncert |
| LBX1 (P52954) | Homo sapiens | 281 | 66.9 | 0.61 | 25.1 | 7.35 | 0.26 | 0 | 22.7 | 51.9 | 0.343 | 1.173 | 2.27 | [-0.222, -0.149, 0.964] | 83:0.39; 37:0.39; 34:0.38 | 0.93 | 0.36 | 3 | LowConf, MultiDomUncert |
| IFT88 (Q13099) | Homo sapiens | 824 | 76.3 | 0.29 | 19.4 | 2.43 | 0.23 | 1 | 38.3 | 92.4 | 0.358 | 1.121 | 2.8 | [-0.626, -0.157, 0.764] | 315:0.38; 643:0.38; 426:0.38 | 0.51 | 0.44 | 3 | MultiDomUncert |
| LMNA (P02545) | Homo sapiens | 664 | 76.4 | 0.31 | 24.9 | 2.56 | 0.26 | 0 | 71.2 | 278.1 | 0.344 | 1.194 | 4.75 | [-0.668, -0.244, 0.703] | 508:0.40; 519:0.39; 30:0.38 | 0.87 | 0.4 | 3 | MultiDomUncert |
| NF1 (P21359) | Homo sapiens | 593 | 87.2 | 0.11 | 9.5 | 2.42 | 0.07 | 1 | 26.1 | 40.7 | 0.35 | 1.116 | 1.93 | [-0.387, -0.133, 0.912] | 221:0.38; 178:0.38; 274:0.38 | 0.34 | 0.37 | 6 | OK |
| PIEZO1 (Q92508) | Homo sapiens | 2521 | 72.0 | 0.33 | 22.7 | 5.74 | 0.17 | 3 | 58.9 | 30.0 | 0.341 | 1.182 | 3.9 | [-0.270, -0.320, 0.908] | 458:0.44; 625:0.42; 513:0.41 | 0.46 | 0.27 | 35 | MultiDomUncert |
| POC5 (Q8NA72) | Homo sapiens | 575 | 64.0 | 0.61 | 25.6 | 3.51 | 0.49 | 5 | 87.3 | 307.4 | 0.364 | 0.848 | 24.69 | [-0.657, -0.161, 0.737] | 156:0.38; 247:0.38; 192:0.37 | 1.0 | 0.36 | 2 | LowConf, MultiDomUncert |
| ITGB1 (P05556) | Homo sapiens | 798 | 85.9 | 0.11 | 18.2 | 4.9 | 0.03 | 10 | 45.8 | 94.9 | 0.305 | 1.725 | 3.23 | [-0.504, -0.483, 0.716] | 193:0.39; 474:0.38; 521:0.38 | 0.34 | 0.35 | 10 | MultiDomUncert |
| COL1A1 (P02452) | Homo sapiens | 1464 | 52.7 | 0.8 | 27.4 | 6.55 | 0.67 | 16 | 23.5 | 49.0 | 0.295 | 1.859 | 2.8 | [-0.475, 0.297, 0.828] | 1315:0.39; 1258:0.38; 1431:0.38 | 0.87 | 0.3 | 3 | LowConf, MultiDomUncert |

### CSV Block
```csv
Identity,Species,Length,pLDDT_mean,pLDDT_frac_low,PAE_mean,PAE_blockiness,Disorder_Proxy,Hinge_Cands,Rg,End_to_End,Curvature,Torsion,Anisotropy,Principal_Axis,Hotspots,Exposed_Frac,Charged_Patch,Domains,Flags
PIEZO2 (Q9H5I5),Homo sapiens,709,79.4,0.21,17.0,2.8,0.14,0,43.4,28.4,0.329,1.428,4.44,"[-0.687, -0.068, 0.724]",460:0.38; 239:0.38; 138:0.38,0.56,0.25,7,MultiDomUncert
LBX1 (P52954),Homo sapiens,281,66.9,0.61,25.1,7.35,0.26,0,22.7,51.9,0.343,1.173,2.27,"[-0.222, -0.149, 0.964]",83:0.39; 37:0.39; 34:0.38,0.93,0.36,3,"LowConf, MultiDomUncert"
IFT88 (Q13099),Homo sapiens,824,76.3,0.29,19.4,2.43,0.23,1,38.3,92.4,0.358,1.121,2.8,"[-0.626, -0.157, 0.764]",315:0.38; 643:0.38; 426:0.38,0.51,0.44,3,MultiDomUncert
LMNA (P02545),Homo sapiens,664,76.4,0.31,24.9,2.56,0.26,0,71.2,278.1,0.344,1.194,4.75,"[-0.668, -0.244, 0.703]",508:0.40; 519:0.39; 30:0.38,0.87,0.4,3,MultiDomUncert
NF1 (P21359),Homo sapiens,593,87.2,0.11,9.5,2.42,0.07,1,26.1,40.7,0.35,1.116,1.93,"[-0.387, -0.133, 0.912]",221:0.38; 178:0.38; 274:0.38,0.34,0.37,6,OK
PIEZO1 (Q92508),Homo sapiens,2521,72.0,0.33,22.7,5.74,0.17,3,58.9,30.0,0.341,1.182,3.9,"[-0.270, -0.320, 0.908]",458:0.44; 625:0.42; 513:0.41,0.46,0.27,35,MultiDomUncert
POC5 (Q8NA72),Homo sapiens,575,64.0,0.61,25.6,3.51,0.49,5,87.3,307.4,0.364,0.848,24.69,"[-0.657, -0.161, 0.737]",156:0.38; 247:0.38; 192:0.37,1.0,0.36,2,"LowConf, MultiDomUncert"
ITGB1 (P05556),Homo sapiens,798,85.9,0.11,18.2,4.9,0.03,10,45.8,94.9,0.305,1.725,3.23,"[-0.504, -0.483, 0.716]",193:0.39; 474:0.38; 521:0.38,0.34,0.35,10,MultiDomUncert
COL1A1 (P02452),Homo sapiens,1464,52.7,0.8,27.4,6.55,0.67,16,23.5,49.0,0.295,1.859,2.8,"[-0.475, 0.297, 0.828]",1315:0.39; 1258:0.38; 1431:0.38,0.87,0.3,3,"LowConf, MultiDomUncert"
```

## 2. Key Plots Summary
- `LMNA_plddt.png`: pLDDT profile for LMNA
- `LMNA_pae.png`: PAE heatmap for LMNA
- `COL1A1_plddt.png`: pLDDT profile for COL1A1
- `COL1A1_pae.png`: PAE heatmap for COL1A1
- `POC5_plddt.png`: pLDDT profile for POC5
- `POC5_pae.png`: PAE heatmap for POC5

## 3. Interpretation
**Family: Cilia**
- **IFT88**: IFT88: Anisotropy=2.8, pLDDT=76. Intermediate shape.  Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.
- **POC5**: POC5: Anisotropy=24.7, pLDDT=64. Highly extended/fibrous. Warning: Low confidence structure. Detected 5 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Verify fiber formation in vivo; test mechanical stiffness.

**Family: ECM**
- **COL1A1**: COL1A1: Anisotropy=2.8, pLDDT=53. Intermediate shape. Warning: Low confidence structure. Detected 16 potential flexible hinges; may act as mechanical sensor/switch. (Conf: Low). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Mechanotransduction**
- **PIEZO2**: PIEZO2: Anisotropy=4.4, pLDDT=79. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **LMNA**: LMNA: Anisotropy=4.8, pLDDT=76. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Verify fiber formation in vivo; test mechanical stiffness.
- **PIEZO1**: PIEZO1: Anisotropy=3.9, pLDDT=72. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: Medium). Test: Mutate hinge region to test effect on mechanosensitivity.
- **ITGB1**: ITGB1: Anisotropy=3.2, pLDDT=86. Highly extended/fibrous.  Rigid rod-like geometry suggests load-bearing capacity or long-range connectivity. (Conf: High). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Signaling**
- **NF1**: NF1: Anisotropy=1.9, pLDDT=87. Intermediate shape.  Detected 1 potential flexible hinges; may act as mechanical sensor/switch. (Conf: High). Test: Mutate hinge region to test effect on mechanosensitivity.

**Family: Somite**
- **LBX1**: LBX1: Anisotropy=2.3, pLDDT=67. Intermediate shape. Warning: Low confidence structure. Standard globular domain, likely biochemical role or node in network. (Conf: Low). Test: Check expression timing relative to spine straightening.


## 4. Best Next Move
Cluster by geometry and correlate curvature metrics with known phenotype genes.

## 5. Quality & Reproducibility Checklist
- Data Source: AlphaFold DB (fetched via scripts/02_fetch_afdb.py)
- Date/Time: 2026-01-18 22:01:17
- Code Version: 5ca3b1d
- Parameters: pLDDT threshold >= 70 for geometry; Smoothing window = default
- Notes: 9 structures analyzed. Source config: research/alphafold_countercurvature/config/targets.yaml
# AFCC Daily Refresh: 2026-01-20

## Run Summary
- **Candidates Processed**: 9
- **Top Candidate**: LMNA (Anisotropy: 4.75)
- **Failed/Missing**: FBN1 (Not found in AFDB)

## Top 5 High-Anisotropy Structures
| Gene | Anisotropy | pLDDT (Mean) | Morphology |
|------|------------|--------------|------------|
| LMNA | 4.75 | 76.4 | Fibrous/Extended |
| PIEZO2 | 4.44 | 79.4 | Fibrous/Extended |
| PIEZO1 | 3.90 | 72.0 | Fibrous/Extended |
| IFT88 | 2.80 | 76.3 | Intermediate |
| COL1A1 | 2.80 | 52.7 | Intermediate |

## Key Observations
- **Tension Rods**: LMNA and PIEZO2 continue to show high anisotropy (>4.0), consistent with the "Tension Rod" hypothesis.
- **Structural Confidence**: COL1A1 shows low confidence (pLDDT ~52.7), suggesting it may be unstructured or poorly predicted in isolation.
- **PIEZO Divergence**: PIEZO1 (3.90) is less anisotropic than PIEZO2 (4.44), supporting the Scalar vs Vector sensor dichotomy.

## 2026-01-21: Daily Refresh (Top 10 Candidates)

**Summary:**
- **Processed:** 10 candidates selected.
- **Downloaded:** 9/10 (FBN1 missing in AFDB).
- **Analysis:** Metrics computed for 9 structures.

**Key Findings:**
- **High Anisotropy:** POC5 (24.7), LMNA (4.8), PIEZO2 (4.4).
- **Clusters:**
    - *Cluster 0 (Tension Rods):* PIEZO2, LMNA, PIEZO1 (High Anisotropy, Low Blockiness).
    - *Cluster 1 (Blocky Scaffolds):* LBX1, FLNA, COL1A1 (High Blockiness).
    - *Cluster 2 (Globular/Mixed):* IFT88, NF1.
- **Insight:** PIEZO1 groups with PIEZO2 in "Tension Rods" based on anisotropy (3.90), reinforcing the dichotomy but suggesting they share structural elongation traits despite different sensing modes (Scalar vs Vector).

**Outputs:**
- [Metrics CSV](outputs/afcc/2026-01-21/metrics.csv)
- [Summary Report](outputs/afcc/2026-01-21/summary.md)


## 2026-01-23: Daily Refresh (Top 10 Candidates)

**Summary:**
- **Processed:** 10 candidates selected.
- **Downloaded:** 8/10 (2 missing/failed).
- **Analysis:** Metrics computed for 8 structures.

**Key Findings:**
- **Top Anisotropy:** **LMNA** (4.75)
- **High Anisotropy (>4.0):** PIEZO2, LMNA, EMD

**Outputs:**
- [Metrics CSV](research/alphafold_countercurvature/outputs/afcc/2026-01-23/metrics.csv)
- [Summary Report](research/alphafold_countercurvature/outputs/afcc/2026-01-23/summary.md)
- [Failure Log](research/alphafold_countercurvature/outputs/afcc/2026-01-23/failure.md)
