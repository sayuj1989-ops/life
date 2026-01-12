#!/usr/bin/env bash
set -euo pipefail

# Define output bundle name
OUT="dist/arxiv_bundle_$(date +%Y%m%d).tar.gz"
mkdir -p dist

# Create a temporary directory for bundling
BUNDLE_DIR="dist/bundle_tmp"
rm -rf "$BUNDLE_DIR"
mkdir -p "$BUNDLE_DIR"

echo "Bundling submission artifacts..."

# 1. Main Manuscript Files
# Only copy the specific root tex file
cp manuscript/main.tex "$BUNDLE_DIR/"
cp manuscript/references.bib "$BUNDLE_DIR/"

# 2. Sections
# Copy the sections directory but exclude potential clutter
mkdir -p "$BUNDLE_DIR/sections"
# Find all .tex files in sections/ and copy them
find manuscript/sections -name "*.tex" -exec cp {} "$BUNDLE_DIR/sections/" \;

# 3. Figures (PDFs)
# The generate_manuscript_figures.py script outputs PDFs to manuscript/
# We also check figures/main/ just in case
mkdir -p "$BUNDLE_DIR/figures"

# Copy generated PDFs from manuscript/ (e.g. fig_countercurvature_panelA.pdf)
# We use find to avoid errors if none exist, though they should.
find manuscript -maxdepth 1 -name "*.pdf" -exec cp {} "$BUNDLE_DIR/" \;

# Copy any additional tex figures (like fig_iec_equations.tex) from manuscript/ root
find manuscript -maxdepth 1 -name "fig_*.tex" -exec cp {} "$BUNDLE_DIR/" \;

# If there are pre-generated figures in figures/main, copy them to a figures folder
# (some LaTeX setups might expect figures/filename.pdf)
if [ -d "figures/main" ]; then
    find figures/main -name "*.pdf" -exec cp {} "$BUNDLE_DIR/figures/" \;
    find figures/main -name "*.png" -exec cp {} "$BUNDLE_DIR/figures/" \;
fi

# 4. Root README
# Include the project root README as the main documentation for the bundle
cp README.md "$BUNDLE_DIR/"

# 5. Create the Archive
# Use tar to bundle everything
# --exclude-vcs is good practice, though we are copying specific files.
tar -C "$BUNDLE_DIR" -czf "$OUT" .

# Cleanup
rm -rf "$BUNDLE_DIR"

echo "✅ Submission bundle created: $OUT"
echo "   Contents:"
tar -tf "$OUT" | head -n 10
echo "   (...)"
