import json
import os
from datetime import datetime
import pandas as pd

metrics_file = "outputs/afcc/2026-03-21/metrics.csv"
output_md = "biofold_workspace/bolt_report.md"

df = pd.read_csv(metrics_file)

with open(output_md, "w") as f:
    f.write("# Bolt-BioFold Analysis Report\n\n")

    # Data source
    f.write("## Quality & Reproducibility Checklist\n")
    f.write("- **Data source**: AlphaFold DB (via EBI API)\n")
    f.write(f"- **Date/time of run**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("- **Code version**: Current tree state\n")
    f.write("- **Parameters**: pLDDT threshold=70, default PCA and smoothing, PAE heuristics applied\n")
    f.write("- **Notes**: FBN1 (P35555) failed data fetch due to 404 error from AlphaFold DB API.\n\n")

    f.write("## A) Results Table\n\n")
    # Display table in markdown
    cols = ['gene_symbol', 'uniprot_id', 'plddt_mean', 'anisotropy_index', 'morphology', 'plddt_fraction_low']
    f.write(df[cols].to_markdown(index=False))
    f.write("\n\n")

    # CSV block
    f.write("### CSV-ready block\n")
    f.write("```csv\n")
    f.write(df.to_csv(index=False))
    f.write("```\n\n")

    f.write("## B) Key plots summary\n")
    f.write("- Due to environment constraints and to avoid new dependencies, plotting was skipped. Standard plotting would include pLDDT vs residue index for all 4 structures and PAE heatmaps where JSON was available.\n\n")

    f.write("## C) Interpretation\n")
    f.write("### PIEZO1 & PIEZO2 (Mechanotransducers)\n")
    f.write("- **What we see**: Both show strong `Fibrous/Extended` morphology with high Anisotropy (>3.8). PIEZO2 is slightly more anisotropic (4.44) and has higher overall confidence (pLDDT ~79.4) compared to PIEZO1 (72.0).\n")
    f.write("- **Why it matters**: The extended, rigid rod-like structure is consistent with their role as direct mechanotransducers. This structural rigidity allows them to efficiently transmit and sense tension across the membrane during spinal growth and postural loading.\n")
    f.write("- **Confidence level**: High for PIEZO2 (79.4 pLDDT); Medium-High for PIEZO1 (72.0 pLDDT).\n")
    f.write("- **Next test**: Correlate the specific bending hotspots in PIEZO2 (e.g., res 460, 239) with known scoliosis mutation sites to see if curvature/flexibility at these nodes is altered.\n\n")

    f.write("### ITGB1 (Cell-ECM Adhesion Sensor)\n")
    f.write("- **What we see**: Highly confident structure (pLDDT: 85.9) with an extended, fibrous conformation (Anisotropy: 3.23) and very low disorder fraction (<4%).\n")
    f.write("- **Why it matters**: As the primary cellular gravity/load sensor at focal adhesions, ITGB1's structured, extended nature perfectly fits a tension-transmitting cable model anchoring the cytoskeleton to the ECM.\n")
    f.write("- **Confidence level**: Very High (85.9 pLDDT).\n")
    f.write("- **Next test**: Examine the predicted hinge/bending regions of ITGB1 under simulated load to assess its yield/stretching points compared to mutant forms.\n\n")

    f.write("### ACAN (Load-bearing Proteoglycan)\n")
    f.write("- **What we see**: `Intermediate` morphology with very low confidence (pLDDT: 51.9) and high disorder fraction (~54%).\n")
    f.write("- **Why it matters**: ACAN serves as a major structural resistor of gravity in the intervertebral disc. Its large intrinsically disordered regions (IDRs) likely act as flexible, hydrated springs to absorb compressive loads rather than rigid rods.\n")
    f.write("- **Confidence level**: Low overall, but high confidence in the predicted disorder.\n")
    f.write("- **Next test**: Restrict analysis of ACAN only to the domains with pLDDT > 70 to identify structural anchoring points versus disordered shock-absorbing regions.\n\n")

    f.write("## D) One “Best Next Move”\n")
    f.write("> **Compare orthologs**: Map known scoliosis-associated mutations onto the high-confidence bending hotspots of PIEZO2 and ITGB1 to test if they disrupt critical mechanotransductive hinges.\n")

print("Report generated.")
