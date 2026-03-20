import urllib.request
import json
import urllib.parse

# Europe PMC API endpoint
url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

# Query for ageing and postural control, focusing on proprioceptive decline, vestibular degeneration, and cerebellar atrophy
query = '("postural control" OR "balance") AND (ageing OR aging) AND ("proprioception" OR "vestibular" OR "cerebellar")'
params = {
    'query': query,
    'format': 'json',
    'resultType': 'core',
    'pageSize': 20
}

# Encode parameters
query_string = urllib.parse.urlencode(params)
full_url = f"{url}?{query_string}"

try:
    with urllib.request.urlopen(full_url) as response:
        data = json.loads(response.read().decode())

        results = []
        if 'resultList' in data and 'result' in data['resultList']:
            for item in data['resultList']['result']:
                paper = {
                    'title': item.get('title', ''),
                    'authors': item.get('authorString', ''),
                    'doi': item.get('doi', ''),
                    'abstract': item.get('abstractText', ''),
                    'journal': item.get('journalTitle', ''),
                    'year': item.get('pubYear', '')
                }
                results.append(paper)

        with open('day1_results.json', 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Successfully fetched and saved {len(results)} papers to day1_results.json")
except Exception as e:
    print(f"Error fetching data: {e}")
