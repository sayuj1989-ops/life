# Research Schedule: Gravity as an Optimization Process

**Principal Investigator:** Jules (AI Assistant)
**Date:** October 2026
**Topic:** Theoretical Biology and Biomechanics of Spinal Alignment

## Summary

This research schedule outlines a 12-week program to test the "Gravity as an Optimization Process" framework. We posit that spinal alignment is a gradient descent optimization where the organism minimizes a Total Potential Energy cost function ($U_{CC}$):

$$ U_{CC} = U_{gravity} + U_{elastic} - U_{info} $$

-   **The Cost Function ($U_{CC}$):** The organism minimizes Total Potential Energy (Gravity + Elasticity - Information).
-   **The Gradient:** Detected by mechanosensors (PIEZO2) measuring error between current shape and genetic reference.
-   **The Optimizer:** Shape updates via Differential Growth (Slow) and Muscle Tone (Fast).
-   **The Learning Rate Scheduler:** The Circadian Clock (BMAL1) modulates tissue sensitivity ("Spinal Jetlag" hypothesis).
-   **The Failure Mode:** Scoliosis represents a "Local Minimum" or "Exploding Gradient" due to sensory noise or feedback delays.

**Key Objectives:**
1.  **Phase 1: Computational Proof-of-Concept:** Define $U_{CC}$ explicitly and simulate "Optimization Failure" (Scoliosis).
2.  **Phase 2: The "Spinal Jetlag" Simulation:** Integrate time-dependent learning rates (Circadian Clock) and test desynchronization.
3.  **Phase 3: Experimental Validation Design:** Design specific wet-lab experiments to validate computational predictions.

---

## 12-Week Schedule

### Phase 1: Computational Proof-of-Concept (Weeks 1-4)
*Focus: PyElastica simulations, Cost Function definition, and Optimization Failure modes.*

| Week | Focus | Task | Hypothesis / Theoretical Component |
| :--- | :--- | :--- | :--- |
| **1** | **Explicit Cost Function** | **Implement `compute_U_CC`** in `src/spinalmodes/countercurvature/pyelastica_bridge.py`. Quantify the trade-off between Gravitational Energy and Informational "Gain". | **Cost Function:** The organism actively minimizes $U_{CC}$, balancing metabolic cost against geometric error. |
| **2** | **The Bio-Gravitational Number** | **Extend `scripts/verify_bg.py`** to calculate $\mathcal{B}_g$ for diverse species (Whale, Giraffe) and conditions (Hyper-gravity). | **$\mathcal{B}_g$ Scaling:** Stability is predicted by $\mathcal{B}_g > 1$. Large organisms require disproportionately higher $\chi_M$ (squared scaling). |
| **3** | **Optimization Failure** | **Run `scripts/experiment_optimization_failure.py`** (create if needed) to map the "Exploding Gradient" region (High $\chi_{\kappa}$, Low Anisotropy). Inject sensory noise ($\nabla I + \eta$). | **Instability Wedge:** Scoliosis is an emergent instability where the "Learning Rate" ($\chi_{\kappa}$) exceeds the structural damping (Anisotropy). |
| **4** | **Vector-Scalar Mismatch** | **Run `scripts/experiment_vector_scalar_mismatch.py`**. Simulate Microgravity: Scalar pressure ($P_{scalar} > 0$) is high, but Vector load ($g=0$) is zero. | **Mismatch:** In Microgravity, the "Vector" term vanishes, leaving unconstrained "Scalar" growth (bloating/buckling). |

### Phase 2: The "Spinal Jetlag" Simulation (Weeks 5-8)
*Focus: Time-dependent Learning Rates, Circadian Clock integration, and Desynchronization.*

