import urllib.request
import urllib.parse
import json

def search_europepmc(query):
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={urllib.parse.quote(query)}&format=json&resultType=core"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get('resultList', {}).get('result', [])
    except Exception as e:
        print(f"Error: {e}")
        return []

queries = [
    '("postural control" OR "proprioception") AND ("aging" OR "ageing")',
    '("vestibular degeneration" OR "vestibular system") AND ("aging" OR "ageing") AND "posture"',
    '"cerebellar atrophy" AND ("aging" OR "ageing") AND "postural"'
]

for q in queries:
    print(f"--- Query: {q} ---")
    results = search_europepmc(q)
    for r in results[:3]:
        print(f"Title: {r.get('title')}")
        print(f"DOI: {r.get('doi')}")
        abstract = r.get('abstractText', '')
        if abstract:
            print(f"Abstract: {abstract[:300]}...\n")
        else:
            print("Abstract: None\n")
