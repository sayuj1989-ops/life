"""
Refresh AlphaFold Structures for Corrected UniProt IDs

This script re-fetches structures for proteins whose UniProt IDs were corrected
in the database verification process.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from alphafold_analysis.fetch_bcc_structures import fetch_protein_structure
from alphafold_analysis.bcc_protein_database import BCC_PROTEINS

# Proteins with corrected UniProt IDs
CORRECTED_PROTEINS = {
    "HOX": [
        "HOXA2",  # O43364
        "HOXA3",  # O43365
        "HOXA4",  # Q00056
        "HOXB4",  # P17483
        "HOXB5",  # P09067
        "HOXC4",  # P09017
        "HOXC10", # Q9NYD6
        "HOXC11", # O43248
        "HOXD10", # P28358
        "HOXD12", # P35452
    ],
    "SEGMENTATION": [
        "DLL3",   # Q9NYJ7
    ],
    "TRANSCRIPTION": [
        "MESP2",  # Q0VG99
    ],
}

def main():
    print("🔄 Refreshing AlphaFold Structures for Corrected UniProt IDs")
    print("=" * 70)
    print()
    
    all_proteins_to_refresh = []
    
    for category, protein_names in CORRECTED_PROTEINS.items():
        category_proteins = BCC_PROTEINS.get(category, {})
        for name in protein_names:
            if name in category_proteins:
                protein_info = category_proteins[name]
                all_proteins_to_refresh.append({
                    "name": name,
                    "category": category,
                    **protein_info
                })
    
    print(f"📊 Found {len(all_proteins_to_refresh)} proteins to refresh\n")
    
    results = []
    for i, protein in enumerate(all_proteins_to_refresh, 1):
        print(f"[{i}/{len(all_proteins_to_refresh)}] {protein['name']} ({protein['gene']})")
        print(f"   UniProt: {protein['uniprot']}")
        
        # Force re-download
        result = fetch_protein_structure(protein, force_refresh=True)
        results.append(result)
        
        status_icon = "✅" if result["status"] in ["downloaded", "cached"] else "❌"
        print(f"   {status_icon} Status: {result['status']}\n")
    
    # Summary
    print("=" * 70)
    print("📊 Summary")
    print("=" * 70)
    
    successful = sum(1 for r in results if r["status"] in ["downloaded", "cached"])
    failed = len(results) - successful
    
    print(f"✅ Successfully refreshed: {successful}/{len(results)}")
    if failed > 0:
        print(f"❌ Failed: {failed}/{len(results)}")
        print("\nFailed proteins:")
        for r in results:
            if r["status"] not in ["downloaded", "cached"]:
                print(f"   - {r['name']}: {r['status']}")
    
    print("\n💡 Next step: Run analysis with corrected structures:")
    print("   python3 alphafold_analysis/analyze_bcc_structures.py")

if __name__ == "__main__":
    main()






