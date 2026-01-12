\section{Results: Gravity-Selected Modes and Biological Countercurvature}

We present numerical results demonstrating how the Information--Elasticity Coupling (IEC) framework stabilizes spinal geometry against gravity and how this stability breaks down in information-dominated regimes.

\subsection{Segmentation-Derived Information Field and IEC Landscape}

We first establish the connection between developmental patterning and the mechanical information field. Figure 1 illustrates the mapping from discrete genetic domains (e.g., HOX boundaries) to a continuous information field $I(s)$.
\begin{figure}[h!]
    \centering
    % Placeholder for Figure 1
    \caption{\textbf{From Genes to Geometry.} (A) Conceptual mapping of HOX/PAX segmentation domains to the scalar information field $I(s)$. (B) The resulting IEC landscape, showing the effective metric factor $g_{\mathrm{eff}}(s)$ and stiffness modulation along the spine. Peaks in $I(s)$ correspond to regions of high counter-curvature demand (lordosis).}
    \label{fig:iec_landscape}
\end{figure}
The resulting field $I(s)$ (Fig.~1B) exhibits peaks in the cervical and lumbar regions. Through the biological metric (Eq.~\ref{eq:biological_metric}), these regions possess a larger ``effective length,'' effectively encoding the target S-shape into the manifold itself.

\subsection{Mode Spectrum of the IEC Beam in Gravity}

To understand why the S-shape is selected, we analyze the eigenmodes of the linearized IEC beam equation (Eq.~\ref{eq:mode_selection}).
\begin{figure}[h!]
    \centering
    % Placeholder for Figure 2
    \caption{\textbf{Gravity-Selected vs. Information-Selected Modes.} (A) Eigenmodes of a uniform beam in gravity, showing the lowest energy state is a C-shaped sag. (B) Eigenmodes of the IEC-coupled beam, where the information field shifts the spectrum, making the S-shaped counter-curvature mode the energetic ground state.}
    \label{fig:mode_spectrum}
\end{figure}
As shown in Figure 2, the passive beam's ground state is a monotonic C-shaped sag. However, with sufficient IEC coupling ($\chi_\kappa > \chi_{\mathrm{crit}}$), the spectrum shifts: the S-shaped mode (resembling the adult spine) becomes the lowest energy configuration. This confirms that the spinal curve is a \emph{gravity-selected mode} of the information-modified system.

\subsection{3D Cosserat Rod S-Curve Solutions}

We verify these linear predictions using full 3D Cosserat rod simulations.
\begin{figure}[h!]
    \centering
    % Placeholder for Figure 3
    \caption{\textbf{3D Equilibrium Configurations.} (A) Comparison of passive sag (gray) and IEC-stabilized S-curve (blue) under Earth gravity. (B) Persistence of the S-curve in microgravity ($g \to 0$), demonstrating that the shape is intrinsic to the information field, not just a reaction to load.}
    \label{fig:3d_solutions}
\end{figure}
Figure 3A shows the equilibrium shape of a rod with human-like parameters. The IEC model reproduces the characteristic cervical and lumbar lordosis. Crucially, this shape is robust to gravitational unloading. As shown in Figure 3B (and quantified by $\widehat{D}_{\mathrm{geo}}$ in Fig.~3C), the S-curve persists even as $g \to 0$, unlike the passive sag which would vanish. This explains the observation that spinal curvature is maintained in microgravity environments~\cite{green2018spinal}.

\subsection{Phase Diagrams of Curvature Patterns}

We map the behavior of the system across the parameter space of coupling strength $\chi_\kappa$ and gravitational acceleration $g$.
\begin{figure}[h!]
    \centering
    % Placeholder for Figure 4
    \caption{\textbf{Phase Diagram of Countercurvature Regimes.} Heatmap of geodesic deviation $\widehat{D}_{\mathrm{geo}}$ in the $(\chi_\kappa, g)$ plane. Three regimes are identified: (I) Gravity-dominated (sag), (II) Cooperative (stable S-curve), and (III) Information-dominated (potential for instability).}
    \label{fig:phase_diagram}
\end{figure}
Figure 4 reveals three distinct regimes. In the \emph{gravity-dominated} regime (low $\chi_\kappa$), the rod follows the passive geodesic (sag). In the \emph{cooperative} regime, information and gravity balance to produce a stable S-curve. In the \emph{information-dominated} regime (high $\chi_\kappa$), the effective metric becomes highly distorted, leading to complex curvature patterns.

\subsection{Perturbations and Pathology-Like Modes}

Finally, we explore the consequences of symmetry breaking in the information field.
\begin{figure}[h!]
    \centering
    % Placeholder for Figure 5
    \caption{\textbf{Emergence of Scoliosis-like Patterns.} (A) A small lateral asymmetry is introduced in the information field. (B) In the cooperative regime, this perturbation is suppressed. (C) In the information-dominated regime, the same perturbation is amplified into a large lateral deviation (scoliosis-like mode), characterized by high Cobb angles and axial rotation.}
    \label{fig:scoliosis}
\end{figure}
In the information-dominated regime, a small asymmetric perturbation (e.g., 5\% difference in left/right information) is amplified into a pronounced lateral deformity with axial rotation (Fig.~5). This suggests that idiopathic scoliosis may represent a "mode shape" of the spine that becomes accessible when the information-elasticity coupling is too strong relative to the stabilizing effect of gravity.
