# LBX1 Falsifiability Plan

## Core Hypothesis
LBX1 is hypothesized to be a mechanosensor or key node in the mechanotransduction pathway that regulates spinal alignment during adolescent growth. The Biological Countercurvature framework requires mechanosensors to integrate mechanical load (gravity/tension) with biological signals.

## Falsification Criteria
The following experiments are designed to test the limits of the LBX1-mechanics link. If the falsification thresholds are met, the hypothesis that LBX1 acts as a primary mechanosensor or structural load-bearing element must be rejected or significantly revised.

### Experiment 1: Structural Integrity Under Load
- **Hypothesis:** If LBX1 acts as a tension-sensing "blocky scaffold," applying physical tension to the cell nucleus or cytoskeleton should trigger a conformational change or altered localization.
- **Assay Design:** Use FRET-based tension sensors inserted into the LBX1 structure in human BMSCs (Bone Marrow Stem Cells). Apply cyclic mechanical stretch (10% strain, 1 Hz) and measure FRET efficiency to detect structural unfolding or tension transmission.
- **Quantitative Readout:** Change in FRET efficiency ($\Delta$FRET) between relaxed and stretched states.
- **Expected Direction:** Decrease in FRET efficiency (indicating structural extension/unfolding under tension).
- **Falsification Threshold:** If $\Delta$FRET < 5% under physiological or hyper-physiological stretch, or if LBX1 behavior is indistinguishable from a cytosolic non-mechanosensitive control (e.g., GAPDH), falsify the claim that LBX1 bears direct mechanical load.

### Experiment 2: Localization Independence from LINC Complex
- **Hypothesis:** LBX1 localization to the nucleus or its retention in mechanically active regions depends on the integrity of the cellular mechanical network (e.g., LINC complex, LMNA).
- **Assay Design:** Perform siRNA-mediated knockdown of LMNA and SUN1/2 (disrupting the LINC complex) in a mechanosensitive cell line (e.g., BMSCs). Quantify the nuclear-to-cytoplasmic ratio of LBX1 under baseline and mechanically loaded conditions.
- **Quantitative Readout:** Nuclear/Cytoplasmic (N/C) fluorescence intensity ratio of LBX1.
- **Expected Direction:** LBX1 N/C ratio decreases or fails to increase under load when the LINC complex is disrupted.
- **Falsification Threshold:** If the LBX1 N/C ratio remains constant (variation < 10%) regardless of mechanical loading and LINC complex integrity, falsify the claim that LBX1 is mechanically coupled to the nuclear envelope or mechanotransduction network.

### Experiment 3: Transcriptional Response vs. Direct Mechanosensing
- **Hypothesis:** LBX1 acts as an early, direct responder to mechanical cues rather than a downstream transcriptional target of a slower, systemic process.
- **Assay Design:** Apply an acute mechanical stimulus (e.g., rapid stretch or fluid shear stress) to cells. Measure the activation time course of LBX1 compared to known rapid mechanosensors (e.g., PIEZO2 calcium flux) and slower transcriptional responses (e.g., YAP/TAZ nuclear translocation). Use protein synthesis inhibitors (cycloheximide) to block new LBX1 production.
- **Quantitative Readout:** Time (in minutes) to reach peak activation or nuclear accumulation.
- **Expected Direction:** If LBX1 is a direct sensor, its response time should be rapid (seconds to minutes) and independent of new protein synthesis.
- **Falsification Threshold:** If LBX1 activation occurs only after a significant delay (>2 hours) or is entirely blocked by cycloheximide, falsify the claim that LBX1 is a *direct* structural mechanosensor, confirming its role instead as a downstream transcriptional effector.
