# Weekly Synthesis: Energy Deficit Phase Diagram

**Date:** 2026-02-08
**Topic:** Energy Deficit Window Bifurcation in (χ_κ, L) Space
**Experiment:** `scripts/weekly_sim_energy_deficit_bifurcation.py`

## Key Findings

The 2D parameter sweep of the IEC coupling strength ($\chi_\kappa$) and spinal length ($L$) reveals a distinct wedge-shaped region of thermodynamic instability.

1.  **Instability Wedge:** The condition $R_{deficit} > 1$ (Metabolic Demand > Supply) forms a wedge that widens with increasing $\chi_\kappa$.
    *   **Low Coupling ($\chi_\kappa < 0.03$):** The spine remains thermodynamically stable ($R_{deficit} < 1$) throughout the growth window ($L=0.25-0.55$m).
    *   **High Coupling ($\chi_\kappa > 0.07$):** The spine enters the Energy Deficit Window early ($L \approx 0.35$m) and remains in deficit for a longer period, creating a broad vulnerability zone.

2.  **Multiplicative Scaling:** The metabolic cost $P_{counter}$ scales as $\sim \chi_\kappa^2 L^3$ (due to $L^2$ scaling of cost functional and linear scaling of curvature with $\chi_\kappa$ in the linear regime). This non-linear growth explains the rapid onset of deficit in high-coupling individuals.

3.  **Mechanical Stability vs. Metabolic Deficit:** The simulation shows that even when mechanically stable (low Cobb angle due to high baseline stiffness $E_0$), the system can be in severe metabolic deficit ($R_{deficit} \gg 1$). This suggests that AIS onset is primarily a metabolic failure of active correction, followed by mechanical collapse (buckling) only after the correction loop fails.

## Clinical Implications

This "Energy Phase Diagram" suggests a new risk stratification metric:
*   **High-Risk Cohort:** Adolescents with high innate spinal rigidity/coupling ($\chi_\kappa$) will hit the energy ceiling earlier in their growth spurt.
*   **Window Duration:** The severity of scoliosis may correlate with the *duration* spent inside the deficit wedge (Time integral of $R_{deficit} - 1$).

## Next Steps
*   Correlate $\chi_\kappa$ estimates from initial radiographs with age-at-onset.
*   Investigate if reducing $\chi_\kappa$ (e.g., via flexibility training or relaxin-like pathways) can narrow the instability wedge.
