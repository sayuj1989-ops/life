"""
Investigate Not Found Proteins
Check for alternate UniProt IDs, isoforms, or reasons why structures aren't in AlphaFold
"""

import urllib.parse
import urllib.request
import json
from pathlib import Path
from typing import Dict, Optional, List

ALPHAFOLD_API_BASE = "https://alphafold.ebi.ac.uk/api/prediction"
UNIPROT_API_BASE = "https://rest.uniprot.org/uniprotkb"
UNIPROT_SEARCH_FIELDS = "accession,id,protein_name,reviewed"

# Proteins not found in AlphaFold
NOT_FOUND_PROTEINS = {
    "HOXA2": "O43364",
    "HOXA3": "O43365",
    "HOXA11": "P31270",
    "HOXB7": "P09629",
    "HOXB8": "P17481",
    "HOXC9": "P31274",
    "HOXD3": "P31249",
    "HOXD9": "P28356",
    "HOXD11": "P31277",
    "HOXD13": "P35453",
    "NOTCH1": "P46531",
    "FGF4": "P08620",
}

def check_alphafold(uniprot_id: str) -> Optional[Dict]:
    """Check if protein exists in AlphaFold"""
    api_url = f"{ALPHAFOLD_API_BASE}/{uniprot_id}"
    try:
        with urllib.request.urlopen(api_url, timeout=10) as response:
            data = json.loads(response.read().decode())
            if data and len(data) > 0:
                return data[0]
    except:
        pass
    return None

def parse_uniprot_tsv(tsv_data: str) -> List[Dict[str, str]]:
    """Parse UniProt TSV response into a list of row dicts"""
    lines = [line for line in tsv_data.splitlines() if line.strip()]
    if len(lines) < 2:
        return []
    header = lines[0].split('\t')
    rows = []
    for line in lines[1:]:
        rows.append(dict(zip(header, line.split('\t'))))
    return rows

def search_uniprot_by_gene(gene_name: str, exclude_accession: str) -> List[Dict[str, str]]:
    """Search UniProt for alternate entries by gene name"""
    def query(reviewed: bool) -> List[Dict[str, str]]:
        query_parts = [f"gene:{gene_name}", "organism_id:9606"]
        if reviewed:
            query_parts.append("reviewed:true")
        params = {
            "query": " AND ".join(query_parts),
            "format": "tsv",
            "fields": UNIPROT_SEARCH_FIELDS,
            "size": 10,
        }
        url = f"{UNIPROT_API_BASE}/search?{urllib.parse.urlencode(params)}"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read().decode()
        return parse_uniprot_tsv(data)

    rows = query(reviewed=True)
    if not rows:
        rows = query(reviewed=False)

    results = []
    for row in rows:
        accession = row.get("Entry")
        if not accession or accession == exclude_accession:
            continue
        results.append({
            "accession": accession,
            "entry_name": row.get("Entry Name", ""),
            "protein_name": row.get("Protein names", ""),
            "reviewed": row.get("Reviewed", ""),
        })
    return results

def check_uniprot_isoforms(uniprot_id: str) -> Dict[str, object]:
    """Check for alternative isoforms and secondary accessions in UniProt"""
    url = f"{UNIPROT_API_BASE}/{uniprot_id}.json"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            # Check for alternative products/isoforms
            isoforms = []
            for comment in data.get("comments", []):
                if comment.get("commentType") in ["ALTERNATIVE_PRODUCTS", "ALTERNATIVE PRODUCTS"]:
                    for isoform in comment.get("isoforms", []):
                        isoform_ids = isoform.get("isoformIds", []) or []
                        name = isoform.get("name", {}).get("value") if isoform.get("name") else ""
                        isoforms.append({
                            "isoform_ids": isoform_ids,
                            "name": name,
                            "sequence_status": isoform.get("sequenceStatus", ""),
                        })
            
            # Check gene name and search for related entries
            gene_name = None
            if "genes" in data and len(data["genes"]) > 0:
                gene_name = data["genes"][0].get("geneName", {}).get("value")
            
            return {
                "gene_name": gene_name,
                "entry_name": data.get("entryName"),
                "protein_name": data.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", ""),
                "length": data.get("sequence", {}).get("length", 0),
                "secondary_accessions": data.get("secondaryAccessions", []),
                "isoforms": isoforms,
            }
    except Exception as e:
        return {"error": str(e)}
    return {}

