# Day 2 Literature Review: Peripheral Neuropathy and Delay (τ) Increase in Ageing

## Key Findings on Nerve Conduction Velocity (NCV) and Ageing

Aging is associated with a progressive decline in peripheral nerve function, which quantitatively increases the sensorimotor delay ($\tau$) in the postural control loop.

1. **General Decline in NCV:**
   - Nerve conduction studies consistently show that NCV slows down with advancing age.
   - A cross-sectional study by Palve & Palve (2018) investigated the impact of aging on late responses and nerve conduction velocities in healthy individuals.
   - The age-related changes are greater in the nerves of the lower extremities than in the median nerve in the upper limb (Palve & Palve, 2018).

2. **Quantitative Estimates of Decline:**
   - Palve & Palve (2018) note a significant negative correlation between age and both motor and sensory NCV.
   - Age increases the F-wave latency by 0.03 ms/year in the upper limbs and 0.1 ms/year in the lower limbs.
   - Specifically, they observed F-wave latency increases of 0.02 ms/year in the median nerve.

3. **Mechanism of Decline:**
   - At a cellular level, reduced mitochondrial ATP production due to oxygen-free radical damage may contribute to the slowing of muscle contraction and neuromuscular junction transmission.

## Relevance to the Terminal Derivative Gain Gap Model

The progressive slowing of NCV directly corresponds to an increase in the delay parameter ($\tau$) in our delayed PID inverted pendulum model.
Unlike adolescence, where the body grows too fast for the nervous system to adapt, ageing represents a structural degradation of the sensory and transmission lines themselves. As $\tau$ increases beyond critical thresholds (e.g., >200ms as established in Paper 2), the phase margin of the postural control system degrades. When this is coupled with a degrading actuator gain (sarcopenia, to be explored in Day 3), the system approaches a terminal instability—manifesting clinically as an increased risk of falls.

### References
- Palve SS, Palve SB (2018). Impact of Aging on Nerve Conduction Velocities and Late Responses in Healthy Individuals. *Journal of Neurosciences in Rural Practice*, 9(1):112-116. DOI: 10.4103/jnrp.jnrp_323_17
