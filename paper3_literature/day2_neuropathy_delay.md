# Day 2: Peripheral Neuropathy and Nerve Conduction Velocity in Ageing

## Key Findings

1. **Age-related Decline in Nerve Conduction Velocity (NCV):**
   - Nerve conduction velocity transitions from pediatric to adult values by age 5, then remains relatively stable before starting to decline with age.
   - Studies consistently show an age-related decline in both sensory and motor nerve conduction velocities, with decreases becoming particularly significant after 40-60 years of age.
   - The decline in NCV is typically greater in sensory nerves compared to motor nerves, and in lower limbs compared to upper limbs.
   - One study found median sensory nerve conduction velocity decreases at a rate of roughly 0.14 m/s per year after age 40. Other reports suggest an overall decrease in conduction velocity of around 0.41 m/s per year of age, or a 10% reduction by age 60.

2. **Physiological Mechanisms:**
   - The decrease in conduction velocity is likely related to structural changes in peripheral nerves, such as segmental demyelination, axonal loss, and reduction in nerve fiber diameter.
   - The electrical stimulus threshold required to record nerve responses also increases significantly with age (e.g., from 15-25 mV in young adults to 40-50 mV in older age groups).
   - Decreased sensory NCV is associated with subjective complaints of pain and impaired motor function, while decreased motor NCV is associated with reduced fine motor skills (e.g., fingertip dexterity).

3. **Impact on Proprioceptive Delay ($\tau$):**
   - In the inverted pendulum PID model, $\tau$ represents the total neural processing delay, which includes afferent (sensory) nerve conduction, central processing, and efferent (motor) nerve conduction.
   - The observed reduction in NCV (especially sensory) directly translates to an increase in transmission time for both proprioceptive feedback and motor commands.
   - This progressive increase in the $\tau$ parameter in the PID controller model degrades the system's phase margin, making the control loop more susceptible to instability, especially when compensatory mechanisms (like derivative gain $K_d$) are also degrading.

## References

- Palve SS, Palve SB. "Impact of Aging on Nerve Conduction Velocities and Late Responses in Healthy Individuals." J Neurosci Rural Pract. 2018 Jan-Mar;9(1):112-116. DOI: 10.4103/jnrp.jnrp_323_17.
- Fukumoto Y, Wakisaka T, Misawa K, Hibi M, Suzuki T. "Decreased nerve conduction velocity may be a predictor of fingertip dexterity and subjective complaints." Exp Brain Res. 2023 Feb;241(2):661-675. DOI: 10.1007/s00221-023-06556-2.
- Ranganathan P. "A study on median nerve conduction velocity in different age groups." Academia.edu (Accessed 2025).
