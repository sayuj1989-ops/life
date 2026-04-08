# Bolt-BioFold Cycle Report: Default Seed List Proxy (PIEZO2, DMD, DAG1)

**Date**: 2026-04-08
**Source**: Local AlphaFold DB Cache (`data/afdb_cache/`) as default seed list proxy due to API 404s.
**Code Version**: `outputs/bolt_biofold_cycle/run_biofold_local.py`
**Parameters**: pLDDT threshold $\geq 70$, PAE threshold $>15$ for multi-domain uncertainty, smoothing window = 5 residues.

## A) Results Table

| protein_id | length | pLDDT_mean | IDR_proxy | domains | Rg | e2e_dist | anisotropy | curv_mean | torsion_mean | bending_hotspots | PAE_mean |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---|---:|
| PIEZO2_Q9H5I5 | 709 | 79.44 | 0.137 | 5 | 43.41 | 97.92 | 4.43 | 1.469 | -0.013 | 412-416, 523-527, 237-241 | 16.99 |
| DMD_P11532 | 525 | 76.35 | 0.175 | 2 | 22.82 | 76.06 | 1.32 | 1.588 | -0.117 | 157-161, 467-471, 33-37 | 19.01 |
| DAG1_Q14118 | 895 | 68.17 | 0.380 | 6 | 31.58 | 75.13 | 2.90 | 1.120 | 0.053 | 344-348, 672-676, 735-739 | 25.46 |

*(Note: SASA/exposed_surface_proxy requires external dependencies. PAE blockiness and hinge candidates marked as not implemented in this pass.)*

## B) Key Plots Generated

- **pLDDT**: `outputs/bolt_biofold_cycle/figures/{PIEZO2,DMD,DAG1}_pLDDT.png`
- **PAE**: `outputs/bolt_biofold_cycle/figures/{PIEZO2,DMD,DAG1}_PAE.png`
- **Curvature**: `outputs/bolt_biofold_cycle/figures/{PIEZO2,DMD,DAG1}_curvature.png`

## C) Interpretation

* **What we see**:
  - **PIEZO2** shows strong structural integrity (pLDDT ~79) but high inter-domain flexibility (PAE ~17). It is highly anisotropic (4.43), reflecting a stretched, rod-like geometry, with specific bending hotspots identified at residues like 412-416.
  - **DMD (Dystrophin)** is characterized by two distinct high-confidence domains separated by a long flexible/disordered linker. It has high local curvature (1.588) but low anisotropy (1.32), acting more like a folded spring.
  - **DAG1 (Dystroglycan)** is very disordered (38% IDR proxy) with low overall confidence (pLDDT 68.17) and very high PAE (25.46), making its backbone geometry calculations less reliable globally.

* **Why it matters for spine development/countercurvature**:
  - The high anisotropy and rigid-but-flexible inter-domain nature of **PIEZO2** perfectly suits a mechanosensor. The identified bending hotspots may represent the functional hinges that open the channel under spinal mechanical load.
  - The domain-linker-domain architecture of **DMD** provides a highly elastic "molecular spring" that protects muscle sarcolemma from contraction-induced stress, essential for maintaining postural tone against gravity.

* **Confidence level**:
  - **PIEZO2**: Medium-High (good local pLDDT, uncertain global packing).
  - **DMD**: Medium (high confidence in discrete domains).
  - **DAG1**: Low (dominated by intrinsically disordered regions, explicit low confidence warning).

* **Next test**: The bending hotspots (e.g. PIEZO2 412-416) are primary candidates for mechanically-induced conformational changes. We predict that applying simulated tension across these specific hinges will correlate with channel opening dynamics.

## D) Best Next Move
Correlate the specific bending hotspots and curvature summaries of these mechanotransducers with known pathogenic missense mutation locations to see if scoliosis-driving variants cluster at mechanical hinges.
