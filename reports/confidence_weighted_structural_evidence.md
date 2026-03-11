# Confidence-Weighted Structural Evidence

## Overview
This report re-ranks AlphaFold structural proxy metrics with explicit confidence weighting. A major vulnerability in previous cluster analyses was treating high-anisotropy artifacts (arising from long unstructured regions) equally with rigidly structured tension rods.
Authoritative snapshot: `outputs/afcc/2026-02-16/metrics.csv`

## 1. High-Anisotropy + Adequate-Confidence Candidates
**Threshold**: `Anisotropy >= 3.0` AND `pLDDT >= 70.0`
**Significance**: These represent structurally certain, elongated architectures capable of transmitting mechanical force.

- **CNNM2**: Anisotropy = 8.54, pLDDT = 70.4, PAE Blockiness = 4.83
- **FBLN5**: Anisotropy = 7.05, pLDDT = 83.3, PAE Blockiness = 3.55
- **STOML3**: Anisotropy = 5.56, pLDDT = 84.3, PAE Blockiness = 0.00
- **PANX3**: Anisotropy = 5.08, pLDDT = 81.7, PAE Blockiness = 2.77
- **PIEZO2**: Anisotropy = 4.44, pLDDT = 79.4, PAE Blockiness = 2.80
- **ROCK1**: Anisotropy = 3.29, pLDDT = 76.1, PAE Blockiness = 4.95
- **ADGRG6**: Anisotropy = 3.06, pLDDT = 73.7, PAE Blockiness = 6.78

## 2. High-Anisotropy + Low-Confidence Candidates (Exploratory Only)
**Threshold**: `Anisotropy >= 3.0` AND `pLDDT < 70.0`
**Significance**: High anisotropy here is often an artifact of unfolded loops extended by AlphaFold without structural context. These are strictly hypothesis-generating and cannot be used as primary evidence for tension rods.

- **POC5**: Anisotropy = 24.69, pLDDT = 64.0, PAE Blockiness = 3.51
- **GHR**: Anisotropy = 5.13, pLDDT = 58.7, PAE Blockiness = 5.31
- **EMD**: Anisotropy = 4.29, pLDDT = 60.3, PAE Blockiness = 9.13
- **MESP2**: Anisotropy = 4.03, pLDDT = 54.2, PAE Blockiness = 0.00
- **ARNTL**: Anisotropy = 3.32, pLDDT = 65.5, PAE Blockiness = 3.59

## 3. LBX1 Comparator Analysis
Comparison of LBX1 against reference mechanosensors and low-confidence outliers:

- **POC5**: Anisotropy=24.69, pLDDT=64.0 (Low (<70)) -> Low Confidence Artifact Warning
- **GHR**: Anisotropy=5.13, pLDDT=58.7 (Low (<70)) -> Low Confidence Artifact Warning
- **PIEZO2**: Anisotropy=4.44, pLDDT=79.4 (Adequate (>=70)) -> Reliable Structural Model
- **ADGRG6**: Anisotropy=3.06, pLDDT=73.7 (Adequate (>=70)) -> Reliable Structural Model
- **LBX1**: Anisotropy=2.27, pLDDT=66.9 (Low (<70)) -> Core Target - Low Confidence, Intermediate Anisotropy

*Note: LMNA is absent from the 2026-02-16 snapshot, though historical records show Anisotropy=4.75, pLDDT=76.4.*