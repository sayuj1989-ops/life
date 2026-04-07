# Day 2: Peripheral Neuropathy and Nerve Conduction Velocity in Ageing

## Summary of Findings

1. **Nerve Conduction Velocity (NCV) Declines with Age**:
   - Both motor and sensory NCV decrease with advancing age in healthy humans. The change is often reported to become clinically significant beyond the age of 60.
   - For example, motor nerve conduction velocity in healthy adults is around 50–60 m/s depending on the limb, but can decrease with age due to myelin breakdown, reduced axon diameter, and increased internodal distance.
   - A study by Stetson et al. (1992) demonstrated that sensory nerve action potential (SNAP) amplitudes and NCV decrease predictably with age.
   - **Quantifying the Delay (\tau)**: While exact formulas differ, a common rule of thumb is a decrease of about 1-2 m/s per decade after age 20-30. Over 4 decades (age 30 to 70), this translates to an approximate 10% reduction in conduction speed, proportionately increasing the pure neural conduction delay time.

2. **Structural Causes**:
   - **Demyelination and Axonal Loss**: Ageing is associated with structural changes in peripheral nerves, including segmental demyelination, remyelination, and a loss of large myelinated fibers.
   - **Oxidative Stress & Myelin**: Studies in mice (e.g., PMC4612382) show oxidative stress, altered myelin protein, and lipid composition contribute to age-related NCV decline.

3. **Link to Posture and "Proprioceptive Delay"**:
   - In control-theoretic models of posture (like the delayed PID inverted pendulum), the total time delay (\tau) includes neural transmission, cognitive processing, and muscle activation.
   - Normal adult \tau is roughly 150-170 ms. In the elderly, especially those with peripheral neuropathy, \tau can exceed 200 ms. Peripheral nerve slowing directly contributes to this \tau expansion, fundamentally degrading the derivative gain (rate sensing).

## Key References

- Stetson, D. S., et al. (1992). Effects of age, sex, and anthropometric factors on nerve conduction measures. *Muscle & Nerve*. DOI: 10.1002/mus.880151007
- Taylor & Francis Knowledge Centers on Nerve Conduction Velocity. Shows that normal motor conduction velocity is >50 m/s (upper limbs) and >40 m/s (lower limbs), but declines with age, increasing the temporal delay of sensory-motor feedback.
- PMC5812134: Impact of Aging on Nerve Conduction Velocities and Late Responses in Healthy Individuals. Concludes older patients have longer latencies, smaller amplitudes, and slower conduction velocities.
- PMC4612382: Use of Nerve Conduction Velocity to Assess Peripheral Nerve Health in Aging Mice.
