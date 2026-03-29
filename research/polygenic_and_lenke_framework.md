# Polygenic Stacking and Lenke Framework

## 1. Why only 2–4% if the Allometric Trap is universal?

The allometric trap creates a **universal vulnerability window** — every adolescent passes through it during the growth spurt. However, passing through the window does not guarantee instability. It is a necessary but not sufficient condition.

In the baseline scenario, a "generic" adolescent with population-mean parameters stays just above the Hopf bifurcation threshold, possessing a stability margin of **+5.3 ms**. They traverse the danger zone and come out the other side intact.

What pushes an individual across the boundary is the **individual-specific stacking of molecular parameters**:

- **Reduced damping $b$** (e.g., COL1A1/COL2A1 flexibility variants leading to a 29% reduction).
- **Increased proprioceptive delay $\tau$** (e.g., PIEZO2/GPR126/MTNR1B variants leading to $\tau_{eff} = 96.4$ ms compared to 70 ms baseline).
- **Shifted $K_d$ toward the trap peak** (e.g., LBX1 variant leading to $K_d = 12.96$, approaching the critical 12.6).
- **Increased gravitational load parameter** (e.g., PAX1 variant leading to $mgL = 93.7$ compared to 73.6 baseline).

While each variant alone narrows the margin, the **combined scenario** flips it to **−26.3 ms**. The 2–4% prevalence reflects the fraction of the population whose specific genetic combination pushes enough parameters simultaneously past the threshold. This logic aligns perfectly with the **polygenic threshold model**, as AIS involves dozens of identified risk loci, each contributing a small effect size. Only when a critical mass of these variants co-occur does the system destabilize.

The narrow 5.3 ms baseline margin predicts the low prevalence quantitatively: it is small enough that modest multi-gene perturbations can breach it, but large enough that most individuals don't. The 8:1 female predominance follows from estrogen shifting the distribution—lowering damping via collagen cross-linking and steepening the growth trajectory, causing a larger fraction of females to land in the unstable zone.

**Conclusion:** Everyone enters the trap. Most escape. The 2–4% represent those whose molecular parameters collectively block the exit.

## 2. Multi-Segment Cosserat Rod & Lenke Curve Types

The single-link inverted pendulum DDE model captures the *onset* of instability (the Hopf bifurcation) but treats the spine as a single unit. To explain the different Lenke curve types (1–6), the model is extended to a **multi-segment Cosserat rod** incorporating spatial heterogeneity:

- **Regional variation in stiffness $EI(s)$:** Differences between thoracic kyphosis and lumbar lordosis, and the structural buttressing provided by the rib cage.
- **Segmental differences in proprioceptive delay $\tau(s)$:** Varying mechanoreceptor densities from T5-T12 versus L1-L5.
- **Local damping $b(s)$ variations:** Disc composition, facet joint orientation, and paraspinal muscle bulk vary by vertebral level.
- **Asymmetric loading:** Cardiovascular asymmetries (cardiac offset, aortic pulsation) and handedness.

These regional variations dictate which vertebral segments destabilize *first* once the global Hopf threshold is breached. The resulting curve morphology emerges as the dominant eigenmode of the multi-segment system:

- **Lenke Type 1 (Main Thoracic):** Destabilization at the segment with minimal rib cage stiffening and maximal gravitational moment arm.
- **Lenke Type 5 (Thoracolumbar/Lumbar):** Onset in the transition zone where thoracic and lumbar parameter sets converge unfavorably.
- **Lenke Types 2, 3, 4 (Double/Triple Major):** Cascading bifurcations at secondary structural nodes.

Thus, the global instability acts as the *upstream trigger*, while the multi-segment mechanics govern the *downstream patterning*.
