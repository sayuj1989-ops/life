"""Fetch AlphaFold metadata (and optionally structures) for a set of UniProt IDs.

Usage (defaults to the scoliosis/countercurvature panel):
    python scripts/fetch_alphafold_metadata.py

Specify custom IDs (comma-separated):
    python scripts/fetch_alphafold_metadata.py --ids Q92949,Q8TE73

Download PDB and PAE JSON alongside metadata:
    python scripts/fetch_alphafold_metadata.py --download-pdb --download-pae

Notes
-----
AlphaFold DB coverage is not a 1:1 mirror of UniProt. In particular, very long
axonemal dynein heavy chains (e.g., DNAH5/DNAH11) may return HTTP 404 from the
AlphaFold prediction API even though they exist in UniProt. This script records
those cases explicitly as "missing" when using the default panel.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib import error, request


ALPHAFOLD_ENDPOINT = "https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
UNIPROT_ENTRY_ENDPOINT = "https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"

DEFAULT_PANEL: List[Dict[str, Any]] = [
    # Cilia / LR asymmetry (human)
    {"id": "Q92949", "panelGene": "FOXJ1", "role": "cilia_regulator"},
    {"id": "Q9UFE4", "panelGene": "CCDC39", "role": "cilia_structure"},
    # HOX segmentation (human)
    {"id": "P31260", "panelGene": "HOXA10", "role": "hox_patterning"},
    {"id": "P28358", "panelGene": "HOXD10", "role": "hox_patterning"},
    # Mechanosensing / actuation (human)
    {"id": "Q9H5I5", "panelGene": "PIEZO2", "role": "mechanosensor"},
    # Dynein heavy chains (human biology; often missing in AlphaFold API)
    {"id": "Q8TE73", "panelGene": "DNAH5", "role": "dynein_heavy_chain"},
    {"id": "Q96DT5", "panelGene": "DNAH11", "role": "dynein_heavy_chain"},
]

FRAGMENTS_PANEL: List[Dict[str, Any]] = [
    # Known short fragment that DOES have an AlphaFold entry (not full-length DNAH5).
    {"id": "O95496", "panelGene": "DNAH5", "role": "dynein_fragment", "isFragment": True, "proxyFor": "Q8TE73"},
    # Alternative protein mapped to DNAH11 locus (short; NOT the heavy chain).
    {"id": "L0R5A4", "panelGene": "DNAH11", "role": "dynein_alt_protein", "isFragment": True, "proxyFor": "Q96DT5"},
    # Mouse Dnah5 partial (domain-scale proxy; NOT the full heavy chain).
    {"id": "Q5DTW4", "panelGene": "DNAH5", "role": "dynein_proxy_fragment", "isFragment": True, "proxyFor": "Q8TE73"},
]


def _fetch_json(url: str) -> Any:
    with request.urlopen(url) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_prediction(uniprot_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Fetch AlphaFold metadata for a UniProt ID. Returns the first model entry."""
    url = ALPHAFOLD_ENDPOINT.format(uniprot_id=uniprot_id)
    try:
        data = _fetch_json(url)
    except error.HTTPError as exc:
        if exc.code == 404:
            return None, "AlphaFold API 404 (no entry)"
        return None, f"AlphaFold API HTTP {exc.code}"
    except Exception as exc:  # pragma: no cover - network error path
        return None, f"AlphaFold fetch failed: {exc}"

    if not data:
        return None, "AlphaFold response empty"
    if not isinstance(data, list):
        return None, f"Unexpected AlphaFold response type: {type(data)}"
    return data[0], None


