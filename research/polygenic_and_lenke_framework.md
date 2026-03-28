# Polygenic Threshold and Lenke Curve Framework

## 1. The Polygenic Threshold: Explaining the 2–4% Prevalence

The Allometric Trap ($Bg \approx 0.01$) creates a universal vulnerability window that every adolescent passes through during the growth spurt. However, passing through this window is a necessary but not sufficient condition for developing Adolescent Idiopathic Scoliosis (AIS).

In a generic adolescent with population-mean parameters, the baseline scenario maintains a stability margin of **+5.3 ms**, keeping the system just above the Hopf bifurcation threshold. To cross this boundary and trigger the instability, an individual-specific stacking of molecular parameters is required.

This is explained through the **polygenic threshold model**, where dozens of identified risk loci (e.g., LBX1, PAX1, GPR126) with small effect sizes co-occur to destabilize the system. The specific genetic combination narrows and eventually breaches the stability margin:

- **Reduced damping $b$**: COL1A1/COL2A1 flexibility variants lead to a $\sim 29\%$ reduction.
- **Increased proprioceptive delay $\tau$**: PIEZO2/GPR126/MTNR1B variants shift the effective delay from $70$ ms (baseline) to $96.4$ ms ($\tau_{eff}$).
- **Shifted derivative gain $K_d$**: The LBX1 variant shifts $K_d$ to $12.96$, approaching the critical threshold of $12.6$.
- **Increased gravitational load parameter $mgL$**: The PAX1 variant increases the load parameter from $73.6$ (baseline) to $93.7$.

Each variant alone only slightly narrows the margin. However, their combined effect flips the margin to **−26.3 ms**, causing the system to destabilize. The 2–4% clinical prevalence of AIS reflects the fraction of the population where this specific combination of genetic variants pushes enough parameters past the threshold simultaneously.

Furthermore, this framework predicts the 8:1 to 10:1 female predominance: estrogen shifts the distribution by lowering damping (via collagen cross-linking) and steepening the growth trajectory, causing a larger fraction of females to land in the unstable zone.

## 2. Lenke Curve Diversity: The Multi-Segment Cosserat Rod

While the single-link inverted pendulum model captures the global onset of instability (the Hopf bifurcation trigger), it treats the spine as a single unit and cannot explain the spatial diversity of curve patterns. Different Lenke types (1–6) are defined by curve location (e.g., main thoracic, thoracolumbar) and structural modifiers.

To explain the emergence of the 6 Lenke curve types, the framework extends to a **multi-segment Cosserat rod**. This multi-segment model incorporates regional parameter differences that determine which vertebral segments destabilize first once the global threshold is breached. The resulting curve morphology emerges as the dominant eigenmode of the multi-segment system.

The key regional variations include:

- **Regional variation in stiffness $EI(s)$**: Differences such as thoracic kyphosis versus lumbar lordosis, and the buttressing effect of the rib cage.
- **Segmental differences in proprioceptive delay $\tau(s)$**: Variations in mechanoreceptor density, for example, between T5-T12 and L1-L5.
- **Local damping $b(s)$ variations**: Influenced by disc composition, facet joint orientation, and paraspinal muscle bulk, which differ by spinal level.
- **Asymmetric loading**: Factors like cardiac offset, aortic pulsation, and handedness creating localized stress biases.

By modeling the spine as a multi-segment system with these localized parameters, the diverse Lenke curve patterns become predictable outcomes. For instance:
- **Lenke Type 1 (Main Thoracic)**: May reflect destabilization at the segment with minimum rib cage stiffening.
- **Lenke Type 5 (Thoracolumbar)**: May reflect the transition zone where thoracic and lumbar parameter sets converge unfavorably.

This extension naturally bridges the upstream trigger of global instability onset with the downstream patterning of specific vertebral buckling configurations.
