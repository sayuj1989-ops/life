import csv
import os

MASTER_FILE = "data/candidates_master.csv"
DOC_FILE = "docs/candidate_registry.md"

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    candidates = []
    with open(MASTER_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['priority_score'] = int(row['priority_score'])
            except ValueError:
                continue # Skip invalid scores
            candidates.append(row)

    # Filter and Sort
    priority_candidates = [c for c in candidates if c['priority_score'] >= 85]
    priority_candidates.sort(key=lambda x: x['priority_score'], reverse=True)

    # Generate Markdown
    with open(DOC_FILE, 'w') as f:
        f.write("# Candidate Registry\n\n")
        f.write("****Last Updated:** Week 14 Cycle - Gravity x Spine Expansion\n")
        f.write("**Focus:** Gravity, Mechanotransduction, and Spinal Curvature\n\n")
        f.write("This registry tracks high-priority gene and protein candidates identified as relevant to the \"Biological Counter-Curvature\" hypothesis. Candidates are scored based on their relevance to:\n")
        f.write("1.  **Gravity/Mechanotransduction**: Ability to sense or resist physical forces.\n")
        f.write("2.  **Spinal Curvature**: Genetic or experimental links to scoliosis or vertebral defects.\n")
        f.write("3.  **Developmental Role**: Involvement in key spinal formation pathways (Somites, PCP, Cilia).\n\n")

        f.write("## Priority Candidates (Score >= 85)\n\n")
        f.write("| Rank | Gene Symbol | Score | Mechanism / Rationale | Gravity/Mechano Link |\n")
        f.write("|:----:|:-----------:|:-----:|:----------------------|:---------------------|\n")

        for i, c in enumerate(priority_candidates, 1):
            # Parse tags to find primary mechanism
            tags = c['pathway_tags'].split(',')
            mechanism = tags[0].strip() if tags else "Unknown"

            # Format rationale with mechanism bolded
            rationale_text = f"**{mechanism}**: {c['justification']}"

            f.write(f"| {i} | **{c['gene_symbol']}** | {c['priority_score']} | {rationale_text} | {c['gravity_link']} |\n")

        f.write("\n## Selection Methodology\n\n")
        f.write("Candidates were selected based on a \"Gravity x Curvature\" cross-referencing strategy:\n")
        f.write("*   **Seed Categories**: Mechanotransduction, Cilia/PCP, Somite Segmentation, Growth Plate.\n")
        f.write("*   **Expansion Criteria**: Direct literature evidence connecting the gene to both mechanical sensing/response and spinal alignment defects (Scoliosis, Kyphosis, AIS).\n")
        f.write("*   **Scoring**:\n")
        f.write("    *   **90-100**: Proven causative gene for Scoliosis with direct mechanotransduction role.\n")
        f.write("    *   **80-89**: Strong association with Scoliosis and clear mechanobiological function.\n")
        f.write("    *   **70-79**: Pathway member with experimental links to spine development or gravity response.\n\n")

        f.write("## Next Steps\n\n")
        f.write("1.  **AlphaFold Analysis**: Run the \"Bolt-BioFold\" pipeline on the top new candidates (PCDH15, USH1C) to assess structural anisotropy.\n")
        f.write("2.  **ECM Dynamics**: Investigate the role of load-induced degradative enzymes (MMP13, ADAMTS5) in the `CounterCurvatureRodSystem` remodeling term.\n")
        f.write("3.  **Simulation**: Investigate the role of FLNA/Actin-mediated cytoskeletal stiffness in the `pyelastica` rod models.\n")
        f.write("4.  **Literature Review**: Deep dive into the \"Cilia Motility\" mechanism for RSPH1 and DNAI1.\n")

    print(f"Successfully regenerated {DOC_FILE}")

if __name__ == "__main__":
    main()
