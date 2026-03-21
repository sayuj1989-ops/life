import urllib.request
import urllib.parse
import json
import time

QUERIES = [
    '("proprioceptive delay" OR "proprioception delay" OR "proprioception latency")',
    '"peripheral transduction delay" OR ("mechanotransduction" AND "delay" AND "proprioceptor") OR ("Piezo2" AND "transduction delay")',
    '"afferent conduction delay" OR ("conduction velocity" AND "proprioceptive afferent") OR ("Group Ia afferent" AND "conduction delay")',
    '"spinal relay delay" OR ("spinal cord" AND "synaptic delay" AND "proprioception")',
    '"cerebellar processing delay" OR ("cerebellum" AND "processing delay" AND "proprioception") OR "forward model delay"',
    '"efferent conduction delay" OR ("motor conduction velocity" AND "delay")',
    '"neuromuscular junction delay" OR "NMJ transmission delay"',
    '"electromechanical delay" AND "proprioception"'
]

BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

results = {}

for query in QUERIES:
    print(f"Querying: {query}")
    params = {
        'query': query,
        'format': 'json',
        'resultType': 'core',
        'pageSize': 15
    }

    query_string = urllib.parse.urlencode(params)
    url = f"{BASE_URL}?{query_string}"

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            results[query] = data.get('resultList', {}).get('result', [])
    except Exception as e:
        print(f"Error querying {query}: {e}")
        results[query] = []

    time.sleep(1) # Be polite

with open("paper4_literature/raw_citations.json", "w") as f:
    json.dump(results, f, indent=2)

print("Finished fetching data.")
