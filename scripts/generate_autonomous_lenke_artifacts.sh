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

if [ ! -f outputs/experiments/lenke_six_types.csv ]; then
    PYTHONPATH=src:scripts:scripts/experiments:scripts/data_management python3 scripts/experiments/experiment_lenke_classes.py
fi

# Generate text descriptions for paperbanana
cat << 'TXT' > jules_polygenic_stacking_lenke.txt
Polygenic Stacking Threshold Model for Adolescent Idiopathic Scoliosis (AIS).
The allometric trap creates a universal vulnerability window with a +5.3 ms baseline stability margin.
Individual-specific genetic variants (e.g., reduced damping from COL1A1, increased delay from PIEZO2, shifted Kd from LBX1, increased load from PAX1) each narrow the margin.
The combined polygenic trap flips the margin to -26.3 ms, explaining the 2-4% clinical prevalence.
TXT

cat << 'TXT' > jules_lenke_6_types_abstract.txt
Multi-segment Cosserat Rod Modeling of all 6 Lenke Curve Types.
Different Lenke types (1-6) emerge as distinct, dominant buckling eigenmodes dictated by spatial parameter variations:
- Main Thoracic (Type 1): Thoracic buckling dominates due to minimum rib cage buttressing.
- Double Thoracic (Type 2): Upper and main thoracic vulnerability.
- Double Major (Type 3): Coupled instability across the thoracic and lumbar segments.
- Triple Major (Type 4): Whole-spine cascade across three domains.
- Thoracolumbar/Lumbar (Type 5): Primary vulnerability concentrated at the thoracolumbar junction transition zone.
- Thoracolumbar/Lumbar - Main Thoracic (Type 6): Complex interactions between thoracic and thoracolumbar transition parameters.
These physical mechanisms map global allometric trap instability directly to specific 3D clinical morphologies.
TXT

# Generate conceptual diagrams
paperbanana generate --input jules_polygenic_stacking_lenke.txt --caption "Polygenic Threshold: The 2-4% Prevalence" --output research/figures/jules_polygenic_stacking_lenke.png

paperbanana generate --input jules_lenke_6_types_abstract.txt --caption "Multi-segment Cosserat Rod: 6 Lenke Curve Morphologies" --output research/figures/jules_lenke_6_types.png

# Generate data plots
paperbanana plot --data outputs/experiments/polygenic_stacking_results.csv --intent "Plot a bar chart mapping the Scenario to the X-axis and Stability Margin to the Y-axis. Highlight the Combined Polygenic Trap scenario." --output research/figures/plot_polygenic_stacking.png

paperbanana plot --data outputs/experiments/lenke_six_types.csv --intent "Plot a line chart mapping the Normalized Position to the X-axis and Type 1 through 6 eigenmodes to the Y-axis. Use distinct colors for each curve type." --output research/figures/jules_plot_lenke_6_types.png

echo "Autonomous Lenke artifacts generated."
