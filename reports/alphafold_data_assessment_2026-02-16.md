# AlphaFold Data Assessment (LBX1 Focus)

## Data Provenance
- Report generated: 2026-02-19 19:05:04 UTC
- Repository: `origin=https://github.com/sayujks0071/life`
- MCP status: `MCP endpoint reachable, but no mounted MCP server in current client.`
- Authoritative snapshot: `outputs/afcc/2026-02-16/metrics.csv`
- Trend window: `2026-01-09` to `2026-02-16` (dated folders under `outputs/afcc/`)
- Runs detected in window: 18
- Future-dated narrative notes excluded as non-observational: 3
- Excluded files: 2026-06-01__cluster_note.md, 2026-07-23__cluster_note.md, 2026-10-31__cluster_note.md

## Quantitative Findings
### Quality and Integrity Checks
- Schema validation: 18 metrics files parsed.
- Schema drift: none detected in scoped files (canonical schema available).
- Row counts by run: 2026-01-09:9, 2026-01-14:9, 2026-01-16:3, 2026-01-18:9, 2026-01-20:9, 2026-01-21:9, 2026-01-27:9, 2026-01-31:9, 2026-02-05:9, 2026-02-06:9, 2026-02-07:9, 2026-02-08:9, 2026-02-09:10, 2026-02-10:219, 2026-02-11:10, 2026-02-12:10, 2026-02-13:48, 2026-02-16:25

### Latest Snapshot Ranking (2026-02-16)
- Genes ranked: 25
- Confidence threshold: `pLDDT_mean >= 70`
- High-anisotropy threshold: `anisotropy_index >= 3.0`

#### High anisotropy + high confidence (strongest structural signal)
1. CNNM2: anisotropy=8.54, pLDDT=70.4, PAE_blockiness=4.83
2. FBLN5: anisotropy=7.05, pLDDT=83.3, PAE_blockiness=3.55
3. STOML3: anisotropy=5.56, pLDDT=84.3, PAE_blockiness=0.00
4. PANX3: anisotropy=5.08, pLDDT=81.7, PAE_blockiness=2.77
5. PIEZO2: anisotropy=4.44, pLDDT=79.4, PAE_blockiness=2.80
6. ROCK1: anisotropy=3.29, pLDDT=76.1, PAE_blockiness=4.95
7. ADGRG6: anisotropy=3.06, pLDDT=73.7, PAE_blockiness=6.78

#### High anisotropy + low confidence (hypothesis-generating only)
1. POC5: anisotropy=24.69, pLDDT=64.0, PAE_blockiness=3.51
2. GHR: anisotropy=5.13, pLDDT=58.7, PAE_blockiness=5.31
3. EMD: anisotropy=4.29, pLDDT=60.3, PAE_blockiness=9.13
4. MESP2: anisotropy=4.03, pLDDT=54.2, PAE_blockiness=0.00
5. ARNTL: anisotropy=3.32, pLDDT=65.5, PAE_blockiness=3.59

## LBX1 Deep Dive
- Latest rank by anisotropy: 16/25
- Latest LBX1 metrics: anisotropy=2.27, pLDDT=66.9, PAE_blockiness=7.35, morphology=Intermediate
- Confidence class: Low confidence
- Trend presence: 17 run(s) in scope contain LBX1.
- Trend variance: anisotropy SD=0.000000, pLDDT SD=0.000000, PAE blockiness SD=0.000000 (effectively static across runs).

### LBX1 Comparator Panel (latest snapshot)
- LBX1: anisotropy=2.27, pLDDT=66.9, PAE_blockiness=7.35, confidence=low
- PIEZO2: anisotropy=4.44, pLDDT=79.4, PAE_blockiness=2.80, confidence=adequate
- LMNA: not present in 2026-02-16 snapshot
- POC5: anisotropy=24.69, pLDDT=64.0, PAE_blockiness=3.51, confidence=low
- GHR: anisotropy=5.13, pLDDT=58.7, PAE_blockiness=5.31, confidence=low

## Confidence and Failure Modes
- Measured data source priority: `metrics.csv` > summary markdown > cluster narrative notes.
- Major caveat: high anisotropy can co-occur with low pLDDT; these signals are tentative and should not be treated as confirmatory.
- Current high-anisotropy/low-confidence genes: POC5, GHR, EMD, MESP2, ARNTL.
- Core-gene trend caveat: LBX1, PIEZO2, LMNA, POC5, GHR show static metrics across available runs; temporal wording should not imply metric drift.
- Potential hypothesis inflation flags (narrative updates despite static metrics): 6 note/gene instances.
  - 2026-01-13__cluster_note.md: PIEZO2 (narrative update despite static metrics)
  - 2026-01-15__cluster_note.md: PIEZO2 (narrative update despite static metrics)
  - 2026-01-15__cluster_note.md: LMNA (narrative update despite static metrics)
  - 2026-01-20__cluster_note.md: LBX1 (narrative update despite static metrics)
  - 2026-01-20__cluster_note.md: PIEZO2 (narrative update despite static metrics)
  - 2026-01-20__cluster_note.md: LMNA (narrative update despite static metrics)
- Cross-check (`reports/afcc_latest.md`): Linked dated metrics in report: 2026-01-21, 2026-01-23, 2026-01-27, 2026-01-31, 2026-02-06, 2026-02-09, 2026-02-13
- Cross-check (`reports/afcc_latest.md`): Dangling links (metrics missing locally): 2026-01-23

## Conclusions
- [Confirmed by metrics] In the latest snapshot, strongest high-anisotropy/high-confidence signals are `CNNM2`, `FBLN5`, `STOML3`, `PANX3`, and `PIEZO2`.
- [Confirmed by metrics] `LBX1` is intermediate anisotropy with low confidence (anisotropy ~2.27, pLDDT ~66.9, high PAE blockiness ~7.35); this supports a modular/blocky architecture hypothesis but not high-confidence structural certainty.
- [Confirmed by metrics] `LBX1`, `PIEZO2`, `LMNA`, `POC5`, and `GHR` values are effectively unchanged across the scoped run window whenever present; this indicates repeated reuse of stable structural inputs rather than evolving estimates.
- [Supported but uncertain] Very high anisotropy outliers with low confidence (for example `POC5`, `GHR`) remain plausible mechanistic candidates but require orthogonal validation.
- [Speculative narrative] Cluster-note claims about newly emerging structural classes are hypothesis-level when underlying core metrics are static.

### What To Trust Most Now (LBX1-centered)
1. LBX1 is consistently a low-confidence, intermediate-anisotropy, high-blockiness candidate.
2. PIEZO2 and LMNA are more reliable mechanosensor anchors than LBX1 for geometry-driven inference because their pLDDT is higher and stable.
3. Any causal claim that LBX1 geometry changed over Jan-Feb is not supported by the available metrics; prioritize functional assays over additional reinterpretation of the same structure snapshot.

## Priority Next Experiments
1. Validate LBX1 structural state experimentally: domain-fragment constructs plus nuclear-tension perturbation (e.g., LMNA/LINC modulation) with localization/activity readouts.
2. Run ensemble/alternative structure workflows for LBX1 and RUNX3 (multimer context, disorder-aware models, MD relaxation) to test whether high blockiness is robust to modeling assumptions.
3. Add a data-freshness gate to AFCC reports: automatically flag when “latest” summaries are generated from unchanged per-gene metrics.
4. For high-anisotropy low-confidence outliers (POC5, GHR), prioritize orthogonal evidence (proteomics localization, perturbation phenotypes, biophysical stiffness assays) before mechanistic elevation.
