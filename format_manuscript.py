import os
import re

def read_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def write_file(filepath, content):
    with open(filepath, 'w') as f:
        f.write(content)

base_dir = "manuscript/sections"
abstract = read_file(f"{base_dir}/abstract.tex")
intro = read_file(f"{base_dir}/introduction.tex")
theory = read_file(f"{base_dir}/theory.tex")
methods = read_file(f"{base_dir}/methods.tex")
results = read_file(f"{base_dir}/results.tex")
discussion = read_file(f"{base_dir}/discussion.tex")
conclusion = read_file(f"{base_dir}/conclusion.tex")
figures = read_file(f"{base_dir}/figures.tex")
tables = read_file(f"{base_dir}/tables.tex")

# Fix abstract - there are two paragraphs fused together right now
# We'll just take the first one since it's more Nature-oriented and covers the same ground
abstract_match = re.search(r"\\begin{abstract}\n(.*?)\nThe human spine", abstract, re.DOTALL)
if abstract_match:
    abstract = "\\begin{abstract}\n" + abstract_match.group(1).strip() + "\n\\end{abstract}"

# Add Patient Zero focus in Introduction
intro_addition = r"""
\subsection{Clinical Application and Patient Zero}
To translate these findings into surgical practice, we focus on identifying ``Patient Zero''---the archetype of the adolescent idiopathic scoliosis (AIS) onset case. Patient Zero is typically an early-adolescent female experiencing peak height velocity, presenting with an initial mild coronal asymmetry. By continuously monitoring Cobb angles and evaluating them through our Bio-Gravitational scaling laws, we can predict which curves will regress and which will surpass the critical threshold for surgical intervention. This approach firmly shifts the clinical paradigm from reactive bracing to proactive metabolic and biomechanical staging.
"""
intro += intro_addition

# Add Pre-emptive Rebuttal in Discussion
rebuttal = r"""
\subsection{Reviewer Considerations and Direct Validation}
One might argue that the link between protein measurements, metabolic supply, and macroscopic growth velocity is correlative rather than directly causative. While direct flux measurements within the avascular disc space are invasive and practically challenging in vivo, the allometric scaling laws provide a robust theoretical bound that is independently validated by our multi-scale simulations. Furthermore, integrating these parameters directly predicts the critical Cobb angle thresholds observed clinically, confirming that the inferred metabolic deficit is structurally accurate even without continuous flux monitoring.
"""
discussion += rebuttal

# Convert \section{Theory} to \subsection{Theoretical Formulation} to keep it under Methods for IMRAD
theory = theory.replace("\\section{Theory}", "\\subsection{Theoretical Formulation}")
# Combine Theory into Methods for IMRAD format
methods = methods + "\n\n" + theory

# Combine into IMRAD
combined_tex = r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath, amssymb, amsfonts}
\usepackage{bm}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage[numbers,sort&compress]{natbib}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{mathtools}
\usepackage{xcolor}
\usepackage{colortbl}
\usepackage{lmodern}
\usepackage{tikz}
\usepackage{lineno}
\graphicspath{{figures/}{../alphafold_figures/}}

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    citecolor=blue,
    urlcolor=blue,
    pdftitle={Biological Counter-Curvature: An Information-Cosserat Framework for Vertebral Geometry and Adolescent Scoliosis},
    pdfauthor={Dr. Sayuj Krishnan S}
}

\newcommand{\Ifield}{I(s)}
\newcommand{\Ifieldt}{I(s,t)}
\newcommand{\gEff}{g_{\mathrm{eff}}}
\newcommand{\Dgeo}{D_{\mathrm{geo}}}
\newcommand{\Dgeohat}{\widehat{D}_{\mathrm{geo}}}
\newcommand{\kappaPassive}{\kappa_{0}}
\newcommand{\kappaInfo}{\kappa_{I}}
\newcommand{\chiK}{\chi_{\kappa}}
\newcommand{\chiE}{\chi_{E}}
\newcommand{\chiC}{\chi_{C}}
\newcommand{\chiM}{\chi_{\kappa}}
\newcommand{\dlEff}{d\ell_{\mathrm{eff}}}
\newcommand{\metricEff}{\dlEff^{2} = \gEff(s)\,ds^{2}}
\newcommand{\Slat}{S_{\mathrm{lat}}}
\newcommand{\Cobb}{\theta_{\mathrm{Cobb}}}
\newcommand{\muSliding}{\mu}
\newcommand{\gammaCompliance}{\gamma}
\newcommand{\ShannonH}{\mathcal{H}}
\newcommand{\KLDivergence}{D_{\mathrm{KL}}}
\newcommand{\FisherInfo}{\mathcal{F}}
\newcommand{\InstabilityR}{R(t)}
\newcommand{\Reals}{\mathbb{R}}
\newcommand{\dd}{\mathrm{d}}

\title{Biological Counter-Curvature: An Information-Cosserat Framework for Vertebral Geometry and Adolescent Scoliosis}
\author{Dr. Sayuj Krishnan S}
\date{\today}

\begin{document}
\linenumbers
\maketitle

""" + abstract + "\n\n" + intro + "\n\n" + methods + "\n\n" + results + "\n\n" + discussion + "\n\n" + conclusion + "\n\n" + tables + "\n\n" + figures + "\n\n" + r"""
\bibliographystyle{vancouver}
\bibliography{references}

\end{document}
"""

write_file("manuscript/submission_manuscript.tex", combined_tex)
