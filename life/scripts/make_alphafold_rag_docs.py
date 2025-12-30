"""Generate RAGFlow-friendly Markdown docs from AlphaFold metadata JSON.

This turns `outputs/alphafold/alphafold_metadata.json` into a small corpus of
per-target Markdown files (plus an index) that you can upload to a RAGFlow
knowledge base using the "General" parser.

Usage:
    python scripts/make_alphafold_rag_docs.py
    python scripts/make_alphafold_rag_docs.py --input outputs/alphafold/alphafold_metadata.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _as_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def _md_escape(text: str) -> str:
    return text.replace("|", "\\|")


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _local_file_hint(base_dir: Path, filename: str) -> str:
    candidate = base_dir / filename
    return f"`{candidate}` (exists)" if candidate.exists() else f"`{candidate}` (missing)"


def render_record_md(record: Dict[str, Any], *, base_dir: Path) -> str:
    requested_id = _as_str(record.get("requestedId") or record.get("uniprotAccession") or "")
    panel_gene = _as_str(record.get("panelGene") or record.get("gene") or requested_id)
    status = _as_str(record.get("status") or "")
    title = f"{panel_gene} — {requested_id} ({status})".strip()

    lines: List[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("## Panel Mapping")
    lines.append(f"- panelGene: `{_md_escape(_as_str(record.get('panelGene')))}`")
    lines.append(f"- panelRole: `{_md_escape(_as_str(record.get('panelRole')))}`")
    lines.append(f"- proxyFor: `{_md_escape(_as_str(record.get('proxyFor')))}`")
    lines.append(f"- isFragment: `{_md_escape(_as_str(record.get('isFragment')))}`")
    lines.append(f"- geneMatchesPanel: `{_md_escape(_as_str(record.get('geneMatchesPanel')))}`")
    lines.append("")

    if status != "ok":
        lines.append("## Status")
        lines.append(f"- noAlphafoldEntry: `{_md_escape(_as_str(record.get('noAlphafoldEntry')))}`")
        lines.append(f"- reason: `{_md_escape(_as_str(record.get('reason')))}`")
        lines.append(f"- UniProt gene: `{_md_escape(_as_str(record.get('uniprotGene')))}`")
        lines.append(f"- UniProt entryType: `{_md_escape(_as_str(record.get('uniprotEntryType')))}`")
        lines.append(f"- UniProt organism: `{_md_escape(_as_str(record.get('uniprotOrganism')))}`")
        lines.append("")
        return "\n".join(lines)

    lines.append("## AlphaFold Entry")
    lines.append(f"- gene (from AlphaFold): `{_md_escape(_as_str(record.get('gene')))}`")
    lines.append(f"- organism: `{_md_escape(_as_str(record.get('organism')))}` (taxId `{_md_escape(_as_str(record.get('taxId')))}`)")
    lines.append(f"- modelEntityId: `{_md_escape(_as_str(record.get('modelEntityId')))}`")
    lines.append(f"- global pLDDT: `{_md_escape(_as_str(record.get('globalPlddt')))}`")
    lines.append(
        f"- sequence range: `{_md_escape(_as_str(record.get('sequenceStart')))}`–`{_md_escape(_as_str(record.get('sequenceEnd')))}`"
    )
    lines.append("")

    pdb_url = _as_str(record.get("pdbUrl"))
    pae_url = _as_str(record.get("paeDocUrl"))
    conf_url = _as_str(record.get("plddtDocUrl"))
    msa_url = _as_str(record.get("msaUrl"))

    lines.append("## Links")
    if pdb_url:
        lines.append(f"- pdbUrl: {pdb_url}")
    if pae_url:
        lines.append(f"- paeDocUrl: {pae_url}")
    if conf_url:
        lines.append(f"- plddtDocUrl: {conf_url}")
    if msa_url:
        lines.append(f"- msaUrl: {msa_url}")
    lines.append("")

    # Local cache hints (if user ran --download-pdb/--download-pae).
    uniprot_accession = _as_str(record.get("uniprotAccession") or requested_id)
    if uniprot_accession:
        lines.append("## Local Cache (optional)")
        lines.append(f"- PDB: {_local_file_hint(base_dir, f'{uniprot_accession}.pdb')}")
        lines.append(f"- PAE: {_local_file_hint(base_dir, f'{uniprot_accession}_pae.json')}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Markdown docs from AlphaFold metadata JSON.")
    parser.add_argument(
        "--input",
        type=str,
        default="outputs/alphafold/alphafold_metadata.json",
        help="Path to `alphafold_metadata.json`.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs/alphafold/rag_docs",
        help="Directory to write Markdown files.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Missing input file: {input_path}")

    records = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise SystemExit("Expected input JSON to be a list of records.")

    out_dir = Path(args.output_dir)
    base_dir = input_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # Index
    index_lines: List[str] = []
    index_lines.append("# AlphaFold Panel Index")
    index_lines.append("")
    index_lines.append(f"Source: `{input_path}`")
    index_lines.append("")
    index_lines.append("| panelGene | requestedId | status | organism | global pLDDT | file |")
    index_lines.append("|---|---|---|---|---:|---|")

    for record in records:
        requested_id = _as_str(record.get("requestedId") or "")
        panel_gene = _as_str(record.get("panelGene") or record.get("gene") or requested_id)
        status = _as_str(record.get("status") or "")
        organism = _as_str(record.get("organism") or record.get("uniprotOrganism") or "")
        plddt = record.get("globalPlddt")
        plddt_str = f"{plddt:.2f}" if isinstance(plddt, (int, float)) else ""

        safe_name = panel_gene.replace("/", "_").replace(" ", "_") or requested_id
        file_name = f"{safe_name}__{requested_id}.md".strip("_")
        md_path = out_dir / file_name

        _write(md_path, render_record_md(record, base_dir=base_dir))

        index_lines.append(
            f"| `{_md_escape(panel_gene)}` | `{_md_escape(requested_id)}` | `{_md_escape(status)}` | `{_md_escape(organism)}` | {plddt_str} | `{md_path.name}` |"
        )

    _write(out_dir / "alphafold_panel_index.md", "\n".join(index_lines) + "\n")
    print(f"✅ Wrote {len(records)} Markdown docs to {out_dir}")
    print(f"   Index: {out_dir / 'alphafold_panel_index.md'}")


if __name__ == "__main__":
    main()
