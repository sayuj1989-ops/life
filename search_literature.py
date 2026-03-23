import urllib.request
import urllib.parse
import json

def fetch_bibtex(doi):
    url = f"https://doi.org/{doi}"
    req = urllib.request.Request(url, headers={'Accept': 'application/x-bibtex'})
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        return f"Error fetching BibTeX for DOI {doi}: {e}"

def search_europepmc(query, max_results=5):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={encoded_query}&format=json&resultType=core"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('resultList', {}).get('result', [])[:max_results]
    except Exception as e:
        print(f"Error querying EuropePMC: {e}")
        return []

def main():
    queries = [
        "ageing postural control",
        "proprioceptive decline age",
        "vestibular degeneration ageing",
        "cerebellar atrophy aging posture"
    ]

    results_by_query = {}

    for query in queries:
        print(f"Searching for: {query}")
        results = search_europepmc(query, max_results=3)
        results_by_query[query] = results

    with open('paper3_literature/day1_postural_ageing.md', 'w') as f:
        f.write("# Day 1: Ageing and Postural Control\n\n")
        f.write("## Literature Search Summary\n\n")

        for query, results in results_by_query.items():
            f.write(f"### Query: `{query}`\n\n")
            if not results:
                f.write("No results found or error occurred.\n\n")
                continue

            for res in results:
                title = res.get('title', 'No title')
                doi = res.get('doi', None)
                abstract = res.get('abstractText', 'No abstract available.')

                f.write(f"#### {title}\n")
                if doi:
                    f.write(f"- **DOI**: {doi}\n")
                    bibtex = fetch_bibtex(doi)
                    f.write(f"- **BibTeX**:\n```bibtex\n{bibtex}\n```\n")
                else:
                    f.write("- **DOI**: Not available\n")

                f.write(f"- **Abstract**: {abstract}\n\n")

if __name__ == '__main__':
    main()
