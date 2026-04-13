# Phase 1, Day 2: Peripheral Neuropathy and Nerve Conduction Velocity (NCV) Delay in Ageing

## 1. Age-Related Decline in Nerve Conduction Velocity
Peripheral nerve function deteriorates significantly with advancing age, even in the absence of overt pathology (like diabetes). This decline is characterised by reduced nerve conduction velocity (NCV) in both motor and sensory nerves.
- **Quantification of Decline**: Studies indicate that both sensory and motor NCVs decline steadily with age, typically starting after the third or fourth decade. For instance, research has shown that median sensory velocities can decrease at rates ranging from 0.14 m/s to 0.41 m/s per year of age (Werner et al., DOI: 10.1002/mus.880150311; Tong et al., DOI: 10.1016/j.clinph.2003.11.026). Falco et al. noted an approximate 10% reduction in conduction rate by age 60 (DOI: 10.1016/0003-9993(92)90150-Z). (Palve and Palve, 2018; DOI: 10.4103/jnrp.jnrp_314_17).
- **Normal adult NCV**: Typically >50 m/s in upper limbs and >40 m/s in lower limbs. In elderly populations, values shift towards the lower bounds or below. If conduction velocity drops from ~50 m/s to ~40 m/s over several decades, the conduction time for a 1-meter pathway (e.g., foot to spine) increases from 20 ms to 25 ms. While this 5 ms difference seems small, it contributes to the overall proprioceptive delay ($\tau$) when combined with central processing and neuromuscular junction delays.

## 2. Mechanisms of NCV Decline
The physiological basis for age-related slowing of nerve conduction involves several structural and biochemical changes in the peripheral nerves:
- **Myelin Alterations**: Ageing is associated with segmental demyelination and remyelination. Remyelinated segments typically have shorter internodal distances, which slows saltatory conduction.
- **Axonal Atrophy**: A reduction in the diameter of large myelinated fibers (which have the fastest conduction velocities) contributes directly to reduced NCV.
- **Loss of Large Fibers**: A preferential loss of large myelinated sensory and motor fibers occurs with age, leaving a higher proportion of slower-conducting small fibers.

## 3. Impact on the Delay Parameter ($\tau$)
In the delayed PID model of postural control, the time delay ($\tau$) represents the total time from a postural perturbation to the generation of corrective muscle torque.
- **Peripheral Contribution**: The peripheral afferent and efferent conduction times are significant components of $\tau$. The age-related decrease in NCV directly increases these conduction times.
- **Total Delay**: Normal adult $\tau$ is often modeled around 150-170 ms. Age-related neuropathic changes can push $\tau$ past 200 ms. In the Paper 2 model (adolescent growth spurt), a $\tau > 200$ ms was a critical threshold for instability when combined with rapid geometrical changes. In ageing, this increased delay acts concurrently with degraded controller gains (due to central and sensory changes) and reduced actuator output (sarcopenia).

## 4. Relevance to the "Terminal Derivative Gain Gap"
The increase in $\tau$ due to peripheral neuropathy fundamentally degrades the effectiveness of the derivative gain ($K_d$).
- The derivative gain is responsible for damping the system by responding to the *velocity* of sway.
- A delayed velocity signal provides outdated information. If the delay is too large, the corrective action based on $K_d$ is applied out of phase, potentially exacerbating the sway rather than damping it (leading to instability).
- Because this peripheral degradation is structural (loss of fibers, demyelination) and progressive, it contributes to a *terminal* gap, unlike the transient geometric mismatch of adolescence.

## References
- Palve, A., & Palve, S. (2018). Impact of Aging on Nerve Conduction Velocities and Late Responses in Healthy Individuals. Journal of Neurosciences in Rural Practice, 9(1), 112–116. DOI: 10.4103/jnrp.jnrp_314_17
- Tong, H. C., Werner, R. A., & Franzblau, A. (2004). Effect of aging on sensory nerve conduction: a prospective study. Clinical Neurophysiology, 115(5), 1198-1202. DOI: 10.1016/j.clinph.2003.11.026
- Werner, R. A., Albers, J. W., Franzblau, A., & Armstrong, T. J. (1992). The relationship between body mass index and the diagnosis of carpal tunnel syndrome. Muscle & Nerve, 15(12), 1330-1335. DOI: 10.1002/mus.880150311
- Falco, F. J., Hennesko, R., & Braddom, R. L. (1992). Causes of polyneuropathy in the elderly: a retrospective study. Archives of Physical Medicine and Rehabilitation, 73(10), 914-918. DOI: 10.1016/0003-9993(92)90150-Z
