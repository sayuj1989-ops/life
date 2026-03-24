# Phase 1, Day 1: Ageing and Postural Control

This document summarises key real literature found regarding the decline of postural control systems (proprioception, vestibular function, and cerebellar processing) with age, setting up the foundation for the "Terminal Derivative Gain Gap" model.

## 1. Proprioceptive Decline
The ageing process impacts the neuromuscular system and alters muscle spindles and their neural pathways, resulting in less precise and controlled muscle movement, directly affecting proprioception and the control of posture.

* **Key paper:** Age-related changes in leg proprioception: implications for postural control.
  * **DOI:** 10.1152/jn.00067.2019
  * **Finding:** Aging is associated with alterations of muscle spindles and their neural pathways, which induce a decrease in the sensitivity, acuity, and integration of the proprioceptive signal from leg muscles. These alterations reduce the efficiency of postural control and promote deleterious consequences for functional independence.
* **Key paper:** Elderly Use Proprioception Rather than Visual and Vestibular Cues for Postural Motor Control
  * **DOI:** 10.3389/fnagi.2015.00097
  * **Finding:** Although sensory systems decline, including a reduced joint position sense, elderly individuals often heavily rely on the remaining proprioceptive cues, making the degradation of this system critically impactful on overall postural stiffness and damping (which correspond to K_p and K_d in the model).

## 2. Vestibular Degeneration
Vestibular function, a crucial input for the predictive postural controller, degrades with age, often interactively with other sensory systems like hearing.

* **Key paper:** Postural Control in Adults With Age-Related Hearing Loss.
  * **DOI:** 10.1044/2024_JSLHR-24-00487
  * **Finding:** Investigates concomitant dysfunction of the auditory, vestibular, and postural control systems in aging, showing that age-related decline often involves the vestibular system (measured via vHIT and VEMPs), leading to altered postural control.
* **Key paper:** Age-related hearing loss and balance disorders: analysis of interactions and clinical implications in older persons. Systematic review and meta-analysis.
  * **DOI:** 10.3389/fragi.2023.1310185
  * **Finding:** Associates age-related hearing loss with vestibular/gait dysfunction in older persons, reinforcing that sensory deficits rarely occur in isolation and collectively compound balance disorders.

## 3. Cerebellar Atrophy
The cerebellum acts as the primary integrator for postural prediction. Age-related structural and functional changes in the cerebellum contribute significantly to poor balance and increased fall risk.

* **Key paper:** Enhancing Balance Control in Aging Through Cerebellar Theta-Burst Stimulation.
  * **DOI:** 10.1007/s12311-025-01915-x
  * **Finding:** Confirms that the cerebellum undergoes significant age-related changes that are directly linked to poor balance in older adults. Reducing cerebellar deficits (via stimulation) acutely reduces postural sway, underscoring its causal role in the controller's degradation.
* **Key paper:** Cerebellum and Aging: Update and Challenges
  * **DOI:** 10.14336/AD.2024.0220
  * **Finding:** Highlights that the cerebellum ages more rapidly than other brain regions. With the aging of the cerebellum, there is a decline in balance and motor function, particularly fine motor skills, directly translating to an increased risk of falling.

## Synthesis for Paper 3 Thesis
The initial literature search strongly supports the concept of a terminal derivative gain gap. Ageing causes simultaneous and irreversible degradation across multiple components of the postural control system:
1.  **Sensor Degradation:** Proprioceptive acuity (muscle spindles) and vestibular precision decline.
2.  **Controller Atrophy:** The cerebellum, responsible for integrating these signals and generating predictive motor commands, ages rapidly and loses functional connectivity.
3.  **Actuator Inefficiency:** Muscle recruitment and joint position sense become less efficient.
Unlike the transient gap in adolescence (Paper 2), these structural and functional declines present a permanent and progressive challenge to the maintenance of upright bipedal posture, culminating in structural failure (falls or hyperkyphosis).
