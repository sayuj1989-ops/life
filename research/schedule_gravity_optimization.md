# Research Schedule: Gravity as a Morphogenetic Optimizer

**Principal Investigator:** Jules (AI)
**Date:** October 26, 2026
**Subject:** 12-Week Execution Plan for Project "Spinal Descent"

## Executive Summary

This schedule operationalizes the hypothesis that spinal morphogenesis is a **Stochastic Gradient Descent (SGD)** process where the organism minimizes a functional $U_{CC}$ (Counter-Curvature Potential). We posit that Idiopathic Scoliosis is an "Optimization Failure"—specifically, an **Exploding Gradient** problem caused by a mismatch between the **Learning Rate** (Circadian Sensitivity) and the **Error Signal** (Gravitational Strain).

Our primary theoretical tool is the **Bio-Gravitational Number ($\mathcal{B}_g$)**, a dimensionless quantity representing the ratio of Gravitational Drive to Elastic Resistance. Our primary failure mode to investigate is **"Spinal Jetlag,"** where the internal learning rate scheduler (the Circadian Clock) desynchronizes from the external error signal (the Gravity Vector).

---

## Phase 1: The Optimization Landscape (Weeks 1-4)
**Objective:** Define the Cost Function $U_{CC}$ in `pyelastica` and simulate "Static" Optimization Failure.

| Week | Focus | Task (Computational/Theoretical) | Hypothesis |
| :--- | :--- | :--- | :--- |
| **1** | **The Cost Function** | **Refactor `pyelastica_bridge.py`:** Implement a monitoring callback that explicitly calculates $U_{total} = U_{elastic} + U_{grav} - U_{info}$ at each timestep. Visualize the "Energy Landscape" of a healthy spine. | The spine naturally settles into a global minimum of $U_{total}$ when $\mathcal{B}_g \approx 1$. |
| **2** | **The Gradient (Error Signal)** | **Implement "Active Error Feedback":** Modify the `ScoliosisMuscle` class. Instead of fixed activation, make muscle tension proportional to the local curvature error: $\tau \propto -\alpha (\kappa_{current} - \kappa_{target})$. | A simple proportional controller (P-controller) is sufficient to maintain spinal verticality under static gravity. |
| **3** | **Exploding Gradients** | **Simulate Feedback Gain Failure:** In `experiment_optimization_failure.py`, systematically increase the feedback gain $\alpha$ (the "Learning Rate") and introduce sensory noise. Look for bifurcation points where the spine buckles into a stable S-curve (a "Local Minimum"). | **H1 (The High-Gain Hypothesis):** Scoliosis is caused by *over-correction* to sensory noise, not weakness. High $\alpha$ leads to instability. |
| **4** | **The Bio-Gravitational Number** | **Dimensional Analysis & Sweep:** rigorous calculation of $\mathcal{B}_g = \frac{\rho g L^3}{EI}$ for Human vs. Mouse parameters. Run a parameter sweep in `weekly_sim_growth_anisotropy_map.py` to find the critical $\mathcal{B}_g$ where the "Optimizer" fails. | Humans exist near a critical phase transition ($\mathcal{B}_g \approx \mathcal{B}_{critical}$) making them uniquely susceptible to optimization errors. |

---

## Phase 2: Temporal Dynamics & "Spinal Jetlag" (Weeks 5-8)
**Objective:** Integrate Time ($t$) and the Circadian Clock as the "Learning Rate Scheduler."

