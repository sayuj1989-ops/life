# Research Execution Prompt: Validating the "Spinal Jetlag" Framework

**Role:** Computational Biologist & Experimental Neuroscientist
**Objective:** Operationalize the theoretical framework for Adolescent Idiopathic Scoliosis (AIS) by implementing the "Spinal Jetlag" simulation, estimating biological parameters from literature, and detailing the experimental protocols.

## Context

We have derived a rigorous theoretical framework (`scoliosis_theoretical_framework.md`) positing that AIS is a **control system failure** caused by:

1. **Delay-Induced Instability:** Feedback latency $\tau$ coupled with rapid growth $\dot{L}$.
2. **Symmetry Breaking:** Twist-bend coupling due to circadian phase shifts $\Delta \phi$ between left/right growth plates.

We must now move from **Theory** to **Validation**.

---

## Task 1: Computational Implementation (The Simulation)

**Goal:** Create `scripts/experiment_spinal_jetlag.py` to numerically solve the Delay Differential Equations (DDEs) derived in Section 3 & 4 of the framework.

**Requirements:**

1. **Equations:** Implement the coupled DDE system:
    $$
    \rho \ddot{\kappa}_1 + \eta \dot{\kappa}_1 + B_1 \kappa_1'''' + K \kappa_1(t-\tau) = 0 \quad \text{(Sagittal)}
    $$
    $$
    \rho \ddot{\kappa}_2 + \eta \dot{\kappa}_2 + B_2 \kappa_2'''' + \alpha_{TB} \omega'' = F_{circadian}(t) \quad \text{(Coronal)}
    $$
    $$
    I \ddot{\omega} + C \omega'' + \alpha_{TB} \kappa_2'' = M_{torsion}(t) \quad \text{(Axial)}
    $$
    *Note: Use `jitcdde` or `scipy.integrate` (handling delays via history functions).*

2. **Growth Kinematics:** Make $L(t)$, $\tau(t)$, and $B(t)$ time-dependent:
    - $\tau(t) = L(t)/v + \tau_0$
    - Growth function: Logistic curve peaking at $t=14$ years.

3. **Outputs:**
    - **Phase Diagram:** Plot Initial Perturbation vs. Growth Velocity $\dot{L}$. Color code by Cobb Angle.
    - **Time Evolution:** Animate the spine shape over the 2-year growth spurt. Show the transition from small oscillation to permanent helical deformity.

---

## Task 2: Parameter Estimation (Biological Grounding)

**Goal:** Find literature values to constrain the model parameters.

**Prompt:** "Search PubMed/biorxiv for the following physiological parameters in humans (adolescents) and model organisms (zebrafish/mice):"

1. **Proprioceptive Delay ($\tau$):** Conduction velocity of Ia afferents ($v_{nerve}$), synaptic delays in spinal cord vs. cortex.
    - *Target:* $\tau \approx 40-100$ ms?
2. **Spinal Stiffness ($B$):** Flexural rigidity ($EI$) of the adolescent spine (in vivo vs. cadaveric).
    - *Target:* $EI \approx 1-5$ Nm$^2$?
3. **Growth Velocity ($\dot{L}$):** Peak Height Velocity (cm/year) for males vs. females.
    - *Target:* $\sim 8-12$ cm/year.
4. **Circadian Phase Shift ($\Delta \phi$):** Magnitude of left-right asymmetry in clock gene expression (Per2/Bmal1) in bilateral tissues (e.g., somites).
    - *Target:* Is a 1-hour phase shift physically possible?

---

## Task 3: Experimental Protocol Design (The "Wet Lab" Plan)

**Goal:** Detail the steps for the "Smoking Gun" experiments (Section 6).

### Protocol A: The "Cooled Ganglion" (Rat Model)

* **Hypothesis:** Increasing $\tau$ induces scoliosis.
- **Method:**
    1. Design a minimal implantable cooling loop (Peltier or microfluidic) for L1-L5 DRGs.
    2. Target temperature: 15°C (slows conduction by ~50%).
    3. Control: Implant without cooling.
    4. Timeline: Cool for 4 hours/day during peak growth (weeks 4-8).

### Protocol B: The "Jetlagged" Zebrafish

* **Hypothesis:** Asymmetric circadian entrainment causes torsion.
- **Method:**
    1. Use `Tg(per2:luc)` reporter line to visualize clock phase.
    2. Chamber Design: Split-tank illumination. Left side: LD 12:12 (Phase 0). Right side: LD 12:12 (Phase +4h).
    3. Confocal Imaging: Measure vertebral aspect ratio and rotation weekly.

---

## Task 4: The "Grand Unification" Figure

**Goal:** conceptualize `research/figures/visual_abstract_final.png`.

**Layout:**

1. **Top:** The **"Gravity Well"**: Spacetime curvature visuals showing the metabolic cost of "standing still".
2. **Middle:** The **"Control Loop"**: A feedback diagram (CNS $\leftrightarrow$ Muscle) with a visible **Delay Block** ($e^{-s\tau}$).
3. **Bottom:** The **"Bifurcation"**:
    - Left: Stable Growth (Straight Spine).
    - Right: Unstable Growth (Helical Buckling).
    - Separated by the **"Energy Deficit Window"** (where Supply < Demand).

---

**Next Steps explicitly for the AI Agent:**

1. Execute **Task 1** immediately (Python implementation).
2. Use the results of Task 1 to refine the parameters for **Task 3**.
