# Toy Models Plan

**Purpose:** To de-risk the complex Cosserat simulation and provide intuitive validation for "Metabolic Buckling" and "Active Countercurvature". By providing analytically tractable toy models, we build reviewer confidence in the core mechanisms before introducing the computationally heavy Cosserat elastica models.

**Status:** Ongoing Integration

## Phase 1: Minimal Sanity Checks (Completed)

### Toy Model A: 1D Thermostatic Column (Thermodynamic)
- **Objective:** Demonstrate "Energy Deficit Bifurcation" in a minimal system without complex geometry.
- **Method:** 1D column of height $L$. Active Curvature Cost: $C(L) \propto \chi_\kappa^2 L^3$. Metabolic Supply: $S(L) \propto L^2$.
- **Success Metric:** Clear identification of critical length $L_{crit}$ where Deficit $D(L) > 0$.
- **Status:** ✅ **Validated** (`scripts/experiments/toy_model_thermostatic.py`)

### Toy Model B: Anisotropy-Stability Link
- **Objective:** Explicitly link molecular anisotropy to macro-scale buckling resilience.
- **Method:** Model $L_{crit}$ as a function of protein anisotropy $A$.
- **Success Metric:** Demonstrate $L_{crit} \propto A^{-0.5}$, proving that high-anisotropy sensors (like PIEZO2) delay metabolic buckling.
- **Status:** ✅ **Validated** (`scripts/toy_model_anisotropy_link.py`)

## Phase 2: Proposed Additional Toy Models & Real Experiments (Pending)

### Toy Model C: Sensory Noise Ablation
- **Objective:** Isolate the impact of the sensory noise parameter ($\sigma$) on optimal curvature.
- **Method:** Run identical Cosserat simulations with $\sigma = 0$ (perfect gradient information) vs $\sigma > 0$ (noisy gradient).
- **Success Metric:** Show that perfect information always finds the S-curve global minimum, while noise induces "Exploding Gradients" (scoliosis) above a critical threshold.
- **Stop Condition:** Generation of a clear phase boundary plot mapping $\sigma$ to Cobb angle.

### Toy Model D: Delay Equation Model (Neural Latency)
- **Objective:** Validate the $\mathcal{P}_{latent}$ hypothesis regarding neural delay.
- **Method:** Formulate the active control loop as a Delayed Differential Equation (DDE).
- **Success Metric:** Prove analytically that as physical growth ($L$) accelerates, fixed neural delay ($\tau$) causes the system to undergo a Hopf bifurcation (oscillatory structural failure).

### Toy Model E: Gravity Inversion (Negative Control)
- **Objective:** Test the "Stagnant Pool" hypothesis (microgravity persistence).
- **Method:** Simulate the system with $g \to -g$.
- **Success Metric:** The biological countercurvature mechanism should attempt to invert the S-curve to maintain the same energetic optimization against the inverted vector, validating the active nature of the shape.

## Real Experiments for Falsification

### Real Exp 1: Simulated HOX Boundary Shift
- **Objective:** Falsify the dependency of inflection points on HOX gradients.
- **Method:** Synthetically shift the vector information gradient $\mathbf{V}(s)$ peak 10% cranially.
- **Success Metric:** The resulting emergent structural S-curve inflection point must shift exactly in phase with the $\mathbf{V}(s)$ perturbation. If it does not, the model fails to link genetics to geometry.

### Real Exp 2: Cross-Species Circadian Mismatch
- **Objective:** Validate Spinal Jetlag outside humans.
- **Method:** Map $B_g$ scaling against circadian amplitude (BMAL1 expression) for a quadruped (e.g., mouse).
- **Success Metric:** Model predicts that because mouse $B_g \gg 1$ (passively stable), circadian desynchrony should *not* produce geometric drift, unlike humans ($B_g < 1$).
