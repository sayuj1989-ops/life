# Research Schedule: Gravity as an Optimization Process

## Summary
This 12-week research schedule outlines the computational and experimental validation of the "Gravity as an Optimization Process" hypothesis for spinal alignment. The central premise is that the spine minimizes a Total Potential Energy cost function ($U_{CC}$) via a gradient descent process, where the learning rate is modulated by the Circadian Clock (Spinal Jetlag) and stability is governed by the Bio-Gravitational Number ($\mathcal{B}_g$).

**Objective:** To demonstrate that Scoliosis is a failure of this optimization process—either a local minimum (stable deformity) or an exploding gradient (instability)—caused by sensory noise, circadian desynchronization, or scaling mismatches.

**Tools:** `pyelastica` (Physics Engine), `formalism_01.md` (Theory), `experiment_optimization_failure.py`, `experiment_spinal_jetlag.py`.

---

## Phase 1: Computational Proof-of-Concept (Weeks 1-4)
**Focus:** Defining the Cost Function and Simulating Optimization Failure.
**Goal:** Establish the baseline "Healthy" optimization and map the "Failure" landscape.

| Week | Focus | Task (Code/Experiment) | Hypothesis / Theory |
| :--- | :--- | :--- | :--- |
| **1** | **The Cost Function ($U_{CC}$)** | **Script:** `scripts/calculate_bio_gravitational_number.py`<br>Implement the calculation of $\mathcal{B}_g$ and $U_{CC}$ (Gravity + Elasticity - Information) for different species (Zebrafish, Mouse, Human). <br>**Ref:** `formalism_01.md` (Sec 2.3, 5). | **H_Bg_Scaling:** $\mathcal{B}_g \approx 1$ is a conserved constant across healthy species. Scoliosis occurs when $\mathcal{B}_g < 1$ (Gravity dominance). |
| **2** | **Optimization Failure** | **Script:** `scripts/experiment_optimization_failure.py`<br>Refine the "Exploding Gradient" map. Sweep `chi_kappa` (Learning Rate) vs. `sigma_noise` (Sensory Noise).<br>**Action:** Add a "Local Minimum" detection metric (stable high energy state). | **H_ExplodingGradient:** High learning rate ($\eta_{spine}$) + High Noise ($\sigma$) $\to$ Instability. |
| **3** | **Vector-Scalar Mismatch** | **Script:** `scripts/experiment_vector_scalar_mismatch.py`<br>Simulate Microgravity ($g \to 0$) by removing the Vector component of the load while maintaining the Scalar (pressure) component.<br>**Ref:** `formalism_01.md` (Sec 2.7, 2.20). | **H_VS_Mismatch:** The organism relies on the Vector/Scalar ratio ($\Phi_{VS}$) to orient. In $\mu g$, $\Phi_{VS} \to 0$, causing "Geometric Hallucination". |
| **4** | **The Critical Length ($L_{crit}$)** | **Script:** `scripts/experiment_energy_deficit_window.py`<br>Validate the "Energy Deficit Window" where metabolic supply ($L^{0.5}$) fails to meet mechanical demand ($L^2$).<br>**Action:** Correlate $L_{crit}$ with the adolescent growth spurt. | **H_Scaling_Catch22:** Instability is inevitable at specific developmental lengths unless $\chi_M$ (Stiffness) scales super-linearly. |

---

## Phase 2: The "Spinal Jetlag" Simulation (Weeks 5-8)
**Focus:** Integrating Time-Dependent Learning Rates (Circadian Clock).
**Goal:** Demonstrate that temporal desynchronization drives geometric instability.

