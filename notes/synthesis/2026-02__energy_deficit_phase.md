# Synthesis: Energy Deficit Phase Diagram (2026-02)

## Overview
This week's simulation (`scripts/weekly_sim_energy_deficit_bifurcation.py`) mapped the **Energy Deficit Window** in the $(\chi_\kappa, L)$ parameter space, testing Hypothesis **H_2026_02_08_EnergyPhase**. The goal was to identify where the metabolic cost of counter-curvature ($P_{counter}$) exceeds the proprioceptive supply capacity ($S_{proprio}$), creating a region of instability ("vulnerability window").

## Key Findings

### 1. The Wedge-Shaped Instability Region
The 2D phase diagram reveals a distinct **wedge-shaped region** where $R_{deficit} = P_{counter} / S_{proprio} > 1$.
- **Low $\chi_\kappa$ (< 0.03):** The system remains stable ($R < 1$) throughout the growth period ($L \in [0.25, 0.55]$ m). These individuals likely represent the healthy population.
- **High $\chi_\kappa$ (> 0.05):** The system enters the deficit window at a shorter spinal length (earlier in adolescence). For example, at $\chi_\kappa = 0.08$, instability onset occurs around $L \approx 0.30$ m.
- **Scaling Effect:** The metabolic cost $P_{counter}$ scales roughly as $L^2$ (due to moment arms and mass), while supply $S_{proprio}$ scales as $L^{0.7}$ (allometric scaling). This mismatch means *everyone* eventually approaches a deficit, but high $\chi_\kappa$ (strong coupling/drive) accelerates this process, pushing the crossover point into the rapid growth phase.

### 2. Clinical Correlation
The simulation supports the "Mismatch" model of AIS onset:
- **Early Onset:** Patients with high intrinsic drive ($\chi_\kappa$) hit the energy wall earlier (shorter $L$).
- **Severity:** The magnitude of the deficit ($R \gg 1$) correlates with the potential for catastrophic collapse (Cobb angle amplification).
- **Vulnerability Window:** High $\chi_\kappa$ patients not only enter the window earlier but stay in it longer (or deeper) during the critical growth spurt.

### 3. Bifurcation Logic
The Cobb angle heatmap confirms that significant lateral deformation ("scoliosis") only emerges when $R_{deficit} > 1$. Below this threshold, lateral perturbations ($\epsilon_{asym}$) are corrected elastically. Above it, the feedback gain fails (or flips), amplifying the defect. This matches the clinical observation of a "tipping point" or bifurcation.

## Implications for Theory
- **Thermodynamic Limit:** Scoliosis may be fundamentally a thermodynamic failure—the inability to pay the metabolic bill for a straight spine against gravity during rapid growth.
- **Risk Stratification:** If $\chi_\kappa$ (active curvature drive) can be estimated early (e.g., via sagittal profile analysis), it could predict the "safe length" limit for a patient.

## Next Steps
- Validate the $L^{0.7}$ supply scaling assumption against metabolic data.
- Investigate if reducing $\chi_\kappa$ (e.g., via bracing or physiotherapy to reduce lordotic drive?) can exit the wedge.
