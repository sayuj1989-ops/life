# Phase 1, Day 1: Decomposition of Proprioceptive Delay ($\tau$)

The total proprioceptive delay ($\tau$) in the derivative gain gap model (Paper 2) is the sum of several physiological components. To bridge control theory to molecular genetics, we must quantify each sub-delay from published electrophysiology.

## The $\tau$ Budget

Based on literature review, the total proprioceptive delay ($\tau_{total}$) can be decomposed into the following sequential components:

$$ \tau_{total} = \tau_{transduction} + \tau_{afferent} + \tau_{spinal} + \tau_{cerebellar} + \tau_{efferent} + \tau_{NMJ} + \tau_{EM} $$

### 1. Peripheral Transduction Delay ($\tau_{transduction}$)
- **Description**: The time required for mechanical deformation of the proprioceptor (e.g., muscle spindle) to open force-gated ion channels and generate a receptor potential.
- **Key Molecules**: Piezo2.
- **Estimated Delay**: **1-2 ms**.
- **Evidence**: Mechanotransduction via Piezo2 in sensory neurons occurs rapidly. Studies combining atomic force microscopy and electrophysiology show nearly instantaneous (<1 ms) or slightly delayed (~2 ms) transduction depending on channel density and cytoskeletal architecture.
- **Reference**:
  - *The energetics of rapid cellular mechanotransduction*, PNAS. [DOI: 10.1073/pnas.2215747120]
  - *Mechanically gated currents in mouse sensory neurons lacking PIEZO2*. Latency reported as ~2 ms. [PMC12820996]

### 2. Afferent Conduction Delay ($\tau_{afferent}$)
- **Description**: The time for the action potential to travel from the peripheral proprioceptor to the dorsal root ganglion and into the spinal cord.
- **Key Molecules**: GPR126 (myelination), Nav1.7/1.5 (sodium channels), Myelin structural proteins (MBP, MPZ).
- **Estimated Delay**: **8-14 ms** (assuming ~1 meter path length).
- **Evidence**: Group Ia afferent fibers (from muscle spindles) are the fastest conducting sensory fibers, heavily myelinated, with conduction velocities ranging from 70-120 m/s. For a tall adolescent (~1.5m to spine), travel distance is roughly 1 meter.
- **Reference**:
  - *Proprioception: clinical relevance and neurophysiology*, Current Opinion in Physiology (2021). [Prochazka, 2021]

### 3. Spinal Relay Delay ($\tau_{spinal}$)
- **Description**: Synaptic processing time in the spinal cord, primarily in Clarke's column for the dorsal spinocerebellar tract, or monosynaptic Ia connections.
- **Key Molecules**: LBX1 (interneuron specification), Synaptic vesicle proteins.
- **Estimated Delay**: **0.5-1.5 ms**.
- **Evidence**: The central delay of monosynaptic stretch reflexes is approximately 0.5-0.8 ms per synapse. Disynaptic or polysynaptic relays (e.g., to the cerebellum via Clarke's column) add proportional synaptic delays.
- **Reference**:
  - *Reflexes evoked in human thenar muscles during voluntary activity and their conduction pathways*. Estimated central delay of about 0.8 ms for monosynaptic H-reflex. [PMC493216]
  - *Circuitry of the Human Spinal Cord*. Central delay of disynaptic group I effects is ~0.7 ms longer than monosynaptic.

### 4. Cerebellar Processing Delay ($\tau_{cerebellar}$)
- **Description**: The time taken by the cerebellum to integrate the afferent signal, update the forward model, and compute the necessary corrective motor command.
- **Key Molecules**: Purkinje cell synapse proteins, calcium channels.
- **Estimated Delay**: **10-20 ms** (local computation time; full loop is longer).
- **Evidence**: The cerebellum utilizes forward internal models to predict consequences and overcome time delays. While the whole predictive loop is ~80-100 ms, the local processing delay separating afferent arrival and efferent departure is estimated in the tens of milliseconds.
- **Reference**:
  - *Predictive Modeling by the Cerebellum Improves Proprioception*. [ResearchGate: 256448990]

### 5. Efferent Conduction Delay ($\tau_{efferent}$)
- **Description**: The time for the descending motor command to travel from the motor cortex/brainstem down the spinal cord and peripheral motor nerve to the muscle.
- **Key Molecules**: Corticospinal tract myelination proteins, Motor neuron myelin.
- **Estimated Delay**: **14-15 ms** (assuming ~1 meter path length).
- **Evidence**: Corticospinal tract physiological conduction velocity is calculated to be between 65-70 m/s. Alpha-motoneuron axons conduct at ~50-100 m/s.
- **Reference**:
  - *Determining the Corticospinal and Neuromuscular Responses Following a Warm-Up Protocol*. CST conduction velocity 65-70 m/s. [ResearchGate: 342092980]
  - *The Corticospinal Discrepancy: Where are all the Slow Pyramidal Tract Neurons?* Maximum conduction velocity ~67 m/s. [PMC6896975]

### 6. Neuromuscular Junction Delay ($\tau_{NMJ}$)
- **Description**: Synaptic transmission time at the motor endplate.
- **Key Molecules**: Acetylcholine receptors, presynaptic voltage-gated calcium channels.
- **Estimated Delay**: **0.5-1.0 ms**.
- **Evidence**: Transmission of an action potential across a chemical synapse involves neurotransmitter release, diffusion, and receptor binding.
- **Reference**:
  - *Cholinergic regulation of the evoked quantal release at frog neuromuscular junction*. Synaptic delay ~0.2-0.5 ms. [PMC1665191]

### 7. Electromechanical Delay ($\tau_{EM}$)
- **Description**: The time elapsed between the onset of electrical activation of the muscle (measured by EMG) and the onset of measurable force production. Includes excitation-contraction coupling and stretching of series elastic elements.
- **Key Molecules**: Ryanodine receptors, Titin, Myosin heavy chains.
- **Estimated Delay**: **30-50 ms** (during voluntary contraction).
- **Evidence**: EMD reflects both electrochemical processes and mechanical force transmission. Measured values range from ~30 ms to ~50 ms for voluntary isometric contractions.
- **Reference**:
  - *Detection of the electromechanical delay and its components during voluntary isometric contraction of the quadriceps femoris muscle*, Frontiers in Physiology. EMD measured as ~49.7 ms. [DOI: 10.3389/fphys.2014.00494]
  - *Characterization of Electromechanical Delay Based on a Biophysical Multi-Scale Skeletal Muscle Model*. Simulated physiological range 6.1-68.6 ms, heavily dependent on neural control and recruitment. [PMC6795131]

## Summary Budget
- $\tau_{transduction}$ $\approx$ 2 ms
- $\tau_{afferent}$ $\approx$ 12 ms
- $\tau_{spinal}$ $\approx$ 1 ms
- $\tau_{cerebellar}$ $\approx$ 15 ms
- $\tau_{efferent}$ $\approx$ 15 ms
- $\tau_{NMJ}$ $\approx$ 1 ms
- $\tau_{EM}$ $\approx$ 40 ms

**Total Estimated Baseline $\tau_{total}$**: **~86 ms**.
*(Note: This represents the shortest possible physiological loop for a complex predictive response. The 200ms threshold from Paper 2 likely incorporates slower polysynaptic pathways, visual integration delays, or age/growth-related variations not accounted for in adult normative data).*
