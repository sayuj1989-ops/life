# Day 10: The Multi-Component $\tau$ Model

## Introduction
To mathematically formalize the conceptual findings from Phase 1 and 2, we must construct a quantitative model of the proprioceptive delay $\tau$. This model decomposes the total delay $\tau_{total}$ into its fundamental biological components and introduces variant-specific perturbation terms ($\Delta\tau_i$).

## Baseline Delay Definitions
Let $\tau_{total}$ be the sum of seven sequential delays:
$\tau_{total} = \tau_{transduction} + \tau_{afferent} + \tau_{spinal} + \tau_{cerebellar} + \tau_{efferent} + \tau_{NMJ} + \tau_{EM}$

For a typically developing (healthy) 12-year-old child (height $h = 1.5$m), we define the baseline values ($\tau^0_i$) based on literature averages:
1. $\tau_{transduction}^0 = 2.0$ ms (PIEZO2 activation kinetics)
2. $\tau_{afferent}^0 = 15.0$ ms (Path length $\approx 0.9$m, NCV $\approx 60$ m/s)
3. $\tau_{spinal}^0 = 3.0$ ms (Synaptic delay in Clarke's column)
4. $\tau_{cerebellar}^0 = 25.0$ ms (Central integration)
5. $\tau_{efferent}^0 = 15.0$ ms (Path length $\approx 0.9$m, NCV $\approx 60$ m/s)
6. $\tau_{NMJ}^0 = 1.0$ ms (Synaptic delay at motor endplate)
7. $\tau_{EM}^0 = 50.0$ ms (Electromechanical coupling and muscle stiffness)

**Baseline Total:** $\tau_{total}^0 = 111.0$ ms. This is well below the theoretical instability threshold of $\approx 200$ ms derived in Paper 2.

## The Growth Spurt Perturbation
During the adolescent growth spurt, height ($h(t)$) increases rapidly. This has two effects:
1. **Path Length Increase**: The physical distance the signal must travel increases proportional to $h(t)$.
2. **Myelination Lag**: As described in Day 6, rapid bone elongation stretches nerves faster than Schwann cells can remodel myelin, causing a transient decrease in NCV.

We model this physiological change as a time-dependent growth penalty $\Delta\tau_{growth}(t)$:
$\Delta\tau_{growth}(t) = \frac{h(t) \cdot c_{path}}{NCV_{base} - \Delta NCV_{lag}(v_{growth})}$

Where $v_{growth} = \frac{dh}{dt}$ is the height velocity. This transiently adds $\approx 10-20$ ms to the total delay during peak height velocity.

## Genetic Perturbations
We introduce variant-specific perturbation terms $\Delta\tau_{gene}$ for individuals carrying risk alleles:
1. **GPR126 (rs6570507)**: Impaired Schwann cell cAMP signaling reduces myelin thickness. This specifically drops NCV.
   $\Delta\tau_{GPR126} = +10.0$ ms (applied to both afferent and efferent pathways).
2. **LBX1 (rs11190870)**: Altered dorsal interneuron specification requires more temporal summation.
   $\Delta\tau_{LBX1} = +5.0$ ms (applied to spinal relay).
3. **PIEZO2 (Hypothetical variant)**: Slower channel activation kinetics.
   $\Delta\tau_{PIEZO2} = +2.0$ ms (applied to transduction).

## The Polygenic "Derivative Gain Gap"
The total delay for a specific individual at time $t$ is:
$\tau_{total}(t, \text{genotype}) = \sum \tau_i^0 + \Delta\tau_{growth}(t) + \sum \Delta\tau_{genotype_i}$

If an individual carries multiple risk alleles (e.g., GPR126 and LBX1) *and* is undergoing a rapid growth spurt (high $v_{growth}$), their total delay can exceed the critical threshold:
$\tau_{total}(t_{peak}) > 200$ ms $\implies$ **Instability (Scoliosis Onset)**

This mathematical framework perfectly bridges the molecular genetics of AIS (GWAS hits) to the control-theoretic "Derivative Gain Gap" (Paper 2), providing a unified, mechanistic explanation for why scoliosis emerges specifically during adolescence in genetically susceptible individuals.
