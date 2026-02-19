# Synthesis: Energy Deficit Phase Diagram

**Date:** 2026-02
**Simulation:** `scripts/weekly_sim_energy_deficit_bifurcation.py`
**Hypothesis ID:** `H_2026_02_08_EnergyPhase`

## Summary
This weekly simulation performed a 2D parameter sweep of the Information-Elasticity Coupling (IEC) strength ($\chi_\kappa$) and spinal length ($L$) to map the "Energy Deficit Window" where metabolic demand for posture maintenance ($P_{counter}$) exceeds the proprioceptive supply capacity ($S_{proprio}$).

## Key Findings

1.  **Wedge-Shaped Instability Region**:
    The phase diagram of the Energy Deficit Ratio ($R_{deficit} = P_{counter} / S_{proprio}$) reveals a distinct wedge-shaped region of vulnerability ($R > 1$).
    -   **Low Coupling ($\chi_\kappa < 0.03$)**: The spine remains largely within the safe zone ($R < 1$) throughout growth.
    -   **High Coupling ($\chi_\kappa > 0.06$)**: The deficit window opens at shorter spinal lengths (or exists from onset) and persists longer. The critical length for stabilization ($R$ dropping below 1) increases as coupling strength increases.

2.  **Correlation with Scoliosis Emergence**:
    The emergence of non-zero Cobb angles (lateral instability) correlates strongly with the Energy Deficit region. While the IEC model primarily drives sagittal counter-curvature, the metabolic deficit creates a permissive environment for lateral buckling under gravity.

## Clinical Implications
This result provides a theoretical basis for risk stratification based on "Morphogenetic Drive" ($\chi_\kappa$):
-   **High-$\chi_\kappa$ Phenotype**: Patients with strong genetic/epigenetic curvature targets are at double risk: they generate higher metabolic costs *and* enter the deficit window earlier (or remain in it longer). This predicts earlier onset and more rapid progression.
-   **Intervention Window**: The phase diagram suggests that metabolic interventions (boosting $S_{proprio}$ or reducing demand) must be timed according to the patient's specific ($\chi_\kappa, L$) trajectory to prevent crossing (or staying within) the $R=1$ boundary.
