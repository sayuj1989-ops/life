# LaTeX Templates

Templates for research documents and manuscripts.

## Basic Research Paper Template

```latex
\documentclass[12pt,a4paper]{article}

% Essential packages
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage[margin=1in]{geometry}

% Theorem environments
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{proposition}{Proposition}
\newtheorem{corollary}{Corollary}
\theoremstyle{definition}
\newtheorem{definition}{Definition}

% Title and authors
\title{Your Research Title}
\author{Author Name\\
\small Institution\\
\small \texttt{email@institution.edu}}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
Your abstract here (150-250 words).
\end{abstract}

\section{Introduction}
Introduction text...

\section{Methods}
Methods description...

\section{Results}
Results presentation...

\section{Discussion}
Discussion and implications...

\section{Conclusion}
Concluding remarks...

\bibliographystyle{plain}
\bibliography{references}

\end{document}
```

## Theoretical Framework Template

```latex
\documentclass[11pt]{article}

\usepackage{amsmath,amssymb,amsthm,physics}
\usepackage{graphicx,float}
\usepackage[margin=1.2in]{geometry}
\usepackage{hyperref}

% Custom commands for common notation
\newcommand{\bvec}[1]{\mathbf{#1}}
\newcommand{\tensor}[1]{\mathsf{#1}}
\newcommand{\dd}{\mathrm{d}}

\title{Theoretical Framework: [Topic]}
\author{[Authors]}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
Framework overview...
\end{abstract}

\tableofcontents

\section{Mathematical Preliminaries}
\subsection{Notation and Conventions}
Define notation...

\section{Core Framework}
\subsection{Fundamental Equations}
Present core equations...

\subsection{Derivations}
Show derivations...

\section{Applications}
Apply framework to specific cases...

\section{Predictions and Tests}
Falsifiable predictions...

\appendix
\section{Detailed Calculations}
Additional mathematical details...

\bibliographystyle{plain}
\bibliography{references}

\end{document}
```

## Preprint Template (arXiv style)

```latex
\documentclass[11pt]{article}

\usepackage{arxiv}  % arXiv preprint style
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{hyperref}

\title{Research Paper Title}

\author{
  Author One \\
  Department of Physics\\
  University Name\\
  \texttt{author1@email.edu} \\
  \And
  Author Two \\
  Department of Biology\\
  Another University\\
  \texttt{author2@email.edu}
}

\begin{document}

\maketitle

\begin{abstract}
Your abstract...
\end{abstract}

\keywords{Keyword1 \and Keyword2 \and Keyword3}

\section{Introduction}
Main content...

\section*{Acknowledgments}
Acknowledgments text...

\bibliographystyle{unsrt}
\bibliography{references}

\end{document}
```

## Mathematical Notation Examples

### Vectors and Tensors

```latex
% Vectors (bold)
\mathbf{r}, \mathbf{v}, \mathbf{F}

% Unit vectors
\hat{\mathbf{e}}_x, \hat{\mathbf{n}}

% Tensors (sans-serif)
\mathsf{T}, \mathsf{g}_{\mu\nu}

% Derivatives
\frac{\partial \mathbf{r}}{\partial t}, \dot{\mathbf{r}}, \ddot{\mathbf{r}}
```

### Equations and Alignments

```latex
% Single equation
\begin{equation}
E = mc^2
\label{eq:einstein}
\end{equation}

% Multiple aligned equations
\begin{align}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\epsilon_0} \label{eq:gauss} \\
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \label{eq:faraday}
\end{align}

% Split long equations
\begin{equation}
\begin{split}
\mathcal{L} &= \frac{1}{2}m\dot{\mathbf{r}}^2 - V(\mathbf{r}) \\
&\quad + \frac{1}{2}I\omega^2 - U_{elastic}
\end{split}
\end{equation}
```

### Special Environments

```latex
% Cases
f(x) = \begin{cases}
x^2 & x > 0 \\
0 & x \leq 0
\end{cases}

% Matrices
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}

% Integrals
\int_0^L f(s) \, \dd s
```

## Figure Inclusion

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.7\textwidth]{figures/diagram.pdf}
\caption{Caption describing the figure content.}
\label{fig:diagram}
\end{figure}

% Reference in text
As shown in Figure~\ref{fig:diagram}...
```

## Multi-Figure Layout

```latex
\usepackage{subcaption}

\begin{figure}[htbp]
\centering
\begin{subfigure}{0.45\textwidth}
    \includegraphics[width=\textwidth]{fig1.pdf}
    \caption{First subfigure}
    \label{fig:sub1}
\end{subfigure}
\hfill
\begin{subfigure}{0.45\textwidth}
    \includegraphics[width=\textwidth]{fig2.pdf}
    \caption{Second subfigure}
    \label{fig:sub2}
\end{subfigure}
\caption{Overall caption for both subfigures.}
\label{fig:combined}
\end{figure}
```

## Bibliography Example

```bibtex
@article{einstein1905,
  title={On the electrodynamics of moving bodies},
  author={Einstein, Albert},
  journal={Annalen der Physik},
  volume={17},
  pages={891--921},
  year={1905}
}

@book{landau1976,
  title={Course of Theoretical Physics: Mechanics},
  author={Landau, L. D. and Lifshitz, E. M.},
  volume={1},
  year={1976},
  publisher={Pergamon Press}
}

@inproceedings{conference2023,
  title={Conference Paper Title},
  author={Author, A. and Coauthor, B.},
  booktitle={Proceedings of Conference},
  pages={123--456},
  year={2023},
  organization={IEEE}
}
```

## Custom Commands for Efficiency

```latex
% In preamble
\newcommand{\kappa}{\boldsymbol{\kappa}}
\newcommand{\bm}[1]{\boldsymbol{#1}}
\newcommand{\dd}{\mathrm{d}}
\newcommand{\R}{\mathbb{R}}
\newcommand{\partial}{\partial}
\newcommand{\grad}{\nabla}

% Usage in document
\kappa instead of \boldsymbol{\kappa}
\int_\Omega f \dd x instead of \int_\Omega f \mathrm{d} x
```

## Compilation Commands

```bash
# Basic compilation
pdflatex document.tex

# With bibliography
pdflatex document.tex
bibtex document
pdflatex document.tex
pdflatex document.tex

# Clean auxiliary files
rm *.aux *.log *.out *.toc *.bbl *.blg
```
