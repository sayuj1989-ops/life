# Decomposition of Proprioceptive Delay ($\tau$)

The total proprioceptive delay ($\tau_{total}$), modeled as a critical parameter in the derivative gain gap hypothesis of Adolescent Idiopathic Scoliosis (AIS), is the sum of several distinct physiological sub-components:

$$ \tau_{total} = \tau_{transduction} + \tau_{afferent} + \tau_{spinal} + \tau_{cerebellar} + \tau_{efferent} + \tau_{NMJ} + \tau_{EM} $$

## 1. Peripheral Transduction Delay ($\tau_{transduction}$)
*   **Definition:** Time taken for muscle spindle stretch-sensitive ion channels (primarily Piezo2) to convert mechanical deformation into receptor potentials.
*   **Molecular Basis:** Piezo2 channel kinetics. Stretch-activated channels (SAC) typically respond to mechanical perturbations within tens of milliseconds (Madame Curie Bioscience Database, NCBI Bookshelf NBK6374).
*   **Estimated Value:** ~10-20 ms [unverified — needs precise Piezo2-specific confirmation].

## 2. Afferent Conduction Delay ($\tau_{afferent}$)
*   **Definition:** Time for action potentials to travel along proprioceptive (Group Ia/II) afferents from paraspinal muscles to the spinal cord.
*   **Molecular Basis:** Axon diameter and myelination quality (governed by GPR126, MBP, PMP22, MPZ). Action potential propagation speed depends on voltage-gated sodium channels (SCN11A / SCN9A).
*   **Estimated Value:** Based on Ia afferent conduction velocities of ~56-64 m/s (Banks 2021; IJSR v4i5), traversing a ~0.5 - 1.0 m pathway (e.g. from distal limbs or paraspinal muscles) yields an estimated delay of ~8-18 ms.

## 3. Spinal Relay Delay ($\tau_{spinal}$)
*   **Definition:** Synaptic processing delay in the spinal cord, primarily in Clarke's column and the dorsal spinocerebellar tract.
*   **Molecular Basis:** Development and specification of dorsal spinal cord interneurons, strongly associated with LBX1.
*   **Estimated Value:** ~1 ms per synapse in the adult spinal cord (Takeoka & Arber, Cell Rep 27: 71-85, 2019, doi: 10.1016/j.celrep.2019.03.010). For a trisynaptic circuit, ~3 ms.

## 4. Cerebellar Processing Delay ($\tau_{cerebellar}$)
*   **Definition:** Integration and prediction generation within the cerebellum (forward model computation).
*   **Molecular Basis:** Synaptic network dynamics in the cerebellar cortex and deep cerebellar nuclei (e.g., Purkinje cell processing of interstimulus intervals up to hundreds of milliseconds, Johansson et al. 2014; Frontiers Comput Neurosci 2023, doi: 10.3389/fncom.2023.1108346).
*   **Estimated Value:** [unverified — needs precise latency confirmation for predictive postural control].

## 5. Efferent Conduction Delay ($\tau_{efferent}$)
*   **Definition:** Time for motor commands to travel from the CNS via descending tracts (e.g., corticospinal, vestibulospinal) to the lower motor neurons.
*   **Molecular Basis:** Myelination of central descending tracts.
*   **Estimated Value:** Based on corticospinal tract conduction velocities of ~67 m/s measured between C6 and L1 (Snooks & Swash, JNNP 1985;48:1135-1139, doi: 10.1136/jnnp.48.11.1135), traversing ~0.5m yields a delay of ~7-10 ms.

## 6. Neuromuscular Junction (NMJ) Delay ($\tau_{NMJ}$)
*   **Definition:** Synaptic transmission delay at the motor endplate, involving acetylcholine release and binding.
*   **Molecular Basis:** Presynaptic release machinery, AChR density.
*   **Estimated Value:** Recordings from neuromuscular junctions reveal a delay of 0.5 to 4.0 milliseconds between the onset of action potential at the nerve terminal and action potential at the postsynaptic site (Britannica, "synaptic delay").

## 7. Electromechanical Delay ($\tau_{EM}$)
*   **Definition:** Time from motor unit activation (muscle fiber action potential) to the onset of measurable force production.
*   **Molecular Basis:** Excitation-contraction coupling (calcium release, cross-bridge formation) and the stretching of the series elastic component (tendon and aponeurosis).
*   **Estimated Value:** ~20-80 ms. Specific measurements show ~53 ms during voluntary contraction in quadriceps and ~80 ms in muscle-tendon actuator models (JOSPT 2002, doi: 10.2519/jospt.2002.32.4.158; Conforto et al. 2006; Hopkins et al. 2007).
