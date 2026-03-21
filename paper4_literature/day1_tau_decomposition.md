# Day 1: Decomposition of Proprioceptive Delay ($\tau$)

## Introduction
The derivative gain gap hypothesis relies on the total proprioceptive delay, $\tau$. In Paper 2, this was treated as a lumped parameter. However, to understand its molecular basis, $\tau$ must be decomposed into its constituent biological processes. Each component has distinct molecular drivers, many of which are implicated in AIS pathogenesis.

Based on a literature search of electrophysiological data, we decompose the total proprioceptive delay $\tau_{total}$ into seven distinct components:

$\tau_{total} = \tau_{trans} + \tau_{afferent} + \tau_{spinal} + \tau_{cereb} + \tau_{efferent} + \tau_{NMJ} + \tau_{EMD}$

## 1. Peripheral Transduction Delay ($\tau_{trans}$)
**Definition:** The time required for mechanical deformation of the muscle spindle to generate a receptor potential via stretch-sensitive ion channels.
**Molecular Drivers:** Primarily mediated by Piezo2 channels.
**Literature Values:** Exact transduction delays in human muscle spindles are difficult to isolate in vivo but are generally rapid (on the order of 1-3 ms), based on related mechanotransduction studies (e.g., *Chesler et al., 2016*, though precise spindle in vivo latency requires further explicit confirmation).
*(Note: Specific human muscle spindle transduction latency value is unverified — needs literature confirmation).*

## 2. Afferent Conduction Delay ($\tau_{afferent}$)
**Definition:** The time for action potentials to travel along Group Ia/II afferent fibers from the periphery to the spinal cord.
**Molecular Drivers:** Determined by axon diameter and myelination quality (e.g., GPR126/ADGRG6, MBP, PMP22, MPZ) and voltage-gated sodium channels (e.g., Nav1.5/1.7, SCN9A/SCN11A).
**Literature Values:** Conduction velocity for human Group Ia afferents is approximately 50-70 m/s. Depending on limb length (e.g., 1 meter from leg to spinal cord), this yields a delay of ~14-20 ms.

## 3. Spinal Relay Delay ($\tau_{spinal}$)
**Definition:** Synaptic processing time within the spinal cord (e.g., Clarke's column) before ascending to the cerebellum.
**Molecular Drivers:** Circuit architecture specified by developmental transcription factors like LBX1.
**Literature Values:** Synaptic delays are typically 0.5-1.0 ms per synapse. A short relay circuit may add 1-3 ms.
*(Note: Exact cumulative delay in the human spinocerebellar relay is an estimate — needs literature confirmation).*

## 4. Cerebellar Processing Delay ($\tau_{cereb}$)
**Definition:** The integration and prediction processing time in the cerebellum (the forward model).
**Literature Values:** This is highly variable depending on task complexity but is often estimated at 10-30 ms in control theory models of human posture.
*(Note: Precise forward model processing time requires further specific literature confirmation).*

## 5. Efferent Conduction Delay ($\tau_{efferent}$)
**Definition:** The time for motor commands to travel from the CNS to the muscle via motor neurons (e.g., corticospinal/vestibulospinal tracts).
**Literature Values:** Similar to afferent conduction, motor conduction velocities are typically 50-60 m/s. For a 1-meter path, this is roughly 15-20 ms.

## 6. Neuromuscular Junction Transmission Delay ($\tau_{NMJ}$)
**Definition:** Time for the action potential to cross the neuromuscular junction and initiate muscle fiber depolarization.
**Literature Values:** Studies on near-fiber electromyography (e.g., DOI: 10.1016/j.clinph.2021.02.008) examine NMJ temporal variability. Standard physiological estimates place NMJ delay around 0.5-1.0 ms.

## 7. Electromechanical Delay ($\tau_{EMD}$)
**Definition:** The time from initial electrical activation of the muscle (EMG onset) to the onset of measurable force production.
**Literature Values:** Studies (e.g., DOI: 10.1051/sicotj/2022018, DOI: 10.1038/s41598-022-21940-8) consistently measure EMD. In lower extremities (e.g., peroneal/quadriceps), it ranges from 30-60 ms, often altered by fatigue or pathology.

## Summary $\tau$ Budget (Estimated Baseline for Adult)
- $\tau_{trans}$: ~2 ms
- $\tau_{afferent}$: ~17 ms (assuming 1m path at 60 m/s)
- $\tau_{spinal}$: ~2 ms
- $\tau_{cereb}$: ~20 ms
- $\tau_{efferent}$: ~17 ms (assuming 1m path at 60 m/s)
- $\tau_{NMJ}$: ~1 ms
- $\tau_{EMD}$: ~40 ms

**Total Estimated Delay ($\tau_{total}$): ~100 ms** (This represents a baseline minimum; during the adolescent growth spurt, path lengths increase while myelination may lag, extending these delays, particularly $\tau_{afferent}$ and $\tau_{efferent}$, potentially pushing total loop delays towards the 200 ms instability threshold modeled in Paper 2).
