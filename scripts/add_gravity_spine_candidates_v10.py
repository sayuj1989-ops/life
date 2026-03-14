import csv
import os

MASTER_FILE = "data/candidates_master.csv"

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    new_candidates = [
        {
            "gene_symbol": "MRTFA",
            "uniprot_id": "Q969V6",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,Transcription_Factor,Actin",
            "gravity_link": "Mechanosensitive transcription factor that translocates to the nucleus upon actin polymerization (high tension).",
            "spine_curvature_link": "Crucial for translating mechanical stress into gene expression; disrupted in load-bearing connective tissue disorders. (PMID: 25983245)",
            "priority_score": "88",
            "justification": "Primary nuclear relay for cytoskeletal tension and mechanotransduction."
        },
        {
            "gene_symbol": "SRF",
            "uniprot_id": "P11831",
            "organism": "Homo sapiens",
            "pathway_tags": "Mechanotransduction,Transcription_Factor,Actin",
            "gravity_link": "Serum response factor; binds MRTFA to activate genes essential for cytoskeletal stiffness against gravity.",
            "spine_curvature_link": "Essential for muscle and bone maintenance under load; conditional knockouts show severe myopathy and skeletal weakness. (PMID: 15312739)",
            "priority_score": "88",
            "justification": "Direct partner of MRTFA, essential for structural mechanotransduction."
        },
        {
            "gene_symbol": "TMC1",
            "uniprot_id": "Q8TDI8",
            "organism": "Homo sapiens",
            "pathway_tags": "Gravity_Sensing,Mechanotransduction,Ion_Channel",
            "gravity_link": "Forms the pore of the mechanotransduction channel in vestibular hair cells, sensing gravity and acceleration.",
            "spine_curvature_link": "Mutations cause profound deafness and vestibular dysfunction; vestibular defects are tightly linked to idiopathic scoliosis. (PMID: 11850618)",
            "priority_score": "90",
            "justification": "Direct mechanotransduction channel for vestibular gravity sensing."
        },
        {
            "gene_symbol": "TMC2",
            "uniprot_id": "Q8TDI7",
            "organism": "Homo sapiens",
            "pathway_tags": "Gravity_Sensing,Mechanotransduction,Ion_Channel",
            "gravity_link": "Functions redundantly with TMC1 in vestibular hair cell mechanotransduction (gravity sensing).",
            "spine_curvature_link": "Essential for early vestibular function and postural reflexes; vestibular areflexia models show spinal curvature. (PMID: 22015306)",
            "priority_score": "85",
            "justification": "Redundant/developmental mechanotransduction channel for vestibular gravity sensing."
        },
        {
            "gene_symbol": "ROCK2",
            "uniprot_id": "O21392",
            "organism": "Homo sapiens",
            "pathway_tags": "Cytoskeleton,Mechanotransduction,Contraction",
            "gravity_link": "Regulates actin-myosin contractility downstream of RhoA, driving cellular tension in response to gravity load.",
            "spine_curvature_link": "Elevated expression observed in scoliotic tissues; drives asymmetric contractility in paraspinal muscles. (PMID: 30065020)",
            "priority_score": "88",
            "justification": "Major effector of RhoA-mediated cytoskeletal tension and tissue stiffness."
        },
        {
            "gene_symbol": "TNC",
            "uniprot_id": "P24821",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Mechanotransduction,Development",
            "gravity_link": "Matricellular protein highly upregulated by mechanical stress and stretch in ligaments/tendons.",
            "spine_curvature_link": "Associated with intervertebral disc degeneration and altered mechanical loading in scoliosis. (PMID: 11116246)",
            "priority_score": "85",
            "justification": "Key mechanosensitive ECM protein upregulated in stressed spinal tissues."
        },
        {
            "gene_symbol": "BBS4",
            "uniprot_id": "Q96RK4",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Trafficking,Syndromic",
            "gravity_link": "Component of the BBSome; essential for ciliary transport of mechanosensitive channels (fluid flow/gravity).",
            "spine_curvature_link": "Mutations cause Bardet-Biedl syndrome, which has a significant prevalence of scoliosis and skeletal defects. (PMID: 17855360)",
            "priority_score": "85",
            "justification": "BBSome component linking ciliary trafficking to syndromic scoliosis."
        },
        {
            "gene_symbol": "GLI1",
            "uniprot_id": "P08151",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Hedgehog,Development",
            "gravity_link": "Transcriptional effector of Hedgehog signaling, entirely dependent on primary cilia (gravity/flow sensors).",
            "spine_curvature_link": "Essential for osteoblast differentiation and vertebral formation; dysregulation causes skeletal anomalies. (PMID: 10471507)",
            "priority_score": "88",
            "justification": "Major effector of the ciliary Hedgehog signaling axis."
        },
        {
            "gene_symbol": "WNT4",
            "uniprot_id": "P56705",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Wnt,Development",
            "gravity_link": "Non-canonical Wnt ligand responsive to mechanical load, driving osteogenesis and cell polarity.",
            "spine_curvature_link": "Mutations cause SERKAL syndrome and Mayer-Rokitansky-Kuster-Hauser syndrome, featuring vertebral anomalies. (PMID: 18335566)",
            "priority_score": "85",
            "justification": "Mechanosensitive Wnt ligand directly linked to syndromic vertebral defects."
        },
        {
            "gene_symbol": "PRG4",
            "uniprot_id": "Q92954",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Mechanotransduction,Lubrication",
            "gravity_link": "Lubricin; provides boundary lubrication in joints under high compressive gravity loads.",
            "spine_curvature_link": "Mutations cause Camptodactyly-arthropathy-coxa vara-pericarditis (CACP) syndrome, featuring joint failure and potential spinal stiffness. (PMID: 10471506)",
            "priority_score": "85",
            "justification": "Essential for mechanical lubrication of load-bearing facet joints in the spine."
        }
    ]

    existing_genes = set()
    with open(MASTER_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_genes.add(row['gene_symbol'].strip().upper())

    count = 0
    with open(MASTER_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["gene_symbol", "uniprot_id", "organism", "pathway_tags", "gravity_link", "spine_curvature_link", "priority_score", "justification"])
        for c in new_candidates:
            if c['gene_symbol'].strip().upper() not in existing_genes:
                c['priority_score'] = c['priority_score'].strip()
                writer.writerow(c)
                count += 1
                print(f"Added {c['gene_symbol']}")
            else:
                print(f"Skipped {c['gene_symbol']} (already exists)")

    print(f"Added {count} new candidates.")

if __name__ == "__main__":
    main()
