import re

def update_theory(filepath):
    with open(filepath, 'r') as f:
        theory = f.read()

    rod_geometry_new = r"""\subsection{Rod Geometry and Kinematic Parameterization}

We model the human spine as a Cosserat rod, defined by a centerline curve $\mathbf{r}(s,t) \in \mathbb{R}^3$ parameterized by arc length $s \in [0, L]$. This dimensionality reduction from 3D elasticity to a 1D director theory is justified by the high aspect ratio of the vertebral column ($L/d \approx 13$). To each point $s$, we attach an orthonormal material frame $\{\mathbf{d}_1(s,t), \mathbf{d}_2(s,t), \mathbf{d}_3(s,t)\}$ describing the cross-sectional orientation~\cite{goriely2017mathematics, gazzola2018forward}. The director $\mathbf{d}_3(s,t)$ aligns with the tangent to the centerline in the absence of shear, while $\mathbf{d}_1(s,t)$ and $\mathbf{d}_2(s,t)$ define the principal axes of the vertebral cross-section. The kinematics are governed by the evolution equations:
\begin{align}
\mathbf{r}'(s) &= \mathbf{v}(s) = \mathbf{d}_3(s) + \boldsymbol{\varepsilon}(s), \\
\mathbf{d}_i'(s) &= \mathbf{u}(s) \times \mathbf{d}_i(s),
\label{eq:cosserat_kinematics}
\end{align}
where $\mathbf{v}(s)$ is the tangent vector, $\boldsymbol{\varepsilon}(s)$ represents shear and extension strains, and $\mathbf{u}(s) = \kappa_1 \mathbf{d}_1 + \kappa_2 \mathbf{d}_2 + \tau \mathbf{d}_3$ is the Darboux vector encoding the flexural curvature components $\kappa_{1,2}$ and torsional twist $\tau$. Physically, we identify $s=0$ with the sacrum (clamped boundary condition: $\mathbf{r}(0)=\mathbf{0}, \mathbf{d}_i(0)=\mathbf{e}_i$) and $s=L$ with the cranium (free boundary condition), representing the aggregate mechanical axis of the vertebral column."""

    info_field_new = r"""\subsection{Developmental Information Fields from Morphogenetic Patterning}

We define a scalar information field $I(s, t) \in [0, 1]$ representing the coarse-grained expression level of anterior-posterior patterning morphogens (e.g., HOX genes). This field serves as a coarse-grained representation of the complex gene regulatory networks governing axial patterning. Following the bimodal Gaussian parameterization (Methods Eq.~\ref{eq:info_field_spinal}), we model $I(s)$ with peaks at the cervical ($A_c=0.5, s_c=0.80$) and lumbar ($A_l=0.7, s_l=0.25$) enlargements, corresponding to regions of high vertebral identity specification. The spatial gradient $\nabla I$ acts as a "curvature generator" via the geometric coupling $\chi_\kappa$:
\begin{equation}
\boldsymbol{\kappa}_{\mathrm{rest}}(s) = \boldsymbol{\kappa}_{\mathrm{gen}} + \chi_\kappa \nabla I(s).
\label{eq:kappa_rest}
\end{equation}

Mechanistically, the information field establishes the sensory set-points for the local mechanotransduction arrays. The developmental logic acts as a continuous spatial phase mapping. Drawing a mathematical analogy to parametric generative algorithms, the biological information field functions similarly: the angular coordinate governs the local pitch and curvature along the rod, behaving as an Euler spiral where curvature varies continuously with arc length. This mechanism yields the smooth, functionally graded transitions between the lordotic and kyphotic segments characteristic of the human spine, mirroring the interplay of static gradients, local magnitudes, and anisotropic phase in Information-Elasticity Coupling.

We quantify the information content of this patterning field using the local Shannon entropy $\ShannonH[I]$, which bounds the precision of the target metric specification:
\begin{equation}
\ShannonH[I] = -\int I(s) \log I(s) \, ds.
\label{eq:shannon_entropy}
\end{equation}
Simultaneously, the field exerts a stiffness via the morphomechanical coupling $\chi_M$, generating the active biological moment $\mathbf{M}_{bio}$ to oppose gravity:
\begin{equation}
\mathbf{M}_{bio} = \chi_M (\mathbf{\Lambda} \cdot \nabla I).
\label{eq:active_moment}
\end{equation}
Stability is quantified by the Bio-Gravitational Number $\mathcal{B}_g$:
\begin{equation}
\mathcal{B}_g = \frac{\chi_M \langle |\nabla I| \rangle}{\rho A g L^2}.
\label{eq:bg_number}
\end{equation}
When $\mathcal{B}_g > 1$, the organism dominates gravity. This framework is physically grounded in the structural specificity of HOX proteins. For example, AlphaFold analysis of HOXC8 (UniProt P31273) and HOXB13 (UniProt Q92826) demonstrates that these proteins possess rigid DNA-binding domains capable of enforcing the sharp identity boundaries necessary for this parameterization."""

    pattern1 = re.compile(r'\\subsection\{Rod Geometry and Kinematic Parameterization\}.*?(?=\\subsection\{Developmental Information Fields from Morphogenetic Patterning\})', re.DOTALL)
    theory = pattern1.sub(rod_geometry_new + "\n\n", theory)

    pattern2 = re.compile(r'\\subsection\{Developmental Information Fields from Morphogenetic Patterning\}.*?(?=\\subsection\{The Information--Cosserat Manifold Framework\})', re.DOTALL)
    theory = pattern2.sub(info_field_new + "\n\n", theory)

    with open(filepath, 'w') as f:
        f.write(theory)

