#!/bin/bash
export PATH="/home/jules/self_created_tools/bin:$PATH"

mkdir -p research/figures

# 1. Polygenic Threshold Stacking
cat << 'TEXT' > research/figures/jules_polygenic_stacking_lenke.txt
The Biological Countercurvature framework reveals a baseline +5.3 ms stability margin for the generic human adolescent during peak height velocity. This creates a universal "Allometric Trap". However, the 2-4% clinical prevalence of Adolescent Idiopathic Scoliosis (AIS) is explained by the Polygenic Stacking Model. This visual demonstrates how individual-specific molecular parameters stack to erode the margin: Reduced damping b (COL1A1/COL2A1), Increased proprioceptive delay tau (PIEZO2/GPR126), Shifted structural demand K_d (LBX1), and Increased gravitational load mgL (PAX1). Each variant narrows the margin, but the combined scenario forcefully flips it to -26.3 ms, triggering Metabolic Buckling. The visual should be a bar or waterfall chart showing the systematic erosion of the stability margin from the safe zone (+5.3) deep into the unstable buckling regime (-26.3).
TEXT

paperbanana generate \
    --input research/figures/jules_polygenic_stacking_lenke.txt \
    --caption "Polygenic Stacking Model" \
    --output research/figures/jules_polygenic_stacking_lenke.png

# 2. Lenke Curve Multi-segment Cosserat Rod Prediction
cat << 'TEXT' > research/figures/jules_lenke_multi_segment.txt
The multi-segment Cosserat rod extension of the Biological Countercurvature theory predicts the six distinct Lenke curve types of Adolescent Idiopathic Scoliosis (AIS). The visual shows the spine not as a single inverted pendulum, but as a multi-segment rod with regional parameter variations: Regional stiffness EI(s) from thoracic rib cage buttressing, Segmental differences in proprioceptive delay tau(s) based on mechanoreceptor density, Local damping b(s) variations from disc composition, and Asymmetric loading from aortic pulsation. The global energy deficit triggers instability, but the *local* energy deficit profile determines the buckling eigenmode. For instance, Lenke Type 1 (Main Thoracic) emerges where the thoracic spine carries maximum moment arm over thinnest paraspinal muscle mass. The visual should illustrate the transition from a global temporal onset to regional spatial patterning, culminating in the distinct geometric forms of Lenke curves 1-6.
TEXT

paperbanana generate \
    --input research/figures/jules_lenke_multi_segment.txt \
    --caption "Lenke Curve Regionalization via Cosserat Rod" \
    --output research/figures/jules_lenke_multi_segment.png

echo "Autonomous Lenke and Polygenic Artifacts Generation Complete."
