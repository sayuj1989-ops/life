import urllib.request
import json

headers = {"User-Agent": "mailto:hellodr@drsayuj.info"}

def query_crossref(query):
    url = f"https://api.crossref.org/works?query={urllib.parse.quote(query)}&rows=1"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data['message']['items']:
                item = data['message']['items'][0]
                return {"title": item.get("title", [""])[0], "doi": item.get("DOI", "")}
    except Exception as e:
        print(f"Error querying {query}: {e}")
    return None

results = {
    "friston_2010": query_crossref("The free-energy principle: a unified brain theory? Friston 2010"),
    "friston_2006": query_crossref("A free energy principle for the brain Friston Kilner Harrison 2006")
}

with open("crossref_results.json", "w") as f:
    json.dump(results, f, indent=2)