def update_tables(filepath):
    tables_content = r"""\section*{Tables}

\begin{table}[h!]
\centering
\caption{List of thermodynamic cost proteins ($n=16$) mapped to the three dissipation terms ($\eta_p, \eta_a, \Gamma_m$). Metrics include Anisotropy Ratio (shape elongation), pLDDT (AlphaFold confidence), and Scaling behavior derived from cellular function. See Eq.~\ref{eq:dissipation} for term definitions.}
\label{tab:thermodynamic_cost_proteins}
\scriptsize
\begin{tabular}{llcclllc}
\toprule
\textbf{Gene} & \textbf{UniProt} & \textbf{Dissipation Term} & \textbf{Anisotropy} & \textbf{Morphology} & \textbf{pLDDT} & \textbf{Residues} & \textbf{L-Scaling} \\
\midrule
\multicolumn{8}{l}{\textit{Proprioceptive Channel Anchors ($\eta_p$)}} \\
PIEZO2 & Q9H5I5 & $\eta_p$ & 4.44 & Fibrous/Extended & 79.4 & 2752 & $L$ \\
PIEZO1 & Q92508 & $\eta_p$ & 3.90 & Fibrous/Extended & 72.0 & 2521 & $L^2$ \\
EGR3 & Q06889 & $\eta_p$ & 3.76 & Fibrous/Extended & 50.0 & 387 & $L$ \\
RUNX3 & Q13761 & $\eta_p$ & 2.06 & Intermediate & 60.6 & 415 & $L$ \\
NTRK3 & Q16288 & $\eta_p$ & 1.94 & Intermediate & 76.8 & 839 & $L$ \\
\midrule
\multicolumn{8}{l}{\textit{Active Maintenance Anchors ($\eta_a$)}} \\
VIM & P08670 & $\eta_a$ & 7.47 & Fibrous/Extended & 77.1 & 466 & $L^3$ \\
LMNA & P02545 & $\eta_a$ & 4.75 & Fibrous/Extended & 76.4 & 664 & $L^2$ \\
CAV1 & Q03135 & $\eta_a$ & 3.98 & Fibrous/Extended & 78.4 & 178 & $L^2$ \\
FLNA & P21333 & $\eta_a$ & 2.50 & Intermediate & 76.5 & 2647 & $L^3$ \\
LBX1 & P52954 & $\eta_a$ & 2.27 & Intermediate & 66.9 & 281 & $L^2$ \\
\midrule
\multicolumn{8}{l}{\textit{Metabolic Supply Scaling ($\Gamma_m$)}} \\
COL1A1 & P02452 & $\Gamma_m$ & 2.80 & Intermediate & 52.7 & 1464 & $L^3$ \\
COMP & P49747 & $\Gamma_m$ & 1.72 & Intermediate & 88.1 & 757 & $L$ \\
SIRT1 & Q96EB6 & $\Gamma_m$ & 1.73 & Intermediate & 65.0 & 747 & Constant \\
SOX9 & P48436 & $\Gamma_m$ & 2.19 & Intermediate & 56.0 & 509 & $L$ \\
SHH & Q15465 & $\Gamma_m$ & 2.12 & Intermediate & 78.4 & 462 & $L$ \\
CDKN1A & P38936 & $\Gamma_m$ & 2.14 & Intermediate & 69.0 & 164 & Threshold \\
\bottomrule
\end{tabular}
\end{table}
"""
    with open(filepath, 'w') as f:
        f.write(tables_content)

if __name__ == '__main__':
    update_theory('manuscript/sections/theory.tex')
    update_tables('manuscript/sections/tables.tex')
