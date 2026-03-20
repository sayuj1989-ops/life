# Phase 1, Day 1: Decomposition of Proprioceptive Delay ($\tau$)

## Introduction
The derivative gain gap model (Paper 2) demonstrates that the proprioceptive delay parameter, $\tau$, is the critical factor determining adolescent idiopathic scoliosis (AIS) risk when interacting with rapid somatic growth. However, $\tau$ is not a monolithic biological quantity. Instead, it is the sum of sequential delays through the sensorimotor loop. This document constructs a "$\tau$ budget," decomposing the total delay into its constituent physiological components based on human neurophysiological data.

## The $\tau$ Budget: Component Breakdown

The total proprioceptive delay ($\tau_{total}$) represents the time elapsed from a mechanical perturbation of the trunk (e.g., postural sway) to the onset of corrective muscle force. It can be modeled as:

$$ \tau_{total} = \tau_{transduction} + \tau_{afferent} + \tau_{spinal} + \tau_{cerebellar} + \tau_{efferent} + \tau_{NMJ} + \tau_{EM} $$

Typical values for long-loop postural responses in the human trunk (e.g., paraspinal muscles responding to sway) range from 100 to 150 ms, while values exceeding ~180-200 ms can lead to instability (the derivative gain gap).

### 1. Peripheral Transduction Delay ($\tau_{transduction}$)
- **Definition:** The time taken for mechanical deformation of the muscle spindle or Golgi tendon organ to be converted into a receptor potential and generate the first action potential.
- **Mechanism:** Stretching of intrafusal fibers opens mechanosensitive ion channels (primarily Piezo2).
- **Estimated Delay:** 1–3 ms [unverified — needs literature confirmation].
- **Notes:** While very short, variations in Piezo2 channel kinetics (activation/inactivation time constants) could introduce subtle temporal smearing.

### 2. Afferent Conduction Delay ($\tau_{afferent}$)
- **Definition:** Time for action potentials to travel from the proprioceptor to the dorsal root ganglion and into the spinal cord.
- **Mechanism:** Conduction velocity (CV) along Group Ia and II sensory axons.
- **Estimated Delay:** 10–20 ms (depends heavily on nerve length and myelination) [unverified — needs literature confirmation].
- **Notes:** In the spine, distances are relatively short, but myelination efficiency (governed by Schwann cell proteins like GPR126, MPZ, PMP22) directly dictates CV. For a 0.5m nerve path at 50 m/s, $\tau_{afferent} = 10$ ms.

### 3. Spinal Relay Delay ($\tau_{spinal}$)
- **Definition:** Synaptic delay in the spinal cord, primarily at Clarke's column and other dorsal horn relays (for ascending pathways) and segmental reflex connections.
- **Mechanism:** Synaptic transmission and local interneuron processing.
- **Estimated Delay:** 2–5 ms per synapse [unverified — needs literature confirmation].
- **Notes:** Development and specification of these interneurons is governed by transcription factors like LBX1. Altered circuitry could add additional synaptic hops, increasing delay.

### 4. Cerebellar / Central Processing Delay ($\tau_{cerebellar}$)
- **Definition:** Time required for integration of the proprioceptive signal within the cerebellum and brainstem, forward model updating, and generation of a descending corrective motor command.
- **Mechanism:** Long-loop (transcortical and transcerebellar) processing.
- **Estimated Delay:** 40–80 ms [unverified — needs literature confirmation].
- **Notes:** This is typically the largest component of postural delay, reflecting the transition from short-latency (monosynaptic) reflexes to complex, goal-directed long-latency stretch reflexes (LLRs) [1].

### 5. Efferent Conduction Delay ($\tau_{efferent}$)
- **Definition:** Conduction time of the descending motor action potential from the spinal cord to the paraspinal muscle via alpha motoneurons.
- **Mechanism:** Conduction along myelinated motor axons.
- **Estimated Delay:** 10–20 ms [unverified — needs literature confirmation].
- **Notes:** Similar to afferent delay, scaling with axonal length and myelination status.

### 6. Neuromuscular Junction (NMJ) Delay ($\tau_{NMJ}$)
- **Definition:** Time for synaptic transmission at the motor endplate.
- **Mechanism:** Acetylcholine release, diffusion, binding to nicotinic receptors, and generation of the muscle action potential.
- **Estimated Delay:** 0.5–1 ms [unverified — needs literature confirmation].

### 7. Electromechanical Delay ($\tau_{EM}$)
- **Definition:** Time between the onset of muscle electrical activity (EMG) and the onset of measurable force production.
- **Mechanism:** Excitation-contraction coupling (calcium release, cross-bridge formation) and stretching of the series elastic component (tendon and aponeurosis).
- **Estimated Delay:** 30–60 ms [unverified — needs literature confirmation].
- **Notes:** Often altered by muscle stiffness, tendon compliance, and aging [2].

## Summary Budget for Long-Loop Postural Response

| Component | Minimum (ms) | Maximum (ms) | Molecular Determinants |
| :--- | :--- | :--- | :--- |
| $\tau_{transduction}$ | 1 | 3 | Piezo2 |
| $\tau_{afferent}$ | 10 | 20 | GPR126, Myelin proteins, NaV channels |
| $\tau_{spinal}$ | 2 | 5 | LBX1 (interneuron specs) |
| $\tau_{cerebellar}$ | 40 | 80 | - |
| $\tau_{efferent}$ | 10 | 20 | Myelin proteins |
| $\tau_{NMJ}$ | 0.5 | 1 | AChR subunits |
| $\tau_{EM}$ | 30 | 60 | Muscle fiber type, titin, collagen |
| **Total ($\tau$)** | **~93.5** | **~189** | |

*Note: The upper bound (~189 ms) closely approaches the critical instability threshold ($\tau > 200$ ms) identified in Paper 2. Subtle genetic variants affecting myelination (GPR126) or transduction (Piezo2) could easily push a growing adolescent over this threshold.*

## References
1. Rohlén R, Torell F, Dimitriou M. Preparation duration shapes the goal-directed tuning of stretch reflex responses. *Experimental Brain Research*, 2025. (DOI: 10.1007/s00221-025-07139-z)
2. Fletcher JR, Strzalkowski NDJ. The neuromechanics of the soleus for fall prevention in aging. *Frontiers in Physiology*, 2025. (DOI: 10.3389/fphys.2025.1743559)
3. Syndergaard I, Free DB, Farina D, Charles SK. Feedback parameters for a closed-loop multiple-input multiple-output model of the upper limb. *PLoS Comput Biol*, 2025. (DOI: 10.1371/journal.pcbi.1013183)