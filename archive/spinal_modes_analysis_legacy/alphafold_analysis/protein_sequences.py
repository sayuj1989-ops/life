"""
Protein Sequence Retrieval from UniProt

Retrieves protein sequences for ciliary proteins, HOX1, and PAX genes.
"""

import argparse
import requests
from pathlib import Path
from typing import List, Dict

# Target proteins for analysis
PROTEIN_TARGETS = {
    "ciliary": [
        "IFT88_HUMAN",   # Intraflagellar transport protein 88
        "KIF3A_HUMAN",   # Kinesin-like protein KIF3A
        "DNAH5_HUMAN",   # Dynein heavy chain 5
        "RPGR_HUMAN",    # Retinitis pigmentosa GTPase regulator
    ],
    "hox1": [
        "HXA1_HUMAN",    # Homeobox protein Hox-A1
        "HXB1_HUMAN",    # Homeobox protein Hox-B1
        "HXC1_HUMAN",    # Homeobox protein Hox-C1  
        "HXD1_HUMAN",    # Homeobox protein Hox-D1
    ],
    "pax": [
        "PAX1_HUMAN",    # Paired box protein Pax-1
        "PAX3_HUMAN",    # Paired box protein Pax-3
        "PAX6_HUMAN",    # Paired box protein Pax-6
        "PAX9_HUMAN",    # Paired box protein Pax-9
    ]
}

def fetch_uniprot_sequence(uniprot_id: str) -> Dict[str, str]:
    """Fetch protein sequence from UniProt"""
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        lines = response.text.strip().split('\n')
        header = lines[0]
        sequence = ''.join(lines[1:])
        
        return {
            "id": uniprot_id,
            "header": header,
            "sequence": sequence
        }
    except Exception as e:
        print(f"❌ Failed to fetch {uniprot_id}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Retrieve protein sequences from UniProt")
    parser.add_argument("--categories", default="ciliary,hox1,pax", 
                       help="Comma-separated categories (ciliary,hox1,pax)")
    parser.add_argument("--output", default="alphafold_analysis/sequences.fasta",
                       help="Output FASTA file")
    
    args = parser.parse_args()
    
    categories = args.categories.split(',')
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("🧬 Retrieving Protein Sequences from UniProt...")
    print("=" * 60)
    
    sequences = []
    for category in categories:
        if category not in PROTEIN_TARGETS:
            print(f"⚠️  Unknown category: {category}")
            continue
            
        print(f"\n📂 Category: {category.upper()}")
        for uniprot_id in PROTEIN_TARGETS[category]:
            print(f"   Fetching {uniprot_id}...", end=" ")
            result = fetch_uniprot_sequence(uniprot_id)
            if result:
                sequences.append(result)
                print(f"✅ ({len(result['sequence'])} aa)")
            else:
                print("❌")
    
    # Write FASTA file
    with open(output_path, 'w') as f:
        for seq in sequences:
            f.write(f"{seq['header']}\n")
            # Write sequence in 60-character lines
            for i in range(0, len(seq['sequence']), 60):
                f.write(f"{seq['sequence'][i:i+60]}\n")
    
    print(f"\n✅ Retrieved {len(sequences)} sequences")
    print(f"📁 Saved to: {output_path}")

if __name__ == "__main__":
    main()
