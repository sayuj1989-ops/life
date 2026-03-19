# Phase 1, Day 1: Decomposition of Proprioceptive Delay ($\tau$)

## Introduction
In the control-theoretic model of Adolescent Idiopathic Scoliosis (AIS) presented in Paper 2, the total proprioceptive delay ($\tau$) is the critical parameter determining stability of the postural control system. However, $\tau$ is not a monolithic variable; it represents the sum of multiple sequential biological and physiological delays.

## The $\tau$ Budget

The total delay $\tau_{total}$ can be decomposed as follows:
$\tau_{total} = \tau_{transduction} + \tau_{afferent} + \tau_{spinal} + \tau_{cerebellar} + \tau_{efferent} + \tau_{NMJ} + \tau_{EM}$

### 1. Peripheral Transduction Delay ($\tau_{transduction}$)
* **Definition**: Time for muscle spindle stretch-sensitive ion channels to convert mechanical deformation into receptor potentials.
* **Key Molecular Mediators**: Piezo2 (mechanotransduction channel).
* **Estimated Delay**: ~1-2 ms.

### 2. Afferent Conduction Delay ($\tau_{afferent}$)
* **Definition**: Time for action potentials to travel along proprioceptive (Group Ia/II) afferents from paraspinal muscles to the spinal cord.
* **Key Molecular Mediators**: GPR126 (myelination), SCN11A/SCN9A (voltage-gated sodium channels).
* **Estimated Delay**: ~15-20 ms (depends heavily on axon length and myelination quality, typically conduction velocities are 40-60 m/s for Ia afferents in humans).

### 3. Spinal Relay Delay ($\tau_{spinal}$)
* **Definition**: Synaptic processing time in Clarke's column and dorsal spinocerebellar tract.
* **Key Molecular Mediators**: LBX1 (dorsal spinal cord interneuron specification).
* **Estimated Delay**: ~2-5 ms per synapse.

### 4. Cerebellar Processing Delay ($\tau_{cerebellar}$)
* **Definition**: Integration and prediction time in the cerebellum (forward model).
* **Estimated Delay**: ~30-50 ms.

### 5. Efferent Conduction Delay ($\tau_{efferent}$)
* **Definition**: Time for motor commands to return via corticospinal and vestibulospinal tracts.
* **Estimated Delay**: ~15-20 ms.

### 6. Neuromuscular Junction (NMJ) Delay ($\tau_{NMJ}$)
* **Definition**: Synaptic transmission time at the motor endplate.
* **Estimated Delay**: ~0.5-1 ms.

### 7. Electromechanical Delay ($\tau_{EM}$)
* **Definition**: Time from motor unit activation to measurable force production.
* **Estimated Delay**: ~30-50 ms.

## Synthesis for the Model
Summing these baseline values yields a normal physiological delay of roughly 100-150 ms. When growth velocity outpaces neurodevelopment (e.g., myelination lagging behind bone growth during puberty), $\tau_{afferent}$ and potentially $\tau_{efferent}$ may increase. A transient increase driving $\tau_{total} > 200$ ms could push the system into the "derivative gain gap," as postulated in Paper 2.
