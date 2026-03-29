#!/bin/bash
export GEMINI_API_KEY="dummy"
mkdir -p research/figures/

echo "Generating jules_polygenic_stacking_lenke.png..."
paperbanana generate --input jules_polygenic_stacking_lenke.txt --caption "Polygenic Stacking Model of AIS Prevalence" --output research/figures/jules_polygenic_stacking_lenke.png

echo "Generating jules_lenke_multi_segment.png..."
paperbanana generate --input jules_lenke_multi_segment.txt --caption "Multi-Segment Cosserat Rod & Lenke Curve Types" --output research/figures/jules_lenke_multi_segment.png

echo "Plotting polygenic stacking data..."
paperbanana plot --data outputs/experiments/polygenic_stacking_results.csv --x "Scenario" --y "Stability Margin (ms)" --output research/figures/jules_polygenic_stacking_plot.png

echo "Lenke artifact generation complete."