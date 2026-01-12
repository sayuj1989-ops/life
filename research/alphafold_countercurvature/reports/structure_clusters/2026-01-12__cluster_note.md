# Structure Cluster Report: The Anisotropic Axis (Cluster 1)
**Date:** 2026-01-12
**Analyst:** Jules (Structure Hypothesis Generator)
**Source:** `research/alphafold_countercurvature/outputs/afcc/2026-01-11/metrics.csv`

## 1. Cluster Definition
**Identity:** Cluster 1 ("High Anisotropy")
**Key Metrics:**
- **Anisotropy Index:** ~12.04 (vs 2.84 in Cluster 0)
- **PAE Blockiness:** ~3.01 (Moderate)

**Members:**
- **VIM** (Vimentin) - Intermediate Filament
- **POC5** (Centriolar Protein) - *POC5*
- **PTK7** (Protein Tyrosine Kinase 7) - Wnt/PCP Signaling
- **SCRIB** (Scribble) - Basolateral Polarity Scaffold

## 2. Structural Analysis
This cluster is defined by **extreme structural elongation**.
- **Vimentin** forms long, non-polar filaments with high tensile strength.
- **PTK7** has a large extracellular domain usually modeled as a rod-like receptor.
- **POC5** is a structural component of the distal centriole lumen.
- **SCRIB** acts as a large scaffold.

The co-clustering of these proteins suggests a **"Structural Axis"** function. Unlike the "Modular/Hinged" proteins in Cluster 2 (YAP1, PIEZO1) or the "Compact/Globular" proteins in Cluster 0 (ACTB, TUBB), these proteins occupy a distinct morphospace characterized by high aspect ratios.

## 3. Mechanistic Hypothesis
**Hypothesis:** *The "Anisotropic Axis" complex (VIM-POC5-PTK7) physically couples the cellular polarity vector (PCP) to the gravitational vertical via the centriole.*

**Rationale:**
- **Vimentin (VIM)** is known to cage the nucleus and anchor the centrosome. It remodels under shear stress and gravity (unloading leads to cytoskeletal collapse).
- **POC5** is essential for centriole integrity. Centrioles define the primary cilium axis.
- **PTK7** establishes planar polarity (tissue-level directionality).

**Proposed Mechanism:**
The high intrinsic anisotropy of these proteins allows them to serve as "molecular plumb lines".
1.  **PTK7** defines the tissue plane.
2.  **Vimentin** cables anchor the Centrosome (**POC5**) to the cortex.
3.  Under gravity (1g), Vimentin tension aligns the POC5-containing centriole vertically, ensuring proper ciliary beating and CSF flow.
4.  In microgravity (0g), Vimentin tension is lost (cages collapse). The centriole (POC5) misorients.
5.  This "Structural Confusion" uncouples the biological axis from the geometric axis, leading to scoliosis.

## 4. Testable Prediction
**Experiment:**
Compare Centriole/Cilia orientation (angle relative to nucleus-centroid axis) in:
1.  Control Fibroblasts (1g)
2.  Clinorotated Fibroblasts (Simulated 0g)
3.  Vimentin-Knockout Fibroblasts (1g)

**Prediction:**
Vimentin-KO cells at 1g will mimic the centriole misorientation phenotype of Wild-Type cells at 0g.
Specifically, the variance in the angle $\theta_{cilia}$ will increase significantly, breaking the coherent "Anisotropy" of the tissue.
