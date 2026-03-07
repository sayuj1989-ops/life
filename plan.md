1. **Refactor Manuscript to JOR Spine Standards**:
   - Use `replace_with_git_merge_diff` on `manuscript/main.tex`:
   ```latex
<<<<<<< SEARCH
    pdftitle={The Allometric Trap: Scaling Laws Predict When Growing Organisms Cannot Afford Their Own Shape},
=======
    pdftitle={Biological Counter-Curvature: An Information-Cosserat Framework for Vertebral Geometry and Adolescent Scoliosis},
>>>>>>> REPLACE
<<<<<<< SEARCH
\title{The Allometric Trap: Scaling Laws Predict When Growing Organisms Cannot Afford Their Own Shape}
=======
\title{Biological Counter-Curvature: An Information-Cosserat Framework for Vertebral Geometry and Adolescent Scoliosis}
>>>>>>> REPLACE
   ```
   - Use `write_file` on `manuscript/sections/abstract.tex` with the following content:
   ```latex
\begin{abstract}
\textbf{Background:} The human spine maintains a complex S-shaped sagittal profile against gravity, yet the physical principle underlying this counter-curvature remains unexplained. Why this geometry is selected, and why it becomes vulnerable specifically during adolescent growth, are open questions.

\textbf{Methods:} We introduce the Information--Elasticity Coupling (IEC) framework, which integrates a developmental information field $I(s)$ — representing HOX-patterned segmental identity — with Cosserat rod mechanics. We implement this as both a linearized eigenvalue problem and a full 3D rod simulation using PyElastica, performing parameter sweeps across coupling strength and gravitational loading.

\textbf{Results:} The IEC framework selects the S-shaped spinal profile as the energetic ground state of the coupled system, reproducing clinically normal lordosis (~42$^\circ$) and kyphosis (~35$^\circ$). Phase diagram analysis reveals three regimes: gravity-dominated (passive sag), cooperative (stable S-curve), and information-dominated (scoliosis-prone). During simulated adolescent growth, small information-field asymmetries (~5\%) are amplified into scoliotic deformities (Cobb >15$^\circ$) through a supercritical bifurcation at a critical length, providing a mechanical explanation for adolescent scoliosis onset. AlphaFold structural analysis of 23 mechanotransduction proteins reveals a 34\% demand–supply anisotropy gap that quantifies the molecular basis of this vulnerability.

\textbf{Conclusions:} Spinal geometry emerges as a thermodynamic standing wave maintained by metabolic expenditure against gravity. The IEC framework unifies developmental patterning and biomechanics, generating specific testable predictions for scoliosis prevention and early detection.
\end{abstract}
   ```
   - Use `replace_with_git_merge_diff` on `manuscript/sections/theory.tex`:
   ```latex
<<<<<<< SEARCH
The Human spine is modeled as a one-dimensional Cosserat rod embedded in three-dimensional Euclidean space. In the IEC framework, we treat the rod's reference configuration not as a flat segment, but as a manifold whose intrinsic geometry is warped by a developmental information field $I(s)$. We draw a formal analogy to General Relativity (GR), where the geometry of space is determined by the mass-energy distribution. For interested readers, the full mathematical details of this analogy, including the mapping of GR variables to IEC morphoelastic variables and the derivation of the effective biological metric using the Fisher Information metric $\FisherInfo(s)$, are provided in the Supplementary Material.
=======
The Human spine is modeled as a one-dimensional Cosserat rod embedded in three-dimensional Euclidean space. In the IEC framework, we treat the rod's reference configuration not as a flat segment, but as a manifold whose intrinsic geometry is warped by a developmental information field $I(s)$. For interested readers, the full mathematical details mapping geometric variables to IEC morphoelastic variables and the derivation of the effective biological metric using the Fisher Information metric $\FisherInfo(s)$, are provided in the Supplementary Material.
>>>>>>> REPLACE
   ```

