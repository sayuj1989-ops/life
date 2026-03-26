# Phase 1, Day 1: Decomposition of Proprioceptive Delay ($\tau$)

The total proprioceptive delay $\tau_{total}$ governing the stability of the upright postural control model (Paper 2) is a composite parameter. In biological terms, it represents the complete latency from a mechanical perturbation (e.g., sway) to the onset of corrective muscle force production. We decompose this delay into seven sequential physiological components:

$$ \tau_{total} = \tau_{transduction} + \tau_{afferent} + \tau_{spinal} + \tau_{cerebellar} + \tau_{efferent} + \tau_{NMJ} + \tau_{EM} $$

## Component Estimates and Literature Budget

1. **Peripheral Transduction Delay ($\tau_{transduction}$)**
   - **Mechanism:** Time required for muscle spindle deformation to open mechanosensitive ion channels (primarily Piezo2) and generate a depolarizing receptor potential sufficient to trigger an action potential.
   - **Estimate:** 1–3 ms.
   - **Molecular Basis:** Piezo2 channel activation kinetics.

2. **Afferent Conduction Delay ($\tau_{afferent}$)**
   - **Mechanism:** Propagation of the action potential along Group Ia and Group II afferent axons from the muscle spindle to the dorsal horn of the spinal cord.
   - **Estimate:** 15–25 ms (assuming a conduction velocity of 60–120 m/s and an afferent pathway length of ~1.0–1.5 meters from lower limb to spinal cord).
   - **Molecular Basis:** Axonal diameter and myelination (Schwann cells in PNS), dependent on proteins like GPR126 and structural myelin proteins (MBP, PMP22, MPZ), as well as voltage-gated sodium channels (e.g., Nav1.5/1.7).

3. **Spinal Relay Delay ($\tau_{spinal}$)**
   - **Mechanism:** Synaptic delay and processing within the spinal cord. For postural control, this includes synapses onto interneurons, Clarke's column, and ascending tracts (e.g., spinocerebellar tract), or direct monosynaptic connections to alpha motor neurons (stretch reflex).
   - **Estimate:** 1–5 ms per synapse. Total estimate ~3–10 ms.
   - **Molecular Basis:** Specification and function of dorsal interneurons and proprioceptive relays, guided by transcription factors like LBX1.

4. **Cerebellar Processing Delay ($\tau_{cerebellar}$)**
   - **Mechanism:** Supraspinal integration, state estimation, and generation of a descending motor command via the forward model in the cerebellum and brainstem.
   - **Estimate:** 30–50 ms.
   - **Molecular Basis:** Cerebellar circuitry, Purkinje cell firing dynamics.

5. **Efferent Conduction Delay ($\tau_{efferent}$)**
   - **Mechanism:** Propagation of the descending motor command from the spinal cord (ventral horn) to the neuromuscular junction via alpha motor neurons.
   - **Estimate:** 15–25 ms (similar lengths and conduction velocities to afferent pathways).
   - **Molecular Basis:** Myelination by oligodendrocytes (CNS) and Schwann cells (PNS).

6. **Neuromuscular Junction Delay ($\tau_{NMJ}$)**
   - **Mechanism:** Synaptic transmission at the motor endplate, involving acetylcholine release, binding, and muscle cell depolarization.
   - **Estimate:** 1–2 ms.

7. **Electromechanical Delay ($\tau_{EM}$)**
   - **Mechanism:** The time interval between the onset of muscle electrical activity (EMG) and the onset of measurable force production. It involves excitation-contraction coupling and the stretching of series elastic components.
   - **Estimate:** 10–30 ms.
   - **Literature Note:** Classic studies such as "Electromechanical delay in human skeletal muscle under concentric and eccentric contractions" (Cavanagh & Komi, 1979, Eur J Appl Physiol; DOI: 10.1007/bf00431022) and "ELECTROMECHANICAL DELAY IN HUMAN SKELETAL .MUSCLE" (Komi, Cavanagh et al., 1977, Medicine & Science in Sports & Exercise; DOI: 10.1249/00005768-197721000-00021) place $\tau_{EM}$ in this range.

**Total Estimated Budget:** ~75–145 ms for lower limb responses. Peterka (2002) fits postural models with $\tau \approx$ 150-200 ms, suggesting supraspinal processing, variable conduction lengths, or non-linear scaling during growth might push this value higher.
