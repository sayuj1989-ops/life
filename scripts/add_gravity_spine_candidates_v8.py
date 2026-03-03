import csv
import os

MASTER_FILE = "data/candidates_master.csv"

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    new_candidates = [
        {
            "gene_symbol": "FGF8",
            "uniprot_id": "P55075",
            "organism": "Homo sapiens",
            "pathway_tags": "Segmentation,Somite,Signaling",
            "gravity_link": "Key morphogen regulating anterior-posterior axis and somite boundary formation; maintains the segmentation clock.",
            "spine_curvature_link": "Fgf8 signaling gradients determine somite size and symmetry; defects lead to severe vertebral malformations and congenital scoliosis. (PMID: 15469966)",
            "priority_score": "88",
            "justification": "Master regulator of vertebral segmentation and axis elongation."
        },
        {
            "gene_symbol": "SUFU",
            "uniprot_id": "Q9UMX1",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Signaling,Hedgehog",
            "gravity_link": "Major negative regulator of Hedgehog signaling, a pathway dependent on primary cilia (cellular gravity sensors).",
            "spine_curvature_link": "Mutations cause Gorlin syndrome (NBCCS) with characteristic skeletal anomalies, including rib and vertebral defects (scoliosis). (PMID: 10581030)",
            "priority_score": "85",
            "justification": "Key regulator in ciliary Hedgehog signaling linked to syndromic skeletal defects."
        },
        {
            "gene_symbol": "GLI1",
            "uniprot_id": "P08151",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Hedgehog,Development",
            "gravity_link": "Transcriptional effector of Hedgehog signaling, mediating cellular responses downstream of primary cilia mechanosensation.",
            "spine_curvature_link": "Essential for proper osteoblast differentiation and bone formation; dysregulation contributes to skeletal dysplasia and altered bone geometry. (PMID: 12692552)",
            "priority_score": "85",
            "justification": "Primary transcriptional effector of the mechanosensitive Hedgehog pathway."
        },
        {
            "gene_symbol": "AGRN",
            "uniprot_id": "O00468",
            "organism": "Homo sapiens",
            "pathway_tags": "Neuromuscular,ECM,Adhesion",
            "gravity_link": "Essential for neuromuscular junction (NMJ) formation and maintenance, required for postural muscle tone against gravity.",
            "spine_curvature_link": "Mutations cause congenital myasthenic syndromes with muscle weakness and secondary spinal deformities (scoliosis). (PMID: 24996465)",
            "priority_score": "88",
            "justification": "Critical for maintaining muscle tone and postural control."
        },
        {
            "gene_symbol": "SDC4",
            "uniprot_id": "P31431",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,ECM,Adhesion",
            "gravity_link": "Transmembrane heparan sulfate proteoglycan acting as a co-receptor for integrins, regulating focal adhesion assembly under tension.",
            "spine_curvature_link": "Modulates cellular responses to mechanical stress in cartilage and intervertebral discs; knockout alters load-induced matrix remodeling. (PMID: 18451786)",
            "priority_score": "85",
            "justification": "Mechanosensitive co-receptor essential for focal adhesion dynamics."
        },
        {
            "gene_symbol": "ACTG1",
            "uniprot_id": "P63261",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Mechanotransduction",
            "gravity_link": "Gamma-actin; essential component of the cytoskeletal network resisting cellular deformation and transmitting mechanical forces.",
            "spine_curvature_link": "Mutations cause Baraitser-Winter syndrome, featuring developmental delay, facial anomalies, and progressive scoliosis. (PMID: 22366783)",
            "priority_score": "85",
            "justification": "Core cytoskeletal component with strong syndromic links to scoliosis."
        },
        {
            "gene_symbol": "CDON",
            "uniprot_id": "Q4KMG0",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Hedgehog,Adhesion",
            "gravity_link": "Cell surface receptor functioning as a Hedgehog co-receptor; involved in myogenic differentiation and tissue patterning.",
            "spine_curvature_link": "Mutations cause holoprosencephaly; pathway disruption affects midline development and skeletal axis formation. (PMID: 16826533)",
            "priority_score": "82",
            "justification": "Hedgehog co-receptor linking cell adhesion to axis patterning."
        },
        {
            "gene_symbol": "PTPN14",
            "uniprot_id": "Q15678",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,Hippo,Adhesion",
            "gravity_link": "Non-receptor tyrosine phosphatase that interacts with YAP; regulates mechanotransduction by sequestering YAP at adherens junctions.",
            "spine_curvature_link": "Regulates osteoblast function; loss of function affects bone density and potentially spinal alignment. (PMID: 23142978)",
            "priority_score": "85",
            "justification": "Negative regulator of YAP/TAZ mechanosensing."
        },
        {
            "gene_symbol": "DOCK5",
            "uniprot_id": "Q9H7D0",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Bone,Adhesion",
            "gravity_link": "Atypical Rac1 GEF essential for osteoclast podosome organization and bone resorption under mechanical load.",
            "spine_curvature_link": "Dock5 knockout mice display increased bone mass and altered bone geometry, affecting vertebral mechanics. (PMID: 20436868)",
            "priority_score": "82",
            "justification": "Key regulator of osteoclast mechanics and bone density."
        },
        {
            "gene_symbol": "MMP9",
            "uniprot_id": "P14780",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Remodeling,Mechanotransduction",
            "gravity_link": "Gelatinase B; degrades ECM components (collagen IV, gelatin) in response to altered mechanical loading in connective tissues.",
            "spine_curvature_link": "Upregulated in scoliotic ligaments and intervertebral disc degeneration; drives pathological ECM remodeling and stiffness loss. (PMID: 11116246)",
            "priority_score": "85",
            "justification": "Mechanosensitive protease directly driving connective tissue remodeling in scoliosis."
        }
    ]

    existing_genes = set()
    with open(MASTER_FILE, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_genes.add(row['gene_symbol'])

    count = 0
    with open(MASTER_FILE, 'a', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["gene_symbol", "uniprot_id", "organism", "pathway_tags", "gravity_link", "spine_curvature_link", "priority_score", "justification"])
        # No header write, appending
        for c in new_candidates:
            if c['gene_symbol'] not in existing_genes:
                writer.writerow(c)
                count += 1
                print(f"Added {c['gene_symbol']}")
            else:
                print(f"Skipped {c['gene_symbol']} (already exists)")

    print(f"Added {count} new candidates.")

if __name__ == "__main__":
    main()