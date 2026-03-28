import urllib.request
import json
import urllib.parse

headers = {'User-Agent': 'mailto:hellodr@drsayuj.info'}

def search_crossref(query):
    url = f"https://api.crossref.org/works?query={urllib.parse.quote(query)}&select=title,author,DOI,abstract&rows=3"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data['message']['items']
    except Exception as e:
        print(f"Error for query '{query}': {e}")
        return []

queries = [
    "muscle spindle afferent conduction velocity human m/s",
    "electromechanical delay human ms",
    "spinal reflex delay latency ms",
    "cerebellar processing delay latency ms",
    "peripheral mechanotransduction delay ms piezo2"
]

for q in queries:
    print(f"=== Results for: {q} ===")
    results = search_crossref(q)
    for r in results:
        title = r.get('title', [''])[0]
        abstract = r.get('abstract', 'No abstract')
        doi = r.get('DOI', '')
        print(f"Title: {title}\nDOI: {doi}\nAbstract: {abstract[:200]}\n")
