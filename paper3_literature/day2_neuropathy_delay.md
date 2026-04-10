# Literature Review: Peripheral Neuropathy and Nerve Conduction Velocity in Ageing

## Key Findings: Age-Related Decline in Nerve Conduction Velocity (NCV)
Nerve conduction velocity declines progressively with age. The physiological changes underlying this include the loss of both myelinated and unmyelinated nerve fibers, reduction in fiber diameter, and alterations in myelin sheath integrity.

*   **Rate of Decline**: Studies indicate that sensory and motor nerve conduction velocities decrease with age. For example, some studies report sensory velocities decreasing at a rate of 0.14 to 0.41 m/s per year of age (Werner et al., Awang et al.). A general estimation is approximately a 10% reduction in conduction rate by age 60 (Falco et al.).
*   **Sensory vs. Motor**: The age-related decline is often more pronounced in sensory nerve conduction than in motor nerves, and late responses (such as F-waves and H-reflexes) show delayed latencies.
*   **Impact on Proprioceptive Delay ($\tau$)**: As nerve conduction velocity decreases, the time taken for proprioceptive signals from the periphery (e.g., muscle spindles in the lower limbs) to reach the central nervous system (CNS), and for motor commands to return, increases. This directly contributes to an increase in the total loop delay, $\tau$, in the postural control system.

## Sources
*   *Impact of Aging on Nerve Conduction Velocities and Late Responses in Healthy Individuals* (PMCID: PMC5812134)
*   *Cross Sectional Study on the Effect of Aging on Peripheral Nerve Conduction Velocity* (IJCPR, Vol 17)

## Relevance to Terminal Derivative Gain Gap Model
In our inverted pendulum PID model of postural control, the derivative gain $K_d$ provides anticipatory correction based on velocity. The effectiveness of this derivative control is highly sensitive to the loop delay $\tau$. The progressive, irreversible decline in nerve conduction velocity with age provides a physiological basis for a monotonic increase in $\tau(age)$. This increasing delay will eventually cause the critical stability margin to be breached, leading to the "terminal derivative gain gap" where the postural control system can no longer maintain stable upright stance, resulting in falls.
