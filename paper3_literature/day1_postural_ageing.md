# Day 1 Literature Review: Ageing and Postural Control

This document summarizes key literature on the progressive degradation of the postural control system in ageing, focusing on proprioceptive decline, vestibular degeneration, and cerebellar changes. This forms the foundation for the "terminal derivative gain gap" hypothesis.

## Key Findings from Recent Literature

### 1. Multisensory Degradation and Age-Related Vulnerability
**Reference:** Akbari Kamrani AA, et al. "Effects of age, sex, and sensory information on balance performance in young and older adults." (DOI: 10.3389/fragi.2026.1761492)
*   **Summary:** Balance performance systematically declines with age and as sensory conditions become more challenging. Older adults (especially >75 years) are significantly more impaired when accurate sensory information (visual, proprioceptive, vestibular) is reduced or altered. This supports a multi-modal degradation of the feedback controller (the sensory pathways).

### 2. Shift from Open-Loop to Closed-Loop Control with Structural Changes
**Reference:** Hosseinabadi M, et al. "Effect of age-related hyperkyphosis on open and closed-loop postural control in older adults." (DOI: 10.1038/s41598-025-12002-w)
*   **Summary:** Age-related hyperkyphosis (altering body alignment) impairs open-loop control and increases reliance on closed-loop mechanisms. Crucially, it potentially *delays responses* and increases fall risk, directly supporting the concept of an increasing delay $\tau$ and an altered plant in the geriatric PID model.

### 3. Decline in Vestibular and Visual Integration
**Reference:** He Y, et al. "Posture control characteristics of different age groups in China based on Bertec® balance advantage CDP/IVR-a cross-sectional study." (DOI: 10.3389/fneur.2025.1658938)
*   **Summary:** Individuals over 45 years exhibit a diminished capacity to integrate visual and vestibular information for complex balance tasks. There are significant age-related declines in Vestibular and Visual scores on the Sensory Organization Test, indicating degradation of key sensory inputs for the postural controller.

### 4. Neuromechanics of the Actuator (Sarcopenia / Plant Degradation)
**Reference:** Fletcher JR, Strzalkowski NDJ. "The neuromechanics of the soleus for fall prevention in aging." (DOI: 10.3389/fphys.2025.1743559)
*   **Summary:** The soleus muscle provides sustained torque for balance. Aging reduces tendon stiffness and the rate of torque development, compromising the "actuator" in our model. Furthermore, age-related mechanical and neural deterioration leads to delayed, less adaptable reflex responses—explicitly linking aging to increased delay $\tau$ and decreased actuator gain.

### 5. Influence of Cognitive/Cerebellar Function
**Reference:** Pereira C, et al. "Influence of cognitive function on postural control in physically independent older women: a time and time-frequency domain analysis." (DOI: 10.1186/s12877-026-06982-1)
*   **Summary:** Cognitive status influences postural control; poorer cognitive performance correlates with poorer balance. Time-frequency parameters associated with cerebellar modulation (medium frequency) and proprioceptive contribution (high frequency) are implicated in more challenging conditions, hinting at central processing degradation.

### 6. Intervention Potential (Sensory Feedback)
**Reference:** Hu X, et al. "Effects of an eight-week composite plantar sensory exercise on postural stability in older adults: a randomised controlled trial." (DOI: 10.1016/j.jesf.2026.200451)
*   **Summary:** Composite plantar sensory exercise improves sensory feedback and static postural stability in healthy older adults, especially under challenging visual/surface conditions. This suggests that the decline in proprioceptive gain ($K_d, K_p$) or the increase in $\tau$ might be partially reversible or compensable through targeted training.

## Synthesis for the Model
*   **Proprioceptive/Sensory Degradation:** The literature confirms a progressive decline in the quality and speed of sensory feedback (vestibular, visual, proprioceptive). This maps to a decrease in sensory precision and an increase in the feedback delay $\tau$.
*   **Actuator Degradation:** Reductions in muscle force development and tendon stiffness (e.g., in the soleus) clearly support a declining actuator gain term in the PID model.
*   **Structural Changes:** Hyperkyphosis changes the mechanical properties of the plant (the inverted pendulum), which combined with delayed closed-loop control, exacerbates instability.
*   **Central Processing:** The cerebellum and cognitive networks, responsible for integrating these signals, also show functional decline, further increasing the total loop delay $\tau$ and reducing predictive capacity.