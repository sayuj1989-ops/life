# Literature Review: Day 1 - Postural Ageing

## Overview
Ageing is characterized by a multi-system decline that progressively impairs bipedal postural control, increasing the risk of falls—a leading cause of morbidity and mortality in the elderly. In the context of the "Terminal Derivative Gain Gap" hypothesis, this deterioration is viewed as a systemic failure of the biological PID controller maintaining upright posture. Specifically, both the rate-sensing derivative component ($K_d$) and the predictive controller models (cerebellum) undergo irreversible degradation.

## 1. Proprioceptive Decline
Proprioception, defined as the body's ability to sense position, movement, and force in space, relies on mechanoreceptors (e.g., muscle spindles, Golgi tendon organs) transmitting feedback to the Central Nervous System (CNS).
* **Mechanisms of Decline:** Age-related decline is primarily attributed to reduced muscle spindle sensitivity, axonal atrophy, and neurochemical changes in the brain [1].
* **Impact on Postural Control:** Older adults often experience deficits in muscle activation perception, which leads to discrepancies between intended and actual muscle engagement. This alters the relative proprioceptive weighting used in postural control, with elderly individuals (especially those with low back pain) demonstrating a decreased reliance on specific proprioceptive signals (like those from the gastrocnemius) during balance tasks [2].
* *Relevance to Model:* The reduction in proprioceptive fidelity and speed directly contributes to an increased time delay ($\tau$) and a degraded derivative gain ($K_d$), expanding the "gain gap" as the controller fails to track body dynamics in real-time.

## 2. Vestibular Degeneration
The vestibular system, crucial for sensing head motion and gravity, also deteriorates with age (presbyvestibulopathy).
* **Mechanisms:** This involves a gradual decline of the inner ear structures or the vestibular nerve, often compounded by cerebrovascular disease or chronic conditions. As the system weakens, the brain receives less accurate information about motion and spatial orientation.
* **Impact on Postural Control:** Elderly patients with vestibular degeneration frequently experience chronic imbalance, vertigo, and visual disturbances during movement. The condition forces an over-reliance on visual and somatosensory inputs, which may themselves be impaired [3].
* *Relevance to Model:* Loss of vestibular fidelity further corrupts the sensory integration needed for the predictive feedforward control of the inverted pendulum plant.

## 3. Cerebellar Atrophy
The cerebellum acts as the primary integrator for postural prediction and the coordination of voluntary movements. It functions as a feedback control system, creating a comprehensive representation of body position by integrating multisensory inputs [4].
* **Mechanisms:** Ageing is associated with structural changes in the cerebellum, notably Purkinje cell loss and cerebellar atrophy.
* **Impact on Postural Control:** Reduced cerebellar volume and connectivity impair the ability to quickly adapt postural responses to internal and external perturbations. Interventions like cerebellar theta-burst stimulation have shown potential in enhancing balance control in older adults [5], highlighting the cerebellum's central role in the age-related postural decline.
* *Relevance to Model:* Cerebellar degradation represents the failure of the predictive, feedforward controller that typically compensates for the sensorimotor delay ($\tau$).

## References & Sources
1. Kanekar N., Aruin A.S. (2014) The effect of aging on anticipatory postural control. *Exp. Brain Res.* 232:1127–1136. doi: 10.1007/s00221-014-3822-3.
2. Wang et al. (2017) Proprioceptive change impairs balance control in older patients with low back pain. *J Phys Ther Sci.* 29(10):1858-1861. doi: 10.1589/jpts.29.1858.
3. Clinical Overviews on Presbyvestibulopathy (e.g., Dr.Oracle, Vitality Physiotherapy resources). *[Note: Specific primary literature needed for exact vestibular cellular degradation metrics.]*
4. Age-Related Dysfunction in Balance: A Comprehensive Review of Causes, Consequences, and Interventions. *Aging and Disease* (2024). doi: 10.14336/AD.2024.0124-1
5. Enhancing Balance Control in Aging Through Cerebellar Theta-Burst Stimulation. *[PMC12507971]*
