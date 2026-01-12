#!/usr/bin/env bash
set -euo pipefail

# Define output bundle name
OUT="dist/arxiv_bundle_$(date +%Y%m%d).tar.gz"
mkdir -p dist

# Ensure manuscript folder has the figures
# (Note: generate_manuscript_figures.py puts them in manuscript/)

# Create a temporary directory for bundling
BUNDLE_DIR="dist/bundle_tmp"
rm -rf "$BUNDLE_DIR"
mkdir -p "$BUNDLE_DIR"

# Copy manuscript source
cp manuscript/main.tex "$BUNDLE_DIR/"
cp manuscript/references.bib "$BUNDLE_DIR/"
cp -r manuscript/sections "$BUNDLE_DIR/"

# Copy generated figures (which are in manuscript/ now)
cp manuscript/*.pdf "$BUNDLE_DIR/" 2>/dev/null || true

# Copy figures from figures/main if they exist
if [ -d "figures/main" ]; then
    cp -r figures/main "$BUNDLE_DIR/figures"
fi
# Also copy fig_iec_equations.tex etc. if needed
cp manuscript/*.tex "$BUNDLE_DIR/"

# Copy README
cp README.md "$BUNDLE_DIR/"

# Create the tarball from the bundle directory
tar -C "$BUNDLE_DIR" -czf "$OUT" .

# Cleanup
rm -rf "$BUNDLE_DIR"

echo "Wrote $OUT"