def main():
    print("🔍 Investigating Not Found Proteins in AlphaFold")
    print("=" * 70)
    print()
    
    results = {}
    
    for name, uniprot_id in NOT_FOUND_PROTEINS.items():
        print(f"📊 {name} ({uniprot_id})")
        alternate_entries = []
        alphafold_candidates = []
        
        # Check AlphaFold
        af_result = check_alphafold(uniprot_id)
        if af_result:
            print(f"   ✅ Found in AlphaFold!")
            results[name] = {"status": "found", "alphafold": af_result}
        else:
            print(f"   ❌ Not in AlphaFold")
            
            # Check UniProt for info
            print(f"   🔍 Checking UniProt...", end=" ")
            uniprot_info = check_uniprot_isoforms(uniprot_id)
            if "error" not in uniprot_info:
                print("✅")
                print(f"      Gene: {uniprot_info.get('gene_name', 'N/A')}")
                print(f"      Length: {uniprot_info.get('length', 0)} aa")
                print(f"      Name: {uniprot_info.get('protein_name', 'N/A')[:60]}")
                isoforms = uniprot_info.get("isoforms", [])
                if isoforms:
                    isoform_ids = [iso_id for iso in isoforms for iso_id in iso.get("isoform_ids", [])]
                    print(f"      Isoforms: {', '.join(isoform_ids[:5])}")
                secondary = uniprot_info.get("secondary_accessions", [])
                if secondary:
                    print(f"      Secondary accessions: {', '.join(secondary[:5])}")

                if uniprot_info.get("gene_name"):
                    alternate_entries = search_uniprot_by_gene(uniprot_info["gene_name"], uniprot_id)
                    if alternate_entries:
                        print("      Alternate UniProt entries:")
                        for entry in alternate_entries[:5]:
                            print(f"         - {entry['accession']} ({entry['entry_name']})")
                # Check AlphaFold for a few alternate IDs/isoforms
                candidate_ids = []
                candidate_ids.extend([iso_id for iso in isoforms for iso_id in iso.get("isoform_ids", [])])
                candidate_ids.extend([entry.get("accession") for entry in alternate_entries])
                candidate_ids.extend(secondary)
                candidate_ids = [c for c in dict.fromkeys(candidate_ids) if c and c != uniprot_id]
                alphafold_candidates = []
                for candidate in candidate_ids[:5]:
                    if check_alphafold(candidate):
                        alphafold_candidates.append(candidate)
                if alphafold_candidates:
                    print(f"      AlphaFold candidates: {', '.join(alphafold_candidates)}")
            else:
                print(f"❌ {uniprot_info['error']}")
            
            results[name] = {
                "status": "not_found",
                "uniprot_id": uniprot_id,
                "uniprot_info": uniprot_info,
                "alternate_entries": alternate_entries,
                "alphafold_candidates": alphafold_candidates,
            }
        
        print()
    
    # Summary
    print("=" * 70)
    print("📊 Summary")
    print("=" * 70)
    
    found = sum(1 for r in results.values() if r.get("status") == "found")
    not_found = len(results) - found
    
    print(f"✅ Found in AlphaFold: {found}/{len(results)}")
    print(f"❌ Not found: {not_found}/{len(results)}")
    
    if not_found > 0:
        print("\n💡 Possible reasons for not found:")
        print("   - Very short proteins (< 30 aa)")
        print("   - Disordered regions (low confidence)")
        print("   - Membrane proteins (limited coverage)")
        print("   - Very large proteins (> 2700 aa)")
        print("   - Alternative isoforms needed")
        print("\n💡 Solutions:")
        print("   - Check for alternative UniProt isoforms")
        print("   - Use experimental structures if available")
        print("   - Skip in analysis (already handled)")
    
    # Save results
    output_file = Path("alphafold_analysis/metadata/not_found_investigation.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Results saved: {output_file}")

if __name__ == "__main__":
    main()





