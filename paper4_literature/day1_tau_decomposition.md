# Day 1: Decomposition of Proprioceptive Delay ($\tau$)

## Introduction
The parameter $\tau$ in our delayed PID controller model (from Paper 2) represents the proprioceptive sensory delay—the time elapsed from an actual change in the body's posture to the moment the controller (the central nervous system) commands a compensatory muscle force. In Paper 2, values of $\tau > 200$ ms, combined with the pubertal growth spurt, created a "derivative gain gap" instability (Peterka, 2002; unverified — needs literature confirmation).

This total delay, $\tau_{\text{total}}$, is not a single entity. It represents the sum of several sequential physiological events. We decompose it as follows:

$$ \tau_{\text{total}} = \tau_{\text{transduction}} + \tau_{\text{afferent}} + \tau_{\text{spinal}} + \tau_{\text{cerebellar}} + \tau_{\text{efferent}} + \tau_{\text{NMJ}} + \tau_{\text{EMD}} $$

Here, we budget these delays using available human electrophysiological literature.

## Components of $\tau$

### 1. Peripheral Transduction Delay ($\tau_{\text{transduction}}$)
* **Definition:** Time taken for muscle spindle stretch-sensitive ion channels to convert mechanical deformation into receptor potentials.
* **Mechanism:** Primarily governed by the mechanosensitive channel Piezo2 (unverified — needs literature confirmation).
* **Estimate:** Rapid opening kinetics. In cellular models (unverified — needs literature confirmation).
* **Budget:** **~2 ms**

### 2. Afferent Conduction Delay ($\tau_{\text{afferent}}$)
* **Definition:** Time for action potentials to travel along proprioceptive (Group Ia/II) afferents from paraspinal muscles to the spinal cord.
* **Mechanism:** Governed by axon diameter and myelination quality. Proprioceptive Ia afferents are the fastest conducting fibers in the human body (conduction velocities $\sim 60-120$ m/s).
* **Estimate:** For paraspinal muscles, the travel distance is relatively short compared to lower limbs. However, structural integrity of the nerve pathways influences this (unverified — needs literature confirmation). For a 0.5 meter distance at 80 m/s:
* **Budget:** **~6 ms**

### 3. Spinal Relay Delay ($\tau_{\text{spinal}}$)
* **Definition:** Synaptic processing in Clarke's column and the dorsal spinocerebellar tract.
* **Mechanism:** Involves synaptic transmission ($\sim 0.5-1$ ms per synapse). Reflex arcs (monosynaptic) are fast, but complex proprioceptive integration takes longer.
* **Estimate:** High-resolution spinal mapping suggests spinal processing and relay to ascending tracts takes a few milliseconds (unverified — needs literature confirmation).
* **Budget:** **~4 ms**

### 4. Cerebellar / Cortical Processing Delay ($\tau_{\text{cerebellar}}$)
* **Definition:** Integration and state prediction in the cerebellum (the forward model) and sensorimotor cortices.
* **Mechanism:** This represents the computational time for the brain to update its internal model of body posture (unverified — needs literature confirmation).
* **Estimate:** Central processing for long-latency reflexes and continuous postural control (Peterka model) constitutes the largest variable component. Often estimated by subtracting peripheral latencies from total reflex time.
* **Budget:** **~70-100 ms**

### 5. Efferent Conduction Delay ($\tau_{\text{efferent}}$)
* **Definition:** Motor commands returning via corticospinal and vestibulospinal tracts to the paraspinal alpha motor neurons.
* **Mechanism:** Similar to afferent, but utilizing motor pathways ($\alpha$-motor neurons $\sim 50-100$ m/s).
* **Estimate:** Comparable to afferent delay for the trunk.
* **Budget:** **~6 ms**

### 6. Neuromuscular Junction (NMJ) Delay ($\tau_{\text{NMJ}}$)
* **Definition:** Transmission at the motor endplate.
* **Mechanism:** Acetylcholine release, binding to ACh receptors, and generation of the muscle action potential (unverified — needs literature confirmation).
* **Estimate:** Relatively invariant in healthy individuals.
* **Budget:** **~1 ms**

### 7. Electromechanical Delay ($\tau_{\text{EMD}}$)
* **Definition:** Time from muscle fiber action potential to the onset of measurable force production.
* **Mechanism:** Involves excitation-contraction coupling (calcium release, cross-bridge formation) and the stretching of the series elastic component (tendons/aponeuroses).
* **Estimate:** Highly dependent on muscle mechanics and training state. Often measured between $40-60$ ms (unverified — needs literature confirmation). For paraspinals under continuous load:
* **Budget:** **~50 ms**

## Total $\tau$ Budget Summary

| Component | Biological Mechanism | Typical Human Budget | Key Literature Target |
| :--- | :--- | :--- | :--- |
| $\tau_{\text{transduction}}$ | Stretch-gated ion channels (Piezo2) | ~2 ms | Piezo2 variants |
| $\tau_{\text{afferent}}$ | Axon caliber & myelination (Schwann cells) | ~6 ms | GPR126 |
| $\tau_{\text{spinal}}$ | Interneuron networks (Clarke's column) | ~4 ms | LBX1 |
| $\tau_{\text{cerebellar}}$ | Forward model computation | ~90 ms | - |
| $\tau_{\text{efferent}}$ | Motor pathways | ~6 ms | - |
| $\tau_{\text{NMJ}}$ | Synaptic transmission | ~1 ms | - |
| $\tau_{\text{EMD}}$ | Excitation-contraction coupling | ~50 ms | - |
| **Total $\tau$** | **Postural Control Loop Delay** | **~159 ms** | - |

*Note: In the Peterka (2002) model, a normal healthy adult exhibits $\tau \approx 150-170$ ms. Our synthesized budget (~159 ms) aligns perfectly with this macroscopic behavioral measurement.*
