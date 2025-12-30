# RAGFlow Research Enhancement: Quick Start Guide

## Overview

This guide helps you integrate RAGFlow with your BCC manuscript research workflow. RAGFlow provides advanced document retrieval and RAG (Retrieval-Augmented Generation) capabilities that complement your existing Instella setup.

## Prerequisites

- ✅ Docker Desktop installed and running
- ✅ RAGFlow ARM64 image built (from previous session)
- ✅ User creation script ready (`create_user.py`)
- ✅ Instella environment configured

## Quick Start (30 Minutes)

### Step 1: Start Docker and RAGFlow

```bash
# Start Docker Desktop (if not running)
open -a Docker

# Wait for Docker to start, then verify
docker ps

# Navigate to RAGFlow directory
cd /Users/mac/LIFE/ragflow

# Start RAGFlow services
docker-compose -f docker/docker-compose.yml up -d

# Check services are running
docker ps | grep ragflow
```

**Expected output**: Multiple RAGFlow containers running (API, database, embedding service)

---

### Step 2: Create RAGFlow User

```bash
# Find the RAGFlow API container
docker ps | grep ragflow | grep api

# Execute user creation script inside container
docker exec -it <container_id> python /ragflow/create_user.py

# Or copy the script and run it
docker cp create_user.py <container_id>:/tmp/
docker exec -it <container_id> python /tmp/create_user.py
```

**Expected output**:
```
✅ Successfully created user: researcher@ragflow.local
   Nickname: researcher
   Password: ragflow123
   User ID: <uuid>
```

---

### Step 3: Verify RAGFlow Access

1. Open browser: http://localhost
2. Login with:
   - Email: `researcher@ragflow.local`
   - Password: `ragflow123`
3. Verify you can access the RAGFlow dashboard

---

### Step 4: Create Knowledge Base

**Via UI**:
1. Click "Knowledge Base" → "Create"
2. Name: "BCC Manuscript"
3. Description: "Biological Counter-Curvature manuscript and related documents"
4. Parser: "General" (for markdown/text)
5. Click "Create"

**Via API** (alternative):
```python
from ragflow_client import RAGFlowClient

client = RAGFlowClient(base_url="http://localhost")
kb = client.create_knowledge_base(
    name="BCC Manuscript",
    description="Biological Counter-Curvature research documents"
)
print(f"Created KB: {kb['id']}")
```

---

### Step 5: Upload Key Documents

**Priority documents** (upload these first):

1. **LaTeX sections**:
   - `/Users/mac/LIFE/life/manuscript/sections/introduction.tex`
   - `/Users/mac/LIFE/life/manuscript/sections/theory.tex`
   - `/Users/mac/LIFE/life/manuscript/sections/methods.tex`
   - `/Users/mac/LIFE/life/manuscript/sections/results.tex`
   - `/Users/mac/LIFE/life/manuscript/sections/discussion.tex`

2. **Draft sections**:
   - `/Users/mac/LIFE/draft_intro_BCC.md`
   - `/Users/mac/LIFE/draft_theory_BCC.md`
   - `/Users/mac/LIFE/draft_results_BCC.md`

3. **Planning docs**:
   - `/Users/mac/LIFE/TARGET_OUTLINE_BCC.md`
   - `/Users/mac/LIFE/MANUSCRIPT_PLAN_BCC.md`

**Upload via UI**: Drag and drop files into the knowledge base

**Upload via API**:
```python
import os
from pathlib import Path

sections_dir = Path("/Users/mac/LIFE/life/manuscript/sections")
for tex_file in sections_dir.glob("*.tex"):
    if tex_file.name in ["introduction.tex", "theory.tex", "methods.tex", "results.tex", "discussion.tex"]:
        client.upload_document(
            kb_id=kb['id'],
            file_path=str(tex_file),
            parser_config={"type": "general"}
        )
        print(f"Uploaded: {tex_file.name}")
```

---

## First Use Cases (Test RAGFlow)

### Use Case 1: Equation Consistency Check

**Query**: "Find all definitions of the Information-Elasticity Coupling (IEC) metric"

**Expected**: RAGFlow returns chunks from theory section showing the metric definition

**Action**: Review chunks to ensure notation is consistent

---

### Use Case 2: Citation Gap Analysis

**Query**: "What claims in the results section need supporting citations?"

**Expected**: RAGFlow identifies strong claims without nearby citations

**Action**: Add citations to flagged claims

---

### Use Case 3: Cross-Section Consistency

**Query**: "How is the term 'counter-curvature' defined in different sections?"

**Expected**: All mentions of "counter-curvature" with context

**Action**: Verify consistent usage and definition

---

## Integration with Instella

Once RAGFlow is working, combine it with Instella for enhanced generation:

```python
from ragflow_client import RAGFlowClient
from instella_client import instella_chat

# Retrieve context from RAGFlow
ragflow = RAGFlowClient()
context_chunks = ragflow.query(
    kb_id="<your_kb_id>",
    question="What is the theoretical framework for Information-Elasticity Coupling?",
    top_k=5
)

# Build context for Instella
context = "\n\n".join([chunk['content'] for chunk in context_chunks])

# Generate with Instella using RAG context
response = instella_chat(
    system="You are writing a scientific paper on biological counter-curvature",
    messages=[{
        "role": "user",
        "content": f"""Using this context from the manuscript:

{context}

Write a 2-paragraph summary of the Information-Elasticity Coupling framework."""
    }],
    max_new_tokens=512,
    temperature=0.3
)

print(response)
```

---

## Troubleshooting

### Docker not starting
```bash
# Check Docker status
docker info

# Restart Docker Desktop
killall Docker && open -a Docker
```

### RAGFlow containers not running
```bash
# Check logs
docker-compose -f docker/docker-compose.yml logs

# Restart services
docker-compose -f docker/docker-compose.yml restart
```

### User creation fails
```bash
# Check if user already exists
docker exec -it <container_id> python -c "
from api.db.services.user_service import UserService
user = UserService.query(email='researcher@ragflow.local')
print('User exists:', user is not None)
"
```

### Cannot access http://localhost
- Check port mapping: `docker ps` (look for port 80 or 8080)
- Try http://localhost:80 or http://localhost:8080
- Check firewall settings

---

## Next Steps

After completing this quick start:

1. **Explore RAGFlow UI**: Try different queries on your manuscript
2. **Implement API client**: Use `ragflow_client.py` for programmatic access
3. **Run hybrid pipeline**: Combine RAGFlow + Instella for section rewrites
4. **Document findings**: Track improvements and insights

---

## Resources

- **Implementation Plan**: `/Users/mac/.gemini/antigravity/brain/408e5de0-d1aa-44b9-b470-d1a7458f3fd7/implementation_plan.md`
- **Research Strategy**: `/Users/mac/LIFE/RAGFLOW_RESEARCH_STRATEGY.md`
- **Instella Mission**: `/Users/mac/LIFE/INSTELLA_ANTIGRAVITY_MISSION.md`
- **RAGFlow Docs**: Check RAGFlow repository for API documentation

---

**Status**: Ready to start  
**Estimated time**: 30-60 minutes for setup  
**Blocker**: Docker must be running

*Last updated: 2025-11-29*
