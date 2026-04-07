# LBX1 Falsifiability Plan

## Overview
This document outlines explicit criteria to falsify the hypothesis linking LBX1 to biomechanical mechanosensing in the context of S-shaped spinal growth and the Biological Countercurvature theory. Given its low AlphaFold confidence (pLDDT ~66.9) and intermediate anisotropy (~2.27), its structural geometry does not deterministically support a role as a load-bearing mechanosensor.

These tests aim to strictly separate inferences from direct measurements.

Source Context: `outputs/afcc/2026-02-16/metrics.csv`
Analysis Date: 2026-04-07

## Experiment 1: In Vitro Tension Sensitivity Assay
**Hypothesis:** If LBX1 directly participates in mechanotransduction, its nuclear localization or expression levels will significantly change in response to cyclical mechanical loading.
**Assay Design:** Apply physiological cyclical strain (10% strain, 1 Hz) to human myoblasts or osteoblasts cultured on elastic silicone membranes for 24 hours.
**Quantitative Readout:** Ratio of nuclear to cytoplasmic LBX1 protein concentration (via immunofluorescence) and LBX1 mRNA fold-change (via RT-qPCR) vs. static control.
**Expected Direction:** Increased nuclear localization and/or transcriptional upregulation in mechanically loaded cells.
**Falsification Threshold:** If the fold-change in nuclear localization or mRNA expression is < 1.2x compared to static controls across three biological replicates, the direct mechanotransduction link is falsified.

## Experiment 2: LBX1 Null Mutant Morphogenic Response
**Hypothesis:** If LBX1 is essential for gravity-induced S-shaped spinal curvature, removing it should abolish curve formation under gravity loading.
**Assay Design:** Utilize a conditional *Lbx1* knock-out mouse model. Subject KO and Wild-Type (WT) cohorts to a bipedal loading protocol (harness/treadmill) designed to induce spinal countercurvature.
**Quantitative Readout:** Cobb angle or 3D spine curvature metrics via micro-CT at baseline and post-loading (6 weeks).
**Expected Direction:** WT mice develop significantly increased curvature; KO mice fail to develop curvature in response to the same bipedal mechanical load.
**Falsification Threshold:** If the post-loading Cobb angle variance between WT and KO cohorts is statistically insignificant (p > 0.05), LBX1 is falsified as the *primary driver* of load-induced spinal countercurvature.

## Experiment 3: Recombinant Protein Rigidity (Atomic Force Microscopy)
**Hypothesis:** If the high anisotropy seen in exploratory AlphaFold models represents a true mechanosensitive rod (rather than a highly flexible/disordered region), the purified protein should exhibit high mechanical stiffness.
**Assay Design:** Single-molecule force spectroscopy using Atomic Force Microscopy (AFM) on purified full-length LBX1 protein.
**Quantitative Readout:** Persistence length (nm) and unfolding force (pN) derived from force-extension curves.
**Expected Direction:** High persistence length comparable to known structural proteins like fibronectin or titin modules.
**Falsification Threshold:** If the measured persistence length is comparable to a random coil (< 2 nm) and lacks discrete unfolding steps under tension, the hypothesis that LBX1 acts as an extended structural tension-sensor is falsified.
