# The Polygenic Stacking and Lenke Curve Framework

## 1. The Polygenic Threshold: Why Only 2-4% Prevalence?

A central question in the biomechanics of Adolescent Idiopathic Scoliosis (AIS) is: if the "Allometric Trap" is a universal scaling constraint of human bipedalism and growth, why do only 2-4% of adolescents develop clinical scoliosis?

The framework answers this by treating the Allometric Trap as a **universal vulnerability window** (a necessary but not sufficient condition). Every adolescent spine passes through this zone of marginal stability. However, the baseline adolescent possesses a small but crucial stability margin above the critical Hopf bifurcation boundary.

### The Stacking Model
In our baseline model parameters, the normal adolescent possesses a stability margin of **+5.3 ms**. They are close to the edge of instability but successfully traverse the growth spurt without buckling.

Clinical scoliosis emerges through the **individual-specific stacking of molecular parameters**, a manifestation of the polygenic threshold model. While individual genetic variants (such as those in LBX1, PAX1, GPR126) have small effect sizes, their concurrent presence pushes the system across the threshold.

Specific parameter shifts include:
- **Reduced damping ($b$)**: Variants in COL1A1/COL2A1 altering flexibility, yielding up to a 29% reduction in damping.
- **Increased proprioceptive delay ($\tau$)**: Variants in PIEZO2/GPR126/MTNR1B increasing the effective neural delay (e.g., $\tau_{eff} = 96.4$ ms vs baseline 70.0 ms).
- **Shifted derivative gain ($K_d$)**: Variants in LBX1 pushing the gain ($K_d = 12.96$) closer to the critical instability peak.
- **Increased gravitational load ($mgL$)**: Variants in PAX1 elevating the effective load parameter (e.g., 93.7 vs 73.6 baseline).

Each isolated variant narrows the baseline +5.3 ms margin. However, when these factors combine in a specific individual, the stability margin collapses and flips to a deeply unstable **-26.3 ms**.

The 2-4% prevalence simply reflects the tail of the population distribution where enough of these molecular parameters simultaneously stack to breach the threshold. Furthermore, the 8:1 female predominance logically follows: estrogen steepens the growth trajectory (increasing $\dot{L}$) and reduces damping via collagen cross-linking modifications, systematically shifting the distribution of female adolescents closer to the unstable regime.

---

## 2. Explaining Lenke Curve Diversity via Multi-Segment Cosserat Rods

While the single-link inverted pendulum Delay Differential Equation (DDE) accurately predicts the *onset* of global instability (when the Hopf boundary is crossed), it treats the spine as a single uniform unit. To explain the *shape* and *location* of the resulting deformity—specifically, the 6 distinct Lenke curve types—the framework must be extended.

The progression from a single inverted pendulum to a **multi-segment Cosserat rod** provides the mechanistic basis for Lenke curve diversity.

### Regional Parameter Variations
The specific Lenke curve pattern that emerges is the dominant eigenmode of the multi-segment system, determined by regional variations in four key parameters:

1. **Regional variation in stiffness ($EI(s)$)**: The thoracic spine is buttressed by the rib cage, while the lumbar spine features greater intrinsic torsional resistance (wider intervertebral discs).
2. **Segmental differences in proprioceptive delay ($\tau(s)$)**: Mechanoreceptor density varies across spinal levels (e.g., T5-T12 vs L1-L5).
3. **Local damping variations ($b(s)$)**: Paraspinal muscle bulk, facet joint orientation, and disc composition differ by level. The thoracic spine overlies relatively thin paraspinal muscle mass compared to the lumbar region.
4. **Asymmetric loading**: The aortic arch systematically displaces the descending thoracic spine leftward, creating a consistent rightward mechanical bias ($\epsilon_{asym}$). Handedness and cardiac offset further modulate this.

### Emergence of Lenke Types

These regional heterogeneities dictate which vertebral segments destabilize *first* once the global Allometric Trap is breached:

- **Lenke Type 1 (Main Thoracic, ~50% of AIS)**: The thoracic spine (T5-T12) carries the maximal gravitational moment arm and has the thinnest paraspinal muscle mass (lowest regional damping). The consistent rightward laterality arises from the aortic arch's asymmetric loading bias.
- **Lenke Type 2 (Double Thoracic)**: Destabilization occurs simultaneously at the main thoracic apex and the cervicothoracic junction (a secondary transition zone with steep patterning gradients).
- **Lenke Types 3 & 4 (Double and Triple Major)**: These represent cascading bifurcations. Compensatory curves initially form flexibly but eventually cross their own local stability thresholds ($L_{crit}$), triggering secondary buckling events in the lumbar or upper thoracic regions.
- **Lenke Type 5 (Thoracolumbar/Lumbar)**: The lumbar spine possesses greater inherent torsional resistance, shifting its local $L_{crit}$ rightward. Therefore, it enters the unstable window later in the growth spurt. If the thoracic spine is relatively stable (e.g., strong rib cage buttressing), the lumbar region becomes the primary site of failure.
- **Lenke Type 6 (TL/L dominant with minor thoracic)**: A mixed presentation where the transition zone between thoracic and lumbar parameter sets converges unfavorably, making the thoracolumbar junction the site of first collapse.

In summary, the polygenic Allometric Trap provides the *upstream trigger* (global instability onset), while the multi-segment Cosserat rod dynamics provide the *downstream patterning* (curve morphology and Lenke classification).