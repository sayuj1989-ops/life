"""
Fetch AlphaFold Structures for BCC Research
Downloads protein structures from AlphaFold Database API
"""

import urllib.request
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import time

# Import protein database
from bcc_protein_database import BCC_PROTEINS, get_all_proteins

ALPHAFOLD_API_BASE = "https://alphafold.ebi.ac.uk/api/prediction"
OUTPUT_DIR = Path("alphafold_analysis/predictions")
METADATA_DIR = Path("alphafold_analysis/metadata")


def fetch_alphafold_metadata(uniprot_id: str) -> Optional[Dict]:
    """Fetch metadata for a protein from AlphaFold API"""
    api_url = f"{ALPHAFOLD_API_BASE}/{uniprot_id}"

    def try_version_guess(uid):
        print(f"   📡 Attempting direct version guess for {uid}...")
        for version in ["v6", "v4", "v3", "v2", "v1"]:
            pdb_url = f"https://alphafold.ebi.ac.uk/files/AF-{uid}-F1-model_{version}.pdb"
            try:
                req = urllib.request.Request(pdb_url, method="HEAD")
                with urllib.request.urlopen(req, timeout=10) as resp:
                    if resp.status == 200:
                        print(f"   ✅ Found version {version} via direct guess")
                        return {
                            "uniprot_id": uid,
                            "pdb_url": pdb_url,
                            "cif_url": f"https://alphafold.ebi.ac.uk/files/AF-{uid}-F1-model_{version}.cif",
                            "confidence_url": f"https://alphafold.ebi.ac.uk/files/AF-{uid}-F1-confidence_{version}.json",
                            "model_url": pdb_url,
                            "model_confidence": None,
                            "uniprot_accession": uid,
                            "uniprot_id_api": uid,
                            "guessed_version": version
                        }
            except Exception:
                continue
        return None

    try:
        try:
            with urllib.request.urlopen(api_url, timeout=30) as response:
                data = json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return try_version_guess(uniprot_id)
            raise e

        if not data or len(data) == 0:
            return try_version_guess(uniprot_id)

        # Get the first entry (usually canonical isoform)
        entry = data[0]
        return {
            "uniprot_id": uniprot_id,
            "pdb_url": entry.get("pdbUrl"),
            "cif_url": entry.get("cifUrl"),
            "confidence_url": entry.get("confidenceUrl"),
            "model_url": entry.get("modelUrl"),
            "model_confidence": entry.get("modelConfidence"),
            "uniprot_accession": entry.get("uniprotAccession"),
            "uniprot_id_api": entry.get("uniprotId"),
        }
    except Exception as e:
        print(f"   ⚠️  API error: {e}")
        return None


def download_pdb(pdb_url: str, output_path: Path) -> bool:
    """Download PDB file from URL"""
    try:
        with urllib.request.urlopen(pdb_url, timeout=60) as response, open(output_path, "wb") as f:
            f.write(response.read())
        return True
    except Exception as e:
        print(f"   ⚠️  Download error: {e}")
        return False


def fetch_protein_structure(protein: Dict, force_refresh: bool = False) -> Dict:
    """Fetch structure for a single protein"""
    name = protein["name"]
    uniprot_id = protein["uniprot"]
    category = protein["category"]

    output_path = OUTPUT_DIR / f"{name}.pdb"
    metadata_path = METADATA_DIR / f"{name}_metadata.json"

    result = {
        "name": name,
        "uniprot_id": uniprot_id,
        "category": category,
        "gene": protein.get("gene", ""),
        "function": protein.get("function", ""),
        "status": "unknown",
        "pdb_path": str(output_path) if output_path.exists() else None,
        "metadata_path": str(metadata_path) if metadata_path.exists() else None,
    }

    # Check if already downloaded
    if output_path.exists() and not force_refresh:
        print(f"   ✅ Already exists: {output_path.name}")
        result["status"] = "cached"
        return result

    # Fetch metadata
    print(f"   📡 Fetching metadata...", end=" ")
    metadata = fetch_alphafold_metadata(uniprot_id)

    if not metadata:
        print("❌ Not found in AlphaFold DB")
        result["status"] = "not_found"
        return result

    if not metadata.get("pdb_url"):
        print("❌ No PDB URL")
        result["status"] = "no_pdb"
        return result

    # Save metadata
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    # Download PDB
    print(f"📥 Downloading PDB...", end=" ")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if download_pdb(metadata["pdb_url"], output_path):
        print("✅")
        result["status"] = "downloaded"
        result["pdb_path"] = str(output_path)
        result["metadata_path"] = str(metadata_path)
    else:
        print("❌")
        result["status"] = "download_failed"

    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch AlphaFold structures for BCC research proteins"
    )
    parser.add_argument(
        "--category",
        choices=[
            "HOX",
            "PAX",
            "MECHANOSENSITIVE",
            "SEGMENTATION",
            "LONGEVITY",
            "ECM",
            "TRANSCRIPTION",
            "GRAVITY",
            "all",
        ],
        default="all",
        help="Protein category to fetch",
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Limit number of proteins to fetch (for testing)"
    )
    parser.add_argument(
        "--force", action="store_true", help="Force re-download even if file exists"
    )
    parser.add_argument("--priority", nargs="+", help="Priority proteins to fetch first (by name)")

    args = parser.parse_args()

    # Get protein list
    if args.category == "all":
        proteins = get_all_proteins()
    else:
        category_proteins = BCC_PROTEINS.get(args.category, {})
        proteins = [
            {"name": name, "category": args.category, **info}
            for name, info in category_proteins.items()
        ]

    # Prioritize specific proteins if requested
    if args.priority:
        priority_proteins = [p for p in proteins if p["name"] in args.priority]
        other_proteins = [p for p in proteins if p["name"] not in args.priority]
        proteins = priority_proteins + other_proteins

    # Apply limit
    if args.limit:
        proteins = proteins[: args.limit]

    print("🧬 Fetching AlphaFold Structures for BCC Research")
    print("=" * 70)
    print(f"📊 Category: {args.category}")
    print(f"📦 Proteins to fetch: {len(proteins)}")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print()

    results = []
    for i, protein in enumerate(proteins, 1):
        print(f"[{i}/{len(proteins)}] {protein['name']} ({protein['gene']})")
        result = fetch_protein_structure(protein, force_refresh=args.force)
        results.append(result)

        # Rate limiting
        if i < len(proteins):
            time.sleep(0.5)  # Be nice to the API

    # Summary
    print("\n" + "=" * 70)
    print("📊 Summary")
    print("=" * 70)

    status_counts = {}
    for result in results:
        status = result["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    for status, count in sorted(status_counts.items()):
        print(f"   {status}: {count}")

    successful = sum(1 for r in results if r["status"] == "downloaded" or r["status"] == "cached")
    print(f"\n✅ Successfully fetched/cached: {successful}/{len(proteins)}")

    # Save results summary
    summary_path = METADATA_DIR / "fetch_summary.json"
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w") as f:
        json.dump(
            {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "category": args.category,
                "total": len(proteins),
                "results": results,
            },
            f,
            indent=2,
        )

    print(f"📝 Summary saved: {summary_path}")


if __name__ == "__main__":
    main()



