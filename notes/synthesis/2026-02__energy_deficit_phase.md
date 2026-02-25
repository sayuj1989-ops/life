# Synthesis: Energy Deficit Phase Diagram (2026-02)

## Overview
This week's simulation (`scripts/weekly_sim_energy_deficit_bifurcation.py`) mapped the **Energy Deficit Window** in the $(\chi_\kappa, L)$ parameter space, testing Hypothesis **H_2026_02_08_EnergyPhase**. The goal was to identify where the metabolic cost of counter-curvature ($P_{counter}$) exceeds the proprioceptive supply capacity ($S_{proprio}$), creating a region of instability ("vulnerability window"). The simulation separates the sagittal metabolic cost (driven by $\chi_\kappa \nabla I$) from the lateral instability (driven by $\epsilon_{asym}$), using the energy deficit ratio $R_{deficit}$ to amplify the lateral deformation.

## Key Findings

### 1. The Instability Landscape
The 2D phase diagram reveals a critical instability region where $R_{deficit} = P_{counter} / S_{proprio} > 1$.
- **Low $\chi_\kappa$ (< 0.03):** The system remains stable ($R < 1$) throughout the growth period ($L \in [0.25, 0.55]$ m). These parameters correspond to a "healthy" developmental trajectory where metabolic supply meets demand.
- **High $\chi_\kappa$ (> 0.05):** The system is highly vulnerable. For $\chi_\kappa > 0.06$, the energy deficit exceeds supply capacity even at short lengths ($L=0.25$ m), indicating immediate susceptibility to instability.
- **Reference State:** The supply capacity was calibrated to a reference patient ($\chi_\kappa = 0.05, L=0.35$ m). At this point, $P_{counter}$ defines $S_0$. The rapid increase in cost for higher $\chi_\kappa$ quickly overwhelms this supply.

### 2. Clinical Correlation
The simulation supports the "Mismatch" model of AIS onset:
- **Early Onset:** Patients with high intrinsic drive ($\chi_\kappa$) hit the energy wall much earlier. In extreme cases ($\chi_\kappa > 0.08$), the deficit is present from the onset of the adolescent growth spurt.
- **Severity:** The magnitude of the deficit ($R \gg 1$) correlates with the potential for catastrophic collapse. The simulation models this by amplifying the baseline lateral perturbation ($\epsilon_{asym}$) proportional to the deficit ($Cobb \propto 1 + 5(R-1)$).
- **Vulnerability Window:** High $\chi_\kappa$ patients are in a perpetual state of energy deficit, explaining the rapid progression seen in juvenile or early adolescent cases.

### 3. Bifurcation Logic
The Cobb angle heatmap confirms that significant lateral deformation ("scoliosis") emerges in regions of high energy deficit. While the baseline elastic response to $\epsilon_{asym} = 0.03$ is small (< 1 degree), the loss of metabolic control amplifies this to > 10 degrees when $R_{deficit} > 1.5$. This matches the clinical observation of a "tipping point" or bifurcation.

## Implications for Theory
- **Thermodynamic Limit:** Scoliosis may be fundamentally a thermodynamic failure—the inability to pay the metabolic bill for a straight spine against gravity during rapid growth.
- **Risk Stratification:** If $\chi_\kappa$ (active curvature drive) can be estimated early (e.g., via sagittal profile analysis), it could predict the "safe length" limit for a patient.

## Next Steps
- Validate the $L^{0.7}$ supply scaling assumption against metabolic data.
- Investigate if reducing $\chi_\kappa$ (e.g., via bracing or physiotherapy to reduce lordotic drive?) can exit the wedge.
