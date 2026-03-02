# Biological Countercurvature Claims Matrix

## Overview
This matrix categorizes structural and mechanistic claims supporting the Biological Countercurvature hypothesis according to their evidentiary strength in the latest AlphaFold Structural Assessment.

## Tiers of Evidence

### 1. Confirmed by Metrics
These claims are directly supported by high-confidence, reproducible structural outputs and quantitative metrics from the AFCC pipeline.

| Claim | Measurement/Metric | Exact File Source / Row |
|---|---|---|
| Strongest high-anisotropy/high-confidence signals include CNNM2, FBLN5, STOML3, PANX3, and PIEZO2. | Anisotropy ≥ 3.0, pLDDT ≥ 70 | `outputs/afcc/2026-02-16/metrics.csv` (CNNM2, FBLN5, STOML3, PANX3, PIEZO2 rows) |
| LBX1 exhibits intermediate anisotropy, low overall structural confidence, and high domain blockiness. | Anisotropy ~ 2.27, pLDDT ~ 66.9, PAE Blockiness ~ 7.35 | `outputs/afcc/2026-02-16/metrics.csv` (LBX1 row) |
| Key structural metrics (Anisotropy, pLDDT) for core candidates (LBX1, PIEZO2, LMNA) are statically reused across the trend window (Jan-Feb). | Identical per-gene vectors across runs | `reports/evidence_freshness_audit.md` (Table: Identical Per-Gene Vectors Across Runs) |

### 2. Supported but Uncertain
These claims involve clear structural signals but suffer from low modeling confidence or depend on exploratory proxy measurements (e.g., predicted IDR segments).

| Claim | Measurement/Metric | Exact File Source / Row |
|---|---|---|
| POC5 and GHR may serve as highly extended, fibrous mechanosensors but require orthogonal validation. | Anisotropy = 24.69 (POC5), 5.13 (GHR); pLDDT < 70 | `outputs/afcc/2026-02-16/metrics.csv` (POC5, GHR rows) |
| LBX1 has a modular/blocky architecture containing potentially flexible hinges connecting independently folded sub-domains. | PAE Blockiness = 7.35 (but low pLDDT ~ 66.9 overall) | `outputs/afcc/2026-02-16/metrics.csv` (LBX1 row) |

### 3. Speculative Narrative
These claims over-interpret static inputs as evolving biological features or assign complex causal mechanistic roles without direct experimental or high-confidence structural evidence.

| Claim | Inference vs Measurement | Exact File Source / Row |
|---|---|---|
| LBX1 structural geometry changed functionally over January-February, dictating mechanosensor cluster formation. | Narrative inflation despite static metrics across 17 runs | `reports/alphafold_data_assessment_2026-02-16.md` (Confidence and Failure Modes) and cluster notes (e.g., `2026-01-20__cluster_note.md`) |
| Newly emerging structural classes (like tension rods vs. blocky scaffolds) actively drive real-time counter-curvature adaptation. | Derived entirely from single, unverified AlphaFold structural snapshots rather than measured in vivo strain | `reports/alphafold_data_assessment_2026-02-16.md` |

