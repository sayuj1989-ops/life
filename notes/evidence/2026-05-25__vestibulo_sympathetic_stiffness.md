# Evidence Note: Vestibulo-Sympathetic Stiffness Control

**Date:** 2026-05-25
**Topic:** Gravity, Vestibular System, and Bone Stiffness
**Reference:** Vignaux, G. et al. (2013). "Evidence of vestibular system involvement in bone mass regulation: The effect of vestibular lesion on bone remodeling in rats". *Bone*, 56(2), 265-272.

## Claim
The gravitational field is not merely a passive load but an active regulator of skeletal stiffness via a specific neurological reflex: the **Vestibulo-Sympathetic Reflex**. The vestibular system (specifically the otoliths) detects the gravity vector and modulates sympathetic outflow to bone tissue, setting the "gain" of skeletal stiffness (bone mass and mineral density) via $\beta_2$-adrenergic receptors.

## Mechanism
1.  **Sensor:** Otolith organs (utricle/saccule) detect gravitational acceleration.
2.  **Controller:** Vestibular nuclei project to the sympathetic nervous system (SNS).
3.  **Effector:** Sympathetic nerves release norepinephrine onto osteoblasts.
4.  **Action:** Activation of $\beta_2$-adrenergic receptors on osteoblasts regulates RANKL/OPG expression, modulating osteoclast activity and bone formation.
5.  **Outcome:** In 1g, this tone maintains high stiffness. In microgravity (or after vestibular lesion), this tone is disrupted, leading to rapid "unloading" osteopenia—which is actually a "neurogenic" osteopenia.

## Relevance to Counter-Curvature
This mechanism provides the biological implementation of the **Stiffness Gain ($K_g$)** parameter in our Information-Elasticity Coupling (IEC) model.
*   **Microgravity:** The loss of gravity input reduces the "prior" for stiffness. The system minimizes free energy by reducing structure (bone mass) to match the expected low-load environment, but this is mediated *anticipatorily* by the vestibular system, not just by local strain.
*   **Scoliosis:** If the vestibular input is asymmetric (e.g., otolith asymmetry or central integration defect), the sympathetic tone will be asymmetric. This leads to **Asymmetric Stiffness Gain**, where one side of the vertebrae becomes softer (osteopenic) than the other, facilitating the "buckling" or rotation observed in scoliosis (Wolff's Law driven by neural error).

## Open Question & Proposed Test
**Question:** Is the scoliotic curve initiation driven by a vestibular-induced sympathetic asymmetry?
**Proposed Test:** Perform unilateral vestibular lesions in mice and measure:
1.  Vertebral curvature (Micro-CT).
2.  Sympathetic nerve density in paraspinal tissues.
3.  Bone mineral density (BMD) asymmetry.
**Intervention:** Can unilateral systemic $\beta$-blockade (or local sympathectomy) induce or rescue curvature?

## Integration
This connects **Hypothesis H_2026_02_05_Gain_Hysteresis** (gain control) to **Hypothesis H_2025_02_20_Active_Inference** (gravity as prior).
