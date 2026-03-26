import urllib.request
import json

queries = [
    "ageing postural control cerebellar atrophy",
    "vestibular decline ageing postural stability",
    "age-related proprioceptive decline postural control"
]

results = []
for q in queries:
    url = f"https://api.crossref.org/works?query={urllib.parse.quote(q)}&select=DOI,title,author,abstract,published-print,published-online&rows=3"
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:hellodr@drsayuj.info'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            items = data.get('message', {}).get('items', [])
            for item in items:
                title = item.get('title', [''])[0]
                doi = item.get('DOI', '')
                authors = [a.get('family', '') + ' ' + a.get('given', '') for a in item.get('author', [])]
                abstract = item.get('abstract', 'No abstract')
                print(f"Title: {title}\nDOI: {doi}\nAuthors: {', '.join(authors)}\nAbstract: {abstract[:200]}...\n")
                results.append(item)
    except Exception as e:
        print(f"Error querying {q}: {e}")
