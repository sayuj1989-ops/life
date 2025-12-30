import requests
import glob
import os

API_KEY = "ragflow-mcp-researcher-token"
BASE_URL = "http://localhost:9380/api/v1"
DATASET_ID = "1424d812dcae11f08b84b2358273016d"

headers = {"Authorization": f"Bearer {API_KEY}"}

files = glob.glob("/Users/mac/LIFE/life/manuscript/sections/*.tex")
files.append("/Users/mac/LIFE/life/manuscript/refs.bib")

for filepath in files:
    filename = os.path.basename(filepath)
    display_name = filename
    if filename.endswith(".tex") or filename.endswith(".bib"):
        # Create a temp file with .txt extension
        temp_filename = f"{filename}.txt"
        with open(filepath, "r") as src, open(temp_filename, "w") as dst:
            dst.write(src.read())

        print(f"Uploading {temp_filename} (as {display_name})...")
        try:
            with open(temp_filename, "rb") as f:
                # We upload with the .txt filename so RAGFlow accepts it
                files_data = {"file": (temp_filename, f, "text/plain")}
                response = requests.post(
                    f"{BASE_URL}/datasets/{DATASET_ID}/documents", headers=headers, files=files_data
                )
                print(response.json())
        except Exception as e:
            print(f"Failed to upload {temp_filename}: {e}")
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
        continue

    # Fallback for other files (unused here but good for safety)
    print(f"Uploading {filename}...")
    try:
        with open(filepath, "rb") as f:
            files_data = {"file": (filename, f, "application/octet-stream")}
            response = requests.post(
                f"{BASE_URL}/datasets/{DATASET_ID}/documents", headers=headers, files=files_data
            )
            print(response.json())
    except Exception as e:
        print(f"Failed to upload {filename}: {e}")

# After uploads, trigger parsing
print("Triggering parsing for all uploaded documents...")
try:
    # 1. Get List of Documents
    res = requests.get(f"{BASE_URL}/datasets/{DATASET_ID}/documents?page_size=100", headers=headers)
    docs = res.json().get("data", {}).get("docs", [])
    doc_ids = [d["id"] for d in docs]

    if doc_ids:
        # 2. Trigger Parsing
        payload = {"document_ids": doc_ids}
        res = requests.post(
            f"{BASE_URL}/datasets/{DATASET_ID}/chunks", headers=headers, json=payload
        )
        print(f"Parsing Triggered: {res.json()}")
    else:
        print("No documents found to parse.")

except Exception as e:
    print(f"Failed to trigger parsing: {e}")
