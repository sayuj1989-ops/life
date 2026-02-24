# Cluster Report: Disordered Proprioceptive Transcription Factors
**Date:** 2026-03-04
**Source:** `outputs/afcc/current_metrics.csv` (N=9, Cluster 5 & 1)

## Cluster Members
*   **RUNX3** (Proprioception Development, Anisotropy: 2.06, Disorder Proxy: 0.56, pLDDT: 60.6)
*   **EGR3** (Muscle Spindle Morphogenesis, Anisotropy: 3.76, Disorder Proxy: 0.64, pLDDT: 50.0)
*   **LBX1** (Muscle Precursor Migration, Anisotropy: 2.27, Disorder Proxy: 0.26, pLDDT: 66.9)

## Shared Properties
1.  **High Intrinsic Disorder:** These transcription factors exhibit significantly higher disorder (0.26 - 0.64) compared to structured signaling proteins (e.g., NF1: 0.07, PLOD1: 0.03).
2.  **Low Confidence Structure:** Low pLDDT scores (50-67) indicate large flexible regions likely involved in protein-protein interactions or phase separation.
3.  **Proprioceptive/Muscle Function:** All three are critical regulators of the proprioceptive hardware (muscle spindles, sensory neurons) that senses gravity.

## Hypothesized Mechanical Role
**"Disordered Proprioceptive Transcription Factors act as Nuclear Mechanosensors via Phase Separation"**

We hypothesize that the high intrinsic disorder of RUNX3, EGR3, and LBX1 allows them to form biomolecular condensates (via Liquid-Liquid Phase Separation, LLPS) within the nucleus. The formation and stability of these condensates are highly sensitive to nuclear biophysical properties (stiffness, crowding, osmotic pressure), which are in turn modulated by external mechanical loading (gravity).

This creates a **Developmental Checkpoint**:
1.  **Gravity Loading** -> **Nuclear Deformation/Stiffening**.
2.  **Nuclear Stiffening** -> **Condensate Formation/Dissolution** of IDR-TFs (RUNX3/EGR3).
3.  **Condensate State** -> **Transcriptional Activity** (gating proprioceptive gene expression).
4.  **Gene Expression** -> **Proprioceptive Hardware Formation** (Spindles/Neurons).

In microgravity or under altered loading (scoliosis), this checkpoint fails ("Nuclear Mechanoblindness"), leading to malformed or desensitized proprioceptive circuits, further exacerbating the loss of postural tone.

## Concrete Test
**In Vitro Phase Separation Assay under Osmotic Stress:**
1.  Tag RUNX3 and EGR3 with GFP.
2.  Express in DRG sensory neurons or C2C12 myoblasts.
3.  Subject cells to:
    *   **Hypo-osmotic shock** (nuclear swelling/softening - mimicking microgravity/unloading).
    *   **Hyper-osmotic shock** (nuclear compression/crowding - mimicking loading).
    *   **Stiff vs Soft Substrates** (0.5 kPa vs 40 kPa).
4.  **Measure:** Number, size, and liquidity (FRAP) of nuclear condensates.
5.  **Prediction:** Condensate properties will shift significantly with nuclear mechanics, correlating with transcriptional output (e.g., target gene mRNA levels).
