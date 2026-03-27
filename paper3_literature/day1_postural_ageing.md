# Ageing and Postural Control

## Overview
This document summarizes literature related to ageing and postural control, focusing on proprioceptive decline, vestibular degeneration, and cerebellar changes.

## Key Findings

1. **Age-Related Changes in Postural Control**
   * *Reference:* Michalska et al., "Age-Related Changes in Postural Control: transitional task", 2020. DOI: 10.21203/rs.3.rs-42683/v1
   * *Summary:* The study identified age-related postural changes during transitional tasks. It found that double-support time and transit time increase significantly with age, particularly in those over 70 years old. These parameters indicate early signs of balance changes and postural control degradation in middle-aged and older adults.

2. **Proprioceptive and Sensorimotor Changes**
   * *Reference:* Henry & Baudry, "Age-related changes in leg proprioception: implications for postural control", 2019. DOI: 10.1152/jn.00067.2019
   * *Summary:* There are age-related changes in leg proprioception that modify the neural control of upright standing. This indicates that proprioceptive acuity and sensorimotor integration are impacted by age, directly affecting postural stability.
   * *Relevance to Model:* This supports the degradation of the $K_p$ and $K_d$ gains, and specifically the increase in proprioceptive delay ($\tau$) in the PID model.

3. **Vestibular Degeneration and Balance**
   * *Reference:* "Age-Related Vestibular Dysfunction; Vestibulo-Ocular Reflex, Dynamic Visual Acuity, Dizziness and Falls: A Review", 2021. DOI: 10.31707/vdr2021.7.4.p279
   * *Summary:* Age-related loss of vestibular functions can occur even without specific vestibular pathologies. This contributes significantly to balance issues and fall risk in the elderly. Vestibular rehabilitation, such as gaze stability exercises, can improve postural stability.
   * *Relevance to Model:* The vestibular system provides critical state estimation for postural control. Its degradation implies that the control system relies more heavily on delayed proprioceptive feedback, exacerbating the derivative gain gap.

4. **Cerebellar Atrophy and Postural Instability**
   * *Reference:* Mauritz, Schmitt, & Dichgans, "DELAYED AND ENHANCED LONG LATENCY REFLEXES AS THE POSSIBLE CAUSE OF POSTURAL TREMOR IN LATE CEREBELLAR ATROPHY", Brain (1981). DOI: 10.1093/brain/104.1.97
   * *Summary:* Late cerebellar atrophy is associated with delayed and enhanced long latency reflexes, which can cause postural tremor and instability.
   * *Relevance to Model:* The cerebellum acts as a predictive controller. Its atrophy correlates directly with an inability to compensate for sensory delays, meaning the effective proprioceptive delay ($\tau$) experienced by the controller increases, leading to instability (the "Terminal Derivative Gain Gap").
