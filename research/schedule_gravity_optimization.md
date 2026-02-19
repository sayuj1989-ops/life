# Research Schedule: Gravity as an Optimization Process (12-Week Plan)

**Principal Investigator:** Jules
**Subject:** The "Gradient Descent" Model of Spinal Morphogenesis
**Target:** *Nature* Submission / Validated Computational Framework

## Executive Summary

We are formally redefining spinal growth as a **Gradient Descent Optimization** problem. The spine does not merely "grow"; it iteratively solves for a shape that minimizes a thermodynamic Cost Function ($U_{CC}$), balancing gravitational potential, elastic strain, and information density.

Scoliosis is therefore reclassified not as a disease of structure, but as a **failure of optimization**—specifically, a "Local Minimum" trap caused by a desynchronized "Learning Rate" (Circadian Clock) or a "Vanishing Gradient" (Microgravity/Disuse).

This 12-week schedule is designed to mathematically formalize this optimizer, break it in simulation ("Spinal Jetlag"), and design the physical experiments to prove it.

---

## Phase 1: Computational Proof-of-Concept (Weeks 1-4)
**Objective:** Encode the "Cost Function" $U_{CC}$ into `pyelastica_bridge.py` and demonstrate that a healthy spine is the Global Minimum of this function.

| Week | Focus | Task (Computational/Theoretical) | Hypothesis / Theoretical Component |
| :--- | :--- | :--- | :--- |
| **01** | **The Cost Function ($U_{CC}$)** | **Code:** Modify `compute_U_CC` in `pyelastica_bridge.py`. Explicitly sum: $U_{grav} + U_{elas} - \lambda I_{Info}$. <br>**Deliverable:** Heatmap of $U_{CC}$ for various spinal shapes (S, C, Straight). | The "Straight" spine is only the Global Minimum when Information Entropy is maximized ($\lambda I_{Info}$). Without it, the spine collapses (buckles). |
| **02** | **The Optimizer (Gradient Descent)** | **Code:** Implement a feedback loop where Growth Rate $\dot{L} \propto -\nabla U_{CC}$. <br>**Sim:** Run a simulation where a deformed spine "finds" the straight line via differential growth. | **Mechanotransduction as Gradient Calculation.** Piezo1/2 acts as the backpropagation algorithm, calculating the error vector relative to gravity. |
| **03** | **The Bio-Gravitational Number ($\mathcal{B}_g$)** | **Theory:** Define $\mathcal{B}_g = \frac{\rho g L^3}{EI \cdot \mathcal{S}_{sens}}$ (Gravity / Stiffness $\times$ Sensitivity). <br>**Code:** Parameter sweep of $\mathcal{B}_g$ in `weekly_sim_energy_deficit_bifurcation.py`. | **The Stability Boundary.** There exists a critical $\mathcal{B}_g^*$ above which the optimizer diverges (High gravity, low stiffness, or *hypersensitivity*). |
| **04** | **Simulating "Exploding Gradients"** | **Code:** Introduce "Sensory Noise" (random fluctuations in Piezo signaling). <br>**Sim:** High-gain feedback loops causing oscillations (Scoliosis). | **Scoliosis as Overfitting.** If the learning rate (sensitivity) is too high, the spine over-corrects for minor deviations, creating a permanent curve. |

---

## Phase 2: The "Spinal Jetlag" Simulation (Weeks 5-8)
**Objective:** Integrate Time. The "Learning Rate" is not constant; it is modulated by the Circadian Clock (BMAL1). We test what happens when the Clock and Gravity desynchronize.

