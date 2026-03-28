#!/bin/bash
export GEMINI_API_KEY="dummy"
export PATH="/home/jules/self_created_tools/bin:$PATH"

echo "Generating Polygenic Stacking Visual..."
paperbanana generate \
    --input "jules_polygenic_stacking_lenke.txt" \
    --caption "Polygenic Threshold of AIS" \
    --output "research/figures/jules_polygenic_stacking_lenke.png"

echo "Generating Lenke Multi-Segment Visual..."
paperbanana generate \
    --input "jules_lenke_multi_segment.txt" \
    --caption "Multi-Segment Cosserat Rod Modeling of Lenke Types" \
    --output "research/figures/jules_lenke_multi_segment.png"

echo "Artifact generation complete."
