#!/bin/bash

export GEMINI_API_KEY="dummy"
export PATH="/home/jules/self_created_tools/bin:$PATH"

mkdir -p research/figures

# Generate polygenic stacking visual
paperbanana generate --input research/descriptions/jules_polygenic_stacking_lenke.txt \
  --caption "Polygenic Stacking in the Allometric Trap (2-4% Prevalence)" \
  --output research/figures/jules_polygenic_stacking_lenke.png

# Generate multi-segment Cosserat rod visual
paperbanana generate --input research/descriptions/jules_lenke_multi_segment.txt \
  --caption "Multi-Segment Cosserat Rod: Lenke Curve Emergence" \
  --output research/figures/jules_lenke_multi_segment.png

echo "Done."
