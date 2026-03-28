# Day 1: Decomposition of Proprioceptive Delay ($\tau$)

The proprioceptive delay ($\tau$) in postural control can be decomposed into several physiological components:

$$\tau_{total} = \tau_{transduction} + \tau_{afferent} + \tau_{spinal} + \tau_{cerebellar} + \tau_{efferent} + \tau_{NMJ} + \tau_{EM}$$

Based on the literature search, we attempt to quantify these sub-components in humans:

1. **Peripheral Transduction Delay ($\tau_{transduction}$):**
   - Mechanosensitive channel (e.g., Piezo2) activation time.
   - *Unverified — needs literature confirmation for exact human values.*

2. **Afferent Conduction Delay ($\tau_{afferent}$):**
   - Conduction along Group Ia/II proprioceptive afferents.
   - **Quantification:** Muscle afferent conduction velocity in humans is approximately **57.6 m/s**.
   - *Reference:* Shefner & Logician (DOI: 10.1002/mus.880170712).

3. **Spinal Relay Delay ($\tau_{spinal}$):**
   - Synaptic and structural delay in dorsal column nuclei and Clarke's column.
   - *Unverified — precise latency not extracted in initial search.*

4. **Cerebellar Processing Delay ($\tau_{cerebellar}$):**
   - Time for state estimation and forward model processing in the cerebellum.
   - *Unverified — needs literature confirmation for human latency.*

5. **Efferent Conduction Delay ($\tau_{efferent}$):**
   - Descending motor command conduction (e.g., corticospinal/vestibulospinal tracts).
   - Motor CV is approximately **52.4 m/s** (Shefner & Logician, DOI: 10.1002/mus.880170712).
   - *Delay depends on exact pathway length.*

6. **Neuromuscular Junction Delay ($\tau_{NMJ}$):**
   - Synaptic transmission at the motor endplate.
   - *Unverified — needs literature confirmation.*

7. **Electromechanical Delay ($\tau_{EM}$):**
   - Latency between muscle activation (EMG) and force production.
   - *Unverified — exact value pending further literature extraction.*

## Preliminary $\tau$ Budget Calculation
Given a typical distance from paraspinal muscle spindle to spinal cord (e.g., $\sim 0.1$ meters for a thoracic segment, or $\sim 1.0$ meters for lumbar to brainstem):
- $\tau_{afferent}$ (thoracic): $0.1m / 57.6 \text{m/s} \approx 1.7 \text{ms}$.
- $\tau_{efferent}$ (thoracic): $0.1m / 52.4 \text{m/s} \approx 1.9 \text{ms}$.

This represents a starting point. Further literature must be queried to assign numerical values to transduction, central processing, and electromechanical coupling.
