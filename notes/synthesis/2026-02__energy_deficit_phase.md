# Weekly Synthesis: Energy Deficit Phase Diagram
**Date:** 2026-02-08
**Related Experiment:** `scripts/weekly_sim_energy_deficit_bifurcation.py`

## 1. The Wedge of Instability
The 2D parameter sweep across IEC coupling strength ($\chi_\kappa$) and spinal length ($L$) has revealed a distinct **wedge-shaped instability region** in the phase diagram.

- **Low Coupling ($\chi_\kappa < 0.03$):** The system remains energetically stable ($R_{deficit} < 1$) throughout the adolescent growth range ($L \in [0.25, 0.55]$ m). The metabolic cost of maintaining the target curvature is low enough that proprioceptive supply is never overwhelmed.
- **High Coupling ($\chi_\kappa > 0.06$):** The system enters the **Energy Deficit Window** at significantly shorter spinal lengths ($L_{crit} \approx 0.30$ m).
- **The Bifurcation:** As $L$ increases, the metabolic demand $P_{counter}$ scales as $\sim L^2$ (or higher depending on curvature intensity), while supply $S_{proprio}$ scales sub-linearly ($\sim L^{0.7}$). This creates a crossover point $L_{crit}$ that moves to the left (earlier in time) as $\chi_\kappa$ increases.

## 2. Clinical Risk Stratification
These findings suggest a counter-intuitive risk factor: **"Stronger" genetic instructions for spinal curvature (high $\chi_\kappa$) increase vulnerability.**

- **Early Onset:** Patients with high intrinsic drive for counter-curvature (high $\chi_\kappa$) will hit the energy ceiling earlier in their growth spurt. This correlates with the clinical observation that **Early Onset Scoliosis (EOS)** or early-adolescent onset is often more severe than late-onset cases.
- **Wider Vulnerability Window:** High $\chi_\kappa$ patients not only enter the window earlier but spend a larger fraction of their total growth period in the deficit state, allowing more time for plastic deformation (Hueter-Volkmann remodeling) to lock in the scoliotic curve.
- **Risk Prediction:** If $\chi_\kappa$ can be estimated from pre-symptomatic sagittal profiles (e.g., highly pronounced lordosis/kyphosis relative to vertebrae size), it could serve as a biomarker for high-risk progression.

## 3. Mechanism of Collapse
The simulation confirms that the onset of scoliosis in this model is a **metabolic bifurcation**, not a purely mechanical buckling event.
- The loss of lateral stability is triggered when the thermodynamic cost of the sagittal S-curve exceeds the available proprioceptive bandwidth ($R_{deficit} > 1$).
- In this regime, the system "sacrifices" lateral stiffness to maintain the sagittal primary curve, allowing small lateral asymmetries ($\epsilon_{asym} = 0.03$) to amplify into clinically significant Cobb angles ($> 10^\circ$).

## 4. Next Steps
- **Retrospective Validation:** We need to test the prediction that pre-onset sagittal curvature magnitude (proxy for $\chi_\kappa$) correlates with age at diagnosis in retrospective cohorts.
- **Metabolic Rescue:** Simulations should test if boosting $S_{proprio}$ (e.g., via metabolic interventions or sensory training) can shift the $L_{crit}$ boundary to the right, closing the window for high-risk patients.
