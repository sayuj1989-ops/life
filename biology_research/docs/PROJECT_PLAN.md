# Biological Counter-Curvature: Project Plan

## Mission
To build, formalize, test, and write the theory of **Biological Counter-Curvature**: how the vertebral column develops and maintains a programmed counter-curvature *against* gravity.

---

## Milestones

### Phase 1: Concept & Toy Mathematical Models
**Goal:** Establish the theoretical framework and mathematical language.
- [ ] Create `docs/concept_map_countercurvature.md`: Define entities (cilia, HOX, PAX), processes, and mathematical objects.
- [ ] Draft `models/toy_curvature_model.py`: Simple Python script demonstrating a "sagging" beam vs. a "counter-curving" beam.
- [ ] Formulate the Energy Functional: Define $E[\kappa(s)]$ including gravity, bending, and cost terms.
- [ ] Define Riemannian & Lorentzian metric analogies in LaTeX/Markdown.

### Phase 2: Gene–Protein–Mechanics Mapping (AlphaFold Layer)
**Goal:** Connect specific molecules to mechanical parameters.
- [ ] Create `docs/alphafold_structure_to_mechanics_map.md`: Table linking genes to protein structures and mechanical roles.
- [ ] Analyze key structures (dyneins, HOX homeodomains, collagen fibrils) using AlphaFold data.
- [ ] Map mutations to parameter shifts (e.g., $DNAH5$ mutation $\to \epsilon \to 0$ in symmetry breaking).

### Phase 3: Full Rod/Growth Model + Parameter Sweeps
**Goal:** Implement a rigorous biomechanical simulation.
- [ ] Implement Cosserat Rod model in Python (using `scipy` or specific mechanics lib).
- [ ] Implement "Growth Tensor" evolution: $\frac{\partial g}{\partial t} = f(\text{gene}, \text{mechanics})$.
- [ ] Perform parameter sweeps: Vary HOX-defined stiffness $EI(s)$ and rest curvature $\kappa_0(s)$.
- [ ] Simulate "Microgravity" vs "1g" developmental trajectories.

### Phase 4: Data Linkage & Inference Plan
**Goal:** Validate with real-world data constraints.
- [ ] Define data schemas (`data_schemas/`) for spine imaging (curvature $\kappa(s)$ profiles).
- [ ] Propose fit metric: How well does the model prediction match human population variance?
- [ ] Outline pilot study: Retrospective analysis of scoliosis curvature patterns vs. genetic markers.

### Phase 5: Manuscript & Figure Production
**Goal:** High-impact publication (*Nature Communications*, *Development*, etc.).
- [ ] Maintain `docs/manuscript_outline.md`.
- [ ] Generate Figure 1: The Concept (Gravity vs. Counter-Curvature).
- [ ] Generate Figure 2: The Gene-Mechanics Map (HOX/PAX spatial fields).
- [ ] Generate Figure 3: Simulation Results (Phase plots, bifurcations).
- [ ] Write Draft 1.0.

---

## Directory Structure
- `docs/`: Concepts, plans, manuscript drafts.
- `models/`: Python implementations of rod mechanics and growth.
- `notebooks/`: Exploratory analysis and figure generation.
- `data_schemas/`: JSON/YAML definitions of expected data formats.
- `figures/`: Output for manuscript.
