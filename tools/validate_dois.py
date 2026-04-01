import urllib.request
import json
import sys

def check_doi(doi):
    url = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Jules-Agent/1.0 (hellodr@drsayuj.info)'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data['message']['title'][0]
    except Exception as e:
        return f"Error: {e}"

if len(sys.argv) > 1:
    for doi in sys.argv[1:]:
        print(f"{doi}: {check_doi(doi)}")
