# Phase 2, Day 9: Free-energy and pathology

## Computational Psychiatry and FEP
The Free-Energy Principle has been extensively applied to model pathology, particularly in psychiatry ("Computational Psychiatry"). These models almost exclusively focus on aberrant precision-weighting as the core mechanism of disease.

- **Schizophrenia:** Modeled as a failure to attenuate sensory precision (or overly precise sensory prediction errors), leading to hallucinations (predictions dominating perception) and delusions (aberrant belief updating to explain away persistent prediction errors).
- **Autism:** Modeled as an excessively high precision weighting on sensory prediction errors (HIPPEa: High, Inflexible Precision of Prediction Errors in Autism). The system cannot generalize well because it overfits to noisy sensory details, treating everything as surprising.
- **Chronic Pain / Functional Neurological Disorders:** Modeled as overly precise priors for symptoms (e.g., pain, paralysis). The top-down predictions of pain are so strong that sensory evidence to the contrary is ignored (attenuated).

## AIS as a Transient "Computational Orthopaedics" Pathology
We are translating the logic of Computational Psychiatry into "Computational Orthopaedics."
- Unlike schizophrenia or autism, which are typically modeled as persistent trait-level differences in precision-weighting architectures, Adolescent Idiopathic Scoliosis (AIS) in our model is a *transient, state-level* pathology.
- **The Trigger:** The precision collapse in AIS is triggered externally by the physical body (the plant) changing faster than the biological learning rate. It is a perfectly *rational* (Bayes-optimal) response by the nervous system to an unreliable plant, not an intrinsic hardware defect in the brain's precision-weighting circuitry itself.
- **The Entrapment:** The transient drop in precision ($\Pi_{y,1}$) creates a temporary period of instability (the Derivative Gain Gap). The tragedy of AIS is that during this transient window, the system falls into a new local free-energy minimum (the curved posture). Once growth stabilizes, the system updates its prior to expect this new curvature. The transient functional problem thus crystallizes into a permanent structural reality.

## Comparison Table: Aberrant Precision
| Condition | Primary Defect | FEP Interpretation |
| :--- | :--- | :--- |
| Schizophrenia | Aberrant attribution of salience | Failure to attenuate sensory precision |
| Autism | Over-sensitivity, rigid priors | Excessively high sensory precision |
| **AIS (Our Model)** | **Postural instability during growth** | **Transient collapse of proprioceptive velocity precision ($\Pi_{y,1} \downarrow$)** |
