"""
BCC Research Protein Database
Comprehensive list of proteins relevant to Biological Countercurvature research
"""

# Proteins organized by functional category
BCC_PROTEINS = {
    # Developmental Patterning Genes (HOX cluster)
    "HOX": {
        "HOXA1": {"uniprot": "P49639", "gene": "HOXA1", "function": "Cervical vertebral identity"},
        "HOXA2": {"uniprot": "O43364", "gene": "HOXA2", "function": "Cervical patterning"},
        "HOXA3": {"uniprot": "O43365", "gene": "HOXA3", "function": "Cervical/thoracic boundary"},
        "HOXA4": {"uniprot": "Q00056", "gene": "HOXA4", "function": "Thoracic identity"},
        "HOXA5": {"uniprot": "P20719", "gene": "HOXA5", "function": "Thoracic patterning"},
        "HOXA7": {"uniprot": "P31268", "gene": "HOXA7", "function": "Thoracic identity"},
        "HOXA9": {"uniprot": "P31269", "gene": "HOXA9", "function": "Lumbar identity"},
        "HOXA10": {"uniprot": "P31260", "gene": "HOXA10", "function": "Lumbar/sacral boundary"},
        "HOXA11": {"uniprot": "P31270", "gene": "HOXA11", "function": "Sacral identity"},
        "HOXB1": {"uniprot": "P14653", "gene": "HOXB1", "function": "Cervical identity"},
        "HOXB2": {"uniprot": "P14652", "gene": "HOXB2", "function": "Cervical patterning"},
        "HOXB4": {"uniprot": "P17483", "gene": "HOXB4", "function": "Thoracic identity"},
        "HOXB5": {"uniprot": "P09067", "gene": "HOXB5", "function": "Thoracic patterning"},
        "HOXB6": {"uniprot": "P17509", "gene": "HOXB6", "function": "Thoracic identity"},
        "HOXB7": {"uniprot": "P09629", "gene": "HOXB7", "function": "Thoracic/lumbar boundary"},
        "HOXB8": {"uniprot": "P17481", "gene": "HOXB8", "function": "Lumbar identity"},
        "HOXB9": {"uniprot": "P17482", "gene": "HOXB9", "function": "Lumbar patterning"},
        "HOXC4": {"uniprot": "P09017", "gene": "HOXC4", "function": "Thoracic identity"},
        "HOXC6": {"uniprot": "P09630", "gene": "HOXC6", "function": "Thoracic identity"},
        "HOXC8": {"uniprot": "P31273", "gene": "HOXC8", "function": "Lumbar identity"},
        "HOXC9": {"uniprot": "P31274", "gene": "HOXC9", "function": "Lumbar identity"},
        "HOXC10": {"uniprot": "Q9NYD6", "gene": "HOXC10", "function": "Lumbar identity"},
        "HOXC11": {"uniprot": "O43248", "gene": "HOXC11", "function": "Sacral identity"},
        "HOXD1": {"uniprot": "Q9GZZ0", "gene": "HOXD1", "function": "Cervical identity"},
        "HOXD3": {"uniprot": "P31249", "gene": "HOXD3", "function": "Cervical/thoracic boundary"},
        "HOXD4": {"uniprot": "P09016", "gene": "HOXD4", "function": "Thoracic identity"},
        "HOXD8": {"uniprot": "P13378", "gene": "HOXD8", "function": "Lumbar identity"},
        "HOXD9": {"uniprot": "P28356", "gene": "HOXD9", "function": "Lumbar identity"},
        "HOXD10": {"uniprot": "P28358", "gene": "HOXD10", "function": "Lumbar/sacral boundary"},
        "HOXD11": {"uniprot": "P31277", "gene": "HOXD11", "function": "Sacral identity"},
        "HOXD12": {"uniprot": "P35452", "gene": "HOXD12", "function": "Sacral identity"},
        "HOXD13": {"uniprot": "P35453", "gene": "HOXD13", "function": "Sacral/caudal identity"},
    },
    # PAX Genes (Segmentation and vertebral identity)
    "PAX": {
        "PAX1": {
            "uniprot": "P15863",
            "gene": "PAX1",
            "function": "Sclerotome development, vertebral formation",
        },
        "PAX2": {
            "uniprot": "Q02962",
            "gene": "PAX2",
            "function": "Kidney development, segmentation",
        },
        "PAX3": {
            "uniprot": "P23760",
            "gene": "PAX3",
            "function": "Neural crest, somite development",
        },
        "PAX6": {
            "uniprot": "P26367",
            "gene": "PAX6",
            "function": "Eye development, neural patterning",
        },
        "PAX9": {
            "uniprot": "P55771",
            "gene": "PAX9",
            "function": "Pharyngeal arch, vertebral identity",
        },
    },
    # Mechanotransduction Proteins
    "MECHANOSENSITIVE": {
        "YAP1": {
            "uniprot": "P46937",
            "gene": "YAP1",
            "function": "Hippo pathway, mechanosensitive transcription",
        },
        "TAZ": {
            "uniprot": "Q9GZV5",
            "gene": "WWTR1",
            "function": "Hippo pathway, mechanosensitive transcription",
        },
        "PIEZO1": {
            "uniprot": "Q92508",
            "gene": "PIEZO1",
            "function": "Mechanosensitive ion channel",
        },
        "PIEZO2": {
            "uniprot": "Q9H5I5",
            "gene": "PIEZO2",
            "function": "Mechanosensitive ion channel",
        },
        "TRPV4": {
            "uniprot": "Q9HBA0",
            "gene": "TRPV4",
            "function": "Mechanosensitive calcium channel",
        },
        "INTEGRIN_B1": {
            "uniprot": "P05556",
            "gene": "ITGB1",
            "function": "Mechanotransduction, ECM sensing",
        },
        "VINCULIN": {
            "uniprot": "P18206",
            "gene": "VCL",
            "function": "Focal adhesion, force transmission",
        },
        "TALIN1": {
            "uniprot": "Q9Y490",
            "gene": "TLN1",
            "function": "Focal adhesion, mechanosensing",
        },
    },
    # Segmentation Clock Genes
    "SEGMENTATION": {
        "NOTCH1": {
            "uniprot": "P46531",
            "gene": "NOTCH1",
            "function": "Segmentation clock, somite formation",
        },
        "NOTCH2": {"uniprot": "Q04721", "gene": "NOTCH2", "function": "Segmentation clock"},
        "NOTCH3": {"uniprot": "Q9UM47", "gene": "NOTCH3", "function": "Segmentation clock"},
        "DLL1": {"uniprot": "O00548", "gene": "DLL1", "function": "Notch ligand, segmentation"},
        "DLL3": {"uniprot": "Q9NYJ7", "gene": "DLL3", "function": "Notch ligand, segmentation"},
        "HES1": {
            "uniprot": "Q14469",
            "gene": "HES1",
            "function": "Notch target, clock oscillation",
        },
        "HES7": {"uniprot": "Q9BYE0", "gene": "HES7", "function": "Segmentation clock oscillator"},
        "WNT3A": {"uniprot": "P56704", "gene": "WNT3A", "function": "Wnt signaling, segmentation"},
        "WNT5A": {"uniprot": "P41221", "gene": "WNT5A", "function": "Wnt signaling, morphogenesis"},
        "FGF8": {"uniprot": "P55075", "gene": "FGF8", "function": "FGF signaling, segmentation"},
        "FGF4": {"uniprot": "P08620", "gene": "FGF4", "function": "FGF signaling, growth"},
    },
    # Longevity and Stress Response (connected to mechanotransduction)
    "LONGEVITY": {
        "FOXO3": {
            "uniprot": "O43524",
            "gene": "FOXO3",
            "function": "Longevity, stress response, mechanosensitive",
        },
        "SIRT1": {"uniprot": "Q96EB6", "gene": "SIRT1", "function": "NAD+ deacetylase, longevity"},
        "KLOTHO": {
            "uniprot": "Q9UEF7",
            "gene": "KL",
            "function": "Anti-aging, calcium homeostasis",
        },
        "PGC1A": {"uniprot": "Q9UBK2", "gene": "PPARGC1A", "function": "Mitochondrial biogenesis"},
        "AMPK": {
            "uniprot": "Q13131",
            "gene": "PRKAA1",
            "function": "Energy sensing, mechanosensitive",
        },
    },
    # Extracellular Matrix and Structural Proteins
    "ECM": {
        "COL1A1": {
            "uniprot": "P02452",
            "gene": "COL1A1",
            "function": "Type I collagen, bone matrix",
        },
        "COL2A1": {
            "uniprot": "P02458",
            "gene": "COL2A1",
            "function": "Type II collagen, cartilage",
        },
        "FIBRONECTIN": {
            "uniprot": "P02751",
            "gene": "FN1",
            "function": "ECM protein, mechanosensing",
        },
        "LAMININ_A1": {
            "uniprot": "P25391",
            "gene": "LAMA1",
            "function": "Basement membrane, structure",
        },
    },
    # Transcription Factors and Co-activators
    "TRANSCRIPTION": {
        "SOX9": {
            "uniprot": "P48436",
            "gene": "SOX9",
            "function": "Chondrogenesis, vertebral development",
        },
        "RUNX2": {
            "uniprot": "Q13950",
            "gene": "RUNX2",
            "function": "Osteogenesis, bone development",
        },
        "TBX6": {"uniprot": "O95947", "gene": "TBX6", "function": "Somite specification"},
        "MESP2": {"uniprot": "Q0VG99", "gene": "MESP2", "function": "Somite segmentation"},
    },
    # Gravity Sensing and Gravitropism
    "GRAVITY": {
        "LAZY1": {
            "uniprot": "Q5XV40",
            "gene": "LAZY1",
            "function": "Plant gravitropism, PIN polarization",
        },
        "PIN3": {
            "uniprot": "Q9C5L7",
            "gene": "PIN3",
            "function": "Auxin transporter, gravity response",
        },
        "ARG1": {
            "uniprot": "P93005",
            "gene": "ARG1",
            "function": "Gravity signal transduction (DnaJ-like)",
        },
        "MCA1": {"uniprot": "Q8L7E9", "gene": "MCA1", "function": "Mechanosensitive Ca2+ channel"},
        "DRO1": {
            "uniprot": "Q9S771",
            "gene": "DRO1",
            "function": "Deeper rooting 1, root architecture",
        },
        "TAC1": {"uniprot": "F4IJ79", "gene": "TAC1", "function": "Tiller angle control 1"},
        "OC90": {
            "uniprot": "Q02509",
            "gene": "OC90",
            "function": "Otolith matrix protein 90, biomineralization",
        },
        "OTOLIN1": {"uniprot": "A6NHN0", "gene": "OTOL1", "function": "Otolith scaffold protein"},
        "OTOGLIN": {"uniprot": "Q6ZRI0", "gene": "OTOG", "function": "Otolith anchoring protein"},
        "COCHLIN": {
            "uniprot": "O43405",
            "gene": "COCH",
            "function": "Otolith matrix, crystal formation",
        },
    },
}


