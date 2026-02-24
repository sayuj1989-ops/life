# Experiment Registry (2026-03-10)

| Experiment | Description | Output Location | Current Status/Result |
|---|---|---|---|
| `experiment_energy_deficit_window.py` | Simulates metabolic cost of counter-curvature maintenance at different spinal lengths. | `outputs/thermodynamic_cost/energy_deficit_window.csv` | **Complete.** Confirmed ~41% metabolic deficit at critical lengths. |
| `experiment_spinal_jetlag.py` | Tests effect of circadian phase mismatch ($\phi$) on spinal curvature. | `outputs/spinal_jetlag/jetlag_cycles.csv` | **Complete.** Validated $\phi=\pi$ (Jetlagged) yields 15.31° vs 10.03° (Entrained). |
| `experiment_optimization_failure.py` | Explores "Exploding Gradient" instability regime with noise and high coupling. | `outputs/optimization_failure/exploding_gradient.csv` | **Stable (Preliminary).** Shows stability (Cobb < 10°) up to $\chi_\kappa=20, \sigma_{noise}=2.0$. Needs higher range. |
| `bolt_biofold_analysis.py` | AlphaFold pipeline for structural metrics (pLDDT, PAE, curvature) of candidate proteins. | `outputs/bolt_biofold_report.md` | **Partial.** Analyzed 8 proteins (PIEZO2, COL1A1, etc.). FBN1 failed (404). |
| `sim_active_curvature_sweep.py` | Sweeps active curvature drive against anisotropy. | `outputs/sim/active_curvature_sweep/` (MISSING) | **Missing.** Script exists but output folder not found. Need to re-run. |
| `experiment_integrated_simulation.py` | Full integrated simulation combining gravity, growth, and IEC. | `outputs/integrated_sim/results.csv` | **Complete.** Results available for analysis. |
