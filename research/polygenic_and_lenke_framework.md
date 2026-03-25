# Polygenic Stacking and Multi-Segment Cosserat Extension

## The Allometric Trap & Polygenic Stacking (Why 2-4% Prevalence?)

The Metabolic Buckling framework establishes that human adolescents enter a uniquely vulnerable "Allometric Trap" ($Bg \approx 0.01$) during peak height velocity (PHV). However, passing through this window is a necessary but not sufficient condition for developing Adolescent Idiopathic Scoliosis (AIS). At baseline, a "generic" adolescent with population-mean parameters maintains a stability margin of **+5.3 ms**, staying just above the Hopf bifurcation threshold.

What pushes the 2-4% of the population *across* the boundary is the **individual-specific stacking of molecular parameters**, consistent with a polygenic threshold model. Identified risk loci (such as LBX1, PAX1, GPR126) individually exert small effect sizes, but when stacked, they conspire to close the exit from the Allometric Trap.

Key molecular parameter perturbations include:
1. **Reduced damping ($b$):** Variants in COL1A1/COL2A1 affecting flexibility lead to a $\approx 29\%$ reduction in damping.
2. **Increased proprioceptive delay ($\tau$):** Variants in mechanosensory proteins like PIEZO2, GPR126, or MTNR1B increase the effective neural delay from a baseline of $70$ ms to $\tau_{\text{eff}} = 96.4$ ms.
3. **Shifted $K_d$:** Variants such as LBX1 shift the derivative gain towards the trap peak, moving $K_d$ to $12.96$ (approaching the critical $12.6$).
4. **Increased gravitational load parameter:** Variants in PAX1 increase the load parameter ($mgL$) from a baseline $73.6$ to $93.7$.

When combined, these modest multi-gene perturbations flip the stability margin from $+5.3$ ms to **$-26.3$ ms**, plunging the system deep into the unstable zone. This quantitative prediction explains the 2-4% prevalence: the margin is narrow enough that a combination of several variants can breach it, yet wide enough that the majority of the population escapes intact. The 10:1 female-to-male surgical prevalence is further explained by estrogen's role in shifting this distribution (lowering damping via collagen cross-linking and steepening the growth trajectory).

## Multi-Segment Cosserat Rod: Predicting Lenke Curve Types

While the single-link delayed differential equation (DDE) inverted pendulum model accurately captures the *onset* of global instability (the temporal lock to PHV), it treats the spine as a single unit. To explain *where* the curve occurs and *what shape* it takes—the six distinct Lenke curve types—the framework extends to a **multi-segment Cosserat rod** model.

Different Lenke types (1-6) emerge as the dominant eigenmode of the multi-segment system, determined by regional parameter variations:

1. **Regional variation in stiffness ($EI$):** Differences between thoracic kyphosis and lumbar lordosis, modified by the rib cage buttressing effect.
2. **Segmental differences in proprioceptive delay ($\tau$):** Variations in mechanoreceptor density at different levels (e.g., T5-T12 versus L1-L5).
3. **Local damping ($b$) variations:** Differences in disc composition, facet joint orientation, and paraspinal muscle bulk across segments.
4. **Asymmetric loading:** Structural asymmetries such as cardiac offset, aortic pulsation, or handedness-related muscle imbalances.

These regional differences determine which vertebral segments destabilize *first* once the global Hopf threshold is breached.
- **Lenke Type 1 (Main Thoracic):** Destabilization occurs at the segment with minimum rib cage stiffening and maximal moment arm.
- **Lenke Type 5 (Thoracolumbar):** Reflects the transition zone where both thoracic and lumbar parameter sets converge unfavorably.

By modeling these regional heterogeneities, the framework maps the spatial localization of the Energy Deficit Window to distinct curve patterns, uniting the upstream trigger (metabolic buckling) with the downstream patterning (Lenke classification).
