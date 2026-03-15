1. **Explore Context and State:** Review the current instructions and context. The goal is to act as "Theory Refiner" by adding ONE concrete formal element to the theory notes (`docs/theory/*`).
2. **Select Theory Element:** The prompt memory states: "When acting as 'Theory Refiner', perform one cycle by adding ONE concrete formal element (defining symbols, units, a coupling constant with dimensional analysis, and a measurable proxy) and a 'Falsifiable Tests' subsection to the theory notes (`docs/theory/*`). The tests must specify data needed and refutation conditions. Keep modifications grounded in biomechanics and developmental biology, cite >=2 references, use operational definitions instead of metaphysics, add no new dependencies, and open a PR titled 'weekly-theory: formalize <element>'."
3. **Formulate New Element:** I will formalize the "Delayed Control Model" currently sketched in `docs/theory/delayed_control_model.md` as a new formal number in `docs/theory/formalism_01.md`.
    *   **Element Name**: The Proprioceptive Delay Number ($\mathcal{D}_{prop}$)
    *   **Concept**: Ratio of neural transmission delay ($\tau$) to the characteristic mechanical buckling time ($\tau_{mech}$) of the spine.
    *   **Symbols/Units/Dimensions**:
        *   $\tau = \frac{2L}{v_{nerve}} + \tau_{syn}$ (Delay time, $[T]$)
        *   $\tau_{mech} \approx \sqrt{\frac{mL^2}{EI}}$ (Mechanical response time, $[T]$)
        *   $\mathcal{D}_{prop} = \frac{\tau}{\tau_{mech}}$ (Dimensionless, $[1]$)
    *   **Interpretation**: If $\mathcal{D}_{prop} \gg 1$, the feedback is too slow compared to mechanical dynamics, leading to a Hopf bifurcation (oscillatory instability / scoliosis).
    *   **Measurable Proxy**: Ratio of Somatosensory Evoked Potential (SSEP) latency to the pendulum sway period in a perturbation test.
    *   **Falsifiable Tests**:
        *   Test 1: Growth Spurt Delay Exacerbation (Refutation: If artificially increasing nerve conduction velocity via demyelination rescue doesn't reduce instability).
        *   Test 2: Latency-Matched Deformity (Refutation: If patients with high $\mathcal{D}_{prop}$ do not progress more than those with low $\mathcal{D}_{prop}$).
    *   **References**:
        *   Reference 1: Milton, J., et al. (2009). "The time-delayed inverted pendulum..." *Journal of Sound and Vibration*.
        *   Reference 2: Franklin, S., et al. (2007). "Proprioceptive regulation..." *Spine*.
4. **Append to `docs/theory/formalism_01.md`**:
    *   Add section `2.40. The Proprioceptive Delay Number ($\mathcal{D}_{prop}$)`
    *   Add tests to the end of the new section.
    *   Append references to the References section.
5. **Run Tests**: `pytest tests/`
6. **Pre-commit**: Complete pre-commit steps.
7. **Submit**: Open PR titled `weekly-theory: formalize The Proprioceptive Delay Number`.
