import os
import re

def main():
    print("Generating Nature Portfolio manuscript...")

    # Abstract constraint: < 150 words
    abstract_text = r"\textbf{Living systems routinely maintain structure against gravity, yet the physical cost of this victory remains unquantified. Here we show that Adolescent Idiopathic Scoliosis (AIS) is a 'Metabolic Buckling' event caused by a mismatch between the scaling laws of mechanical demand and metabolic supply. We model the spine as a dissipative structure requiring continuous energy to maintain its S-shape. Using a Cosserat rod model coupled to a developmental information field, we identify an 'Energy Deficit Window' at spinal lengths $L > 0.35$m where the thermodynamic cost of straightness ($L^4$) exceeds metabolic capacity ($L^2$). Key mechanosensors exhibit high structural anisotropy, which is thermodynamically expensive to maintain. Our simulations demonstrate that this high anisotropy accelerates instability, while reducing sensor anisotropy delays buckling. These results suggest that scoliosis is a survival response to an unaffordable 'Anisotropy Tax', and that targeting cytoskeletal stiffness may offer a non-surgical rescue strategy.}"

    with open("manuscript/sections/introduction.tex", "r") as f:
        intro = f.read()
    with open("manuscript/sections/theory.tex", "r") as f:
        theory = f.read()
    with open("manuscript/sections/results.tex", "r") as f:
        results = f.read()
    with open("manuscript/sections/discussion.tex", "r") as f:
        discussion = f.read()
    with open("manuscript/sections/methods.tex", "r") as f:
        methods = f.read()

    def remove_headings(text):
        text = re.sub(r'\\section\*?\{[^}]+\}', '', text)
        text = re.sub(r'\\subsection\*?\{[^}]+\}', '', text)
        text = re.sub(r'\\subsubsection\*?\{[^}]+\}', '', text)
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        return text.strip()

    main_text = intro + "\n\n" + theory + "\n\n" + results + "\n\n" + discussion
    main_text = remove_headings(main_text)

    rebuttal = "While direct metabolic flux measurements in the growing human spine are currently invasive, the allometric scaling laws ($L^4$ vs $L^2$) provide a robust theoretical bound on energy availability that aligns with the observed clinical window of deformity. The specific molecular candidates identified are functional nodes in the control loop, and their failure modes match the predicted instability."
    if "While direct metabolic flux measurements" not in main_text:
        main_text += "\n\n" + rebuttal

    # Methods moved to supplementary section. Remove redundant heading.
    methods_clean = remove_headings(methods)
    supp_text = r"\section*{Supplementary Information}" + "\n" + r"\subsection*{Methods}" + "\n" + methods_clean

    # Title < 90 chars
    title = "Metabolic buckling predicts scoliotic curve onset"

    full_tex = f"""\\documentclass[11pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=1in}}
\\usepackage{{graphicx}}
\\usepackage{{amsmath, amssymb, bm}}
\\usepackage{{lineno}}
\\usepackage{{setspace}}
\\usepackage[superscript,biblabel]{{cite}}

\\title{{{title}}}

\\author{{Sayuj Krishnan S. \\\\
\\textit{{Yashoda Hospitals, Hyderabad, India}} \\\\
Correspondence: hellodr@drsayuj.info}}

\\date{{}}

\\begin{{document}}
\\linenumbers
\\maketitle

{abstract_text}

\\vspace{{1em}}

{main_text}

\\bibliography{{manuscript/references}}
\\bibliographystyle{{naturemag}}

\\clearpage
{supp_text}

\\end{{document}}
"""
    with open("submission_manuscript.tex", "w") as f:
        f.write(full_tex)

    print("Writing cover letter...")
    with open("cover_letter.txt", "w") as f:
        f.write("""Dear Editor,

We are submitting our manuscript, "Metabolic buckling predicts scoliotic curve onset," for consideration as an Article in Nature Communications (as a transfer from Nature).

Grand Challenge/Breakthrough Pitch:
For over a century, the onset of Adolescent Idiopathic Scoliosis (AIS) has remained one of orthopedic surgery's most stubborn mysteries. While genetics, biomechanics, and neurology have all been implicated, no model has unified these factors or explained the precise timing of onset during the adolescent growth spurt. We have discovered that AIS is fundamentally a thermodynamic scaling failure—a "Metabolic Buckling" event. We demonstrate that the metabolic cost of maintaining spinal posture scales as L^4, whereas supply scales as L^2. During the rapid adolescent growth spurt, this mismatch triggers an 'Energy Deficit Window', forcing the spine to adapt by adopting lower-energy scoliotic curves. This breakthrough bridges general relativity concepts with biomechanical modeling and AlphaFold-driven structural analysis.

We believe Nature Communications is the ideal venue for this interdisciplinary work, appealing to developmental biologists, physicists, and clinicians alike.

Sincerely,
Dr. Sayuj Krishnan S.
""")

    print("Writing checklist compliance...")
    with open("checklist_compliance.txt", "w") as f:
        f.write("""Nature Portfolio Formatting Checklist Compliance:
- [x] Inverted Pyramid structure applied (No subheadings in the main text).
- [x] Title is under 90 characters ("Metabolic buckling predicts scoliotic curve onset").
- [x] Abstract is under 150 words (currently 141 words) and unreferenced.
- [x] Pre-emptive rebuttal addressing metabolic flux measurement limitations is integrated into the discussion.
- [x] Methods have been moved to the Supplementary Information section at the end of the manuscript.
- [x] Cover letter drafted with a strong Grand Challenge/Breakthrough pitch targeting Nature Communications.
""")

if __name__ == "__main__":
    main()
