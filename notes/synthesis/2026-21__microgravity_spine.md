# Weekly Synthesis: Microgravity × Spine (2026-21)

## Key Findings

1.  **LINC Complex Degradation as "Vector Sensor" Failure**
    Simulated microgravity (clinostat) leads to the specific degradation of **Lamin A/C** and **Sun-2** (LINC complex elements) in mesenchymal stem cells. This disconnects the nucleus from the cytoskeleton, preventing the sensing of gravitational vectors. Crucially, Low Intensity Vibration (LIV) (0.7g, 90Hz) rescues this degradation, restoring the mechanical coupling.
    *Citation:* Touchstone et al. (2019) - *"Recovery of Stem Cell Proliferation in Simulated Microgravity via Low Intensity Vibration"*

2.  **Reactive Astrogliosis as Sensory Mismatch**
    In the context of the "Urotensin Relay", scoliosis is linked to **reactive astrogliosis** (GFAP upregulation) in ependymal cells. This state is triggered when ciliary sensory input fails (e.g., cilia paralysis). Microgravity likely mimics this "sensory silence," acting as a mismatch signal that triggers the same inflammatory/gliotic pathway, disrupting the Reissner fiber.
    *Citation:* Djebar et al. (2024) - *"Reissner fiber-induced urotensin signaling from cerebrospinal fluid-contacting neurons prevents scoliosis"*

3.  **Growth Gain without Vector Direction**
    Simulations of the "Counter-Curvature" rod system show that a high growth gain ($\chi_\kappa = 12.0$) is required to maintain spinal flatness against gravity. However, in the absence of a gravity vector ($g=0$), this high gain system becomes unstable or "noisy," leading to emergent S-shapes or spirals driven purely by initial noise rather than adaptive feedback.
    *Citation:* Internal Simulation - *`scripts/run_growth_shape_sweep.py` Results*

## Mechanistic Bridge

**The "Vector-Scalar Mismatch" Theory:**

1.  **Vector Sensors (High Anisotropy):** Structures like the **LINC Complex** (Lamin A/C) and **Primary Cilia** (IFT88/POC5) are highly anisotropic and rely on a directional force vector (gravity/shear) to maintain their alignment and signaling competence. In microgravity, these sensors degrade or "disengage."
2.  **Scalar Sensors (Low Anisotropy):** Diffusible factors and metabolic sensors (e.g., **MMP1/3**, **YAP** cytosolic fraction) respond to scalar stress (hydrostatic pressure, swelling). These remain active or become hyperactive due to fluid shifts.
3.  **The Mismatch:** The spine retains its **Growth Potential** (Scalar) but loses its **Directional Guide** (Vector). The system continues to "push" (growth) but has no "rudder" (gravity vector), leading to geometric disorganization (scoliosis/flattening) rather than adaptive straightening.

## Predicted Directionality

| Feature | Microgravity (Unloading) | 1g (Loading) |
| :--- | :--- | :--- |
| **Lamin A/C (LINC)** | **Decreased** (Degraded) | High (Stiff Nucleus) |
| **Reissner Fiber Tone** | **Lost** (Buckling) | High (Taut) |
| **Ependymal GFAP** | **Increased** (Astrogliosis) | Low (Quiescent) |
| **Urp1/2 Expression** | **Decreased** | High |
| **Spinal Shape** | **Unstable / Flattened** | S-Shape / Straight |

## Testable Predictions

| ID | Statement | Rationale |
| :--- | :--- | :--- |
| **H_2026_05_25_Reissner_Buckling** | In microgravity, the Reissner Fiber will lose tension and exhibit "buckling" or coiling phenotypes due to altered CSF flow gradients. | The RF is a tension-dependent structure; flow reduction/alteration removes the tensioning force. |
| **H_2026_05_25_Growth_Asymmetry** | If the "Growth Gain" ($\chi_\kappa$) remains high during unloading, the spine will develop random, non-planar curvatures (spirals) rather than maintaining a 2D profile. | Without the gravity vector to penalize lateral deviation, the active moment works against noise, amplifying it. |
