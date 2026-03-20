# Paper 3 Progress Tracker

## Session: 2026-03-20

**Phase/Day Completed:** Phase 1, Day 1 (Literature Review on Ageing and Postural Control)

**Key Findings:**
*   Sensory systems (proprioception, vestibular, visual) progressively degrade with age, particularly in challenging conditions, supporting a progressive decline in $K_d$ and $K_p$.
*   There's a shift towards reliance on closed-loop control in older adults with hyperkyphosis, coupled with increased response delays, which maps perfectly to the $\tau$ term in the PID model.
*   Actuator mechanics (e.g., soleus muscle tendon stiffness and torque rate) decline with age, supporting a reduction in the "actuator gain" term.
*   Cerebellar/cognitive function decline correlates with poorer postural control.
*   Interventions (like composite plantar sensory exercise) can improve sensory feedback and static stability, suggesting the terminal decline is somewhat modifiable.

**Issues/Open Questions for Dr. Sayuj:**
*   **PID Parameterisation:** We see literature pointing to a decline in $K_d, K_p$, increase in $\tau$, and decrease in actuator gain. Are there specific baseline parameter values for young vs. old (e.g., from Peterka 2002) you'd prefer to start anchoring the simulation against before we introduce the telomere clock?
*   **Hyperkyphosis:** Should we explicitly model the structural plant change (shift in the center of mass due to hyperkyphosis) in addition to the sensory/actuator decay, or keep the pendulum mass constant and focus purely on the feedback degradation?

**Next Session Plan:**
*   Phase 1, Day 2: Search for papers on peripheral neuropathy and nerve conduction velocity changes with age. Focus on quantifying how the delay parameter ($\tau$) increases with age.