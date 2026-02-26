# Evidence Note: Metabolic Protein Expansion in AFCC Pipeline (Confirmed)

**Date:** 2026-03-12
**Topic:** Formal expansion of AlphaFold Counter-Curvature (AFCC) pipeline to include key metabolic regulators.

## Context
To close the loop on the "Supply Side" of the thermodynamic cost equation ($\Gamma_m$), we have formally added the following proteins to the automated Bolt-BioFold analysis pipeline (`research/alphafold_countercurvature`):
- **PPARGC1A** (PGC-1alpha): Mitochondrial biogenesis master regulator.
- **GHR**: Growth Hormone Receptor.
- **ARNTL** (BMAL1): Circadian clock master regulator.
- **MYLK**: Myosin Light Chain Kinase.

We also re-verified metrics for **IGF1R** and **DMD** which were already in the pipeline.

## Automation Results (2026-03-12)
The AFCC pipeline (`00_build` -> `01_map` -> `02_fetch` -> `04_analyze`) was executed successfully. The metrics are now persisted in `research/alphafold_countercurvature/data/processed/protein_metrics.csv`.

| Gene | Anisotropy | pLDDT (Mean) | Morphology | Rg | Hinges | Interpretation |
|---|---|---|---|---|---|---|
| **GHR** | 5.13 | 58.7 | Fibrous/Extended | 31.4 | 54 | Highly anisotropic receptor, consistent with signal transduction role. Low confidence suggests flexibility/disorder. |
| **ARNTL** | 3.32 | 65.5 | Fibrous/Extended | 32.1 | 6 | Anisotropic transcription factor. |
| **PPARGC1A** | 2.19 | 52.7 | Intermediate | 31.3 | 0 | Largely disordered (IDR-heavy), consistent with being a transcriptional co-activator scaffold. |
| **MYLK** | 1.46 | 65.9 | Globular | 41.5 | 31 | Globular kinase with significant flexibility (hinges). |
| **IGF1R** | 1.43 | 78.0 | Globular | 43.2 | 35 | Large globular receptor. |
| **DMD** | 1.32 | 76.4 | Globular | 22.8 | 1 | Globular fragment (likely not full length dystrophin which is massive). |

## Implications
- **GHR** and **ARNTL** show significant anisotropy (>3.0), reinforcing the idea that "Supply" regulators might also have structural features or engage in anisotropic complexes.
- **PPARGC1A** is confirmed to be highly disordered (pLDDT ~52), fitting the profile of a "Hub" protein that binds multiple partners, representing a high entropic cost/signaling capacity.
- These metrics are fully synchronized with `outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv`.

## Next Steps
- Integrate these anisotropy values into the $\Gamma_m$ calculation (Confirmed).
- Investigate the specific "Hinges" in GHR and MYLK for potential mechanosensitivity.
