# Weekly Synthesis: Energy Deficit Phase Diagram
**Date:** 2026-02-08
**Topic:** Thermodynamic Vulnerability in Parameter Space

## Overview
The weekly simulation `scripts/weekly_sim_energy_deficit_bifurcation.py` performed a 2D parameter sweep of the Energy Deficit Window across the Information-Elasticity Coupling strength ($\chi_\kappa$) and Spinal Length ($L$). This experiment maps the "thermodynamic risk landscape" for Adolescent Idiopathic Scoliosis (AIS).

## Key Findings

### 1. The Wedge of Instability
The phase diagram of the Energy Deficit Ratio ($R_{deficit} = P_{counter} / S_{proprio}$) reveals a distinct wedge-shaped instability region where $R_{deficit} > 1$.
- **Dependency on $\chi_\kappa$:** The metabolic cost of counter-curvature ($P_{counter}$) scales roughly as $\chi_\kappa^2$. Consequently, higher coupling strengths drive the system into energy deficit at significantly shorter spinal lengths.
- **Dependency on $L$:** As length increases, $P_{counter}$ grows faster ($~L^2$) than the proprioceptive supply ($~L^{0.7}$), eventually crossing the threshold.

### 2. Clinical Stratification
The results suggest a clear stratification mechanism for AIS onset:
- **High $\chi_\kappa$ (Strong Driver):** Patients enter the deficit window early in adolescence (short $L$). This corresponds to early-onset or severe juvenile scoliosis.
- **Moderate $\chi_\kappa$:** Patients enter the window during the peak growth spurt ($L \approx 0.35 - 0.45$ m). This matches the typical AIS demographic.
- **Low $\chi_\kappa$:** The trajectory may remain below the $R=1$ contour entirely, explaining why some individuals with similar growth rates never develop scoliosis ("Resilient" phenotype).

### 3. Lateral Instability (Cobb Angle)
The Cobb angle heatmap (`outputs/figures/phase_diagram_energy_deficit_cobb.png`) confirms that significant lateral deviation emerges primarily within the high-deficit region. This supports the hypothesis that the energy deficit—specifically the failure to fuel the active counter-curvature correction—is the proximal cause of the geometric collapse.

## Implication for Therapy
Therapeutic interventions should aim to either:
1.  **Reduce $\chi_\kappa$:** Dampen the intrinsic curvature drive (e.g., via localized inhibition of the specific signaling pathway).
2.  **Boost $S_{proprio}$:** Increase the available metabolic supply or efficiency of the proprioceptive system (e.g., metabolic support, specific exercise).
3.  **Delay Growth:** Slowing $\dot{L}$ might not help if the path eventually crosses the wedge, but it allows more time for $S_{proprio}$ to adapt if supply is rate-limited rather than capacity-limited.

## Reference Artifacts
- **Phase Diagram:** `outputs/figures/phase_diagram_energy_deficit.png`
- **Cobb Angle Map:** `outputs/figures/phase_diagram_energy_deficit_cobb.png`
- **Data:** `outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv`
