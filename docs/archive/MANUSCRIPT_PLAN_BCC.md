# Manuscript Plan: Biological Countercurvature of Spacetime

## 1. Project Map & Directory Structure

### Root: `/Users/mac/LIFE/life`

- **`manuscript/`**: Contains the main LaTeX files.
    - `main_countercurvature_refined.tex`: **Main Manuscript File**.
    - `sections/`: Individual sections (Intro, Methods, Results, Discussion, etc.).
    - `fig_iec_equations.tex`, `fig_system_architecture.tex`: TikZ/LaTeX figure definitions.
    - `*.pdf`: Generated figure files.
- **`src/spinalmodes/`**: Python package for the solver and models.
    - `countercurvature/`: Core IEC logic, coupling, and info fields.
    - `model/solvers/`: Cosserat and Euler-Bernoulli solvers.
    - `experiments/countercurvature/`: Scripts for running the paper's experiments (microgravity, phase diagram, etc.).
- **`scripts/`**: Utility scripts.
    - `generate_manuscript_figures.py`: Likely the main driver for figure generation.
- **`outputs/`**: Simulation results and generated figures.

## 2. Core Story So Far

**"Developmental information acts as a counter-curvature field against gravity."**

1.  **The Puzzle**: Biological structures (spines, plants) maintain complex shapes against gravity, unlike passive beams which sag.
2.  **The Mechanism**: Genetic patterning (HOX/PAX, segmentation) creates an **Information Field $I(s)$**.
3.  **The Coupling**: This field couples to mechanics via **Information-Elasticity Coupling (IEC)**, modifying rest curvature, stiffness, and active moments.
4.  **The Framework**: We model this as a **Cosserat rod** in an **effective spacetime** metric $d\ell_{\mathrm{eff}}^2 = g_{\mathrm{eff}}(s)ds^2$.
5.  **The Result**:
    -   **Normal Spine**: Gravity + IEC stabilizes a robust **S-curve** (counter-curvature mode).
    -   **Microgravity**: The S-curve persists even as gravity vanishes (unlike passive sag).
    -   **Pathology (Scoliosis)**: In information-dominated regimes, small asymmetries amplify into lateral deformities (scoliosis-like modes).

## 3. Current Manuscript State

**Title**: Biological Countercurvature of Spacetime: An Information--Cosserat Framework for Spinal Geometry
**Authors**: Dr. Sayuj Krishnan S

**Status**: **Advanced Draft**. Most sections are written and logically connected.

| Section | Status | Notes |
| :--- | :--- | :--- |
| **Abstract** | Strong | Covers all key points: IEC, metric, $\widehat{D}_{\mathrm{geo}}$, phase diagram, scoliosis. |
| **Intro** | Strong | Clear motivation and contribution. |
| **Methods** | Strong | Detailed IEC equations, Cosserat formulation, Metric definition. **Gap**: Missing explicit Energy Density equation and Eigenproblem formulation requested in prompt. |
| **Results** | Strong | Covers S-curves, plant growth, microgravity, phase diagram, scoliosis. |
| **Discussion** | Strong | Good interpretation of regimes and analog gravity. |

**Weak Points / Gaps**:
-   **Eq (2) Energy Density**: The prompt asks for $\mathcal{E}(s) = \frac{1}{2} B(s) \kappa(s)^2 w(I(s))$. Current draft has component couplings but not the integral energy form.
-   **Eq (4) Eigenproblem**: The prompt asks for $\mathcal{L}_{\mathrm{IEC}}[y(s)] = \lambda_n y_n(s)$. This is discussed qualitatively but not mathematically.
-   **Figure Mapping**: Need to ensure every figure in the draft corresponds to a specific script in `src/spinalmodes/experiments`.

## 4. Figure to Code Mapping

| Figure | File / Script | Inputs / Params | Biological Message |
| :--- | :--- | :--- | :--- |
| **Fig 1: IEC Equations** | `manuscript/fig_iec_equations.tex` | TikZ definition | Visual summary of the math framework. |
| **Fig 2: System Arch** | `manuscript/fig_system_architecture.tex` | TikZ definition | Overview of the solver/model. |
| **Fig 3: Countercurvature (4 panels)** | `src/spinalmodes/experiments/countercurvature/generate_countercurvature_figure.py` (likely) | `fig_countercurvature_panel*.pdf` | A: Curvature profiles. B: Metric. C: Geodesic deviation. D: Microgravity persistence. |
| **Fig 4: Phase Diagram** | `src/spinalmodes/experiments/countercurvature/experiment_phase_diagram.py` | `fig_phase_diagram_scoliosis.pdf` | Regimes of gravity vs. information dominance. |
| **Fig 5: Scoliosis/Asymmetry** | `src/spinalmodes/experiments/countercurvature/experiment_scoliosis_bifurcation.py` | (Integrated into Fig 4 or separate?) | Small asymmetries amplify in info-dominated regime. |
