# Polygenic Threshold and Regional Morphology: Extending the Allometric Trap

The Biological Countercurvature framework defines the fundamental "Allometric Trap" ($L^4$ metabolic cost scaling vs $L^2$ supply) as a universal thermodynamic constraint on bipedal growth. However, this raises two critical questions:
1. If the trap is universal, why is the clinical prevalence of Adolescent Idiopathic Scoliosis (AIS) only 2–4%?
2. If the initial model treats the spine as a single inverted pendulum, how does the framework explain the highly specific, regional deformity patterns known as Lenke curve types (1–6)?

This document synthesizes the computational and theoretical extensions of the model that directly address these points, moving from the onset of global instability to the patterning of regional deformity.

---

## 1. The Polygenic Threshold: Stacking Parameters Across the Bifurcation Boundary

The allometric trap creates a **universal vulnerability window** — every adolescent passes through it during the growth spurt. But passing through the window doesn't guarantee instability. Think of it as a necessary-but-not-sufficient condition.

In the baseline scenario, a "generic" adolescent with population-mean parameters stays just above the Hopf bifurcation threshold. The model demonstrates a narrow stability margin of **+5.3 ms**. They traverse the danger zone and come out the other side intact.

What pushes an individual *across* the boundary is the **individual-specific stacking of molecular parameters**:

- **Reduced damping $b$:** (e.g., COL1A1/COL2A1 flexibility variants). A 29% reduction in damping directly lowers the critical delay $\tau_{\text{crit}}$.
- **Increased proprioceptive delay $\tau$:** (e.g., PIEZO2/GPR126/MTNR1B variants). Effective delay increases from baseline 70.0 ms to 96.4 ms.
- **Shifted structural demand $K_d$:** (e.g., LBX1 variant). Shifts $K_d = 12.96$, approaching the critical threshold of 12.6.
- **Increased gravitational load $mgL$:** (e.g., PAX1 variant). Increases to 93.7 vs 73.6 baseline.

Each variant alone narrows the margin; the **combined scenario** flips the margin entirely, sending it from $+5.3$ ms to **$-26.3$ ms**.

### Computational Verification
This stacking dynamic is explicitly computationally verifiable (see `scripts/experiment_polygenic_stacking.py`). The 2–4% prevalence reflects the fraction of the population whose specific genetic combination pushes enough parameters simultaneously past the threshold. This is entirely consistent with the **polygenic threshold model** — AIS has dozens of identified risk loci (LBX1, PAX1, GPR126 etc.), each with small effect sizes. Only when enough co-occur does the system destabilize.

The framework quantitatively predicts the low prevalence: the 5.3 ms baseline margin is narrow enough that modest multi-gene perturbations breach it, but wide enough that most individuals don't. The 8:1 female predominance follows because estrogen shifts the distribution — lowering damping via collagen cross-linking and steepening the growth trajectory — so a larger fraction of females land in the unstable zone.

**Conclusion:** Everyone enters the trap. Most escape. The 2–4% are those whose molecular parameters conspire to close the exit.

---

## 2. Explaining Lenke Curve Types: The Multi-Segment Cosserat Rod Prediction

This is where the framework hits a current **limitation that is also a prediction**.

The foundational DDE model is a **single-link inverted pendulum** — it captures the *onset* of instability (the moment the system crosses the Hopf bifurcation boundary) but treats the spine as a single unit. It tells us *when* and *why* scoliosis initiates, but not *where* on the spine or *what shape* the curve takes.

Different Lenke types (1–6) are defined by curve location (main thoracic, thoracolumbar, lumbar) and structural modifier (sagittal thoracic, lumbar side-bending). To explain these, the framework must be extended to a **multi-segment Cosserat rod** where:

- **Regional variation in stiffness $EI$:** Thoracic kyphosis vs lumbar lordosis; explicitly accounting for the rib cage buttressing effect.
- **Segmental differences in proprioceptive delay $\tau$:** Different mechanoreceptor density at T5-T12 vs L1-L5.
- **Local damping $b$ variations:** Disc composition, facet joint orientation, and paraspinal muscle bulk differ by level.
- **Asymmetric loading:** Cardiac offset, aortic pulsation, and handedness.

These regional parameter differences would determine which vertebral segments destabilize *first* once the global Hopf threshold is breached, and the resulting curve morphology would emerge as the dominant eigenmode of the multi-segment system. A Type 1 (main thoracic) might reflect destabilization at the segment with minimum rib cage stiffening, while a Type 5 (thoracolumbar) might reflect the transition zone where both thoracic and lumbar parameter sets converge unfavorably.

**The important point:** The framework doesn't contradict Lenke patterns — it provides the *upstream trigger* (global instability onset), and the multi-segment extension would provide the *downstream patterning* (which segments buckle and in what configuration). This is a natural next step that the Predictions section already gestures toward.