| Week | Focus | Task (Computational/Simulation) | Hypothesis |
| :--- | :--- | :--- | :--- |
| **5** | **The Learning Rate Scheduler** | **Implement `CircadianModulationCallback`:** Create a time-dependent scaler $A(t) = \sin(\omega t + \phi)$ that modulates the feedback gain $\alpha$. The spine is "plastic" (high learning rate) only at night. | The "Learning Rate" must be synchronized with the "Repair Phase" (Night) to prevent erroneous remodeling. |
| **6** | **Spinal Jetlag (Desynchrony)** | **Run `experiment_spinal_jetlag.py`:** Simulate a mismatch between the internal clock phase $\phi_{clock}$ and the external gravity load phase $\phi_{gravity}$. Shift the "Plasticity Window" to the "High Activity" period. | **H2 (Spinal Jetlag):** Remodeling during high physical load (Daytime) instead of low load (Night) causes the optimizer to diverge, cementing deformities. |
| **7** | **Vector-Scalar Mismatch** | **Simulate Microgravity:** Set the gravity vector $\vec{g} \to 0$ but maintain high scalar hydrostatic pressure (swelling) $P_{scalar}$. Use the `solve_beam_static` function to see if the spine expands or buckles without a directional cue. | **H3 (The Blind Optimizer):** Without the vector cue $\vec{g}$, the scalar signal $P$ causes isotropic expansion (lengthening) but loss of geometric fidelity. |
| **8** | **The Damping Factor** | **Viscoelastic Analysis:** Introduce a "Damping" term $\gamma$ into the simulation that represents passive tissue viscosity. Test if high damping rescues the "Exploding Gradient" from Week 3. | Viscoelasticity acts as a "Momentum" term in the SGD optimizer, smoothing out high-frequency sensory noise. |

---

## Phase 3: Experimental Validation Design (Weeks 9-12)
**Objective:** Design Wet-Lab Experiments to validate the "Gradient Descent" model.

| Week | Focus | Task (Experimental Design) | Hypothesis |
| :--- | :--- | :--- | :--- |
| **9** | **The "Clock-less" Spine** | **Design "Test T_Clock":** Protocol for a mouse model with *Bmal1* conditional knockout in Osteoblasts vs. Neurons. Compare spinal alignment under normal gravity vs. hypergravity (centrifuge). | Loss of the "Scheduler" (*Bmal1*) will result in spontaneous scoliosis even without mechanical triggers. |
| **10** | **Pharmacological "Gradient Clipping"** | **Beta-Blocker Design:** Based on `H_2026_11_05_BetaBlocker`, design a study using Propranolol to "dampen" the sympathetic feedback loop (the Gradient) in a scoliotic mouse model. | Reducing the sympathetic gain (lowering the Learning Rate) effectively "clips the gradient," preventing the optimizer from exploding. |
| **11** | **The "Scalar" Trap** | **Agonist Rescue Study:** Design an experiment using Yoda1 (Piezo1 agonist) in a microgravity analog (Hindlimb Unloading). Can we substitute the missing vector $\vec{g}$ with a chemical scalar signal? | **H4 (The Scalar Fallacy):** Scalar agonists cannot rescue vector defects; they will increase bone mass but fail to restore alignment. |
| **12** | **Synthesis & Manuscript** | **Compile Results:** Aggregate Phase 1 & 2 simulation data into `manuscript/sections/results.tex`. Finalize the "Gravity as Optimization" theory section in `formalism_01.md`. | N/A (Documentation & Dissemination). |

---

## Risk Assessment & Theoretical Bottlenecks

1.  **The "Local Minimum" Trap (High Risk):**
    *   *Risk:* The simulation might simply converge to a straight line (Global Minimum) or a completely chaotic state, failing to reproduce the specific *shape* of Scoliosis (a stable Local Minimum).
    *   *Mitigation:* We must carefully tune the "Energy Barrier" in the Cost Function. The active "Counter-Curvature" mechanism must be strong enough to create a potential well at the scoliotic angle.

2.  **Parameter Sensitivity (Medium Risk):**
    *   *Risk:* The Bio-Gravitational Number $\mathcal{B}_g$ might be too sensitive to unknown biological parameters (e.g., exact IVD stiffness).
    *   *Mitigation:* Perform robust parameter sweeps (Week 4) to identify the *topological* features of the phase space, rather than relying on precise numerical values.

3.  **Circadian Coupling (Theoretical Risk):**
    *   *Risk:* The assumption that *Bmal1* directly modulates mechanical sensitivity (the "Learning Rate") might be too simplistic.
    *   *Mitigation:* Literature review (Week 5) to identify specific "Clock-Controlled Genes" (CCGs) that are also mechanosensors (e.g., checking if *Piezo2* promoter has E-box elements).

4.  **Computational Cost:**
    *   *Risk:* Long-term circadian simulations (weeks of biological time) are computationally expensive in `pyelastica`.
    *   *Mitigation:* Use "Time-Slicing" techniques—simulate short bursts of physics to calculate the gradient, then update the "growth" parameters analytically for the inter-burst periods.
