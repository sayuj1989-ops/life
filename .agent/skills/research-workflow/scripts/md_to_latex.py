#!/usr/bin/env python3
"""
Convert research Markdown to LaTeX manuscript.

Usage:
    python md_to_latex.py input.md --output manuscript.tex
"""

import re
import sys
import argparse
from pathlib import Path


def convert_headers(text):
    """Convert markdown headers to LaTeX sections."""
    # H1 -> section
    text = re.sub(r"^# (.+)$", r"\\section{\1}", text, flags=re.MULTILINE)
    # H2 -> subsection
    text = re.sub(r"^## (.+)$", r"\\subsection{\1}", text, flags=re.MULTILINE)
    # H3 -> subsubsection
    text = re.sub(r"^### (.+)$", r"\\subsubsection{\1}", text, flags=re.MULTILINE)
    # H4 -> paragraph
    text = re.sub(r"^#### (.+)$", r"\\paragraph{\1}", text, flags=re.MULTILINE)
    return text


def convert_emphasis(text):
    """Convert markdown emphasis to LaTeX."""
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"\\textit{\1}", text)
    # Code
    text = re.sub(r"`(.+?)`", r"\\texttt{\1}", text)
    return text


def convert_equations(text):
    """Preserve LaTeX equations (already in correct format)."""
    # Equations between $$ or $ are already LaTeX format
    # Just ensure they're preserved
    return text


def convert_lists(text):
    """Convert markdown lists to LaTeX."""
    lines = text.split("\n")
    result = []
    in_itemize = False
    in_enumerate = False

    for line in lines:
        stripped = line.lstrip()

        # Bulleted list
        if stripped.startswith("- "):
            if not in_itemize:
                result.append("\\begin{itemize}")
                in_itemize = True
            item = stripped[2:]
            result.append(f"\\item {item}")
        # Numbered list
        elif re.match(r"^\d+\.\s", stripped):
            if not in_enumerate:
                if in_itemize:
                    result.append("\\end{itemize}")
                    in_itemize = False
                result.append("\\begin{enumerate}")
                in_enumerate = True
            item = re.sub(r"^\d+\.\s", "", stripped)
            result.append(f"\\item {item}")
        else:
            if in_itemize:
                result.append("\\end{itemize}")
                in_itemize = False
            if in_enumerate:
                result.append("\\end{enumerate}")
                in_enumerate = False
            result.append(line)

    # Close any open environments
    if in_itemize:
        result.append("\\end{itemize}")
    if in_enumerate:
        result.append("\\end{enumerate}")

    return "\n".join(result)


def convert_figures(text, input_path):
    """Convert markdown figures to LaTeX."""

    # Pattern: ![caption](path)
    def replace_figure(match):
        caption = match.group(1)
        path = match.group(2)

        # Convert relative path if needed
        if path.startswith("../"):
            path = path[3:]

        # Generate label from caption
        label = re.sub(r"[^\w\s-]", "", caption).strip().lower()
        label = re.sub(r"[-\s]+", "_", label)

        return f"""\\begin{{figure}}[htbp]
\\centering
\\includegraphics[width=0.7\\textwidth]{{{path}}}
\\caption{{{caption}}}
\\label{{fig:{label}}}
\\end{{figure}}"""

    text = re.sub(r"!\[([^\]]+)\]\(([^\)]+)\)", replace_figure, text)
    return text


def convert_citations(text):
    """Convert markdown citations to LaTeX format."""
    # [@author_year] -> \cite{author_year}
    text = re.sub(r"\[@([^\]]+)\]", r"\\cite{\1}", text)
    return text


def create_latex_document(content, title="Research Paper"):
    """Wrap content in LaTeX document structure."""
    template = f"""\\documentclass[11pt,a4paper]{{article}}

\\usepackage[utf8]{{inputenc}}
\\usepackage{{amsmath,amssymb,amsthm}}
\\usepackage{{graphicx}}
\\usepackage{{hyperref}}
\\usepackage[margin=1in]{{geometry}}
\\usepackage{{physics}}

% Custom commands
\\newcommand{{\\bvec}}[1]{{\\mathbf{{#1}}}}
\\newcommand{{\\tensor}}[1]{{\\mathsf{{#1}}}}

\\title{{{title}}}
\\author{{Author Name}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

{content}

\\bibliographystyle{{plain}}
\\bibliography{{references}}

\\end{{document}}
"""
    return template


def convert_markdown_to_latex(md_text, input_path, extract_title=True):
    """Convert markdown text to LaTeX."""
    # Extract title if present (first H1)
    title = "Research Paper"
    if extract_title:
        title_match = re.search(r"^# (.+)$", md_text, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
            # Remove title from content (will be in \title{})
            md_text = md_text[title_match.end() :].lstrip()

    # Apply conversions
    text = convert_headers(md_text)
    text = convert_emphasis(text)
    text = convert_lists(text)
    text = convert_figures(text, input_path)
    text = convert_citations(text)
    text = convert_equations(text)

    # Wrap in document
    latex_doc = create_latex_document(text, title)

    return latex_doc


def main():
    parser = argparse.ArgumentParser(description="Convert research Markdown to LaTeX manuscript")
    parser.add_argument("input", type=Path, help="Input Markdown file")
    parser.add_argument("--output", "-o", type=Path, help="Output LaTeX file")
    parser.add_argument("--title", help="Override document title")

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file {args.input} not found", file=sys.stderr)
        sys.exit(1)

    # Read markdown
    md_text = args.input.read_text(encoding="utf-8")

    # Convert
    latex_text = convert_markdown_to_latex(md_text, args.input)

    # Override title if specified
    if args.title:
        latex_text = re.sub(r"\\title\{[^}]+\}", f"\\\\title{{{args.title}}}", latex_text)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = args.input.with_suffix(".tex")

    # Write output
    output_path.write_text(latex_text, encoding="utf-8")
    print(f"Converted {args.input} -> {output_path}")


if __name__ == "__main__":
    main()
