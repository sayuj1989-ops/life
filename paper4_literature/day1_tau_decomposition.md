# Decomposition of Proprioceptive Delay ($\tau$) in Human Postural Control

The total proprioceptive delay ($\tau$) in human postural control—estimated at 150–200 ms in the Peterka inverted pendulum model (Paper 2)—is a composite of several physiological components. To understand how genetic variants associated with Adolescent Idiopathic Scoliosis (AIS) might alter $\tau$, we must first decompose it into its constituent parts based on established human electrophysiology.

## 1. Peripheral Transduction Delay ($\tau_{transduction}$)
- **Description:** The time required for mechanical deformation of the muscle spindle to be converted into an action potential. This involves the opening of mechanically gated ion channels (primarily Piezo2) and the subsequent depolarization of the Group Ia/II afferent terminal to threshold.
- **Estimated Value:** ~1–3 ms.
- **Key Molecules:** Piezo2.
- **References:**
  - Day et al. (2017) [DOI: 10.1038/nature22324] and Chesler et al. (2016) [DOI: 10.1056/NEJMoa1602812] demonstrated the rapid kinetics of Piezo2 in sensory neurons.

## 2. Afferent Conduction Delay ($\tau_{afferent}$)
- **Description:** The transit time for the action potential to travel from the muscle spindle (e.g., in paraspinal muscles) to the dorsal root ganglion and into the spinal cord.
- **Estimated Value:** ~15–25 ms (varies strongly with height and nerve length).
- **Key Molecules:** Myelin structural proteins (MBP, PMP22, MPZ), Schwann cell regulators (GPR126/ADGRG6), and voltage-gated sodium channels (Nav1.5/Nav1.7 encoded by SCN11A/SCN9A).
- **References:**
  - Normative nerve conduction velocities (NCV) for Group Ia afferents are ~60-70 m/s. For a spine length of ~0.5–0.7m, this yields roughly 10–15 ms, plus time for slower peripheral segments.

## 3. Spinal Relay and Processing Delay ($\tau_{spinal}$)
- **Description:** Synaptic transmission time in the spinal cord, including relays in Clarke's column and interneuron processing before ascending via the spinocerebellar tracts.
- **Estimated Value:** ~3–5 ms per synapse. Total ~5-10 ms.
- **Key Molecules:** Synaptic machinery, developmental transcription factors specifying these circuits (e.g., LBX1).

## 4. Cerebellar Processing Delay ($\tau_{cerebellar}$)
- **Description:** The time taken for the cerebellum and brainstem to integrate the ascending proprioceptive signals, update the forward internal model, and generate a corrective motor command. This is often the largest central component of the delay.
- **Estimated Value:** ~50–80 ms.
- **References:**
  - computational models of cerebellar forward models often require processing delays of this magnitude to explain human visuomotor and proprioceptive tracking behavior.

## 5. Efferent Conduction Delay ($\tau_{efferent}$)
- **Description:** The transit time for the descending motor command from the brainstem/spinal cord to the neuromuscular junction of the paraspinal or lower limb muscles.
- **Estimated Value:** ~15–25 ms.
- **Key Molecules:** Myelin-related proteins (oligodendrocytes in CNS, Schwann cells in PNS), motor neuron Nav channels.

## 6. Neuromuscular Junction (NMJ) Delay ($\tau_{NMJ}$)
- **Description:** The time for presynaptic acetylcholine release, diffusion across the synaptic cleft, binding to nicotinic receptors, and generation of the muscle action potential.
- **Estimated Value:** ~0.5–1 ms.

## 7. Electromechanical Delay ($\tau_{EM}$)
- **Description:** The time from the onset of the muscle action potential (detectable by EMG) to the onset of measurable force production. This involves excitation-contraction coupling (calcium release) and the stretching of the series elastic component (tendons/aponeuroses).
- **Estimated Value:** ~30–50 ms.
- **References:**
  - Esposito et al. (2011) [DOI: 10.1007/s00421-010-1815-4] and Cè et al. (2013) [DOI: 10.1002/mus.23627] characterized EMD components in human skeletal muscle.

## Summary Budget for $\tau_{total}$

| Component | Estimate (ms) | Key Biological Targets / GWAS Hits |
|-----------|---------------|------------------------------------|
| $\tau_{transduction}$ | 1–3 | Piezo2 |
| $\tau_{afferent}$ | 15–25 | GPR126, SCN11A, Myelin proteins |
| $\tau_{spinal}$ | 5–10 | LBX1 |
| $\tau_{cerebellar}$ | 50–80 | |
| $\tau_{efferent}$ | 15–25 | |
| $\tau_{NMJ}$ | 1 | |
| $\tau_{EM}$ | 30–50 | |
| **Total $\tau$** | **~120–190 ms** | Matches Peterka (2002) model values. |
