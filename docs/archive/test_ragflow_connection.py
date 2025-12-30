
from ragflow_client import RAGFlowClient
import sys

try:
    print("Initializing RAGFlow Client...")
    client = RAGFlowClient(
        base_url="http://localhost",
        email="researcher@ragflow.local",
        password="ragflow123"
    )
    
    print("Checking Health...")
    if client.health_check():
        print("✅ Health Check Passed")
    else:
        print("❌ Health Check Failed")
        sys.exit(1)

    print("Attempting Login (implicitly done in __init__)...")
    # If we are here, login likely succeeded or at least didn't raise exception in __init__ if it's called there.
    # Actually __init__ calls _login if email/pass provided.
    
    print("Listing Knowledge Bases...")
    kbs = client.list_knowledge_bases()
    print(f"✅ Found {len(kbs)} Knowledge Bases")
    for kb in kbs:
        print(f" - {kb.get('name')} ({kb.get('id')})")

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
