# LBX1 Falsifiability Plan

## Overview
AlphaFold metrics characterize LBX1 as an intermediate-anisotropy (~2.27), low-confidence (~66.9 pLDDT), highly blocky (PAE ~7.35) structure. This geometry falsifies any model treating LBX1 as a rigid tension rod (like PIEZO2 or LMNA). Instead, the proposed narrative positions LBX1's "blockiness" as uniquely rendering it sensitive to nuclear stiffness, causing potential misfolding or mislocalization under low-tension environments (e.g. microgravity, scoliosis).

To ensure rigorous falsifiability, we propose three concrete experiments capable of invalidating the LBX1-mechanics link.

## Experiment 1: Domain-fragment construct + nuclear tension perturbation
* **Hypothesis**: LBX1's "blocky" architecture relies on high nuclear stiffness (transmitted via LINC/Lamin A/C) to remain extended and properly localized; loss of this tension causes conformational collapse or mislocalization, impairing function.
* **Assay Design**: Express full-length GFP-LBX1 vs GFP-RUNX3 (a rigid comparator) in C2C12 myoblasts or neural progenitors. Perturb nuclear tension using Latrunculin B or Lamin A/C siRNA knockdown.
* **Quantitative Readout**: Measure the Nuclear/Cytoplasmic ratio (localization) and transcriptional activity (using a luciferase reporter for LBX1 target genes).
* **Expected Direction**: GFP-LBX1 will show decreased nuclear accumulation and decreased transcriptional activity under low tension relative to the control, whereas GFP-RUNX3 will remain relatively stable.
* **Falsification Threshold**: If LBX1 localization and transcriptional activity remain unchanged (or parallel the changes of RUNX3) under Lamin A/C knockdown, the "nuclear stiffness-gated transcription" hypothesis is false.

## Experiment 2: Ensemble / alternative structure workflows
* **Hypothesis**: The high PAE blockiness and low pLDDT regions of LBX1 are robust structural features (indicative of true flexible linkers gating functional states) rather than artifacts of isolated monomeric modeling.
* **Assay Design**: Run ensemble modeling (e.g., MD relaxation, multimer context modeling, disorder-aware prediction models) on LBX1 and RUNX3 to evaluate structural stability under varying assumptions.
* **Quantitative Readout**: Change in structural blockiness (PAE), disorder propensity, and average pLDDT across the simulated ensembles.
* **Expected Direction**: LBX1 will maintain distinct domain segregation (high blockiness) across varying conditions, suggesting intrinsic flexibility, while RUNX3 will remain rigid.
* **Falsification Threshold**: If advanced modeling resolves LBX1 into a uniformly rigid or globular structure (eliminating the high blockiness), the entire structural narrative of it being a "beads-on-a-string" tension sensor is false.

## Experiment 3: Orthogonal biophysical or expression timing assay
* **Hypothesis**: LBX1's expression or structural state is acutely regulated by mechanical loads during spinal straightening, functioning as a mechanosensor node rather than a purely constitutive biochemical factor.
* **Assay Design**: Perform a temporal expression study measuring LBX1 mRNA and protein levels in a developmental model (e.g. mouse embryo) exactly at the onset of spinal straightening under gravity, alongside high-resolution spatial mapping in the somites.
* **Quantitative Readout**: LBX1 expression fold-change and spatial gradients correlated directly with the mechanical onset timeline.
* **Expected Direction**: A sharp, localized spike in LBX1 activity coinciding with the biomechanical onset of spinal loading.
* **Falsification Threshold**: If LBX1 expression is constitutive and unaffected by the mechanical onset of straightening, its role as a dynamic mechanical sensor is false, relegating it to a purely generic developmental role.
