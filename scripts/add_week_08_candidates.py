import pandas as pd
import re
from pathlib import Path

# Data for new candidates
new_candidates_data = [
    ["HDAC4", "P56524", "Homo sapiens", "Growth_Plate,Epigenetics,Mechanotransduction", "Nucleocytoplasmic shuttling regulated by mechanical compression in chondrocytes. (PMID: 15155919)", "Essential for growth plate maintenance; deletion leads to premature ossification and deformity.", 88, "Mechano-regulated repressor of chondrocyte hypertrophy."],
    ["TRPM7", "Q96QT4", "Homo sapiens", "Ion_Channel,Mechanotransduction,Kinase", "Mechanosensitive kinase/channel regulating cell adhesion. (DOI: 10.1016/j.cub.2010.03.027)", "Essential for skeletal development; zebrafish mutants have severe spinal curvature.", 88, "Direct link between ion channel kinase and spinal straightness."],
    ["COL12A1", "Q99715", "Homo sapiens", "ECM,Muscle", "FACIT collagen regulating fibril organization and tissue compliance. (DOI: 10.1002/humu.22487)", "Mutations cause myopathic Ehlers-Danlos with spinal deformities/contractures.", 85, "Structural collagen linking muscle/ECM mechanics to spine."],
    ["DYNC1H1", "Q14204", "Homo sapiens", "Cytoskeleton,Motor_Protein,Neuron", "Retrograde motor essential for neuronal survival and muscle innervation. (DOI: 10.1016/j.ajhg.2011.10.012)", "Mutations cause SMA-LED with congenital scoliosis/lordosis.", 85, "Motor protein essential for spinal neuromuscular integrity."],
    ["DMP1", "Q13316", "Homo sapiens", "Bone,Mechanotransduction,ECM", "Osteocyte mechanosensor; expression upregulates with load. (DOI: 10.1038/ng1895)", "Mutations cause ARHR; rickets/osteomalacia leads to spinal deformity.", 82, "Key bone mechanosensor preventing soft bone deformity."],
    ["SPP1", "P10451", "Homo sapiens", "ECM,Bone,Mechanotransduction", "Mechanosensitive matricellular protein; critical for osteoclast attachment. (PMID: 21975231)", "Polymorphisms linked to AIS severity; upregulated in scoliotic concave side.", 82, "Load-responsive ECM protein linked to AIS."],
    ["MAP1B", "P46821", "Homo sapiens", "Cytoskeleton,Proprioception", "Regulates microtubule dynamics in growing axons. (PMID: 11520922)", "Essential for proprioceptive neuron development; loss impairs spinal reflexes.", 82, "Cytoskeletal regulator of proprioceptive circuit formation."],
    ["GPC6", "Q9Y625", "Homo sapiens", "Signaling,ECM,Hedgehog", "Heparan sulfate proteoglycan modulating Hedgehog signaling. (DOI: 10.1016/j.ajhg.2009.09.006)", "Mutations cause Omodysplasia; GWAS hit for Bone Mineral Density and AIS.", 80, "Developmental regulator linked to skeletal dysplasia and AIS."],
    ["LMOD3", "Q0VAK6", "Homo sapiens", "Muscle,Cytoskeleton", "Actin nucleator essential for sarcomere organization. (DOI: 10.1016/j.ajhg.2014.09.004)", "Mutations cause Nemaline Myopathy with scoliosis.", 82, "Muscle structural protein linked to myopathic scoliosis."],
    ["KL", "Q9UEF7", "Homo sapiens", "Signaling,Aging,Bone", "Regulates phosphate homeostasis and aging; interacts with FGF23. (DOI: 10.1126/science.277.5334.1940)", "Deficiency leads to premature aging, kyphosis, and osteopenia.", 80, "Metabolic regulator of spine aging and kyphosis."],
    ["FGF23", "Q9GZV9", "Homo sapiens", "Signaling,Bone", "Regulates phosphate metabolism; produced by osteocytes under load. (DOI: 10.1038/ng0600-112)", "Excess leads to hypophosphatemic rickets and skeletal deformities.", 80, "Bone-derived hormone regulating skeletal mineralization."],
    ["SMARCA4", "P51532", "Homo sapiens", "Chromatin,Development", "Chromatin remodeling (SWI/SNF); regulates developmental gene expression. (DOI: 10.1038/ng.2219)", "Mutations cause Coffin-Siris syndrome, featuring scoliosis.", 80, "Epigenetic remodeler linked to syndromic scoliosis."],
    ["CHD7", "Q9P2D1", "Homo sapiens", "Chromatin,Neural_Crest", "Chromatin remodeling; essential for neural crest development. (DOI: 10.1038/ng1368)", "Mutations cause CHARGE syndrome, with high prevalence of scoliosis.", 80, "Neural crest regulator linked to syndromic spine defects."],
    ["KMT2D", "O14686", "Homo sapiens", "Chromatin,Development", "H3K4 methyltransferase; regulates enhancers. (DOI: 10.1038/ng.625)", "Mutations cause Kabuki syndrome; scoliosis is a common feature.", 80, "Histone methyltransferase linked to syndromic scoliosis."],
    ["ASPN", "Q9BXN1", "Homo sapiens", "ECM,Mechanotransduction", "SLRP; binds collagen and TGF-beta; regulates IVD height. (DOI: 10.1038/ng1502)", "Polymorphisms associated with Lumbar Disc Degeneration and potentially scoliosis.", 78, "ECM regulator of disc height and degeneration."],
    ["MEPE", "Q9NQ76", "Homo sapiens", "Bone,ECM", "ASARM peptide inhibits mineralization; osteocyte specific. (DOI: 10.1038/ng1350)", "Regulates bone mass; knockout mice have increased bone density.", 75, "Negative regulator of bone mineralization."],
    ["PHEX", "P78562", "Homo sapiens", "Bone,Enzyme", "Degrades ASARM peptides; regulates mineralization. (DOI: 10.1038/ng1095-207)", "Mutations cause XLH rickets with skeletal deformities.", 78, "Enzyme critical for bone stiffness vs deformity."],
    ["MATN3", "O15232", "Homo sapiens", "ECM,Cartilage", "Cartilage matrix adaptor; links collagen and proteoglycans. (DOI: 10.1038/ng701)", "Mutations cause Multiple Epiphyseal Dysplasia; spinal involvement.", 78, "Cartilage matrix component linking structure to dysplasia."],
    ["SPARC", "P09486", "Homo sapiens", "ECM,Bone", "Matricellular protein; regulates collagen assembly and calcification. (DOI: 10.1242/jcs.01865)", "Null mice develop osteopenia and disc degeneration.", 75, "Matricellular regulator of bone and disc quality."],
    ["THBS1", "P07996", "Homo sapiens", "ECM,Signaling", "Activates TGF-beta; matricellular response to injury/load. (PMID: 15621726)", "Regulates bone remodeling; deficiency leads to altered bone phenotype.", 75, "Matricellular activator of TGF-beta signaling."]
]

