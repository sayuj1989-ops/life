import requests

ids = ["P02458", "Q9S7Z8", "P13349"]

for uid in ids:
    url = f"https://alphafold.ebi.ac.uk/api/prediction/{uid}"
    try:
        resp = requests.get(url)
        print(f"ID: {uid}, Status: {resp.status_code}, Length: {len(resp.content)}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"  Response type: {type(data)}")
            if isinstance(data, list):
                print(f"  List length: {len(data)}")
                if len(data) > 0:
                    print(f"  First item entryId: {data[0].get('entryId')}")
            else:
                print(f"  Keys: {data.keys()}")
    except Exception as e:
        print(f"ID: {uid}, Error: {e}")
