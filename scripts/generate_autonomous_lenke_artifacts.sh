#!/bin/bash
export GEMINI_API_KEY="dummy"

# 1. Polygenic Stacking Visual
echo "The Allometric Trap is a universal vulnerability window during adolescent growth. The 2-4% prevalence of Adolescent Idiopathic Scoliosis (AIS) is driven by a Polygenic Threshold model. While the population baseline maintains a narrow +5.3 ms stability margin, the specific stacking of polygenic variants (e.g., COL1A1 reducing damping, PIEZO2 increasing delay to 96.4 ms, LBX1 shifting derivative gain, PAX1 increasing load) flips this margin to -26.3 ms, triggering metabolic buckling. This visual abstract should show a distribution curve or a stacking bar chart conceptually demonstrating how multiple small molecular changes push an individual past the universal critical threshold, with estrogen shifting the curve to explain the 8:1 female predominance." > jules_polygenic_stacking_lenke.txt

paperbanana generate --input jules_polygenic_stacking_lenke.txt --caption "Polygenic Stacking and the Allometric Trap" --output research/figures/jules_polygenic_stacking_lenke.png

# 2. Multi-Segment Cosserat Rod & Lenke Curves
echo "The spatial morphology of Adolescent Idiopathic Scoliosis (AIS) falls into 6 distinct Lenke curve types. The Biological Countercurvature framework predicts these shapes as emergent buckling eigenmodes of a multi-segment Cosserat rod. The spine's regions have varying stiffness (EI), neural delay (tau), and damping (b) due to factors like rib cage buttressing and paraspinal muscle mass. When the global stability threshold is breached, the deficit localization determines the primary buckling zone. A visual diagram showing the human spine mapped as a multi-segment Cosserat rod, highlighting localized regions of metabolic energy deficit and their corresponding Lenke curve type (e.g., Type 1 Main Thoracic, Type 5 Thoracolumbar), demonstrating upstream global trigger vs downstream spatial patterning." > jules_lenke_multi_segment.txt

paperbanana generate --input jules_lenke_multi_segment.txt --caption "Lenke Curves as Cosserat Rod Eigenmodes" --output research/figures/jules_lenke_multi_segment.png

echo "Autonomous Lenke & Polygenic artifacts generated in research/figures/."
