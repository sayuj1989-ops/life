# Data Linkage & Inference Plan

## Overview
This document defines the strategy for validating the **Biological Counter-Curvature** theory using real-world clinical and biological data. The goal is to infer unobservable model parameters (e.g., Intrinsic Curvature $\kappa_0(s)$, Feedback Gain $G_{mech}$) from observable phenotypes (Spinal Shape $\mathbf{r}(s)$).

---

## 1. Data Schemas

### A. Imaging Data (Phenotype)
**Source:** EOS Biplanar X-ray / Whole-spine MRI.
**Format:** `spine_geometry_schema.json`

```json
{
  "subject_id": "string",
  "age_years": "float",
  "diagnosis": "enum(Healthy, AIS, Scheuermann)",
  "geometry": {
    "centerline_3d": [[x, y, z], ...],  // 50-100 points
    "cobb_angle_max": "float",
    "kyphosis_max": "float",
    "lordosis_max": "float"
  },
  "metrics": {
    "t1_tilt": "float",
    "pelvic_incidence": "float",
    "sacral_slope": "float"
  }
}
```

### B. Genetic Data (Genotype)
**Source:** Whole Exome Sequencing (WES) / Targeted Panels.
**Format:** `genetic_variant_schema.json`

```json
{
  "subject_id": "string",
  "variants": [
    {
      "gene": "DNAH5",
      "variant_type": "missense/truncation",
      "cadd_score": "float",
      "alphafold_impact": "predicted_mechanical_shift" 
      // e.g., "epsilon_reduction_80%"
    },
    {
      "gene": "COL2A1",
      "variant_type": "synonymous",
      "cadd_score": 0.0,
      "alphafold_impact": "neutral"
    }
  ]
}
```

---

## 2. The Inference Pipeline

### Problem Statement
Given observable shape $\mathcal{S}_{obs}$ and gravity $\mathbf{g}$, find the parameters $\theta = \{EI(s), \kappa_0(s), \epsilon, G_{mech}\}$ that minimize the energy gap:
$$ \hat{\theta} = \arg \min_{\theta} || \mathcal{S}_{model}(\theta) - \mathcal{S}_{obs} ||^2 $$

### Step 1: Inverse Mechanics (Geometry $\to$ Parameters)
*   **Input:** 3D Centerline $(x,y,z)$.
*   **Method:** "Unloading" Algorithm.
    *   Assume current shape is Equilibrium: $\delta E = 0$.
    *   Subtract gravitational deformation to estimate $\kappa_0(s)$.
    *   $\kappa_0(s) \approx \kappa_{obs}(s) - \frac{M_{grav}(s)}{EI(s)}$.
*   **Output:** Estimated Rest Curvature Field $\hat{\kappa}_0(s)$.

### Step 2: Genetic Correlation (Genotype $\to$ Parameters)
*   **Hypothesis Testing:**
    *   Do subjects with *DNAH5* variants have significantly lower $\epsilon$ (inferred torsion)?
    *   Do subjects with *HOX* variants have altered $\hat{\kappa}_0$ inflection points?
*   **Statistical Model:**
    $$ P(\theta_i | G_i) = \mathcal{N}(\mu(G_i), \sigma^2) $$
    Where $G_i$ is the genetic risk score for specific pathways.

---

## 3. Pilot Study Design

### Cohort Definition
1.  **Healthy Controls (N=50):** Asymptomatic, no scoliosis.
2.  **Early Onset Scoliosis (N=20):** rapid progression (Potential Cilia/Piezo defects).
3.  **Adolescent Idiopathic Scoliosis (N=50):** Common variant carriers.

### Validation Success Metrics
*   **Strong Support:** The inferred $\kappa_0(s)$ for Healthy Controls clusters tightly around the "Canonical Anti-Gravity S-Curve" derived in `models/toy_curvature_model.py`.
*   **Strong Support:** *DNAH5* mutation carriers allow the model to predict the *direction* of the curve (Situs Inversus Totalis vs. Levocardia correlations).
*   **Falsification:** If $\kappa_0(s)$ inference yields random noise uncorrelated with gravity moments.

---

## 4. Implementation Next Steps
1.  Write `models/inverse_solver.py`: Script to "unload" a given spinal shape.
2.  Simulate a "Patient Database" using `models/growth_rod_simulation.py` with random noise added.
3.  Test if the Inverse Solver preserves the "Ground Truth" parameters.
