# LBX1 Falsifiability Plan

## Overview
This document establishes strict empirical falsification criteria for the hypothesis that LBX1 functions as a mechanosensor/integrator in the Biological Countercurvature (BCC) framework. Based on authoritative structural data (e.g., outputs/afcc/2026-02-16/metrics.csv), LBX1 has an intermediate, low-confidence static structure (Anisotropy ~2.27, pLDDT ~66.9).

The experiments below are designed to rigorously test this link and explicitly weaken the narrative if evidence is not found.

## Experiment 1: Primary Mechanosensory Capacity Assessment
**Hypothesis:** LBX1 directly senses and responds to mechanical strain via conformational changes (tension rod behavior).
- **Assay Design:** *In vitro* FRET (Förster Resonance Energy Transfer) tension sensor assay using LBX1 constructs expressed in human mesenchymal stem cells (hMSCs). Subject cells to cyclic tensile strain (10%, 1 Hz) for 4 hours.
- **Quantitative Readout:** Change in FRET efficiency (ΔFRET) between resting and strained states, representing conformational extension.
- **Expected Direction:** A significant decrease in FRET efficiency under strain, indicating molecular extension.
- **Falsification Threshold:** If ΔFRET < 5% under physiological strain conditions (10%), LBX1 lacks the intrinsic mechanical elasticity/tension-sensing properties of a primary mechanosensor (unlike PIEZO2 or LMNA). This would strongly falsify its direct mechanical role.

## Experiment 2: Nuclear Translocation vs. Tension Independence
**Hypothesis:** LBX1 relies on upstream canonical mechanotransducers (e.g., YAP/TAZ) and acts purely downstream in the mechanotransductive cascade.
- **Assay Design:** Measure LBX1 nuclear localization and transcriptional target activity under static vs. strained conditions (10% biaxial stretch). Parallel conditions will include pharmacological inhibition of upstream tension (e.g., Latrunculin A to disrupt actin, or Blebbistatin to block myosin II contractility).
- **Quantitative Readout:** Nuclear-to-cytoplasmic (N/C) intensity ratio of LBX1 via quantitative immunofluorescence; qPCR of LBX1 downstream targets.
- **Expected Direction:** LBX1 localization/activity changes under strain but is abrogated when cytoskeletal tension is blocked.
- **Falsification Threshold:** If LBX1 activity/localization under strain remains *unchanged* (p > 0.05) when upstream cytoskeletal tension is pharmacologically abolished, its role is mechanosensitive but *decoupled* from the primary actin/myosin tension network. Conversely, if LBX1 fails to show any strain-dependent activity at all, it is entirely mechanistically decoupled.

## Experiment 3: Spinal Asymmetry Rescue by Overexpression
**Hypothesis:** Enhancing LBX1 expression can computationally/in vivo rescue spinal asymmetry driven by localized mechanical energy deficits.
- **Assay Design:** Using a zebrafish scoliosis model (e.g., ptk7 mutant), apply targeted overexpression of LBX1 in paraxial mesoderm/somites during the rapid growth phase (equivalent to adolescent growth spurt).
- **Quantitative Readout:** Cobb angle (degrees) measured via micro-CT at 30 days post-fertilization (dpf).
- **Expected Direction:** A statistically significant reduction in mean Cobb angle compared to vehicle controls.
- **Falsification Threshold:** If the mean Cobb angle in the LBX1 overexpression group is not reduced by at least 20% compared to controls (p < 0.05), or if structural asymmetry worsens, the hypothesis that LBX1 acts as a compensatory integrator/rescuer of spinal countercurvature is falsified.

## Conclusion
Given LBX1's low confidence and globular morphology (unlike high-anisotropy sensors like PIEZO2), testing these limits is essential. Failure of Experiment 1, in particular, would immediately downgrade LBX1 to a purely downstream biochemical node.
