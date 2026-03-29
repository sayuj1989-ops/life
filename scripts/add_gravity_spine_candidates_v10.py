import csv
import os

MASTER_FILE = "data/candidates_master.csv"

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    new_candidates = [
        {
            "gene_symbol": "TNC",
            "uniprot_id": "P24821",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Mechanotransduction",
            "gravity_link": "Highly mechanosensitive ECM protein that regulates tissue stiffness and responds to mechanical loading.",
            "spine_curvature_link": "Expression is mechanically regulated in the spine, particularly in disc degeneration and scoliotic loading patterns. (DOI: 10.1101/262717)",
            "priority_score": "85",
            "justification": "Mechanosensitive ECM protein regulating tissue stiffness."
        },
        {
            "gene_symbol": "THBS4",
            "uniprot_id": "P35443",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM,Mechanotransduction",
            "gravity_link": "Regulates ECM assembly and muscle-tendon attachment under load.",
            "spine_curvature_link": "Crucial for tendon mechanotransduction; disruption alters stress response in paraspinal tissues. (DOI: 10.1016/j.mod.2009.06.071)",
            "priority_score": "85",
            "justification": "Regulates ECM assembly and muscle-tendon attachment under load."
        },
        {
            "gene_symbol": "VCAN",
            "uniprot_id": "P13611",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM",
            "gravity_link": "Proteoglycan that provides compressive stiffness to tissues against gravity.",
            "spine_curvature_link": "Altered processing and bioactivity in cartilage and spinal discs under compressive loads. (DOI: 10.5204/thesis.eprints.135523)",
            "priority_score": "88",
            "justification": "Major proteoglycan providing compressive stiffness to tissues."
        },
        {
            "gene_symbol": "IQCB1",
            "uniprot_id": "Q15051",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Mechanotransduction",
            "gravity_link": "NPHP5; localizes to primary cilia and links to mechanosensory defects.",
            "spine_curvature_link": "Mutations cause ciliopathies; disrupted mechanosensory motile cilium formation links to spinal defects. (DOI: 10.1186/s13256-025-05655-8)",
            "priority_score": "85",
            "justification": "Ciliary transition zone protein linking to mechanosensory defects."
        },
        {
            "gene_symbol": "BMP2",
            "uniprot_id": "P12643",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Growth_Plate",
            "gravity_link": "Master regulator of bone formation, mechanically activated by strain.",
            "spine_curvature_link": "Essential for new bone formation and healing; mechanical strain dictates scoliotic progression via BMPs. (DOI: 10.7759/cureus.60292)",
            "priority_score": "88",
            "justification": "Master regulator of bone formation, mechanically activated."
        },
        {
            "gene_symbol": "FOXA2",
            "uniprot_id": "Q9Y261",
            "organism": "Homo sapiens",
            "pathway_tags": "Development,Notochord",
            "gravity_link": "Master regulator of notochord formation, establishing the primary mechanical axis.",
            "spine_curvature_link": "Notochord anomalies fundamentally disrupt mechanical loading, leading to congenital scoliosis. (DOI: 10.3410/f.742681863.793600670)",
            "priority_score": "88",
            "justification": "Master regulator of notochord formation, the primary mechanical axis."
        },
        {
            "gene_symbol": "SMO",
            "uniprot_id": "Q9NWM0",
            "organism": "Homo sapiens",
            "pathway_tags": "Signaling,Hedgehog,Cilia",
            "gravity_link": "Key transducer of Hedgehog signaling, which is dependent on ciliary mechanosensors.",
            "spine_curvature_link": "Ciliary dysfunction disrupts SMO signaling, causing asymmetrical vertebral growth. (DOI: 10.1186/2046-2530-4-s1-p35)",
            "priority_score": "90",
            "justification": "Transducer of Hedgehog signaling, dependent on ciliary mechanosensors."
        },
        {
            "gene_symbol": "IFT27",
            "uniprot_id": "Q9BW83",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Mechanotransduction",
            "gravity_link": "IFT complex B protein, essential for cilia formation and structural integrity.",
            "spine_curvature_link": "Impaired mechanotransduction in elongated primary cilia is a hallmark of Idiopathic Scoliosis. (DOI: 10.7554/elife.02419.022)",
            "priority_score": "88",
            "justification": "IFT complex B protein, essential for cilia formation."
        },
        {
            "gene_symbol": "IFT20",
            "uniprot_id": "Q8IY31",
            "organism": "Homo sapiens",
            "pathway_tags": "Cilia,Mechanotransduction",
            "gravity_link": "Links Golgi to cilia, essential for ciliary assembly and mechanosensing.",
            "spine_curvature_link": "Defects in mammalian intraflagellar transport are linked to sensory cilia dysfunction in scoliosis. (DOI: 10.1091/mbc.e06-02-0133)",
            "priority_score": "85",
            "justification": "IFT complex B protein, links Golgi to cilia."
        },
        {
            "gene_symbol": "CHSY1",
            "uniprot_id": "Q86X52",
            "organism": "Homo sapiens",
            "pathway_tags": "ECM",
            "gravity_link": "Synthesizes chondroitin sulfate, crucial for cartilage compressive resistance.",
            "spine_curvature_link": "Maintains biochemical composition and structural integrity of load-bearing cartilage under compression. (DOI: 10.1007/978-4-431-54240-7_73)",
            "priority_score": "85",
            "justification": "Synthesizes chondroitin sulfate, crucial for cartilage compressive resistance."
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
