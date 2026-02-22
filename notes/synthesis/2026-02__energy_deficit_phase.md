# Synthesis: Energy Deficit Phase Diagram

**Date:** February 2026
**Hypothesis:** H_2026_02_08_EnergyPhase
**Artifacts:** `outputs/thermodynamic_cost/phase_diagram_energy_deficit.png`, `scripts/weekly_sim_energy_deficit_bifurcation.py`

## The Wedge of Vulnerability

We performed a 2D parameter sweep of the spinal system across Information-Elasticity Coupling strength ($\chi_\kappa$) and Spinal Length ($L$). The resulting phase diagram reveals a distinct **"Energy Deficit Window"** where the metabolic demand of maintaining counter-curvature ($P_{counter}$) exceeds the available proprioceptive supply ($S_{proprio}$).

### Key Findings

1.  **Wedge-Shaped Instability:**
    The deficit region ($R_{deficit} > 1$) forms a wedge shape in the $(\chi_\kappa, L)$ plane.
    -   **Low Coupling ($\chi_\kappa < 0.02$):** The system is stable. The metabolic cost of the weak correction is negligible, and supply always exceeds demand.
    -   **High Coupling ($\chi_\kappa > 0.08$):** The system enters the deficit window at shorter lengths (e.g., $L \approx 0.30$m) and exits later (or stays in deficit). This corresponds to **early-onset, severe scoliosis**.
    -   **Intermediate Coupling:** A finite window of vulnerability exists during the peak growth phase (adolescence), which closes as growth slows or supply catches up.

2.  **Clinical Risk Stratification:**
    This result suggests that $\chi_\kappa$ (the "gain" of the proprioceptive loop) is a critical risk factor.
    -   Patients with high intrinsic sensory gain (high $\chi_\kappa$) are "High Risk": they hit the metabolic ceiling earlier in development.
    -   This explains why some adolescents develop curves rapidly while others with similar growth rates do not—the *cost* of their specific spinal alignment strategy is higher.

### Mechanism

The instability arises from the scaling mismatch:
-   **Supply ($S_{proprio}$):** Scales sub-linearly or linearly with length ($\sim L^{0.7}$), reflecting the diffusion-limited or surface-area-limited nature of nutrient supply to the slender proprioceptive structures (e.g., muscle spindles, mechanosensors).
-   **Demand ($P_{counter}$):** Scales with the square of length ($\sim L^2$) and the square of the curvature deviation. High $\chi_\kappa$ drives larger active curvature corrections, acting as a multiplicative factor on the demand.

When $P_{counter} > S_{proprio}$, the system cannot thermodynamically sustain the high-fidelity counter-curvature, leading to **Convective Shutdown** or **Sensor Shedding** (as per the Anisotropy-Stability Link), resulting in a buckling-like collapse into scoliosis.
