# Weekly Synthesis: Proprioceptive Collapse & The Spindle Switch

**Date:** 2026-08-05 (Week 27)
**Author:** Microgravity Synthesizer

## 1. Key Findings

### Observed: The "Silent" Spindle
Transcriptomic analysis of paraspinal muscles in microgravity reveals a specific downregulation of **RUNX3** and **EGR3**, the master regulators of muscle spindle development and maintenance. This leads to the atrophy of intrafusal fibers (the sensors) even before extrafusal fibers (the actuators), resulting in a state of "sensory de-afferentation."
* **Source:** Gerwin et al. (2026), *Journal of Physiology*. (See `notes/evidence/2026-08-05__proprioceptive_collapse.md`)

### Observed: Elastic Sheath Failure
The sensitivity of the muscle spindle depends on the compliance of its ECM sheath. We observe significant downregulation of **FBN2** (Fibrillin-2) and **SERPINH1** (Hsp47) in unloaded tissues. FBN2 defects are known to cause Congenital Contractural Arachnodactyly (Beals Syndrome), which shares scoliosis phenotypes, suggesting that "loose" spindles cannot detect weak gravitational cues.
* **Source:** Buchan et al. (2014) / Microgravity Transcriptomics.

### Hypothesized: The Gamma-Loop "Drift"
In 1G, gravity provides a constant "error signal" that the gamma-motor system fights against to maintain posture. In microgravity, this error signal vanishes. The control loop opens, and the "integral term" (accumulated error) drifts, leading to asymmetric muscle tone and curvature.

## 2. Mechanistic Bridge: Tension Tunes The Sensor

The bridge between reduced gravity and spinal curvature is the **Muscle Spindle**:
1.  **The Input:** Gravitational load stretches paraspinal muscles.
2.  **The Sensor:** Intrafusal fibers (tuned by FBN2/Collagen) detect this stretch.
3.  **The Output:** Ia afferents fire, driving Alpha-motor neurons to contract (Tone).
4.  **The Failure:** In microgravity, the stretch is lost -> Spindles go silent -> Tone drops -> Spine buckles.

## 3. Predicted Directionality (Unloading vs. Loading)

| Feature | Unloading (Microgravity) | Loading (1G/Exercise) |
| :--- | :--- | :--- |
| **Spindle State** | **Silent/Atrophic** (Low Ia Firing) | **Active/Tuned** (High Ia Firing) |
| **Regulators** | **RUNX3/EGR3 Low** | **RUNX3/EGR3 High** |
| **ECM Sheath** | **FBN2 Low** (Slack) | **FBN2 High** (Taut) |
| **Control Mode** | **Open Loop** (Drift) | **Closed Loop** (Correction) |

## 4. Testable Predictions

*   **H_2026_08_05_Spindle_Silence**: Loss of gravitational load silences muscle spindles (decreased Ia afferent firing), which removes the tonic "stretch reflex" that maintains spinal straightness.
*   **H_2026_08_05_FBN2_Fail**: Fibrillin-2 (FBN2) mutation/deficiency exacerbates microgravity-induced scoliosis because FBN2 is required to tune the sensitivity of the muscle spindle to weak gravitational loads.
