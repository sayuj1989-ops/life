# Phase 1, Day 2: Peripheral Neuropathy and Nerve Conduction Velocity in Ageing

## Summary
Ageing has a profound and measurable impact on the peripheral nervous system, directly contributing to an increase in proprioceptive delay ($\tau$) in the postural control loop. This delay is primarily driven by progressive degradation of peripheral nerves, including demyelination, axonal atrophy, and a reduction in nerve conduction velocity (NCV).

## Key Findings on Nerve Conduction Velocity (NCV) Decline
* **Linear Decline with Age:** Multiple cross-sectional and longitudinal studies demonstrate that NCV decreases linearly with age, typically starting around 30-40 years of age, with more pronounced declines observed after age 60.
* **Rate of Decline:**
    * A prospective cohort study (Tong et al., 2004) found sensory velocities in the upper limbs decreased at a rate of 0.14 m/s per year.
    * Werner et al. (2012) observed a decrease in conduction velocity at a rate of 0.41 m/s per year of age.
    * The decline in nerve conduction velocity and rise in sensory latency with increasing age is primarily attributed to a loss of myelinated and unmyelinated nerve fibers, as well as a reduction in nerve diameter and changes in fiber membrane (Verdú et al., 2000; Palve & Palve, 2018).
* **Sensory vs. Motor Decline:** The change with age is consistently reported to be greater in sensory nerve conduction compared to motor nerve conduction (Palve & Palve, 2018). This directly impacts the afferent proprioceptive feedback loop, which is critical for sensing posture and joint position.
* **Late Responses and Latency:** The latency of late responses (e.g., F-waves and H-reflexes, which measure conduction along the entire length of the nerve, including the spinal roots) increases with age. For instance, the effect of age on F-wave latency has been reported to increase by 0.1 ms/year in the lower limbs, directly contributing to an increase in $\tau$.
* **Lower Limb vs. Upper Limb:** Age-related changes in NCV are greater in the nerves of the lower extremities than in the upper limbs (Palve & Palve, 2018). This is particularly relevant for postural control, which relies heavily on proprioceptive feedback from the legs and feet.

## Mechanism of Degradation
Verdú et al. (2000) outline the primary mechanisms of age-related peripheral nerve deterioration:
1. **Demyelination and Remyelination:** The deterioration of myelin sheaths may be due to a decrease in the expression of major myelin proteins.
2. **Axonal Atrophy:** Often seen in aged nerves, explained by a reduction in the expression and axonal transport of cytoskeletal proteins.
3. **Loss of Nerve Fibers:** A progressive loss of both myelinated and unmyelinated fibers.

## Relevance to the Derivative Gain Gap Model
In the PID model of postural control, the time delay ($\tau$) represents the total time required for proprioceptive sensing, afferent neural transmission, central processing, efferent motor transmission, and muscle activation.
* The age-related decrease in NCV and the associated increase in nerve latency directly quantify the biological increase in the afferent and efferent transmission components of $\tau$.
* The finding that sensory pathways and lower extremity nerves are disproportionately affected underscores the specific vulnerability of the postural feedback loop to age-related peripheral neuropathy.
* This quantifiable increase in transmission time provides the physiological basis for the "terminal derivative gain gap," where the controller's delay ($\tau$) progressively pushes the system towards instability.

## References
1. Palve SS, Palve SB. (2018). Impact of Aging on Nerve Conduction Velocities and Late Responses in Healthy Individuals. *Journal of Neurosciences in Rural Practice*. 9(1):112-116. doi: 10.4103/jnrp.jnrp_323_17.
2. Verdú E, Ceballos D, Vilches JJ, Navarro X. (2000). Influence of aging on peripheral nerve function and regeneration. *Journal of the Peripheral Nervous System*. 5(4):191-208. doi: 10.1046/j.1529-8027.2000.00026.x.
3. Tong HC, Werner RA, Franzblau A. (2004). Effect of aging on sensory nerve conduction study parameters. *Muscle & Nerve*. 29(5):716-20. doi: 10.1002/mus.20026.
