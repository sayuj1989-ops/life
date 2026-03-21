# Day 1: Postural Control and Aging

## Overview
Age-related decline in postural control is driven by progressive degradation across multiple sensory and central integrator domains. This forms the biological basis for the terminal derivative gain gap model of postural instability.

## Key Domains of Decline

### 1. Proprioceptive Decline
Proprioception, particularly from the muscle spindles and joint mechanoreceptors in the lower extremities, is the primary sensory input for postural control.
* **Findings:** Ageing is associated with reduced muscle spindle density, impaired sensory afferent conduction, and an overall decrease in proprioceptive acuity. This is a critical driver for the increase in proprioceptive delay ($\tau$).
* **Evidence:** Sensory decline is a known factor impairing postural control. A systematic review assessing sensory perturbation effects via force-platform posturography confirms that age-related sensory decline impairs postural control in healthy older adults.
    * *Source:* Impact of sensory afferences in postural control quantified by force platform in healthy older adults: Systematic review and meta-analysis. (DOI: 10.1016/j.exger.2025.112976)

### 2. Vestibular Degeneration
The peripheral vestibular system provides the absolute reference for gravity and head acceleration, crucial for maintaining an upright posture.
* **Findings:** The vestibular system undergoes age-related structural and functional degeneration, including loss of hair cells in the maculae and ampullae.
* **Evidence:** Aging significantly impacts the vestibular system, as seen in disorders like benign paroxysmal positional vertigo (BPPV), which is a prevalent disorder affecting the peripheral vestibular system. Degeneration of this system is strongly linked with aging and leads to poor postural references.
    * *Source:* Research progress on risk factors of recurrence of benign paroxysmal positional vertigo. (DOI: 10.3389/fneur.2025.1735898)

### 3. Cerebellar Atrophy
The cerebellum is the primary integrator for sensory inputs and generates predictive models for postural control. It is vital for tuning the PID gains in the postural controller.
* **Findings:** The cerebellum is significantly affected by aging, with a marked loss of Purkinje cells and overall cerebellar volume reduction.
* **Evidence:** The cerebellum is fundamentally involved in motor control, gait, and posture. Damage or atrophy in the cerebellum, such as seen in various neurodegenerative disorders and typical aging, compromises balance and postural stability.
    * *Source:* Biomarkers of balance and gait deficits in FMR1 premutation carriers: a mini-review. (DOI: 10.3389/fnagi.2025.1637819) - highlights the connection between cerebellar/neurodegenerative disorders and gait/balance deficits.
    * *Source:* The neural underpinnings of cognitive and postural profile of a young adult with congenital cerebellar athrophy: a longitudinal case report. (DOI: 10.3389/fnins.2026.1724744) - outlines the cerebellum's chief involvement in motor control, gait, and posture.

## Synthesis for Paper 3 Model
The literature supports that aging induces a progressive degradation of the primary controller inputs (proprioception, vestibular) and the central integrator (cerebellum). In the control-theoretic model, this corresponds to a terminal degradation of controller parameters, fundamentally pacing the "terminal derivative gain gap".
