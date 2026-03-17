# Phase 1, Day 1: Decomposition of Proprioceptive Delay (τ)

## Overview
Proprioceptive delay ($\tau$) is the total time required for a mechanical change in body posture to be detected, transmitted, processed, and counteracted by muscle force. This document decomposes $\tau$ into its constituent physiological components to establish a baseline "$\tau$ budget" for our control-theoretic model.

## The $\tau$ Budget Components

### 1. Peripheral Transduction Delay ($\tau_{transduction}$)
* **Definition:** Time taken for mechanical deformation of the muscle spindle to open mechanosensitive ion channels (primarily Piezo2) and generate a receptor potential that triggers the first action potential.
* **Mechanism:** Mechanical stretch $\rightarrow$ Piezo2 opening $\rightarrow$ Receptor potential $\rightarrow$ Voltage-gated $Na^+$ channel (Nav) activation $\rightarrow$ Action potential initiation.
* **Estimated Value:** ~1 - 2 ms.
* **Evidence:** Sensory transduction by mechanically gated channels like Piezo2 is extremely fast, typically occurring in the sub-millisecond to millisecond range. Bullinger et al. (2011, *Journal of Neurophysiology*, doi:10.1152/jn.00083.2011) and related studies on muscle spindle firing show very rapid responses to length changes with conduction delays <3ms.

### 2. Afferent Conduction Delay ($\tau_{afferent}$)
* **Definition:** Time for the action potential to travel along Group Ia and II sensory afferent nerve fibers from the muscle spindle to the dorsal root entry zone of the spinal cord.
* **Mechanism:** Action potential propagation along myelinated axons. Speed depends on axon diameter and myelin thickness.
* **Estimated Value:** ~15 - 20 ms.
* **Evidence:** Group Ia afferents are the fastest conducting fibers in the human body, with conduction velocities ranging from 60 - 120 m/s. Assuming a distance of ~1 meter from the lower limb (e.g., soleus muscle) to the lower spinal cord, the delay is roughly $1m / (60m/s)$ to $1m / (120m/s)$ $\approx$ 8 to 17 ms.

### 3. Spinal Relay Delay ($\tau_{spinal}$)
* **Definition:** Time for synaptic transmission and local processing within the spinal cord (e.g., dorsal spinocerebellar tract relays in Clarke's column).
* **Mechanism:** Synaptic delay (neurotransmitter release, diffusion, receptor binding, and postsynaptic depolarization).
* **Estimated Value:** ~2 - 5 ms (per synapse).
* **Evidence:** Typical chemical synaptic delays in the central nervous system are around 1 - 2 ms per synapse. The relay through Clarke's column involves at least one synapse before ascending to the cerebellum.

### 4. Cerebellar Processing Delay ($\tau_{cerebellar}$)
* **Definition:** Time for the cerebellum and brainstem to integrate proprioceptive signals, update the forward model of body geometry, and compute corrective motor commands.
* **Mechanism:** Complex network processing involving mossy fibers, granule cells, Purkinje cells, and deep cerebellar nuclei.
* **Estimated Value:** ~10 - 30 ms.
* **Evidence:** The cerebellum responds to proprioceptive inputs at latencies as short as 4 ms (in animal models), but generating a coordinated corrective motor command takes longer. Feedback processing in the cerebellum for oculomotor and reaching tasks shows delays in the range of tens of milliseconds (unverified — needs literature confirmation).

### 5. Efferent Conduction Delay ($\tau_{efferent}$)
* **Definition:** Time for the motor command (action potentials) to travel along $\alpha$-motor neurons from the spinal cord to the neuromuscular junction.
* **Mechanism:** Action potential propagation along myelinated efferent axons.
* **Estimated Value:** ~15 - 20 ms.
* **Evidence:** Similar to afferent conduction, $\alpha$-motor neurons are large, heavily myelinated fibers with conduction velocities comparable to Group Ia afferents (roughly 60 - 120 m/s). For a 1-meter path, the delay is ~8 - 17 ms.

### 6. Neuromuscular Junction (NMJ) Delay ($\tau_{NMJ}$)
* **Definition:** Time for synaptic transmission at the neuromuscular junction.
* **Mechanism:** Acetylcholine release, diffusion across the synaptic cleft, binding to nicotinic receptors, and generation of the endplate potential.
* **Estimated Value:** ~0.5 - 1 ms.
* **Evidence:** The NMJ is a highly specialized, fast synapse designed for rapid and reliable transmission. Synaptic delay here is minimal.

### 7. Electromechanical Delay ($\tau_{EM}$)
* **Definition:** Time from the onset of the muscle action potential (measurable by EMG) to the generation of measurable muscle force.
* **Mechanism:** Excitation-contraction coupling (calcium release from sarcoplasmic reticulum, binding to troponin, cross-bridge cycling) and the time required to stretch the series elastic components (tendons and connective tissue) to transmit force to the bone.
* **Estimated Value:** ~30 - 60 ms.
* **Evidence:** Numerous biomechanical studies measure EMD. For instance, studies on the quadriceps and peroneal muscles report EMD values in the range of 40 to 60 ms, and sometimes higher (up to 120+ ms) depending on the muscle, task (increasing vs. decreasing force), and state (fatigued vs. rested).

## Total Baseline Proprioceptive Delay ($\tau_{total}$)
Summing these components yields an estimated baseline $\tau_{total}$:

$$ \tau_{total} = \tau_{transduction} + \tau_{afferent} + \tau_{spinal} + \tau_{cerebellar} + \tau_{efferent} + \tau_{NMJ} + \tau_{EM} $$

$$ \tau_{total} \approx (1) + (17) + (3) + (20) + (17) + (1) + (50) \approx 109 \text{ ms} $$

For the longer reflex arcs involved in postural control (e.g., from ankle to brainstem/cerebellum and back), long-loop reflexes typically exhibit total latencies of **100 - 150 ms**, which aligns well with this budget. Paper 2's model identifies a critical threshold where $\tau > 200 \text{ ms}$ combined with high growth velocity triggers the "derivative gain gap" instability. Our molecular investigation will focus on how genetic variants in specific proteins can perturb individual components of this budget, pushing the total $\tau$ toward or beyond the 200 ms instability threshold.