| Week | Focus | Task (Computational/Theoretical) | Hypothesis / Theoretical Component |
| :--- | :--- | :--- | :--- |
| **05** | **The Circadian Learning Rate** | **Code:** Implement $\alpha(t) = A [1 + \sin(\omega t + \phi)]$ in the growth update loop. <br>**Sim:** Growth only occurs during "Night" (high $\alpha$). | **Gating.** The spine is only plastic (high learning rate) during sleep to prevent remodeling under transient daytime loads. |
| **06** | **"Spinal Jetlag" (Phase Shift)** | **Code:** Offset the Clock $\phi$ vs. the Loading Vector (Upright vs. Supine). <br>**Sim:** High Learning Rate while the agent is Upright (or upside down). | **The Mismatch.** If plasticity peaks when the spine is loaded asymmetrically (e.g., bad posture + disrupted clock), the optimizer "learns" the curve. |
| **07** | **Vector-Scalar Mismatch (Microgravity)** | **Code:** Set Gravity $\vec{g} \to 0$ but keep Fluid Pressure (Scalar Stress) high. <br>**Sim:** Run the optimizer with scalar noise but no directional gradient. | **Vanishing Gradient.** In microgravity, $\nabla U_{grav}$ vanishes. The optimizer drifts via random walk (entropic collapse) or locks into a local minimum. |
| **08** | **The Energy Deficit Window** | **Code:** Link `experiment_energy_deficit_window.py` with the Clock. <br>**Sim:** Cost of correction vs. Available Metabolic Power ($P_{supply}$). | **Metabolic Checkpointing.** Optimization stops if $\Delta U_{CC} > P_{supply}$. Scoliosis is a "frozen" optimization step due to energy bankruptcy. |

---

## Phase 3: Experimental Validation Design (Weeks 9-12)
**Objective:** Translate the computational findings into falsifiable wet-lab experiment designs.

| Week | Focus | Task (Experimental Design) | Hypothesis / Theoretical Component |
| :--- | :--- | :--- | :--- |
| **09** | **Experiment: "Test T_Clock"** | **Design:** Protocol for Bmal1-/- mice or Zebrafish under constant light (LL). <br>**Prediction:** Disrupted clock = Constant High Learning Rate = Severe Scoliosis under minor loads. | **Chronotherapy.** Does restoring the rhythm (e.g., Melatonin) rescue the curvature? |
| **10** | **Experiment: The "Sensor-Blind" Control** | **Design:** Piezo1 conditional knockout (Osteoblast specific). <br>**Prediction:** The optimizer receives $\nabla U = 0$. Result: Hypoplastic, straight spine (no growth) or immediate buckling (no correction)? | **Gradient Necessity.** Without the gradient (Piezo), the cost function is invisible to the cells. |
| **11** | **Experiment: The Clinostat (Microgravity)** | **Design:** 3D Clinostat setup for organoids/Zebrafish. <br>**Prediction:** "Vector-Scalar Mismatch" phenotype (High bone density but poor alignment). | **Scalar vs. Vector.** Confirm that cells sense *magnitude* (pressure) but lose *orientation* (gravity). |
| **12** | **Synthesis & Submission** | **Docs:** Compile `formalism_01.md`, simulation heatmaps, and experimental designs into the *Nature* manuscript. <br>**Task:** Finalize `manuscript.md` and `cover_letter.txt`. | **The Grand Unified Theory.** Gravity is the instructor; the Spine is the neural network; the Clock is the scheduler. |

---

## Risk Assessment & Bottlenecks

### 1. Theoretical Risk: The Cost Function is Non-Convex
*   **Risk:** The simulation might get stuck in local minima (scoliosis) *too easily*, making it hard to simulate a healthy spine.
*   **Mitigation:** Calibrate the "Elastic" term. A strong enough elastic reference (The Notochord/IVD) should smooth the landscape. We will use the `Bio-Gravitational Number` to find the convexity threshold.

### 2. Computational Risk: Time-Scale Discrepancy
*   **Risk:** Growth happens over months (slow); muscle tone happens in milliseconds (fast). Simulating both in `PyElastica` is computationally expensive.
*   **Mitigation:** Use "Quasi-Static" updates. Solve the elastic equilibrium (fast), then take one large "Growth Step" (slow), assuming the fast dynamics average out.

### 3. Experimental Risk: Separating Clock from Activity
*   **Risk:** In animals, disrupting the clock also disrupts sleep/activity, changing the mechanical load.
*   **Mitigation:** The "Microgravity" (Clinostat) control. If the clock effect persists even without gravity load, it proves the "Learning Rate" hypothesis is distinct from mechanical load magnitude.

---

### Immediate Next Step
I will begin **Week 01** by inspecting `src/spinalmodes/countercurvature/pyelastica_bridge.py` to explicitly formalize the `compute_U_CC` function to match the $U_{grav} + U_{elas} - \lambda I_{Info}$ definition.
