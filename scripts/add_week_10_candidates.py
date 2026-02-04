import csv
import os

MASTER_FILE = "data/candidates_master.csv"

new_candidates = [
    {
        "gene_symbol": "ITGA11",
        "uniprot_id": "Q9UKX5",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,ECM,Adhesion",
        "gravity_link": "Key sensor of collagen stiffness; essential for establishing tension in connective tissues (ligaments). (DOI: 10.1016/j.matbio.2018.02.008)",
        "spine_curvature_link": "Upregulated in scoliotic ligaments; drives fibrosis and stiffness asymmetry. (DOI: 10.1007/s00586-019-06008-6)",
        "priority_score": 88,
        "justification": "Major collagen receptor on fibroblasts; regulates myofibroblast differentiation and tissue stiffness."
    },
    {
        "gene_symbol": "LOXL2",
        "uniprot_id": "Q9Y4K0",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Enzyme,Mechanotransduction",
        "gravity_link": "Determines ECM stiffness, the primary resistance against gravity. (DOI: 10.1083/jcb.201402096)",
        "spine_curvature_link": "Upregulated in AIS concave side; promotes fibrosis and stiffness asymmetry. (DOI: 10.1038/s41598-017-09200-y)",
        "priority_score": 88,
        "justification": "Crosslinks collagen/elastin; regulated by hypoxia/mechanical stress."
    },
    {
        "gene_symbol": "CALM1",
        "uniprot_id": "P62158",
        "organism": "Homo sapiens",
        "pathway_tags": "Signaling,Mechanotransduction",
        "gravity_link": "Regulates muscle tone and intracellular calcium signaling downstream of mechanochannels. (PMID: 25866164)",
        "spine_curvature_link": "Calmodulin-Melatonin signaling defect is a classic hypothesis for AIS. (DOI: 10.1097/BPO.0000000000000523)",
        "priority_score": 82,
        "justification": "Calcium sensor; mediates melatonin signaling and mechanotransduction."
    },
    {
        "gene_symbol": "MMP14",
        "uniprot_id": "P50281",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Remodeling,Mechanotransduction",
        "gravity_link": "Essential for pericellular proteolysis required for cell migration and sensing stiffness. (DOI: 10.1016/j.devcel.2004.06.013)",
        "spine_curvature_link": "Essential for skeletal development; deficiency leads to severe skeletal anomalies. (DOI: 10.1016/S0092-8674(00)81262-4)",
        "priority_score": 85,
        "justification": "Membrane-tethered MMP; degrades ECM and processes signaling molecules."
    },
    {
        "gene_symbol": "COL22A1",
        "uniprot_id": "Q8NFW1",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Muscle,Adhesion",
        "gravity_link": "Stabilizes myotendinous junctions where force is transmitted. (DOI: 10.1074/jbc.M500473200)",
        "spine_curvature_link": "Associated with AIS susceptibility in some cohorts. (DOI: 10.1093/hmg/ddx178)",
        "priority_score": 80,
        "justification": "FACIT collagen at tissue junctions; force transmission."
    },
    {
        "gene_symbol": "SPARC",
        "uniprot_id": "P09486",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Bone,Mechanotransduction",
        "gravity_link": "Modulates cell-matrix interactions and bone remodeling under load. (DOI: 10.1359/jbmr.0301227)",
        "spine_curvature_link": "Decreased expression linked to disc degeneration; variants potentially linked to AIS. (DOI: 10.1016/j.spinee.2013.06.014)",
        "priority_score": 82,
        "justification": "Matricellular protein regulating collagen assembly and calcification."
    },
    {
        "gene_symbol": "THBS1",
        "uniprot_id": "P07996",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Signaling,Mechanotransduction",
        "gravity_link": "Mechanosensitive release of TGF-beta; regulates tissue remodeling. (DOI: 10.1038/nature13650)",
        "spine_curvature_link": "Polymorphisms associated with IVD degeneration. (DOI: 10.1002/jor.20683)",
        "priority_score": 80,
        "justification": "Matricellular protein; activates TGF-beta in response to stress."
    },
    {
        "gene_symbol": "ADAMTS4",
        "uniprot_id": "O75173",
        "organism": "Homo sapiens",
        "pathway_tags": "ECM,Remodeling",
        "gravity_link": "Load-induced degradation of IVD matrix. (DOI: 10.1016/j.biocel.2010.03.016)",
        "spine_curvature_link": "Major driver of disc degeneration and height loss. (DOI: 10.1002/art.24522)",
        "priority_score": 85,
        "justification": "Degrades aggrecan (shock absorber) under mechanical load."
    },
    {
        "gene_symbol": "PAX3",
        "uniprot_id": "P23760",
        "organism": "Homo sapiens",
        "pathway_tags": "Development,Muscle,Neural_Crest",
        "gravity_link": "Essential for paraspinal muscle development. (DOI: 10.1242/dev.01529)",
        "spine_curvature_link": "Mutations cause Waardenburg syndrome (sometimes spinal defects). (DOI: 10.1038/ng0594-53)",
        "priority_score": 85,
        "justification": "Myogenesis and neural crest regulator; essential for muscle patterning."
    },
    {
        "gene_symbol": "IFT172",
        "uniprot_id": "Q9UG01",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Transport",
        "gravity_link": "Ciliary transport; essential for ciliary structure and signaling (flow sensing). (DOI: 10.1016/j.cub.2005.11.066)",
        "spine_curvature_link": "Mutations cause Jeune syndrome (Asphyxiating thoracic dystrophy) - skeletal defects. (DOI: 10.1016/j.ajhg.2010.04.017)",
        "priority_score": 85,
        "justification": "IFT complex B component linked to skeletal ciliopathies."
    },
    {
        "gene_symbol": "DYNC2H1",
        "uniprot_id": "Q8NCM8",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Motor_Protein,Transport",
        "gravity_link": "Ciliary retrograde transport; maintenance of ciliary mechanosensors. (DOI: 10.1083/jcb.201407008)",
        "spine_curvature_link": "Mutations cause Short-rib polydactyly syndrome and Jeune syndrome. (DOI: 10.1038/ng.2446)",
        "priority_score": 85,
        "justification": "Cytoplasmic dynein 2 heavy chain essential for IFT."
    },
    {
        "gene_symbol": "INPP5E",
        "uniprot_id": "Q9NRR6",
        "organism": "Homo sapiens",
        "pathway_tags": "Cilia,Signaling,Lipid",
        "gravity_link": "Regulates ciliary membrane composition (phosphoinositides) for signaling. (DOI: 10.1038/ncb1933)",
        "spine_curvature_link": "Mutations cause Joubert syndrome (ciliopathy with potential spine issues). (DOI: 10.1038/ng.413)",
        "priority_score": 82,
        "justification": "Ciliary phosphoinositide phosphatase essential for ciliary stability."
    },
    {
        "gene_symbol": "ANXA6",
        "uniprot_id": "P08133",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,Membrane,Repair",
        "gravity_link": "Responds to plasma membrane injury from mechanical stress. (DOI: 10.1152/ajpcell.00247.2005)",
        "spine_curvature_link": "Chondrocyte mechanotransduction and potential matrix maintenance. (PMID: 23625345)",
        "priority_score": 75,
        "justification": "Membrane repair and vesicle trafficking in response to load."
    },
    {
        "gene_symbol": "GPR68",
        "uniprot_id": "Q15743",
        "organism": "Homo sapiens",
        "pathway_tags": "Mechanotransduction,Signaling,pH",
        "gravity_link": "Senses flow and pH changes in loaded tissues (proton sensing). (DOI: 10.1038/nature09163)",
        "spine_curvature_link": "Expressed in osteoclasts/blasts, regulates pH sensing in bone remodeling. (DOI: 10.1002/jbmr.1742)",
        "priority_score": 78,
        "justification": "Proton-sensing GPCR that is also mechanosensitive."
    },
    {
        "gene_symbol": "SNAI1",
        "uniprot_id": "O95863",
        "organism": "Homo sapiens",
        "pathway_tags": "Development,EMT,Fibrosis",
        "gravity_link": "Mechanically induced during fibrosis; responds to tissue stiffness. (DOI: 10.1038/ncb2390)",
        "spine_curvature_link": "Driver of fibrosis in scoliosis (concave side); promotes EMT. (DOI: 10.1007/s00586-018-5696-6)",
        "priority_score": 80,
        "justification": "Transcription factor regulating EMT and fibrosis under mechanical stress."
    }
]

def main():
    if not os.path.exists(MASTER_FILE):
        print(f"Error: {MASTER_FILE} not found.")
        return

    # Read existing
    existing_symbols = set()
    with open(MASTER_FILE, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            existing_symbols.add(row['gene_symbol'])

    # Append new
    with open(MASTER_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        count = 0
        for cand in new_candidates:
            if cand['gene_symbol'] in existing_symbols:
                print(f"Skipping {cand['gene_symbol']} (already exists)")
                continue

            writer.writerow(cand)
            print(f"Added {cand['gene_symbol']}")
            count += 1

    print(f"Successfully added {count} new candidates.")

if __name__ == "__main__":
    main()
