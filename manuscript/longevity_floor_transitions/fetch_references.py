"""Read public Crossref metadata for the manuscript's already identified sources.

No credentials, participant data, or external mutations. Raw records are retained.
Run once to populate the cache; rebuild_documents.py thereafter works offline.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
import html
import json
import re
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "reference_metadata"


def fetch(item):
    key, doi = item
    path = CACHE / f"{key}.json"
    raw = json.loads(path.read_text()) if path.exists() else None
    if raw and raw["message"]["DOI"].lower() != doi.lower():
        # Preserve the rejected match as audit evidence; never silently accept it.
        (CACHE / f"{key}.rejected_doi_match.json").write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n")
        raw = None
    if raw is None:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
        request = urllib.request.Request(url, headers={"User-Agent": "LongevityManuscriptBibliography/1.0", "Accept": "application/json"})
        with urllib.request.urlopen(request, timeout=25) as response:
            raw = json.load(response)
        path.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n")
    m = raw["message"]
    clean = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s))
    # Use print year where available; online-first dates can differ.
    date = m.get("published-print") or m.get("published") or m.get("published-online") or m["issued"]
    title = clean(m["title"][0])
    if m.get("subtitle"):
        title += ": " + clean(m["subtitle"][0])
    ref = {"id": key, "type": "article-journal", "title": title,
           "container-title": clean(m["container-title"][0]),
           "author": [{k: a[k] for k in ("family", "given", "suffix") if k in a} for a in m.get("author", [])],
           "issued": {"date-parts": date["date-parts"]}, "DOI": m["DOI"],
           "URL": "https://doi.org/" + m["DOI"]}
    for field in ("volume", "issue", "page"):
        if m.get(field):
            ref[field] = m[field]
    if m.get("article-number") and "page" not in ref:
        ref["page"] = m["article-number"]
    return key, ref


def main():
    CACHE.mkdir(exist_ok=True)
    seeds = json.loads((ROOT / "reference_seeds.json").read_text())
    results, errors = {}, {}
    with ThreadPoolExecutor(max_workers=1) as pool:
        futures = {pool.submit(fetch, item): item[0] for item in seeds.items()}
        for future in as_completed(futures):
            key = futures[future]
            try:
                _, results[key] = future.result()
            except Exception as error:
                errors[key] = str(error)
    if errors:
        (ROOT / "reference_fetch_errors.json").write_text(json.dumps(errors, indent=2) + "\n")
        print(json.dumps({"fetched": len(results), "errors": errors}, indent=2))
        raise SystemExit("Unresolved metadata; inspect failures before building.")
    # Journal/publisher issue dates explicitly verified in the primary-source audit.
    results["brito2014"]["issued"] = {"date-parts": [[2014]]}
    results["araujo2025"]["issued"] = {"date-parts": [[2025]]}
    # Publisher/PubMed (PMID 1482430) list a coauthor absent from Crossref.
    results["lipsitz1992"]["author"] = [
        {"family":"Lipsitz", "given":"Lewis A."}, {"family":"Goldberger", "given":"A. L."}]
    results["lipsitz1992"]["page"] = "1806–1809"
    manual = [
        {"id": "sasajima2023", "type": "article-journal",
         "title": "Effect of relaxation time on hysteresis of human tendon in vivo",
         "container-title": "Journal of Musculoskeletal and Neuronal Interactions",
         "author": [{"family": "Sasajima", "given": "Shuhei"}, {"family": "Yasuda", "given": "Ayaka"},
                    {"family": "Kosaka", "given": "Takehiro"}, {"family": "Kubo", "given": "Keitaro"}],
         "issued": {"date-parts": [[2023]]}, "volume": "23", "issue": "1", "page": "84–89",
         "URL": "https://pubmed.ncbi.nlm.nih.gov/36856103/"},
        {"id": "krishnan2025", "type": "article-journal",
         "title": "Consciousness, Information, And Emergent Spacetime Biological Counter-Curvature and Cross-Domain Clues for a Mind–Geometry Coupling",
         "container-title": "Quantum Journal of Consciousness",
         "author": [{"literal": "Sasidharan Nair Sayuj Krishnan"}, {"literal": "Pilliai Sasidharan"}, {"literal": "Pillai Resma"}],
         "issued": {"date-parts": [[2025]]}, "volume": "1", "issue": "3", "page": "62–68",
         "URL": "https://quantumjournalofconsciousness.com/articles-3/"}
    ]
    refs = [results[key] for key in seeds] + manual
    (ROOT / "references.json").write_text(json.dumps(refs, ensure_ascii=False, indent=2) + "\n")
    lines = ["# Bibliography metadata audit", "", "Crossref retrieval: " + datetime.now(timezone.utc).isoformat(), "",
             "Raw DOI records are retained locally in reference_metadata/ and omitted from the delivery archive. Curated identities are supplied in references.json. Crossref verifies bibliographic identity; the primary-source evidence audit governs scientific interpretation.", "",
             "| Key | Year | Title | DOI or primary URL |", "|---|---|---|---|"]
    for r in refs:
        year = r["issued"]["date-parts"][0][0]
        target = r.get("URL", "")
        lines.append(f'| {r["id"]} | {year} | {r["title"]} | {target} |')
    lines += ["", "The manual Sasajima entry was checked against its primary PubMed record (PMID 36856103), including all four authors and pages 84–89. The Lipsitz/Goldberger coauthor and page range were corrected against primary PubMed/publisher records (PMID 1482430); the raw Crossref omission remains visible in the cache. Crossref subtitles are retained. The Kurokawa DOI was corrected against PMID 11247934 after title matching exposed an unrelated DOI; the rejected match is preserved but excluded. The previous conceptual article uses publisher-displayed full author names because name segmentation is uncertain; its displayed DOI placeholder is deliberately omitted. Author-name formatting can be finalized by the author."]
    (ROOT / "BIBLIOGRAPHY_AUDIT.md").write_text("\n".join(lines) + "\n")
    prior_error_path = ROOT / "reference_fetch_errors.json"
    if prior_error_path.exists():
        prior = json.loads(prior_error_path.read_text())
        if prior.get("status") != "RESOLVED":
            prior_error_path.write_text(json.dumps({"status":"RESOLVED", "references_fetched":len(results), "previous_errors":prior}, indent=2)+"\n")
    print(json.dumps({"references": len(refs), "crossref": len(results), "manual": len(manual)}, indent=2))


if __name__ == "__main__":
    main()
