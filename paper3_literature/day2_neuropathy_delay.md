# Phase 1, Day 2: Neuropathy and Sensorimotor Delay in Ageing

## Summary
The current focus is on the impact of ageing on nerve conduction velocity (NCV) and proprioceptive delay (sensorimotor delay τ). As the body ages, there is a progressive deterioration of peripheral nerve function, affecting both sensory and motor pathways.

## Key Findings & Literature
1. **Ageing and Nerve Conduction Velocity:**
   - Palve and Palve (2018) demonstrated that ageing has a definite correlation with NCV and late responses. In their study spanning three age groups (18-30, 31-45, 46-60 years), older individuals showed longer latencies, smaller amplitudes, and slower conduction velocities in median, common peroneal, ulnar, and tibial nerves compared to younger age groups. The changes are greater in sensory NCV than in motor NCV. (DOI: 10.4103/jnrp.jnrp_323_17)

2. **Decline is Cross-Species:**
   - A study by Walsh et al. (2014) highlights that NCV declines with age in mice as well. Both male and female mice showed a decline in NCV after 20 months of age. Interestingly, female mice had slower sensory NCV and a slower age-related decline in motor nerves compared to male mice. This supports the biological underpinning of age-related nerve function decline and the reliability of NCV as a healthspan metric. (DOI: 10.1093/gerona/glu208)

3. **Proprioceptive Delay ($\tau$):**
   - The reduction in NCV logically leads to an increase in proprioceptive/sensorimotor delay ($\tau$) in the PID control model of posture. Slower transmission of sensory inputs regarding body sway, and delayed transmission of motor commands to muscles, collectively widen the delay gap. Older adults naturally exhibit an increased $\tau$, which impairs the effectiveness of the derivative gain ($K_d$) component in the control-theoretic inverted pendulum framework.
   - Ward et al. (2016) note the mobility-related consequences of reduced lower-extremity peripheral nerve function with age, directly linking these peripheral changes to functional declines in mobility and balance (DOI: 10.14336/ad.2015.1127).

## Application to Paper 3
In Paper 2, the adolescent "derivative gain gap" was transient (body growing faster than the proprioceptive network recalibrated). In Paper 3 (ageing), this increase in $\tau$ is intrinsic and progressive.
- $\tau(age)$ will be modeled as a strictly increasing function beyond age ~50.
- $K_d(age)$ and actuator gain will decline.
- This creates a **terminal derivative gain gap** leading to instability (e.g., fall incidence).