| Week | Focus | Task (Code/Experiment) | Hypothesis / Theory |
| :--- | :--- | :--- | :--- |
| **5** | **The Clock Model** | **Script:** `scripts/experiment_spinal_jetlag.py`<br>Implement the `chi_kappa(t)` modulation with phase offset $\phi$.<br>**Action:** Verify "Entrained" ($\phi=0$) vs "Free-running" dynamics. | **H_SpinalJetlag:** Gravity acts as a Zeitgeber. Loss of gravity causes phase drift ($\phi \to \pi$), inverting the learning rate during sleep. |
| **6** | **Desynchronization** | **Script:** `scripts/experiment_spinal_jetlag.py`<br>Simulate "Shift Work" or "Jetlag" conditions where the loading cycle is anti-phase to the clock.<br>**Measure:** Cobb angle progression over 30 cycles. | **H_Destructive_Interference:** Anti-phase loading suppresses the "Repair Phase" of the disc, accumulating micro-damage. |
| **7** | **The Stiffness Resonance** | **Script:** `scripts/experiment_peristaltic_spine.py`<br>Model the "Peristaltic Sweep" of stiffness ($\mathcal{K}_{som}$).<br>**Action:** Test if a *traveling* stiffness wave stabilizes the spine better than a static one. | **H_Peristaltic_Rescue:** A traveling stiffness wave prevents buckling by "moving" the weak point before instability grows. |
| **8** | **Microgravity Decay** | **Script:** `scripts/experiment_spinal_jetlag.py`<br>Implement amplitude decay $A(t)$ in the absence of gravity ($g=0$).<br>**Ref:** `formalism_01.md` (Sec 2.11, Entrainment Number $\mathcal{E}_{mech}$). | **H_Amplitude_Death:** Without mechanical entrainment, the spinal clock amplitude $A \to 0$, leading to a "plasticity freeze" ($\eta_{spine} \to 0$). |

---

## Phase 3: Experimental Validation Design (Weeks 9-12)
**Focus:** Designing Wet-Lab Experiments to Validate Computational Predictions.
**Goal:** Output concrete protocols for biological validation.

| Week | Focus | Task (Experiment Design) | Hypothesis / Theory |
| :--- | :--- | :--- | :--- |
| **9** | **Test T_Clock** | **Design:** "The Jetlagged Disc"<br>**Protocol:** Culture IVD explants in a bioreactor with cyclic compression. Shift the phase of loading by 12h relative to the Bmal1-Luc reporter.<br>**Output:** `protocols/exp_jetlagged_disc.md` | **H_Phase_Sensitivity:** Anti-phase loading will downregulate anabolic genes (*ACAN*, *COL2A1*) compared to in-phase loading. |
| **10** | **Test B_g** | **Design:** "The Gravity Centrifuge"<br>**Protocol:** Raise Zebrafish/Mice at 2g vs 1g.<br>**Measure:** Paraspinal muscle density and Spinal Linearity.<br>**Output:** `protocols/exp_hypergravity.md` | **H_Hypergravity_Adaptation:** Organisms in 2g will upregulate $\chi_M$ (Muscle/Stiffness) to maintain $\mathcal{B}_g \approx 1$. Failure to do so leads to buckling. |
| **11** | **Test Vector-Scalar** | **Design:** "The Magnetic Rescue"<br>**Protocol:** Use magnetic tweezers to apply directional force (Vector) to otoliths/cilia in a microgravity analog (Clinostat).<br>**Output:** `protocols/exp_magnetic_rescue.md` | **H_Vector_Rescue:** Artificial restoration of the Vector signal will rescue the "Scalar Hallucination" phenotype. |
| **12** | **Manuscript Synthesis** | **Task:** Compile all results into the final *Nature*/*Spine* manuscript.<br>**Action:** Update `manuscript/submission_manuscript.tex` with Phase 1 & 2 plots and Phase 3 protocols.<br>**Ref:** `manuscript/checklist_compliance.txt`. | **H_Grand_Synthesis:** Gravity is not just a load; it is an information channel essential for the optimization of biological shape. |

---

## Risk Assessment

1.  **Theoretical Risk:** The "Bio-Gravitational Number" $\mathcal{B}_g$ might vary significantly between species (scaling violation), requiring a non-linear correction term (e.g., $\mathcal{B}_g \propto L^{\alpha}$).
    *   *Mitigation:* Use `scripts/calculate_bio_gravitational_number.py` to fit $\alpha$ from existing allometric data before running full simulations.

2.  **Computational Risk:** `pyelastica` simulations for "Spinal Jetlag" (long timescales) might be computationally expensive.
    *   *Mitigation:* Use the "Quasi-Static Cycle" approximation implemented in `experiment_spinal_jetlag.py` (simulating snapshots rather than continuous time) to speed up sweeps.

3.  **Experimental Risk:** "Vector-Scalar" dissociation is difficult to achieve purely pharmacologically.
    *   *Mitigation:* Prioritize the "Magnetic Rescue" design (physical force) over purely chemical perturbations.