def fetch_uniprot_entry(uniprot_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Fetch minimal UniProt metadata for an accession."""
    url = UNIPROT_ENTRY_ENDPOINT.format(uniprot_id=uniprot_id)
    try:
        data = _fetch_json(url)
    except error.HTTPError as exc:
        if exc.code == 404:
            return None, "UniProt 404 (no entry)"
        return None, f"UniProt HTTP {exc.code}"
    except Exception as exc:  # pragma: no cover - network error path
        return None, f"UniProt fetch failed: {exc}"

    if not isinstance(data, dict):
        return None, f"Unexpected UniProt response type: {type(data)}"
    return data, None


def _extract_uniprot_gene(entry: Dict[str, Any]) -> Optional[str]:
    genes = entry.get("genes") or []
    if not genes:
        return None
    gene = genes[0].get("geneName") or {}
    return gene.get("value")


def download_file(url: str, dest: Path) -> bool:
    """Download a file if a URL is provided."""
    if not url:
        return False
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with request.urlopen(url) as resp, open(dest, "wb") as fh:
            fh.write(resp.read())
        return True
    except Exception as exc:  # pragma: no cover - network error path
        print(f"Download failed for {url}: {exc}", file=sys.stderr)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch AlphaFold metadata for UniProt IDs.")
    parser.add_argument(
        "--ids",
        type=str,
        default=",".join(item["id"] for item in DEFAULT_PANEL),
        help="Comma-separated UniProt accessions (default: countercurvature panel).",
    )
    parser.add_argument(
        "--include-fragments",
        action="store_true",
        help="Include known UniProt fragments that have AlphaFold entries (e.g., DNAH5 fragment O95496).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="outputs/alphafold/alphafold_metadata.json",
        help="Path to write aggregated metadata JSON.",
    )
    parser.add_argument(
        "--download-pdb",
        action="store_true",
        help="Download PDB files alongside metadata.",
    )
    parser.add_argument(
        "--download-pae",
        action="store_true",
        help="Download PAE JSON files alongside metadata.",
    )
    args = parser.parse_args()

    ids = [tok.strip() for tok in args.ids.split(",") if tok.strip()]
    if args.include_fragments:
        ids.extend([item["id"] for item in FRAGMENTS_PANEL])
    # De-duplicate while preserving order
    seen: set[str] = set()
    ids = [uid for uid in ids if not (uid in seen or seen.add(uid))]
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    records: List[Dict[str, Any]] = []
    for uniprot_id in ids:
        annotation = next((item for item in DEFAULT_PANEL if item["id"] == uniprot_id), None)
        if annotation is None:
            annotation = next((item for item in FRAGMENTS_PANEL if item["id"] == uniprot_id), None)

        expected_gene = annotation.get("panelGene") if annotation else None

        entry, err = fetch_prediction(uniprot_id)
        if entry is None:
            uniprot_entry, uniprot_err = fetch_uniprot_entry(uniprot_id)
            record = {
                "requestedId": uniprot_id,
                "status": "missing",
                "noAlphafoldEntry": True,
                "reason": err,
                "panelGene": expected_gene,
                "panelRole": annotation.get("role") if annotation else None,
                "proxyFor": annotation.get("proxyFor") if annotation else None,
                "isFragment": bool(annotation.get("isFragment")) if annotation else False,
                "uniprotGene": _extract_uniprot_gene(uniprot_entry) if uniprot_entry else None,
                "uniprotEntryType": uniprot_entry.get("entryType") if uniprot_entry else None,
                "uniprotOrganism": (
                    (uniprot_entry.get("organism") or {}).get("scientificName")
                    if uniprot_entry
                    else None
                ),
                "uniprotError": uniprot_err,
            }
            records.append(record)
            print(f"Missing {uniprot_id}: {err}")
            continue

        resolved_gene = entry.get("gene")
        gene_matches_panel: bool | None
        if resolved_gene and expected_gene:
            gene_matches_panel = str(resolved_gene).lower() == str(expected_gene).lower()
        else:
            gene_matches_panel = None
        record = {
            "requestedId": uniprot_id,
            "status": "ok",
            "panelGene": expected_gene,
            "panelRole": annotation.get("role") if annotation else None,
            "proxyFor": annotation.get("proxyFor") if annotation else None,
            "isFragment": bool(annotation.get("isFragment")) if annotation else False,
            "geneMatchesPanel": gene_matches_panel,
            "uniprotAccession": entry.get("uniprotAccession"),
            "gene": resolved_gene,
            "organism": entry.get("organismScientificName"),
            "taxId": entry.get("taxId"),
            "modelEntityId": entry.get("modelEntityId"),
            "globalPlddt": entry.get("globalMetricValue"),
            "sequenceStart": entry.get("sequenceStart"),
            "sequenceEnd": entry.get("sequenceEnd"),
            "pdbUrl": entry.get("pdbUrl"),
            "cifUrl": entry.get("cifUrl"),
            "bcifUrl": entry.get("bcifUrl"),
            "paeDocUrl": entry.get("paeDocUrl"),
            "plddtDocUrl": entry.get("plddtDocUrl"),
            "paeImageUrl": entry.get("paeImageUrl"),
            "msaUrl": entry.get("msaUrl"),
            "entryId": entry.get("entryId"),
        }
        records.append(record)

        # Optional downloads
        basename = record["uniprotAccession"] or uniprot_id
        if args.download_pdb and record["pdbUrl"]:
            download_file(record["pdbUrl"], output_path.parent / f"{basename}.pdb")
        if args.download_pae and record["paeDocUrl"]:
            download_file(record["paeDocUrl"], output_path.parent / f"{basename}_pae.json")

        print(
            f"Fetched {uniprot_id}: model={record['modelEntityId']} "
            f"pLDDT={record['globalPlddt']} gene={record.get('gene')}"
        )

    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(records, fh, indent=2)
    print(f"✅ Saved metadata for {len(records)} proteins to {output_path}")


if __name__ == "__main__":
    main()
