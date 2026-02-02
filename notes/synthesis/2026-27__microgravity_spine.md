# Weekly Synthesis: The Proprioceptive Void

**Date:** 2026-08-05 (Week 27)
**Author:** Microgravity Synthesizer

## 1. Key Findings

### Observed: The Silent Spindle
Muscle spindles are mechanoreceptors that encode muscle length and velocity. Their sensitivity is tunable via Gamma Motor Neurons. In microgravity, the passive stretch on anti-gravity muscles (Soleus, Paraspinal) is removed. This leads to **"Spindle Silencing"**, where the afferent firing rate drops below the threshold required to maintain tonic contraction.
* **Source:** Proske & Gandevia (2012), *Physiological Reviews*. (See `notes/evidence/2026-02-20__active_inference_spine.md`)

### Hypothesized: The Bayesian Prior of Gravity
According to the **Active Inference** framework, motor control is a process of minimizing prediction error (Free Energy). The CNS predicts a constant gravitational force (the "Prior"). When this force is absent, the discrepancy between prediction (Gravity) and sensation (Floating) creates a massive error. The brain resolves this by lowering the "Precision" (confidence) of proprioceptive inputs, effectively "ignoring" the spine's geometry.
* **Source:** Adams et al. (2013), *Brain Structure and Function*.

### Observed: NMJ Retreat
Transcriptomic analysis of spaceflight muscle reveals a rapid downregulation of Neuromuscular Junction (NMJ) components (Agrin, MuSK, LRP4) preceding gross atrophy. This suggests that the "disconnection" of the motor command occurs at the synaptic level before the contractile apparatus degrades.
* **Source:** Pandit et al. (2025), *bioRxiv*. (See `notes/evidence/2026-08-05__nmj_instability.md`)

## 2. Mechanistic Bridge: Gain Collapse

The spine is an inverted pendulum stabilized by feedback control.
1.  **The Sensor:** Muscle Spindles detect deviation ($\theta$).
2.  **The Gain:** The strength of the correction ($\tau = -G \cdot \theta$).
3.  **The Collapse:** In 1G, $G$ is high to fight gravity. In uG, the "silent spindle" interprets the lack of tension as "no deviation needed," causing $G$ to drop.
4.  **The Result:** A system with low gain ($G < G_{crit}$) becomes susceptible to thermal/growth noise, leading to "Entropic Curvature" (Drift).

**Conclusion:** Scoliosis in microgravity is a "Control Theory Failure" where the gain parameter $G$ drifts below the stability threshold due to sensory deprivation.

## 3. Predicted Directionality (Unloading vs. Loading)

| Feature | Unloading (Microgravity) | Loading (1G/Vibration) |
| :--- | :--- | :--- |
| **Spindle Output** | **Silent** (Rate Code $\to$ 0) | **Active** (Rate Code $\propto$ Stretch) |
| **Control Gain** | **Low/Damped** (Floppy) | **High/Stiff** (Stable) |
| **Bayesian Precision** | **Low** (Ignore Proprioception) | **High** (Trust Proprioception) |
| **NMJ State** | **Fragmented** (Denervation) | **Stable** (Innervation) |

## 4. Testable Predictions

*   **H_2026_08_01_Stochastic_Gain**: Application of stochastic noise (e.g., broad-spectrum vibration) to paraspinal muscles will lower the detection threshold of spindles via Stochastic Resonance, maintaining high proprioceptive gain even in the absence of gravity.
*   **H_2026_08_01_NMJ_Anchor**: Pharmacological stabilization of the NMJ (e.g., via Agrin-mimetics or MuSK agonists) will prevent the "sensory disconnection" and maintain spinal alignment, even if muscle mass itself decreases.
