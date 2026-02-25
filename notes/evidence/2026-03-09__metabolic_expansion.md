# Evidence Note: Metabolic Protein Expansion in AFCC Pipeline

**Date:** 2026-02-25
**Topic:** Expansion of AlphaFold Counter-Curvature (AFCC) pipeline to include key metabolic regulators.

## Context
To close the loop on the "Supply Side" of the thermodynamic cost equation ($\Gamma_m$), we have formally added the following proteins to the Bolt-BioFold analysis pipeline:
- **PPARGC1A** (PGC-1alpha): Mitochondrial biogenesis master regulator.
- **GHR**: Growth Hormone Receptor.
- **ARNTL** (BMAL1): Circadian clock master regulator.
- **MYLK**: Myosin Light Chain Kinase.
- **DMD** (Dystrophin, fragment): Critical muscle-ECM linker.
- **IGF1R**: Insulin-like Growth Factor 1 Receptor.

## Results
The structures were fetched and metrics computed (Run 2026-02-25). Key findings:

| Gene | Anisotropy | pLDDT (Mean) | Morphology | Rg | Hinges | Interpretation |
|---|---|---|---|---|---|---|
| **GHR** | 5.13 | 58.7 | Fibrous/Extended | 31.4 | 54 | Highly anisotropic receptor (Aniso > 5.0), consistent with "Tensile Tether" hypothesis. Low confidence suggests flexibility. |
| **ARNTL** | 3.32 | 65.5 | Fibrous/Extended | 32.1 | 6 | Anisotropic transcription factor; potential vector-alignment capability. |
| **PPARGC1A** | 2.19 | 52.7 | IDR-Heavy | 31.2 | 0 | Largely disordered (IDR-heavy), consistent with being a transcriptional co-activator scaffold (Entropic Hub). |
| **MYLK** | 1.46 | 65.8 | Globular | 41.5 | 31 | Globular kinase with significant flexibility. |
| **IGF1R** | 1.43 | 78.0 | Globular | 43.2 | 35 | Large globular receptor. |
| **DMD** | 1.32 | 76.3 | Globular | 22.8 | 1 | Globular fragment; low anisotropy suggests this specific domain acts as a node rather than a rod. |

## Implications
- **GHR** and **ARNTL** show significant anisotropy (>3.0), reinforcing the idea that "Supply" regulators might also have structural features or engage in anisotropic complexes.
- **PPARGC1A** is confirmed to be highly disordered (pLDDT ~52), fitting the profile of a "Hub" protein that binds multiple partners, representing a high entropic cost/signaling capacity.
- These metrics are now synchronized with `outputs/afcc/current_metrics.csv` and `outputs/thermodynamic_cost/thermodynamic_cost_proteins.csv`.

## Next Steps
- Integrate these anisotropy values into the $\Gamma_m$ calculation.
- Investigate the specific "Hinges" in GHR and MYLK for potential mechanosensitivity.
- Validate **GHR** anisotropy in full-length context if possible (though low pLDDT suggests intrinsic flexibility).
