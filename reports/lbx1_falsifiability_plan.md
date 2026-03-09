# LBX1 Falsifiability Plan

## Context
The Biological Counter-Curvature hypothesis currently posits LBX1 as a structural candidate involved in mechanosensing or force transmission due to its high PAE blockiness and potential interactions. However, current AFCC metrics (`outputs/afcc/2026-02-16/metrics.csv`) demonstrate that LBX1 has low confidence (pLDDT ~66.9) and intermediate anisotropy (~2.27), weakening the purely geometric inference of its load-bearing role. To enforce rigorous scientific standards, we outline three concrete experiments designed to falsify the hypothesis that LBX1 mechanics drive scoliotic curve progression.

## Falsification Experiments

### Experiment 1: Nuclear Localization Under Applied Tension
- **Hypothesis**: If LBX1 acts as a mechanosensor or structural transducer within the LINC-complex pathway, its nuclear localization or chromatin binding affinity will change in response to applied cyclical mechanical tension.
- **Assay Design**: Subject primary human osteoblasts (wild-type vs. LBX1-knockdown) to cyclical mechanical strain (e.g., via a Flexcell system at 10% strain, 1Hz for 24 hours). Measure LBX1 nuclear/cytoplasmic ratio using immunofluorescence and subcellular fractionation.
- **Quantitative Readout**: Ratio of nuclear-to-cytoplasmic LBX1 fluorescence intensity, and Western blot quantification of LBX1 in chromatin-bound versus soluble nuclear fractions.
- **Expected Direction**: Tension increases nuclear localization or chromatin binding affinity of LBX1 compared to static controls.
- **Falsification Threshold**: If the nuclear/cytoplasmic ratio or chromatin-bound fraction of LBX1 does not change significantly (p > 0.05) under mechanical loading compared to static controls, the hypothesis that LBX1 is a dynamic mechanosensor is falsified.

### Experiment 2: Biophysical Stiffness and Disorder-to-Order Transition
- **Hypothesis**: The high PAE blockiness and low pLDDT of LBX1 in AlphaFold predictions indicate an intrinsically disordered region (IDR) that undergoes a functionally relevant disorder-to-order transition upon binding a structural partner or under tension.
- **Assay Design**: Perform single-molecule Force Spectroscopy (e.g., Optical Tweezers or AFM) on purified recombinant LBX1. Measure the force-extension curve. Repeat in the presence of candidate binding partners (e.g., Lamin A/C fragments or putative DNA consensus sequences).
- **Quantitative Readout**: Persistence length ($L_p$) and unfolding force peaks (pN) extracted from the force-extension curves.
- **Expected Direction**: LBX1 exhibits a low persistence length in isolation but a significantly higher $L_p$ and distinct unfolding peaks when bound to a physiological partner or subjected to force, indicating an induced structural state.
- **Falsification Threshold**: If LBX1 behaves purely as a random coil with no discrete unfolding events or significant change in persistence length ($L_p$ increase < 10%) even in the presence of presumed interactors, the hypothesis that its IDR serves a specific, tension-bearing structural role is falsified.

### Experiment 3: Rescue of IEC Failure via Orthogonal Mechanosensors
- **Hypothesis**: LBX1 is necessary for Information-Elasticity Coupling (IEC). If LBX1 function is lost, the resulting proprioceptive deficit leading to scoliotic curvature cannot be rescued by simply upregulating alternative mechanosensors like PIEZO2.
- **Assay Design**: Utilize a validated zebrafish or mouse model of scoliosis driven by LBX1 mutation (e.g., Lbx1 knockout). Perform transgenic overexpression of an established, high-confidence mechanosensor (e.g., Piezo2) specifically in the relevant lineage (e.g., somitic mesoderm or proprioceptive neurons).
- **Quantitative Readout**: Cobb angle severity and incidence of spinal curvature at equivalent developmental stages (e.g., adolescent growth spurt equivalent).
- **Expected Direction**: Piezo2 overexpression fails to rescue the scoliotic phenotype because LBX1 provides a unique, non-redundant mechanical integration function.
- **Falsification Threshold**: If Piezo2 overexpression significantly reduces the incidence or severity of curvature in the LBX1-mutant background (e.g., >50% reduction in mean Cobb angle, p < 0.01), it falsifies the hypothesis that LBX1 has a unique, irreplaceable structural role in the core IEC mechanism, suggesting it acts upstream or parallel to generic mechanotransduction pathways.
