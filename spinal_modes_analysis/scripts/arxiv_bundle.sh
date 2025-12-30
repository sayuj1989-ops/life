#!/usr/bin/env bash
set -euo pipefail

OUT="dist/arxiv_bundle_$(date +%Y%m%d).tar.gz"
mkdir -p dist
tar -czf "$OUT" manuscript figures/*.pdf tables/*.csv README.md
echo "Wrote $OUT"

