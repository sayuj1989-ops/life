# LBX1 Falsifiability Plan

*Based on structural data from `outputs/afcc/2026-02-16/metrics.csv`*

## Background
Current structural analyses place LBX1 as an intermediate-anisotropy (~2.27), low-confidence (pLDDT ~66.9) protein. Its role as a structural "Tension Rod" or mechanosensor anchor in Biological Counter-Curvature is an inferred hypothesis based on static, low-confidence AlphaFold predictions. To solidify or falsify this role, we must prioritize empirical testing over reinterpretation of static structural data.

## Concrete Falsifiability Experiments

### Experiment 1: Nuclear Tension Localization Rescue
**Hypothesis**: If LBX1 acts as a load-bearing mechanosensor (like LMNA), its localization and stability should be dependent on cellular tension and LINC complex integrity.
**Assay Design**:
1. Cultured osteoblasts or somite-derived cells expressing tagged LBX1.
2. Perturb nuclear tension using LINC complex disruption (e.g., KASH domain overexpression) or substrate stiffness modulation (soft vs. stiff hydrogels).
3. Image LBX1 nuclear localization and quantify chromatin association.
**Quantitative Readout**: Nuclear-to-cytoplasmic ratio of LBX1; fraction of chromatin-bound LBX1 via FRAP.
**Expected Direction**: Decreased nuclear tension reduces LBX1 chromatin association.
**Falsification Threshold**: If LBX1 localization/mobility remains unchanged across a 10-fold change in substrate stiffness or complete LINC disruption, the hypothesis that it acts as a primary mechanosensor is strongly weakened.

### Experiment 2: Domain Deletion and Stiffness Assay
**Hypothesis**: If LBX1's specific geometry is crucial for mechanotransduction, deleting its flexible hinge or "blocky" domains will alter cellular mechanical properties.
**Assay Design**:
1. Generate LBX1 wild-type and domain-deletion mutants (specifically targeting regions with high PAE blockiness).
2. Transfect into LBX1-null cells.
3. Measure cellular stiffness and traction forces using Atomic Force Microscopy (AFM) and Traction Force Microscopy (TFM).
**Quantitative Readout**: Cellular Young's modulus (kPa); total traction force (nN).
**Expected Direction**: Domain deletion should fail to rescue wild-type cellular stiffness/traction.
**Falsification Threshold**: If cells expressing domain-deletion mutants exhibit identical stiffness and traction force profiles to wild-type, the structural necessity of these specific domains for mechanical function is falsified.

### Experiment 3: Orthogonal Structural Validation (In-Cell Crosslinking)
**Hypothesis**: LBX1's AlphaFold predicted structure (intermediate anisotropy, high blockiness) reflects its true in vivo conformation and complex formation.
**Assay Design**:
1. Perform in-cell crosslinking mass spectrometry (XL-MS) on native tissues or cell lines.
2. Map crosslinked distance constraints onto the AlphaFold monomer and multimer models.
**Quantitative Readout**: Percentage of XL-MS distance constraints satisfied by the predicted AlphaFold model.
**Expected Direction**: High satisfaction rate for the predicted monomer or a stable multimer state.
**Falsification Threshold**: If >30% of high-confidence crosslinks violate the AlphaFold predicted geometry (e.g., indicating a highly compact globular state rather than an extended/blocky one), the reliance on the current AF prediction for mechanistic inference is falsified.
