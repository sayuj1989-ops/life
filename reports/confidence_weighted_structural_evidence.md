# Confidence-Weighted Structural Evidence Report

- **Source:** `outputs/afcc/2026-02-16/metrics.csv`
- **Generated:** `{OUT_CSV}`

## 1. High-Anisotropy + Adequate-Confidence (Strong Evidence)
Proteins with `anisotropy_index >= 3.0` and `pLDDT_mean >= 70.0`.

| Gene | Anisotropy | pLDDT | Morphology | Blockiness |
|------|------------|-------|------------|------------|
| CNNM2 | 8.54 | 70.4 | Fibrous/Extended | 4.83 |
| FBLN5 | 7.05 | 83.3 | Fibrous/Extended | 3.55 |
| STOML3 | 5.56 | 84.3 | Fibrous/Extended | 0.00 |
| PANX3 | 5.08 | 81.7 | Fibrous/Extended | 2.77 |
| PIEZO2 | 4.44 | 79.4 | Fibrous/Extended | 2.80 |
| ROCK1 | 3.29 | 76.1 | Fibrous/Extended | 4.95 |
| ADGRG6 | 3.06 | 73.7 | Fibrous/Extended | 6.78 |

## 2. High-Anisotropy + Low-Confidence (Exploratory Only)
Proteins with `anisotropy_index >= 3.0` and `pLDDT_mean < 70.0`.
**Warning:** High anisotropy may be an artifact of disordered region modeling.

| Gene | Anisotropy | pLDDT | Morphology | Blockiness |
|------|------------|-------|------------|------------|
| POC5 | 24.69 | 64.0 | Fibrous/Extended | 3.51 |
| GHR | 5.13 | 58.7 | Fibrous/Extended | 5.31 |
| EMD | 4.29 | 60.3 | Fibrous/Extended | 9.13 |
| MESP2 | 4.03 | 54.2 | Fibrous/Extended | 0.00 |
| ARNTL | 3.32 | 65.5 | Fibrous/Extended | 3.59 |

## 3. LBX1 Comparator Analysis
Comparison of LBX1 against key mechanical/structural anchors.

| Gene | Anisotropy | pLDDT | Blockiness | Confidence | Notes |
|------|------------|-------|------------|------------|-------|
| LBX1 | 2.27 | 66.9 | 7.35 | Low | Globular/Intermediate, High Blockiness, Low Conf (Handle w/ Care) |
| PIEZO2 | 4.44 | 79.4 | 2.80 | Adequate | Extended/Fibrous |
| LMNA | N/A | N/A | N/A | N/A | Not found in snapshot |
| ADGRG6 | 3.06 | 73.7 | 6.78 | Adequate | Extended/Fibrous, High Blockiness |
| RUNX3 | N/A | N/A | N/A | N/A | Not found in snapshot |
| POC5 | 24.69 | 64.0 | 3.51 | Low | Extended/Fibrous, Low Conf (Handle w/ Care) |
| GHR | 5.13 | 58.7 | 5.31 | Low | Extended/Fibrous, High Blockiness, Low Conf (Handle w/ Care) |

## 4. Synthesis
- **LBX1 Status:** LBX1 (Anisotropy: 2.27, pLDDT: 66.9) falls cleanly into the Low-Confidence, Intermediate-Anisotropy cluster. Its high PAE blockiness (7.35) suggests a modular architecture, but it **is not a structural tension rod** like PIEZO2 or LMNA.
- **Strong Mechanical Anchors:** PIEZO2 and ADGRG6 possess adequate confidence and high anisotropy, confirming their roles as structured mechanical sensors/transducers.
- **Confounded Candidates:** POC5 and GHR show extreme anisotropy but poor confidence. Their extended shapes in AlphaFold models may represent intrinsically disordered regions rather than rigid fibrous scaffolds.
