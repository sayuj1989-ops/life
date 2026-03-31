#!/bin/bash
export PATH="/home/jules/self_created_tools/bin:$PATH"
export GEMINI_API_KEY="dummy"

mkdir -p research/figures
mkdir -p outputs/experiments
mkdir -p scripts/experiments

# Ensure scripts exist and run them
if [ ! -f outputs/experiments/polygenic_stacking_results.csv ]; then
    python3 scripts/experiments/experiment_polygenic_stacking.py
fi

if [ ! -f outputs/experiments/lenke_eigenmodes.csv ]; then
    python3 scripts/experiments/experiment_lenke_classes.py
fi

# Generate text descriptions for paperbanana
cat << 'TXT' > jules_polygenic_stacking_lenke.txt
Polygenic Stacking Threshold Model for Adolescent Idiopathic Scoliosis (AIS).
The allometric trap creates a universal vulnerability window with a +5.3 ms baseline stability margin.
Individual-specific genetic variants (e.g., reduced damping from COL1A1, increased delay from PIEZO2, shifted Kd from LBX1, increased load from PAX1) each narrow the margin.
The combined polygenic trap flips the margin to -26.3 ms, explaining the 2-4% clinical prevalence.
TXT

cat << 'TXT' > jules_lenke_multi_segment.txt
Multi-segment Cosserat Rod Modeling of Lenke Curve Types.
Different Lenke types (1-6) emerge as distinct buckling eigenmodes dictated by regional parameter variations:
- Thoracic rib cage buttressing (stiffness EI variations)
- Thoracolumbar vulnerability (31.1% stiffness reduction)
- Segmental mechanoreceptor density differences (proprioceptive delay τ)
- Asymmetric loading
These regional differences map global instability onset to specific 3D spatial curve morphologies.
TXT

# Generate conceptual diagrams
paperbanana generate --input jules_polygenic_stacking_lenke.txt --caption "Polygenic Threshold: The 2-4% Prevalence" --output research/figures/jules_polygenic_stacking_lenke.png

paperbanana generate --input jules_lenke_multi_segment.txt --caption "Multi-segment Cosserat Rod: Lenke Curve Morphologies" --output research/figures/jules_lenke_multi_segment.png

# Generate data plots
paperbanana plot --data outputs/experiments/polygenic_stacking_results.csv --x Scenario --y Stability_Margin_ms --output research/figures/plot_polygenic_stacking.png

paperbanana plot --data outputs/experiments/lenke_eigenmodes.csv --x Normalized_Position --y Mode_1 --output research/figures/plot_lenke_mode1.png

echo "Autonomous Lenke artifacts generated."