columns = ["gene_symbol", "uniprot_id", "organism", "pathway_tags", "gravity_link", "spine_curvature_link", "priority_score", "justification"]

def main():
    csv_path = Path("data/candidates_master.csv")
    md_path = Path("docs/candidate_registry.md")

    # 1. Load existing CSV
    print(f"Reading {csv_path}...")
    df = pd.read_csv(csv_path)

    # 2. Append new candidates
    # Check for duplicates based on gene_symbol
    existing_genes = set(df['gene_symbol'].astype(str).str.upper())
    new_rows = []
    for row in new_candidates_data:
        if row[0].upper() not in existing_genes:
            new_rows.append(row)
        else:
            print(f"Skipping duplicate: {row[0]}")

    if new_rows:
        new_df = pd.DataFrame(new_rows, columns=columns)
        df = pd.concat([df, new_df], ignore_index=True)
        print(f"Added {len(new_rows)} new candidates.")
    else:
        print("No new candidates to add.")

    # 3. Save updated CSV
    df.to_csv(csv_path, index=False)
    print(f"Updated {csv_path}")

    # 4. Sort by Priority Score
    df_sorted = df.sort_values(by="priority_score", ascending=False)

    # 5. Generate Markdown Table
    # Table headers: Rank | Gene Symbol | Score | Mechanism / Rationale | Gravity/Mechano Link
    md_table_lines = [
        "| Rank | Gene Symbol | Score | Mechanism / Rationale | Gravity/Mechano Link |",
        "|:----:|:-----------:|:-----:|:----------------------|:---------------------|"
    ]

    rank = 1
    for index, row in df_sorted.iterrows():
        # Clean text for markdown table (remove newlines if any)
        mechanism = str(row['justification']).replace('\n', ' ')
        link = str(row['gravity_link']).replace('\n', ' ')

        line = f"| {rank} | **{row['gene_symbol']}** | {row['priority_score']} | {mechanism} | {link} |"
        md_table_lines.append(line)
        rank += 1

    new_table_str = "\n".join(md_table_lines)

    # 6. Read and Update Markdown File
    print(f"Reading {md_path}...")
    with open(md_path, 'r') as f:
        md_content = f.read()

    # Regex to replace Last Updated
    # Pattern: ****Last Updated:** <content until newline>
    new_updated_line = "****Last Updated:** Week 8 Cycle - Gravity Expansion V (Added HDAC4, TRPM7, COL12A1, etc.)"
    md_content = re.sub(r'\*\*\*\*Last Updated:\*\*.*', new_updated_line, md_content)

    # Regex to replace Table
    # We find the table by looking for the header row and then consuming lines that start with | until we hit a non-table line
    # Actually, simpler to find the header and replace until "## Selection Methodology"

    # Locate the table start
    table_start_marker = "| Rank | Gene Symbol | Score | Mechanism / Rationale | Gravity/Mechano Link |"
    table_end_marker = "## Selection Methodology"

    start_idx = md_content.find(table_start_marker)
    end_idx = md_content.find(table_end_marker)

    if start_idx != -1 and end_idx != -1:
        # Check if there is a newline before Selection Methodology
        # We want to replace everything from start_idx to end_idx (exclusive of end_idx)
        # But we need to keep newlines clean

        pre_table = md_content[:start_idx]
        post_table = md_content[end_idx:]

        # Ensure consistent spacing
        new_content = pre_table + new_table_str + "\n\n" + post_table

        with open(md_path, 'w') as f:
            f.write(new_content)
        print(f"Updated {md_path}")
    else:
        print("Error: Could not locate table markers in markdown file.")

if __name__ == "__main__":
    main()
