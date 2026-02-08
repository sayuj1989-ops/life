# Weekly Synthesis: The Sensory Mismatch (Gain Control)

**Date:** 2026-08-12 (Week 28)
**Author:** Microgravity Synthesizer

## 1. Key Findings

### Observed: Vestibular Down-Weighting
Evidence indicates that in the absence of reliable gravitational cues (or in AIS), the central nervous system down-weights vestibular inputs ($\gamma_V \to 0$) to reduce sensory conflict. Pialasse et al. (2015) demonstrated that AIS patients exhibit reduced vestibular gain during Galvanic Vestibular Stimulation (GVS), relying instead on potentially erroneous proprioceptive signals.
*   **Source:** Pialasse et al. (2015), *Journal of Vestibular Research*. (See `notes/evidence/2025-02-21__vestibular_mismatch_pialasse.md`)

### Observed: Sensory Re-weighting Failure
Peterka (2002) established the "Sensory Re-weighting" model, where the brain dynamically adjusts the gain on Visual, Vestibular, and Proprioceptive inputs based on their signal-to-noise ratio. In microgravity, the Vestibular signal is "silent" (SNR $\to$ 0), forcing an over-reliance on Proprioception ($\gamma_P$). If proprioception is also compromised (muscle atrophy), the system enters a state of "Sensory Indeterminacy."
*   **Source:** Peterka (2002), *Journal of Neurophysiology*.

### Modeled: Instability via Gain Loss
Bastien et al. (2013) showed that postural stability is governed by a critical "Graviceptive Gain" ($\mathcal{B}$). When this gain drops below a threshold (due to unloading or genetic defects like *Egr3* loss), the system undergoes a Hopf bifurcation, transitioning from a stable straight line to an oscillatory (S-shaped) buckling mode.
*   **Source:** Bastien et al. (2013), *Frontiers in Plant Science* (adapted to spine).

## 2. Mechanistic Bridge: The Gain Control Loop

The spine is a **Servo-Controlled Tensegrity Structure**.
1.  **Reference Signal (Gravity):** Detected by Otoliths (Utricle/Saccule).
2.  **Controller (Vestibulospinal Tract):** Sets the "Tone" ($\gamma$-bias) on muscle spindles.
3.  **Error Feedback (Proprioception):** Muscle spindles detect deviation from the reference.
4.  **Failure Mode:** In microgravity, the Reference is lost. The Controller turns down the Gain ($\gamma_V \to 0$). The Spindles become slack (Loss of Pre-stress). The system drifts, chasing "Phantom Errors" (Geometric Hallucinations).

## 3. Predicted Directionality (Unloading vs. Loading)

| Feature | Unloading (Microgravity) | Loading (1G/Exercise) |
| :--- | :--- | :--- |
| **Vestibular Gain ($\gamma_V$)** | **Suppressed** (Noise Reduction) | **High** (Active Reference) |
| **Proprioceptive Gain ($\gamma_P$)** | **Dominant but Noisy** (Drift) | **Balanced** (Correction) |
| **Muscle Spindle Tone** | **Slack** (Reduced Sensitivity) | **Taut** (High Sensitivity) |
| **Curvature Outcome** | **Oscillatory Buckling** (S-Shape) | **Stable Verticality** (I-Shape) |

## 4. Testable Predictions

*   **H_2026_08_12_Gain_Clamping**: If spinal curvature in microgravity is driven by "hunting" for a missing reference signal, then clamping proprioceptive feedback (e.g., via 80Hz tendon vibration to saturate Ia afferents) will paradoxically *reduce* curvature drift by blinding the system to false errors.
*   **H_2026_08_12_Otolith_Rescue**: Artificial stimulation of the otoliths (e.g., via sub-threshold Noisy Galvanic Vestibular Stimulation, nGVS) during unloading will maintain Vestibulospinal Tract activity, preserving paraspinal muscle tone and preventing atrophy.
