# Pending Work Registry (2026-03-10)

This registry tracks specific, actionable tasks for the "Biological Counter-Curvature" project.

## Theme: Clinical Validation (High Priority)
- [ ] **Extract Cohort Data:** Retrieve Cobb angle distributions, Peak Height Velocity (PHV) timing, and curve progression rates from published literature (e.g., Lonstein et al., 2008).
    - *Effort:* 3 days.
    - *Dependencies:* Access to journals.
    - *Risk:* Data gaps for specific parameters.
- [ ] **PHV Timing Analysis:** Map model "Instability Window" to extracted PHV timing data.
    - *Effort:* 1 day.
- [ ] **Sexual Dimorphism Check:** Run simulations with male vs. female growth rates to test prevalence prediction.
    - *Effort:* 2 days.

## Theme: Code & Experiments (Medium Priority)
- [ ] **Fix FBN1 Retrieval:** Debug `bolt_biofold_analysis.py` to handle FBN1 (P35555) data fetching (currently 404 error).
    - *Effort:* 1 hour.
- [ ] **Exploding Gradient Search:** Run `experiment_optimization_failure.py` with higher $\chi_\kappa$ (e.g., 20-50) and $\sigma_{noise}$ (e.g., 2.0-5.0) to find the instability threshold.
    - *Effort:* 2 days (compute intensive).
    - *Current Result:* Stable up to $\chi_\kappa=20$.
- [ ] **Spinal Jetlag - Phase Sweep:** Run finer sweep of phase mismatch $\phi$ (e.g., $\pi/4$ increments) to map the full response curve.
    - *Effort:* 1 day.
    - *Current Result:* Validated at $\phi=0$ and $\phi=\pi$.

## Theme: Manuscript & Figures (High Priority)
- [ ] **Shorten Abstract:** Reduce from 210 words to 150 words (Nature limit) or structured format (*Spine* requirement).
    - *Effort:* 2 hours.
    - *Status:* Draft needs edit.
- [ ] **Expand References:** Add 70+ citations, focusing on *Spine*, *Eur Spine J*, and recent mechanobiology papers (2023-2025).
    - *Effort:* 1 day.
    - *Status:* 15 core refs present.
- [ ] **Generate Figure 1 (Phase Diagram):** Create high-res plot of $\eta = I/(\rho g L^2)$ showing 3 regimes.
    - *Effort:* 4 hours.
    - *Source:* `outputs/thermodynamic_cost/phase_diagram_energy_deficit.csv` (Verified exists).
- [ ] **Generate Figure 2 (S-Curve):** Visualize rod configurations at increasing coupling strengths.
    - *Effort:* 4 hours.
    - *Source:* `outputs/integrated_sim/results.csv` (Verified exists).
- [ ] **Generate Figure 3 (Cross-Species):** Plot predicted vs. observed curvature for 9 species.
    - *Effort:* 1 day (Data missing).
    - *Source:* `data/comparative_morphology.csv` (Missing - need to recreate/extract).

## Theme: Theory (Low Priority)
- [ ] **Toy Model - 1D Spring Chain:** Implement simple 1D model to demonstrate IEC principle without full Cosserat complexity.
    - *Effort:* 1 day.
- [ ] **Toy Model - Thermostat:** Implement scalar control loop to demonstrate "Exploding Gradient" mechanism.
    - *Effort:* 1 day.
