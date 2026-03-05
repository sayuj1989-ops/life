# LBX1 Falsifiability Package

**Objective:** Define concrete, measurable falsifiability criteria for the hypothesis that LBX1 plays a mechanical or structural role (e.g., as a direct mechanosensor or structural scaffold) in the Biological Countercurvature framework. Based on recent AFCC analysis (`outputs/afcc/2026-02-16/metrics.csv`), LBX1 is intermediate-anisotropy (~2.27), low-confidence (pLDDT ~66.9), and highly blocky, casting doubt on it serving as a direct rigid mechanical element.

## Experiment 1: Direct Mechanical Loading Response (Nucleus vs. Cytoplasm)
- **Hypothesis:** If LBX1 acts as a direct mechanosensor or mechanical transducer in somitic/muscle development, physical strain will rapidly alter its nuclear localization or immediate biochemical state prior to secondary signaling cascades.
- **Assay Design:** Apply controlled, high-magnitude cyclic and static biaxial stretch to cultured myoblasts/somitic progenitor cells expressing endogenously tagged LBX1. Monitor subcellular localization in real-time (minutes) and measure complex formation (e.g., via co-IP) with known force-transducing elements like the LINC complex (LMNA).
- **Quantitative Readout:** Ratio of nuclear to cytoplasmic LBX1 fluorescence intensity over time; protein-protein interaction affinity constant changes with LMNA under strain.
- **Expected Direction (if hypothesis holds):** Strain induces a >50% rapid (within 10 minutes) shift in nucleocytoplasmic ratio or binding affinity to the nuclear lamina, similar to YAP/TAZ mechanotransduction.
- **Falsification Threshold:** If LBX1 localization and LINC binding affinity change by less than 15% after 30 minutes of 10-15% mechanical strain, the hypothesis that LBX1 is an immediate, direct mechanosensor is **falsified**.

## Experiment 2: Structural Rigidity and Disordered Region Analysis
- **Hypothesis:** Despite low AlphaFold pLDDT scores, LBX1 forms a rigid, multi-domain "blocky" scaffold in vivo that supports load-bearing or tension-transmitting functions.
- **Assay Design:** Perform in vitro single-molecule Force Spectroscopy (e.g., optical or magnetic tweezers) on purified LBX1 to measure its force-extension curve and unfolding force. Compare with established intrinsically disordered proteins (IDPs) and known rigid mechanosensors (e.g., talin rod domains).
- **Quantitative Readout:** Unfolding force (pN) and persistence length (Lp) of the LBX1 protein chain.
- **Expected Direction (if hypothesis holds):** LBX1 exhibits distinct, high-force unfolding events characteristic of rigid, structured domains resisting tension (>10-15 pN).
- **Falsification Threshold:** If the force-extension curve behaves identically to a random coil IDP (WLC model with very low persistence length) with no significant force peaks >5 pN, the hypothesis that LBX1 acts as a rigid structural scaffold is **falsified**.

## Experiment 3: Phenotypic Rescue via Biochemical vs. Mechanical Analogs
- **Hypothesis:** LBX1's role in spinal development and preventing curvature defects is fundamentally linked to its mechanical/structural properties rather than purely its biochemical transcription-factor activity.
- **Assay Design:** In an LBX1-knockout animal model (e.g., zebrafish) that exhibits spinal curvature/muscle defects, attempt genetic rescue using two different constructs:
  1. A purely biochemical equivalent (a different transcription factor engineered to bind the same target DNA sequences and recruit the same co-activators/repressors as LBX1).
  2. A purely structural equivalent (a rigid spacer protein lacking DNA binding domains but possessing the hypothesized mechanical properties of LBX1).
- **Quantitative Readout:** Penetrance and severity (Cobb angle equivalent) of spinal curvature in the rescued populations compared to wild-type and full knockout.
- **Expected Direction (if hypothesis holds):** The purely biochemical equivalent fails to rescue the spinal defect (or does so poorly), while the structural/mechanical presence (or a hybrid) is strictly required for normal geometry.
- **Falsification Threshold:** If the purely biochemical equivalent completely rescues the normal straight-spine phenotype (reducing curvature incidence to wild-type levels), the hypothesis that LBX1's *mechanical* structure is the driving force in countercurvature is **falsified**, confirming it acts solely as a standard biochemical signaling node.
