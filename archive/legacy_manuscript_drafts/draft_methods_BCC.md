\section{Methods: Deterministic Beam Model and PyElastica Simulations}

We implement the Information--Cosserat framework using two complementary numerical approaches: a fast deterministic beam model for parameter sweeps and eigenanalysis, and a full three-dimensional Cosserat rod simulation for capturing large deformations and geometric nonlinearities.

\subsection{Deterministic IEC Beam Model}

To explore the mode selection mechanism (Eq.~\ref{eq:mode_selection}), we discretize the linearized beam equations using a finite difference scheme on a 1D domain $s \in [0, L]$. The rod is divided into $N=100$ segments. The information field $I(s)$ is mapped to local stiffness $E_i$ and rest curvature $\kappa_{i}$ at each node. We solve the resulting boundary value problem (BVP) using a standard shooting method (or sparse matrix solver for the eigenproblem). This allows rapid exploration of the $(\chi_\kappa, g)$ parameter space to identify regions where S-modes become the ground state.

\subsection{3D Cosserat Rod Implementation (PyElastica)}

For full 3D simulations, we utilize \texttt{PyElastica}~\cite{pyelastica_zenodo,gazzola2018forward}, an open-source Python implementation of Cosserat rod theory. The spine is modeled as a Cosserat rod with the following specifications:

\begin{itemize}
    \item \textbf{Discretization}: The rod is discretized into $n=50$--$100$ elements.
    \item \textbf{IEC Coupling}: We implemented a custom callback in \texttt{PyElastica} that updates the local rest curvature vector $\bm{\kappa}^0(s)$ and bending stiffness matrix $\mathbf{B}(s)$ at each time step (or initialization) based on the information field $I(s)$.
    \item \textbf{Boundary Conditions}: The rod is clamped at the base (sacrum) and free at the top (cranium), simulating a cantilever column under gravity. For specific validation cases, clamped-clamped conditions are used.
    \item \textbf{Gravitational Loading}: Gravity is applied as a uniform body force $\mathbf{f} = \rho A \mathbf{g}$.
    \item \textbf{Damping}: To find static equilibrium configurations, we apply external damping ($\nu \sim 0.1$--$1.0$) and integrate the dynamic equations until the kinetic energy dissipates ($v_{\max} < 10^{-6}$ m/s).
\end{itemize}

The source code for the IEC-modified Cosserat solver is available in the \texttt{spinalmodes} Python package (see Data Availability).

\subsection{Parameter Sweeps and Mode Classification}

We perform systematic parameter sweeps over the coupling strength $\chi_\kappa$ (range $[0, 0.1]$) and gravitational acceleration $g$ (range $[0.01, 1.0]$ $g_{\mathrm{Earth}}$). For each simulation, we compute the equilibrium shape and evaluate the following metrics:
1.  \textbf{Geodesic Deviation} $\widehat{D}_{\mathrm{geo}}$: Quantifies the difference between the realized shape and the gravity-only geodesic.
2.  \textbf{Lateral Deviation} $S_{\mathrm{lat}}$: Measures symmetry breaking in the coronal plane.
3.  \textbf{Cobb Angle}: Standard clinical measure for scoliotic curves.

Regimes are classified as \emph{gravity-dominated} ($\widehat{D}_{\mathrm{geo}} < 0.1$), \emph{cooperative} ($0.1 < \widehat{D}_{\mathrm{geo}} < 0.3$), or \emph{information-dominated} ($\widehat{D}_{\mathrm{geo}} > 0.3$).

\subsection{Validation}

The numerical implementation was validated against analytical solutions for small-deflection Euler-Bernoulli beams. The \texttt{PyElastica} implementation was further verified by reproducing standard buckling and hanging chain benchmarks (see Supplementary Material).
