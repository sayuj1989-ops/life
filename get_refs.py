import urllib.request
import urllib.parse
import json

def search(query, limit=3):
    url = "https://api.crossref.org/works?query=" + urllib.parse.quote(query) + "&select=DOI,title,author,published-print,published-online,abstract&rows=" + str(limit)
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:hellodr@drsayuj.info'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            for item in data['message']['items']:
                authors = [a.get('family', '') for a in item.get('author', [])]
                year = ''
                if 'published-print' in item:
                    year = item['published-print']['date-parts'][0][0]
                elif 'published-online' in item:
                    year = item['published-online']['date-parts'][0][0]
                print(f"- {', '.join(authors)} ({year}). {item.get('title', [''])[0]}. DOI: {item.get('DOI', '')}")
    except Exception as e:
        print("Error:", e)

print("Proprioceptive delay components:")
search("proprioceptive reflex delay components latency", 5)

print("\nMuscle spindle transduction latency Piezo2:")
search("muscle spindle transduction latency Piezo2 proprioception", 5)

print("\nElectromechanical delay proprioception:")
search("electromechanical delay latency proprioception muscle", 5)
