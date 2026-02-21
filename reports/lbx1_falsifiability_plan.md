# LBX1 Falsifiability Package
**Date:** 2026-02-20
**Focus:** Testing the "Blocky Switch" and "Entropic Rheostat" hypotheses for LBX1.

## Overview
LBX1 (Ladybird Homeobox 1) is a top GWAS hit for AIS, but our structural analysis (AFCC) shows it has **moderate anisotropy (2.27)** and **low structural confidence (pLDDT 66.9)**. This contradicts a direct "Tension Rod" role. We propose it acts as an **Entropic Rheostat**—a transcription factor whose nuclear localization or activity is gated by nuclear stiffness and crowding.

This document defines three concrete experiments to FALSIFY this hypothesis.

---

## Experiment 1: The Nuclear Stiffness Gate
**Hypothesis:** LBX1 nuclear entry or retention requires high nuclear stiffness (mediated by Lamin A/C), acting as a mechanosensor for tissue integrity.
**Rationale:** The "blocky" IDR structure of LBX1 may collapse or aggregate in soft nuclei (simulating microgravity or connective tissue defects).

### Assay Design
1.  **System:** C2C12 Myoblasts or Neural Progenitors (high endogenous tension).
2.  **Perturbation:**
    -   **Control:** Scramble siRNA.
    -   **Soft Nucleus:** `LMNA` knockdown (siRNA) or Latrunculin B (actin depolymerization).
    -   **Stiff Nucleus:** Overexpression of Lamin A (progerin mimic).
3.  **Reporter:** GFP-LBX1 fusion protein.

### Quantitative Readout
-   **Primary:** Nuclear-to-Cytoplasmic (N/C) fluorescence ratio via confocal microscopy.
-   **Secondary:** Transcriptional activity of LBX1 targets (e.g., *GCH1* luciferase reporter).

### Falsification Criteria
-   **Hypothesis Falsified If:** The N/C ratio and luciferase activity remain **statistically unchanged** (p > 0.05) between Control and `LMNA` knockdown conditions.
-   **Threshold:** A change of < 15% is considered biologically insignificant.

---

## Experiment 2: Condensation Dynamics (In Vitro)
**Hypothesis:** LBX1 functions via liquid-liquid phase separation (LLPS), which is sensitive to macromolecular crowding (entropic pressure).
**Rationale:** The low-confidence/IDR regions suggest propensity for condensation. If LBX1 is a standard globular protein, it should not condense.

### Assay Design
1.  **System:** Purified Recombinant LBX1-GFP in buffer.
2.  **Perturbation:** Titration of crowding agent (PEG-8000) from 0% to 20%.
3.  **Control:** Purified GFP (globular control).

### Quantitative Readout
-   **Primary:** Turbidity (OD600) and Droplet Count (microscopy).
-   **Secondary:** FRAP (Fluorescence Recovery After Photobleaching) to measure internal diffusion.

### Falsification Criteria
-   **Hypothesis Falsified If:**
    1.  LBX1 does not form droplets even at 20% PEG (remains soluble).
    2.  LBX1 forms solid aggregates immediately (no FRAP recovery), indicating misfolding rather than liquid condensation.
-   **Threshold:** Saturation concentration ($C_{sat}$) > 50 µM (unphysiological).

---

## Experiment 3: The Temporal Window (In Vivo)
**Hypothesis:** LBX1 expression is strictly coupled to the "Energy Deficit Window" of rapid spinal elongation and straightening.
**Rationale:** If LBX1 drives the "counter-curvature" reflex, it must be active during the specific developmental phase where $\chi_\kappa$ (proprioceptive gain) is high.

### Assay Design
1.  **System:** Zebrafish (*Danio rerio*) or Mouse development series.
2.  **Timeline:**
    -   **Zebrafish:** 24 hpf to 14 dpf (covering notochord straightening).
    -   **Mouse:** E10.5 to P10.
3.  **Measurement:**
    -   **Metric A:** Spinal curvature rate ($d\kappa/dt$) via morphometrics.
    -   **Metric B:** *LBX1* mRNA expression (qPCR) in dorsal root ganglia/neural tube.

### Quantitative Readout
-   **Primary:** Pearson correlation coefficient ($r$) between *LBX1* expression and straightening rate.

### Falsification Criteria
-   **Hypothesis Falsified If:**
    1.  *LBX1* expression peaks **after** the spine is fully straight.
    2.  *LBX1* expression is constant (constitutive) throughout development ($CV < 20\%$).
-   **Threshold:** Correlation $|r| < 0.5$.

---

## Summary of Expectations

| Experiment | Expected Result (Support) | Falsification Result (Reject) |
| :--- | :--- | :--- |
| **1. Stiffness Gate** | LBX1 mislocalizes in `LMNA` KD | LBX1 unaffected by `LMNA` KD |
| **2. Condensation** | Forms liquid droplets at phys. pH | Soluble or Aggregates |
| **3. Temporal** | Peaks during straightening | Constant or late expression |
