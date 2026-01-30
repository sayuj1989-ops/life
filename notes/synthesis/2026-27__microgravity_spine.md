# Weekly Synthesis: The Tensor-Scalar Mismatch (Piezo1 vs Piezo2)

**Date:** 2026-08-05 (Week 27)
**Author:** Microgravity Synthesizer

## 1. Key Findings

### Observed: Piezo1 as the Scalar Stiffness Sensor
Recent work confirms that **Piezo1** functions primarily as a "Scalar Sensor," responding to hydrostatic pressure, membrane tension, and local confinement rather than directional shear. In zebrafish, *Piezo1* mutants develop severe scoliosis characterized by low bone mineral density (BMD) and "soft" intervertebral discs that fail to resist compressive loads.
* **Source:** Ramli et al. (2024), *Journal of Biomechanics*. (See `notes/evidence/2026-06-24__piezo1_piezo2_duality.md`)

### Observed: Piezo2 as the Vector Alignment Sensor
Conversely, **Piezo2** in proprioceptive neurons acts as a "Vector Sensor," encoding the directionality and velocity of muscle stretch. Loss of *Piezo2* leads to spinal curvature not because the spine is weak, but because the neuromuscular control system is "blind" to alignment errors.
* **Source:** Assaraf et al. (2020), *Nature Communications*. (See `notes/evidence/2026-06-24__piezo1_piezo2_duality.md`)

### Hypothesized: The "Soft & Blind" Spine
Microgravity represents a unique "Double Hit" where both channels fail simultaneously but distinctly:
1.  **Scalar Silence:** The loss of gravitational weight (hydrostatic column) downregulates Piezo1, leading to ECM degradation and softening (Osteopenia/Disc degeneration).
2.  **Vector Silence:** The loss of postural sway and directional strain downregulates Piezo2, leading to proprioceptive drift.
The result is a spine that is structurally vulnerable (Soft) and neurologically uncontrolled (Blind), explaining the rapid onset of back pain and elongation in astronauts.

## 2. Mechanistic Bridge: The Mismatch

The core failure mode in microgravity is a **Vector-Scalar Mismatch**:
*   **Loading (1G):** High Scalar Load (Gravity) + High Vector Signal (Movement) -> Stiff & Aligned.
*   **Unloading (uG):** Low Scalar Load + Low Vector Signal -> Soft & Drifting.
*   **Pathology (The Trap):** If swelling (IVD congestion) artificially increases *Scalar* stress (Piezo1) while *Vector* stress (Piezo2) remains absent, the cell perceives a "Confined/Static" environment (like a scar or fibrosis), triggering aberrant remodeling (calcification or senescence) rather than healthy maintenance.

## 3. Predicted Directionality (Unloading vs. Loading)

| Feature | Unloading (Microgravity) | Loading (1G) |
| :--- | :--- | :--- |
| **Piezo1 Activity** | **Low** (or "Confined" if swollen) | **High** (Pulsatile) |
| **Piezo2 Activity** | **Silent** (Noise only) | **High** (Directional) |
| **Structural Outcome** | **Softening** (Buckling risk) | **Stiffening** (Stability) |
| **Control Outcome** | **Drift** (Loss of set-point) | **Correction** (Negative feedback) |

## 4. Testable Predictions

*   **H_2026_08_05_Piezo_Ratio**: The ratio of Piezo1/Piezo2 activation determines the "Osteogenic vs Adipogenic" fate; Mismatch (High P1, Low P2) drives inflammatory senescence.
*   **H_2026_08_05_Critical_Buckling**: *Piezo1* loss reduces the Critical Buckling Load ($P_{crit}$) of the spine, while *Piezo2* loss affects only the active correction gain; double mutants will show synergistic failure.