2. **Add Missing Figures**:
   - Run `cat >> manuscript/sections/figures.tex` to append the newly generated figures.
   ```latex
% Figure 8: Clinical Cohort Validation
\begin{figure}[h!]
    \centering
    \includegraphics[width=0.8\textwidth]{fig_clinical_cohort_data.png}
    \caption{\textbf{Clinical Cohort Validation.} Trajectories of adolescent scoliosis plotted against historical clinical data (Weinstein 1983 and Lonstein 1984 cohorts).}
    \label{fig:clinical_cohort}
\end{figure}

% Figure 9: Peak Height Velocity (PHV) Timing
\begin{figure}[h!]
    \centering
    \includegraphics[width=0.8\textwidth]{fig_phv_timing.png}
    \caption{\textbf{Metabolic Deficit Window vs. Clinical Peak Height Velocity (PHV).} The model's predicted instability window closely overlaps with the clinical onset timing of maximum growth velocity, providing retrospective validation.}
    \label{fig:phv_timing}
\end{figure}

% Figure 10: Sexual Dimorphism
\begin{figure}[h!]
    \centering
    \includegraphics[width=0.8\textwidth]{fig_sexual_dimorphism.png}
    \caption{\textbf{Metabolic Dimorphism.} Differences in peak metabolic demand and supply capacity between females and males explain the observed 10:1 female-to-male ratio in adolescent idiopathic scoliosis prevalence.}
    \label{fig:sexual_dimorphism}
\end{figure}

% Figure 11: Lenke Classes as Eigenmodes
\begin{figure}[h!]
    \centering
    \includegraphics[width=1.0\textwidth]{fig_lenke_classes.png}
    \caption{\textbf{Lenke Curve Classes as Eigenmodes.} The Information-Elasticity Coupling (IEC) framework models various clinical curve patterns (e.g., Lenke Types 3, 4, 5) directly as emergent eigenmodes of the coupled Cosserat rod system based on localized metabolic deficit.}
    \label{fig:lenke_classes}
\end{figure}
   ```
   - Verify the append operation using `tail -n 30 manuscript/sections/figures.tex`.

3. **Incorporate Statistical Results and Clinical Validations into Text**:
   - Use `replace_with_git_merge_diff` on `manuscript/sections/discussion.tex`:
   ```latex
<<<<<<< SEARCH
\subsection{The Allometric Trap as a Universal Constraint}

Our results reveal a previously unrecognized physical constraint on vertebrate morphogenesis: the Allometric Trap. The Bio-Gravitational Number $\mathcal{B}_g$ provides a simple, dimensionless criterion for predicting whether an organism can passively maintain its shape against gravity or must invest metabolic energy in active form maintenance.
=======
\subsection{The Allometric Trap as a Universal Constraint}

Our results reveal a previously unrecognized physical constraint on vertebrate morphogenesis: the Allometric Trap. The Bio-Gravitational Number $\mathcal{B}_g$ provides a simple, dimensionless criterion for predicting whether an organism can passively maintain its shape against gravity or must invest metabolic energy in active form maintenance. Specifically, cross-species analysis of the Bio-Gravitational Number $\mathcal{B}_g$ against body mass demonstrates a robust allometric scaling ($R^2 = 0.744, p = 1.31 \times 10^{-3}$) with a scaling exponent of $-0.282 \pm 0.072$.
>>>>>>> REPLACE
   ```
   - Run `cat >> manuscript/sections/results.tex` to append the Clinical Validations subsection.
   ```latex
\subsection{Clinical Validations}
Our computational framework was validated against multiple clinical dimensions. First, the model's trajectory accurately matches the historical curve progression data from the Weinstein 1983 and Lonstein 1984 cohorts (Fig.~\ref{fig:clinical_cohort}). Second, the predicted metabolic instability window aligns with the clinical onset timing of Peak Height Velocity (PHV) (Fig.~\ref{fig:phv_timing}). Third, by incorporating metabolic dimorphism parameters, the model successfully reproduces the pronounced 10:1 female-to-male prevalence ratio observed in adolescent idiopathic scoliosis (Fig.~\ref{fig:sexual_dimorphism}). Finally, the framework demonstrates that the common clinical curve patterns, formalized by the Lenke classification (e.g., Types 3, 4, and 5), emerge naturally as eigenmodes of the coupled Cosserat rod system driven by localized metabolic deficits (Fig.~\ref{fig:lenke_classes}).
   ```
   - Verify the append operation using `tail -n 20 manuscript/sections/results.tex`.

4. **Verify Codebase Integrity**:
   - Run `pytest` and `ruff check .` using `run_in_bash_session`.

5. **Compile the Manuscript**:
   - Run `bash -c "cd manuscript && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex"` to verify LaTeX compilation.

6. **Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done**.
   - Call `pre_commit_instructions` and follow them exactly.

7. **Submit**:
   - Call `submit` with a descriptive message outlining the Nature-to-JOR-Spine pivot.
