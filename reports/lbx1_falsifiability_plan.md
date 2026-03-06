# LBX1 Falsifiability Plan

This document outlines rigorous, quantitative falsifiability criteria for the hypothesis that LBX1 acts as a mechanosensor within the Biological Counter-Curvature framework. Given the low-confidence structural data (`pLDDT ~66.9`) and high PAE blockiness (`~7.35`) derived from `outputs/afcc/2026-02-16/metrics.csv`, we must define explicit conditions under which the mechanosensor hypothesis would be refuted.

## Experiment 1: Domain-Fragment Structural Integrity
- **Hypothesis:** LBX1's predicted intermediate-anisotropic, "blocky" architecture is a functional structural module responsive to physical tension, rather than a non-physiological artifact of intrinsically disordered regions in the AlphaFold model.
- **Assay Design:** Express full-length LBX1 and isolated high-blockiness domain fragments in vitro. Subject the constructs to varying mechanical tension using magnetic tweezers or AFM while monitoring unfolding events via single-molecule FRET.
- **Quantitative Readout:** Force required for domain unfolding (pN) and the subsequent change in FRET efficiency ($\Delta E$).
- **Expected Direction:** If it is a structural mechanosensor, domains should unfold cooperatively at physiologically relevant forces (e.g., 5-15 pN), exhibiting a distinct sigmoidal unfolding curve.
- **Falsification Threshold:** If full-length LBX1 acts as a random coil with no cooperative unfolding events under tension, or unfolds at forces `<2 pN` (indistinguishable from thermal noise), the hypothesis that it forms a coherent, tension-bearing mechanical rod is falsified.

## Experiment 2: Nuclear Tension Perturbation and Localization
- **Hypothesis:** If LBX1 senses mechanical load, its subcellular localization or transcriptional activity is coupled to nuclear tension (e.g., via the LINC complex or LMNA).
- **Assay Design:** Use CRISPR/Cas9 to endogenously tag LBX1 in chondrocytes. Apply cyclic mechanical stretch (1 Hz, 10% strain) to the cell culture. Concurrently, perturb nuclear tension using an established dominant-negative LINC complex disruptor (e.g., KASH domain overexpression).
- **Quantitative Readout:** Nuclear-to-cytoplasmic ratio of LBX1 fluorescence intensity, quantified via high-content imaging.
- **Expected Direction:** Mechanical stretch should increase the nuclear localization of LBX1, and this effect should be abrogated upon LINC complex disruption.
- **Falsification Threshold:** If the nuclear-to-cytoplasmic ratio of LBX1 changes by `< 1.2-fold` under stretch, or if the stretch-induced localization is entirely unaffected by LINC disruption (ratio change within 5% of wild-type), the hypothesis that LBX1 specifically integrates mechanical signals via nuclear tension is falsified.

## Experiment 3: In Silico Conformational Ensemble Validation
- **Hypothesis:** The blocky, intermediate-anisotropy geometry of LBX1 is robust to varying modeling assumptions and multimeric contexts, rather than an artifact of single-chain AlphaFold predictions.
- **Assay Design:** Perform ensemble-level structural predictions of LBX1 using AlphaFold-Multimer (exploring homo-dimer/trimer states), followed by 500 ns Molecular Dynamics (MD) relaxation simulations in explicit solvent using GROMACS.
- **Quantitative Readout:** Root Mean Square Deviation (RMSD) and Radius of Gyration ($R_g$) trajectories over the 500 ns MD simulation.
- **Expected Direction:** The overall anisotropic, blocky architecture should remain stable over the simulation timescale, maintaining an $R_g$ within 15% of the starting AlphaFold conformation.
- **Falsification Threshold:** If the MD trajectory shows massive structural collapse (e.g., $R_g$ decreases by `> 30%` within the first 100 ns) or if the domains completely dissolve into a disordered globule, the static AF structural hypothesis is falsified as a physically impossible conformation in solution.
