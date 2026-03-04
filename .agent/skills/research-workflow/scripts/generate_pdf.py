#!/usr/bin/env python3
"""
Generate PDF from LaTeX manuscript.

Usage:
    python generate_pdf.py manuscript.tex
"""

import argparse
import subprocess
import sys
from pathlib import Path


def compile_latex(tex_file, runs=2):
    """
    Compile LaTeX file to PDF.

    Args:
        tex_file: Path to .tex file
        runs: Number of pdflatex runs (for TOC, references)
    """
    tex_path = Path(tex_file)

    if not tex_path.exists():
        print(f"Error: {tex_file} not found", file=sys.stderr)
        return False

    # Change to directory containing tex file
    work_dir = tex_path.parent
    tex_name = tex_path.name

    print(f"Compiling {tex_name}...")

    # Check for bibliography file
    bib_file = tex_path.with_suffix(".bib")
    has_bib = bib_file.exists()

    # Also check for references.bib in same directory
    if not has_bib:
        ref_bib = work_dir / "references.bib"
        if ref_bib.exists():
            has_bib = True

    try:
        # First pdflatex run
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_name],
            cwd=work_dir,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("Error during first compilation:", file=sys.stderr)
            print(result.stdout, file=sys.stderr)
            return False

        print("✓ First compilation complete")

        # Run bibtex if bibliography exists
        if has_bib:
            base_name = tex_path.stem
            result = subprocess.run(
                ["bibtex", base_name], cwd=work_dir, capture_output=True, text=True
            )

            if result.returncode == 0:
                print("✓ Bibliography processed")
            else:
                print("Warning: BibTeX had issues (might be okay if no citations)")

        # Additional pdflatex runs for cross-references
        for i in range(runs):
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_name],
                cwd=work_dir,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                print(f"Error during run {i + 2}:", file=sys.stderr)
                print(result.stdout, file=sys.stderr)
                return False

            print(f"✓ Compilation run {i + 2} complete")

        pdf_path = tex_path.with_suffix(".pdf")
        print(f"\n✓ PDF generated: {pdf_path}")
        return True

    except FileNotFoundError:
        print("Error: pdflatex not found. Please install a LaTeX distribution.", file=sys.stderr)
        print("  macOS: brew install --cask mactex", file=sys.stderr)
        print("  Linux: apt-get install texlive-full", file=sys.stderr)
        return False


def clean_auxiliary_files(tex_file, keep_pdf=True):
    """Remove auxiliary LaTeX files."""
    tex_path = Path(tex_file)
    base = tex_path.stem
    work_dir = tex_path.parent

    extensions = [".aux", ".log", ".out", ".toc", ".bbl", ".blg", ".fls", ".fdb_latexmk"]

    for ext in extensions:
        aux_file = work_dir / f"{base}{ext}"
        if aux_file.exists():
            aux_file.unlink()
            print(f"Cleaned: {aux_file.name}")


def main():
    parser = argparse.ArgumentParser(description="Generate PDF from LaTeX manuscript")
    parser.add_argument("input", type=Path, help="Input LaTeX file (.tex)")
    parser.add_argument("--runs", type=int, default=2, help="Number of pdflatex runs (default: 2)")
    parser.add_argument(
        "--clean", action="store_true", help="Clean auxiliary files after compilation"
    )

    args = parser.parse_args()

    # Compile
    success = compile_latex(args.input, runs=args.runs)

    if not success:
        sys.exit(1)

    # Clean if requested
    if args.clean:
        print("\nCleaning auxiliary files...")
        clean_auxiliary_files(args.input)

    print("\n✓ Done!")


if __name__ == "__main__":
    main()