def get_all_proteins():
    """Get all proteins as a flat list"""
    all_proteins = []
    for category, proteins in BCC_PROTEINS.items():
        for name, info in proteins.items():
            all_proteins.append({"name": name, "category": category, **info})
    return all_proteins


def get_proteins_by_category(category: str):
    """Get proteins in a specific category"""
    return BCC_PROTEINS.get(category, {})


def get_proteins_by_function(function_keyword: str):
    """Search proteins by function keyword"""
    results = []
    for category, proteins in BCC_PROTEINS.items():
        for name, info in proteins.items():
            if function_keyword.lower() in info["function"].lower():
                results.append({"name": name, "category": category, **info})
    return results


if __name__ == "__main__":
    # Print summary
    print("🧬 BCC Research Protein Database")
    print("=" * 60)

    all_proteins = get_all_proteins()
    print(f"\n📊 Total proteins: {len(all_proteins)}")

    for category, proteins in BCC_PROTEINS.items():
        print(f"\n📂 {category}: {len(proteins)} proteins")
        for name, info in list(proteins.items())[:3]:  # Show first 3
            print(f"   - {name} ({info['gene']}): {info['function']}")
        if len(proteins) > 3:
            print(f"   ... and {len(proteins) - 3} more")

    print(f"\n✅ Database ready for AlphaFold analysis")



