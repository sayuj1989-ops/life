# Toy Models & Experiments Plan

## Toy Models (Mechanism Validation)

1.  **Toy Model A: 1D Thermostatic Column (Metabolic Buckling)**
    *   **Objective:** Validate the core scaling mismatch ($L^5$ mass vs $L^2$ surface area) leading to "Metabolic Buckling".
    *   **Method:** Simple 1D thermostatic control model balancing heat generation and loss without rod mechanics.
    *   **Success Metric:** Demonstration of sudden divergence/instability at a critical length $L_{crit}$.
    *   **Expected Outcome:** Validated ($L_{crit} \approx 0.35$m aligns with human growth).

2.  **Toy Model B: Anisotropy-Stability Link**
    *   **Objective:** Connect protein-level aspect ratio (Anisotropy $A$) to macro-level spinal stability.
    *   **Method:** 2D mapping relating critical length to inverse square root of anisotropy ($L_{crit} \propto A^{-0.5}$).
    *   **Success Metric:** Clear mathematical and visual relationship showing highly anisotropic structures tolerate greater lengths.
    *   **Expected Outcome:** Validated (supports FBN1/Marfan mapping).

3.  **Toy Model D: Lenke Classifications (Spatial Deficits)**
    *   **Objective:** Predict scoliotic curve shape (Lenke classes 1-6) based on spatial distribution of sensory/energy deficits.
    *   **Method:** 1D column model with variable "deficit zones" mapping to predicted curvature maxima.
    *   **Success Metric:** Coherent mapping of distinct deficit patterns to recognized clinical Lenke shapes.
    *   **Expected Outcome:** In progress (Script `toy_model_lenke_classes.py` actively developed).

4.  **Toy Model E: Torsional Buckling Model**
    *   **Objective:** Demonstrate active torque resistance and its failure modes.
    *   **Method:** Simple rotational spring-mass system subject to increasing longitudinal growth drive.
    *   **Success Metric:** Emergence of coupled lateral-torsional instability upon exceeding torque threshold.
    *   **Expected Outcome:** Validated.

## "Real" Experiments (Validation, Ablation, Falsification)

1.  **Clinical PHV Overlay (CLIN_01)**
    *   **Objective:** Map model Instability Window against Peak Height Velocity clinical growth charts.
    *   **Method:** Overlay simulated instability probability distributions (from `experiment_energy_deficit_window.py`) onto real clinical age-of-onset histograms.
    *   **Success Metric:** High correlation ($R^2 > 0.7$) between predicted peak instability (e.g., $L_{crit}$ converted to age via growth curve) and actual adolescent onset.
    *   **Expected Outcome:** Pending literature search and data alignment.
    *   **Stop Condition:** If $L_{crit}$ consistently maps to pre-pubertal or post-pubertal ages in $>80\%$ of test cases.

2.  **Sexual Dimorphism Parameter Sweep (CLIN_04)**
    *   **Objective:** Test if the 7:1 female-to-male clinical prevalence ratio emerges naturally from growth velocity/stiffness differences.
    *   **Method:** Run large ensemble parameter sweeps varying growth rate ($v_g$) and tissue stiffness ($E$) within known empirical ranges for male vs female adolescents.
    *   **Success Metric:** Emergence of a significantly higher failure rate (instability) in the "female" parameter cluster (e.g., faster early growth spurt, lower relative stiffness).
    *   **Expected Outcome:** Planned.
    *   **Stop Condition:** If failure rates remain roughly equal (e.g., 1:1 to 2:1) across all realistic parameter combinations.

3.  **Cross-Species Geodesic Scaling (EXP_06)**
    *   **Objective:** Validate that the required "counter-curvature" scaling holds across different biological species of varying size.
    *   **Method:** Plot model predictions against mass/length data for 9 distinct species.
    *   **Success Metric:** Empirical data points falling along the predicted scaling curve.
    *   **Expected Outcome:** Validated (Script `experiment_cross_species_scaling.py` completed).

4.  **Random Anisotropy Falsification (Negative Control)**
    *   **Objective:** Prove that *structured* information (anisotropy directionality) is required for counter-curvature, not just stiffening.
    *   **Method:** Run the core Cosserat model (`experiment_minimal_elastica.py`) but with a randomized, non-directional anisotropy tensor field.
    *   **Success Metric:** The rod should buckle randomly or collapse under gravity, failing to maintain an S-shape or upright posture.
    *   **Expected Outcome:** Not yet explicitly scripted as a standalone test, but theoretically expected based on model formulation.
    *   **Stop Condition:** If the rod successfully forms a stable S-shape despite completely random internal anisotropy.
