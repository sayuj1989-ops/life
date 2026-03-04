#!/usr/bin/env python3
"""
Automatically embed figures in research documents.

Scans markdown file for figure references and validates them.

Usage:
    python embed_figures.py document.md --figures-dir ../figures
"""

import argparse
import re
from pathlib import Path


def find_figure_references(text):
    """
    Find all figure references in markdown text.

    Returns list of (caption, path) tuples.
    """
    pattern = r"!\[([^\]]*)\]\(([^\)]+)\)"
    matches = re.findall(pattern, text)
    return matches


def validate_figure_path(fig_path, doc_path, figures_dir=None):
    """
    Validate that figure file exists.

    Returns (exists, absolute_path).
    """
    # Convert to Path
    fig_path = Path(fig_path)
    doc_path = Path(doc_path)

    # If absolute path
    if fig_path.is_absolute():
        return fig_path.exists(), fig_path

    # Relative to document
    abs_path = (doc_path.parent / fig_path).resolve()
    if abs_path.exists():
        return True, abs_path

    # Relative to figures_dir if provided
    if figures_dir:
        abs_path = (Path(figures_dir) / fig_path.name).resolve()
        if abs_path.exists():
            return True, abs_path

    return False, abs_path


def suggest_figure_fixes(doc_path, figures_dir):
    """
    Suggest how to fix missing figures.
    """
    suggestions = []

    if figures_dir:
        fig_dir = Path(figures_dir)
        if fig_dir.exists():
            # List available figures
            image_extensions = {".png", ".jpg", ".jpeg", ".pdf", ".svg"}
            available = [f for f in fig_dir.iterdir() if f.suffix.lower() in image_extensions]

            if available:
                suggestions.append("\nAvailable figures in {}:".format(fig_dir))
                for fig in sorted(available):
                    suggestions.append(f"  - {fig.name}")

    return "\n".join(suggestions)


def generate_figure_markdown(caption, path, relative_to=None):
    """
    Generate markdown for figure embedding.
    """
    if relative_to:
        # Make path relative to document
        try:
            rel_path = Path(path).relative_to(Path(relative_to).parent)
            path = str(rel_path)
        except ValueError:
            # Can't make relative, use absolute
            pass

    return f"![{caption}]({path})"


def check_figures(md_file, figures_dir=None, verbose=False):
    """
    Check all figures in markdown file.

    Returns (total_figs, missing_figs, report).
    """
    md_path = Path(md_file)

    if not md_path.exists():
        return 0, 0, f"Error: {md_file} not found"

    # Read markdown
    text = md_path.read_text(encoding="utf-8")

    # Find figure references
    references = find_figure_references(text)

    if not references:
        return 0, 0, "No figure references found"

    # Check each figure
    report_lines = [f"Checking {len(references)} figure(s) in {md_file}:\n"]
    missing_count = 0

    for i, (caption, path) in enumerate(references, 1):
        exists, abs_path = validate_figure_path(path, md_path, figures_dir)

        if exists:
            status = "✓"
            detail = f"Found: {abs_path}"
        else:
            status = "✗"
            detail = f"Missing: {path}"
            missing_count += 1

        report_lines.append(f"  [{status}] Figure {i}: {caption[:50]}...")

        if verbose or not exists:
            report_lines.append(f"      {detail}")

    # Add suggestions if there are missing figures
    if missing_count > 0:
        suggestions = suggest_figure_fixes(md_path, figures_dir)
        if suggestions:
            report_lines.append(suggestions)

    report = "\n".join(report_lines)
    return len(references), missing_count, report


def add_figure_to_document(md_file, caption, figure_path, section=None):
    """
    Add a new figure to the markdown document.
    """
    md_path = Path(md_file)
    text = md_path.read_text(encoding="utf-8")

    # Generate markdown
    fig_md = generate_figure_markdown(caption, figure_path, relative_to=md_file)

    # Add to document
    if section:
        # Try to find section and add after it
        section_pattern = f"^##+ {re.escape(section)}$"
        match = re.search(section_pattern, text, re.MULTILINE)
        if match:
            # Insert after section heading
            insert_pos = match.end()
            text = text[:insert_pos] + f"\n\n{fig_md}\n" + text[insert_pos:]
        else:
            # Section not found, append to end
            text += f"\n\n## {section}\n\n{fig_md}\n"
    else:
        # Append to end
        text += f"\n\n{fig_md}\n"

    # Write back
    md_path.write_text(text, encoding="utf-8")
    print(f"Added figure to {md_file}")


def main():
    parser = argparse.ArgumentParser(description="Check and embed figures in research documents")
    parser.add_argument("input", type=Path, help="Input Markdown file")
    parser.add_argument("--figures-dir", type=Path, help="Directory containing figures")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed information")
    parser.add_argument(
        "--add", nargs=2, metavar=("CAPTION", "PATH"), help="Add new figure with caption and path"
    )
    parser.add_argument("--section", help="Section to add figure to (when using --add)")

    args = parser.parse_args()

    if args.add:
        # Add new figure
        caption, path = args.add
        add_figure_to_document(args.input, caption, path, section=args.section)
    else:
        # Check existing figures
        total, missing, report = check_figures(
            args.input, figures_dir=args.figures_dir, verbose=args.verbose
        )

        print(report)

        if missing > 0:
            print(f"\n⚠️  {missing} of {total} figures are missing!")
            return 1
        else:
            print(f"\n✓ All {total} figures found!")
            return 0


if __name__ == "__main__":
    import sys

    sys.exit(main() or 0)
