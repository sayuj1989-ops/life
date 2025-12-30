import re
import os

# Configuration
SOURCE_DIR = "/Users/mac/LIFE"
DEST_DIR = "/Users/mac/LIFE/countercurvature"
ASSETS_DIR = "assets"

FILE_MAPPING = [
    ("ABSTRACT_TITLE_OPTIONS_BCC.md", "01_Abstract.md"),
    ("draft_intro_BCC.md", "02_Introduction.md"),
    ("draft_theory_BCC.md", "03_Theory.md"),
    ("draft_methods_BCC.md", "04_Methods.md"),
    ("draft_results_BCC.md", "05_Results.md"),
    ("draft_discussion_BCC.md", "06_Discussion.md"),
    ("draft_conclusion_BCC.md", "07_Conclusion.md"),
]

FIGURE_MAPPING = {
    "fig:iec_landscape": "fig_gene_to_geometry.png",
    "fig:mode_spectrum": "fig_mode_spectrum.png",
    "fig:3d_solutions": "fig_countercurvature_panelA.pdf",
    "fig:phase_diagram": "fig_phase_diagram_scoliosis.pdf",
    "fig:scoliosis": "fig_phase_diagram_scoliosis.pdf", # Best guess
}

# 1. Parse Bibliography
bib_db = {}
with open(os.path.join(SOURCE_DIR, "life/manuscript/refs.bib"), "r") as f:
    bib_content = f.read()
    # Simple regex to find Key and Year.
    # Entry pattern: @type{key, ... year = {YYYY} ... }
    # This is a rough parser.
    entries = re.split(r'@\w+\{', bib_content)
    for entry in entries:
        if not entry.strip(): continue
        try:
            key = entry.split(',')[0].strip()
            year_match = re.search(r'year\s*=\s*\{(\d+)\}', entry)
            if year_match:
                bib_db[key] = year_match.group(1)
        except:
            pass

def process_content(content, filename):
    # 1. Headers
    content = re.sub(r'\\section\{([^}]+)\}', r'# \1', content)
    content = re.sub(r'\\subsection\{([^}]+)\}', r'## \1', content)
    
    # 2. Citations
    def replace_cite(match):
        keys = match.group(1).split(',')
        refs = []
        for k in keys:
            k = k.strip()
            if k in bib_db:
                refs.append(f"{k}, {bib_db[k]}")
            else:
                refs.append(k)
        return f"({'; '.join(refs)})"
    
    content = re.sub(r'\\cite\{([^}]+)\}', replace_cite, content)
    
    # 3. Figures
    # Pattern: \begin{figure} ... \caption{TEXT} \label{KEY} ... \end{figure}
    # This is multiline, tricky with regex. We'll use a finite state machine approach or dotall.
    
    def replace_figure(match):
        block = match.group(0)
        caption_match = re.search(r'\\caption\{((?:[^{}]|\{.*\})*)\}', block, re.DOTALL)
        label_match = re.search(r'\\label\{([^}]+)\}', block)
        
        caption = "Figure"
        if caption_match:
            caption = caption_match.group(1).replace('\n', ' ').strip()
            # Remove \textbf
            caption = re.sub(r'\\textbf\{([^}]+)\}', r'**\1**', caption)
        
        image_file = "placeholder.png"
        if label_match:
            label = label_match.group(1)
            if label in FIGURE_MAPPING:
                image_file = FIGURE_MAPPING[label]
            else:
                image_file = f"MISSING_FIG_{label}.png"
                
        return f"\n![{caption}]({ASSETS_DIR}/{image_file})\n**{caption}**\n"

    content = re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', replace_figure, content, flags=re.DOTALL)
    
    # 4. Math
    # $...$, $$...$$, \begin{equation}...\end{equation}
    content = re.sub(r'\\begin\{equation\}', r'$$', content)
    content = re.sub(r'\\end\{equation\}', r'$$', content)
    content = re.sub(r'\\begin\{align\}', r'$$', content)
    content = re.sub(r'\\end\{align\}', r'$$', content)
    content = re.sub(r'\\nonumber', '', content)
    
    # 5. Reviewer cleanup (Lines like "The following code has been modified...")
    lines = content.split('\n')
    clean_lines = []
    for line in lines:
        if line.startswith("The following code has been modified") or line.startswith("The above content shows"):
            continue
        # Remove line numbers "1: "
        line = re.sub(r'^\d+:\s', '', line)
        clean_lines.append(line)
        
    return '\n'.join(clean_lines)

# Main Loop
for src, dest in FILE_MAPPING:
    src_path = os.path.join(SOURCE_DIR, src)
    dest_path = os.path.join(DEST_DIR, dest)
    
    if not os.path.exists(src_path):
        print(f"Skipping {src}, not found.")
        continue
        
    with open(src_path, 'r') as f:
        raw_content = f.read()
        
    processed_content = process_content(raw_content, src)
    
    # Special handling for Abstract choice
    if src == "ABSTRACT_TITLE_OPTIONS_BCC.md":
        # Extract Option 1
        match = re.search(r'### Option 1: Theory-Heavy\n(.*?)\n###', processed_content, re.DOTALL)
        if match:
            abstract_text = match.group(1).strip()
            title_match = re.search(r'\*\*T1 \(Primary\)\*\*: "(.*?)"', processed_content)
            title = title_match.group(1) if title_match else "Biological Countercurvature"
            processed_content = f"# {title}\n\n## Abstract\n{abstract_text}\n"
    
    with open(dest_path, 'w') as f:
        f.write(processed_content)
    print(f"Processed {dest}")

# Create README
with open(os.path.join(DEST_DIR, "README.md"), "w") as f:
    f.write("# Biological Countercurvature\n\n")
    f.write("## Table of Contents\n\n")
    for _, dest in FILE_MAPPING:
        name = dest.replace('_', ' ').replace('.md', '')[3:] # Remove "01_"
        f.write(f"- [{name}]({dest})\n")
