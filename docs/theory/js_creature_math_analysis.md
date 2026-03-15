# JS Creature Mathematical Analysis: Mapping to Biological Countercurvature

The provided p5.js "Creature" algorithm demonstrates emergent geometry from the interaction of spatial gradients, oscillations, and scalar constraints. This provides a minimal 2D analog for the Biological Countercurvature (IEC) framework.

## Variable Mapping to IEC Theory

| JS Variable | Mathematical Form | Biological Countercurvature Analog |
| :--- | :--- | :--- |
| `k` | $5 \cos(\frac{x}{14}) \cos(\frac{y}{30})$ | **Spatial Interference Pattern**: A spatial standing wave or interference pattern. |
| `e` | $\frac{y}{8} - 13$ | **Linear Gradient**: A linear gradient in y, shifted. |
| `d` | $\frac{k^2 + e^2}{59} + 4$ | **Inverse Distance / Potential Well**: A distance metric in $(k,e)$ space. |

This model is already incorporated into the project as **Toy Model C** (`scripts/experiments/toy_model_js_creature.py`) to provide a visual, 2D validation of "Metabolic Buckling" for biomechanics reviewers.