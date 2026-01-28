# Evidence Note: The Voltage-Gated Proprioceptive Gain

**Date:** 2024-10-03
**Author:** Curvature Librarian
**Topic:** Piezo2 Voltage-Block as a Gain Control Mechanism for Spinal Alignment

## Core Insight
Sánchez-Carranza et al. (2024) demonstrate that **Piezo2** mechanosensitivity is strongly regulated by membrane voltage. At resting potential, the channel is subject to a "Voltage-Block" that dampens its response to mechanical stimuli. Relieving this block (via depolarization) significantly increases sensitivity, essentially amplifying the mechanotransductive signal.

## Mechanism
*   **Voltage-Block:** At hyperpolarized resting potentials, Piezo2 channels exhibit reduced open probability or conductance in response to force.
*   **Gain Modulation:** Depolarization acts as a "Gain Control" knob. A depolarized cell is "listening harder" to mechanical cues than a hyperpolarized one.
*   **Gene/Protein:** *Piezo2* (Vector Sensor).

## Implications for Counter-Curvature
In our **Bastien-Countercurvature Framework**, the stability of the spine depends on the ratio of the **Proprioceptive Gain ($\gamma$)** to the Gravitational Load ($E$).
$$ \frac{d\kappa}{dt} = -\beta \sin\theta - \gamma \kappa $$
If $\gamma$ falls below a critical threshold relative to $E$, the system succumbs to gravitational instability (scoliosis/buckling).

This finding implies that $\gamma$ is not a static constant but a dynamic variable regulated by the **Resting Membrane Potential ($V_{mem}$)** of proprioceptive neurons (e.g., in the Dorsal Root Ganglia or paraspinal muscle spindles).
*   **Risk Factor:** Factors that hyperpolarize proprioceptors (e.g., K+ channel openers, metabolic shifts) effectively reduce $\gamma$, potentially driving the spine into the unstable regime even under normal gravity.
*   **Therapeutic Avenue:** Pharmacological agents that relieve the voltage block (or slightly depolarize proprioceptors) could boost $\gamma$ to compensate for structural weakness or microgravity unloading.

## Open Question
Does the "spinal jetlag" or circadian desynchronization observed in scoliosis involve a rhythmic oscillation of this voltage block? If the "gain" fluctuates with the circadian clock (via ion channel expression), then the spine may be vulnerable at specific times of day.

## Proposed Test
**The "Voltage-Gain" Assay:**
*   **Hypothesis:** Pharmacological hyperpolarization of paraspinal proprioceptors will induce scoliotic curvature by reducing $\gamma$.
*   **Experiment:** Treat wild-type mice with a specific KCNQ channel activator (hyperpolarizing agent) restricted to the paraspinal region. Monitor spinal curvature via micro-CT over 4 weeks.
*   **Prediction:** Treated mice will develop progressive curvature indistinguishable from proprioceptive-null mutants.
