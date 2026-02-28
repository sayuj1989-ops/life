# Toy Models & Falsification Plan

**Purpose:** To de-risk complex Cosserat simulations and provide intuitive, falsifiable validation of the core mechanisms.

## Implemented Toy Models (Validation)

### Toy Model A: 1D Thermostatic Column (Metabolic Buckling)
*   **Location:** `scripts/experiments/toy_model_thermostatic.py`
*   **Objective:** Demonstrate the "Energy Deficit Bifurcation" in a minimal system without complex Cosserat geometry.
*   **Method:** Models a 1D column where Active Curvature Cost scales as $L^3$ (Volume) and Metabolic Supply scales as $L^2$ (Surface Area).
*   **Success Metric:** Identifies a critical length $L_{crit} \approx 0.35$m where Deficit $> 0$.
*   **Status:** ✅ **Completed**

### Toy Model B: Anisotropy-Stability Link
*   **Location:** `scripts/toy_model_anisotropy_link.py`
*   **Objective:** Validate that decreasing structural anisotropy lowers the critical threshold for instability.
*   **Method:** Calculates $L_{crit} \propto A^{-0.5}$, showing that isotropic structures fail at shorter lengths under gravity.
*   **Success Metric:** Plotting $A$ vs $L_{crit}$ yields an inverse square-root relationship.
*   **Status:** ✅ **Completed**

## Proposed Falsification Tests & Ablations

### Test 1: Absolute Zero Gravity Ablation
*   **Objective:** Confirm that without gravity ($g=0$), the active counter-curvature drive produces a massive over-correction (resembling the "Stagnant Pool" effect observed in microgravity).
*   **Method:** Run `experiment_minimal_elastica.py` with gravity vector explicitly set to `[0, 0, 0]`.
*   **Success Metric:** The rod should curl into a tight loop or extreme S-shape, maximizing internal strain energy without external restoring force.
*   **Stop Condition:** Simulation crashes due to infinite self-intersection.

### Test 2: Infinite Supply Ablation
*   **Objective:** Prove that the Energy Deficit Window is strictly caused by supply limitations scaling at $L^2$.
*   **Method:** Modify `experiment_energy_deficit_window.py` to set $S_{proprio} = \infty$ for all $L$.
*   **Success Metric:** The deficit $D(L)$ should never cross zero; no instability should occur at any length.
*   **Stop Condition:** The entire biological parameter range is simulated without a single zero crossing.

### Test 3: "Noise-Free" Digital Twin Falsification
*   **Objective:** Validate that sensory noise ($\sigma$) is the driver of the "Exploding Gradient" in genetic optimization failure.
*   **Method:** Run `experiment_optimization_failure.py` mapping genes with noise strictly clamped to 0.
*   **Success Metric:** Even highly mutated matrices (e.g., FBN1 proxy) should maintain stability much longer without sensory noise amplification.
*   **Stop Condition:** Output data confirms stability boundary shifting to $Bg >> 1$.
