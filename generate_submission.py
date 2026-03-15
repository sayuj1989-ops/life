import re

def read_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def process_section(text):
    # Remove section headings for Nature's "Inverted Pyramid" structure
    text = re.sub(r'\\section\*?\{[^}]+\}', '', text)
    text = re.sub(r'\\subsection\*?\{[^}]+\}', '', text)
    text = re.sub(r'\\subsubsection\*?\{[^}]+\}', '', text)
    return text.strip()

def main():
    # Read core sections
    abstract = read_file('manuscript/sections/abstract.tex')
    intro = read_file('manuscript/sections/introduction.tex')
    results = read_file('manuscript/sections/results.tex')
    discussion = read_file('manuscript/sections/discussion.tex')
    methods = read_file('manuscript/sections/methods.tex')
    theory = read_file('manuscript/sections/theory.tex')

    # Process Abstract (<150 words requirement)
    # The existing abstract is likely close, but we extract the text block
    abstract_match = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', abstract, re.DOTALL)
    if abstract_match:
        abstract_text = abstract_match.group(1).strip()
    else:
        abstract_text = abstract

    # Process Intro and Results (Merge, no headings)
    merged_main_text = process_section(intro) + "\n\n" + process_section(theory) + "\n\n" + process_section(results)

    # Process Discussion and add pre-emptive rebuttal
    discussion = process_section(discussion)
    rebuttal = "While direct flux measurements are invasive, the scaling laws provide a robust theoretical bound on energy availability."
    if "While direct flux" not in discussion:
        discussion += "\n\n" + rebuttal

    # Methods go to Extended Data/Supplementary
    methods = "\\section*{Supplementary Information (Methods)}\n" + process_section(methods)

    # Build the full TeX document
    full_tex = r"""\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\usepackage{graphicx}
\usepackage{amsmath, amssymb, bm}
\usepackage{lineno}
\usepackage{setspace}
\usepackage[superscript,biblabel]{cite}

\title{Metabolic buckling of the growing spine}

\author{Sayuj Krishnan S. \\
\textit{Yashoda Hospitals, Hyderabad, India} \\
Correspondence: hellodr@drsayuj.info}

\date{}

\begin{document}

\maketitle

\begin{abstract}
Adolescent Idiopathic Scoliosis (AIS) represents a profound failure of the spine during rapid skeletal growth, yet the fundamental etiology remains unknown. We present an Information-Elasticity Coupling framework modeling the spine as a dissipative structure requiring continuous energy to maintain its sagittal S-curve against gravity. We identify a fundamental "Gravity Paradox": during the adolescent growth spurt, the mechanical cost of counteracting gravity via spinal elongation scales exponentially ($L^4$), while nutrient diffusion scales strictly as surface area ($L^2$). This mismatch creates a transient "Energy Deficit Window" corresponding to clinical AIS onset. We show that mechanosensory feedback delay ("Spinal Jetlag") forces the system into a thermodynamic energy-minimizing state, spontaneously breaking symmetry. The coronal plane exhibits peak susceptibility due to cytoskeletal structural anisotropy. These findings reframe AIS as a systemic mechanobiological scaling failure, prioritizing metabolic diffusion and proprioceptive synchronization over passive external bracing.
\end{abstract}

""" + merged_main_text + "\n\n" + discussion + "\n\n" + methods + r"""

\bibliography{references}
\bibliographystyle{naturemag}

\end{document}
"""

    with open('manuscript/submission_manuscript.tex', 'w') as f:
        f.write(full_tex)

if __name__ == '__main__':
    main()
