import json

with open("paper4_literature/raw_citations.json") as f:
    data = json.load(f)

for k, v in data.items():
    print(f"--- Query: {k} ---")
    for item in v[:5]:
        print(f"Title: {item.get('title')}")
        print(f"DOI: {item.get('doi', 'N/A')}")
        abstract = item.get('abstractText', 'N/A')
        print(f"Abstract: {abstract[:400]}..." if len(abstract) > 400 else f"Abstract: {abstract}")
        print("-" * 20)
