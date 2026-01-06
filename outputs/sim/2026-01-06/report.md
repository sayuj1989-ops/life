# Parameter Sweep Report: Countercurvature Gain vs Gravity

**Date:** 2026-01-06
**Sweep Parameter:** `chi_kappa` (Countercurvature Gain)
**Range:** 0.0 to 20.0

## Goal
To investigate whether an S-shaped spinal profile emerges under gravity-like loading when the intrinsic "countercurvature" response to an information gradient is increased.

## Setup
- **Model:** Cosserat Rod (PyElastica) with 50 elements.
- **Loading:** Gravity in -Z direction.
- **Initial State:** Horizontal rod along +X axis (cantilevered at X=0).
- **Information Field:** Sinusoidal $I(s) = \sin^2(2\pi s/L)$, creating a periodic gradient.
- **Coupling:** `chi_kappa` modulates the rest curvature $\kappa_{rest} \propto \chi_\kappa \nabla I$.

## Findings

### 1. Shape Emergence
- **Low Gain ($\chi_\kappa \approx 0$):** The rod exhibits a classic cantilever "sag" under gravity, curving downward (negative Z). The shape is essentially a C-curve.
- **Medium Gain ($\chi_\kappa \approx 4-10$):** The rest curvature begins to fight gravity. Since the information field is periodic, the rest curvature induces a wave-like intrinsic shape. This interacts with the gravity sag.
- **High Gain ($\chi_\kappa > 15$):** The intrinsic curvature dominates gravity. The rod adopts a complex shape with significant positive and negative vertical deflections, resembling a standing wave or S-shape.

### 2. Metrics
- **Sagittal S-Index ($S_{lat}$):** Increases with $\chi_\kappa$, indicating the emergence of inflection points and deviation from a monotonic sag.
- **Vertical Deflection:** Generally decreases or becomes oscillatory as the countercurvature "lifts" the rod against gravity.

## Conclusion
The parameter sweep confirms that increasing the biological countercurvature gain ($\chi_\kappa$) transitions the system from a gravity-dominated C-shape to a structure-dominated S-shape (or multi-wave shape). This supports the hypothesis that scoliosis-like or physiological S-curves can emerge from the competition between morphomechanical programming and environmental loads.

## Next Steps
- Sweep `chi_E` (stiffness modulation) to see if stiffening high-information regions stabilizes the shape.
- Investigate `base_direction` tilt to simulate posture changes.
