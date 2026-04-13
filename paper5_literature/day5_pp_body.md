# Phase 1, Day 5: Predictive Processing and body representation

## Core Concepts
Predictive Processing (PP) provides a unified account of perception, action, and interoception/proprioception.
- **Proprioception & Body Schema:** The brain maintains a dynamic, probabilistic model of the body's state (posture, kinematics). This model is updated by proprioceptive prediction errors (from muscle spindles, Golgi tendon organs, joint receptors).
- **Interoception:** Similar to exteroception and proprioception, the brain predicts the internal state of the body (visceral, autonomic).
- **Precision Weighting:** A crucial mechanism in PP. The brain dynamically adjusts the "precision" (inverse variance or confidence) of sensory signals versus top-down predictions.
    - High precision on sensory input: The model updates rapidly based on new data.
    - Low precision on sensory input (high precision on predictions): The system relies on its prior expectations, effectively ignoring sensory evidence.

## Sensory Attenuation and Action
To initiate movement in the active inference framework, the brain must temporarily *attenuate* (down-weight the precision of) the current proprioceptive evidence. If it didn't, the discrepancy between the current static position and the predicted moving position would cause the model to update its belief to match the current static position, preventing movement.
- **The "Tickle" Paradigm:** We can't tickle ourselves because the motor command generates a precise forward prediction of the sensory consequence (efference copy). The resulting sensory input perfectly matches the prediction, so the prediction error is zero. Furthermore, the precision of that sensory channel is preemptively attenuated during the self-generated action.

## Relevance to Adolescent Idiopathic Scoliosis (AIS)
1. **The Growth Spurt as Model Misspecification:** During rapid adolescent growth, the physical dimensions and inertial properties of the body change drastically. The brain's generative model of the body (body schema) becomes outdated.
2. **Precision Weighting in Postural Control:** Postural control relies on high-precision proprioceptive feedback to detect small deviations from upright.
3. **The Derivative Gain Gap via PP:** When the body grows faster than the model can update, proprioceptive predictions about movement (velocity) become systematically wrong. The brain detects this increased prediction error variance and *optimally* down-weights the precision of those signals ($\Pi_{y,1} \downarrow$).
4. **Clinical Implications (Testable Predictions):**
    - If AIS involves a transient drop in proprioceptive precision ($\Pi_{y,1}$), these patients should exhibit generalized alterations in sensory attenuation during the growth spurt.
    - They might show altered responses in force-matching tasks or the self-tickling paradigm compared to age-matched controls, specifically reflecting reduced precision on proprioceptive/kinesthetic prediction errors.