| Week | Focus | Task | Hypothesis / Theoretical Component |
| :--- | :--- | :--- | :--- |
| **5** | **Time-Dependent Learning Rate** | **Create `scripts/experiment_spinal_jetlag.py`**. Implement time-varying sensitivity: $\chi_{\kappa}(t) = \chi_0 (1 + A \cos(\omega t))$. | **Circadian Gating:** The "Learning Rate" is not constant but gated by the clock to coincide with activity phases. |
| **6** | **Entrainment ($\mathcal{E}_{mech}$)** | **Modify `experiment_spinal_jetlag.py`** to couple Gravity to Clock Phase. Gravity acts as the Zeitgeber ($K_{ent} > 0$). | **Phase Coherence:** Constructive interference ($\phi \approx 0$) maximizes adaptation; destructive interference ($\phi \approx \pi$) suppresses it. |
| **7** | **Desynchronization (Jetlag)** | **Simulate "Jetlag" condition**: Scalar pressure is constant, but Vector load is phase-shifted ($\phi \neq 0$). Track curvature drift over multiple cycles. | **Spinal Jetlag:** Desynchronization acts as a "Vector-Scalar Mismatch" in the time domain, leading to geometric drift (kinking). |
| **8** | **The Energy Deficit Window** | **Integrate Metabolic Cost**. Scale $L$ and check if metabolic demand exceeds supply during rapid growth + jetlag. | **Thermodynamic Collapse:** Metabolic limits combined with temporal mismatch trigger the "Energy Deficit Window" ($\mathcal{M}_{prop} < 1$). |

### Phase 3: Experimental Validation Design (Weeks 9-12)
*Focus: Wet-lab experiment design to validate computational predictions.*

| Week | Focus | Task | Hypothesis / Theoretical Component |
| :--- | :--- | :--- | :--- |
| **9** | **Test T_Clock (Circadian Rescue)** | **Design "The Desynchronization Drift"**. Protocol for measuring Bioluminescence (PER2::LUC) in loaded vs. unloaded disc explants. | **Entrainment (Test U/V):** Mechanical load is the primary Zeitgeber for the spinal clock. Loss of load leads to amplitude decay. |
| **10** | **Test V_S (Vector Rescue)** | **Design "The Mismatch Rescue"**. Protocol using Magnetic Tweezers to apply directional force in Microgravity models (e.g., Zebrafish in Clinostat). | **Vector Rescue (Test K/L):** Restoring the "Vector" signal artificially can rescue the phenotype even in the absence of gravity. |
| **11** | **Test B_g (Allometric Scaling)** | **Design "The Scaling Law"**. Protocol for comparative analysis of paraspinal muscle PCSA vs. Spine Length across species. | **Invariant $\mathcal{B}_g$:** The Bio-Gravitational Number is a conserved invariant across vertebrate evolution. |
| **12** | **Synthesis & Review** | **Synthesize "Gravity as Optimization" Manuscript**. Compile results into a unified paper integrating mechanical, circadian, and metabolic findings. | **Unified Theory:** The optimization framework unifies mechanical and metabolic theories of scoliosis. |

---

## Risk Assessment

### Theoretical Bottlenecks
1.  **Parameter Sensitivity:** The model relies on phenomenological coupling constants ($\chi_M, \chi_{\kappa}, \chi_E$).
    *   *Mitigation:* Use `experiment_parameter_map.py` to bound these values with biological data (stiffness measurements).
2.  **Definition of Reference Metric:** The "Reference Metric" is abstract.
    *   *Mitigation:* Ground it in HOX gene expression patterns (AlphaFold analysis).

### Computational Risks
1.  **Long-Term Drift:** Integrating "Spinal Jetlag" over many cycles may accumulate numerical error.
    *   *Mitigation:* Use Symplectic Integrators (Position Verlet) in PyElastica and rigorous energy conservation checks.
2.  **Optimization Landscape:** The $U_{CC}$ landscape may be non-convex, leading to multiple stable states.
    *   *Mitigation:* Perform extensive basin-of-attraction analysis (Monte Carlo sweeps).

### Experimental Feasibility
1.  **Microgravity Simulation:** True microgravity is inaccessible.
    *   *Mitigation:* Use Clinostats (Random Positioning Machines) and "Buoyancy" analogs (Neutral Buoyancy Tanks) as proxies.
2.  **In Vivo Monitoring:** Measuring "Clock Phase" in deep tissues (spine) is difficult.
    *   *Mitigation:* Use `Per2::Luc` reporter mice and ex vivo organotypic culture models.
