# RunPod GPU Manuscript Editing - Quick Start Guide

## Fastest Method: Use RunPod Web Interface

### Step 1: Get RunPod Account
1. Go to https://www.runpod.io
2. Sign up / Log in
3. Add credits ($5-10 is plenty)

### Step 2: Deploy Pod
1. Click "Deploy" → "GPU Pods"
2. Select GPU: **RTX 4090** (best value: $0.39/hr, ~200 tokens/sec)
3. Template: **RunPod PyTorch 2.1**
4. Volume: 20 GB
5. Click "Deploy On-Demand"

### Step 3: Upload Files
Once pod is running:
1. Click "Connect" → "Start Web Terminal"
2. Upload these files via drag-and-drop:
   - `edit_manuscript.py`
   - `langchain_manuscript_analyzer.py`  
   - `instella_client.py`
   - `instella_tasks.py`
   - Entire `life/manuscript/` directory
   - Entire `chroma_db/` directory (if needed)

### Step 4: Install Dependencies
In the web terminal:
```bash
pip install transformers accelerate langchain langchain-community chromadb sentence-transformers
```

### Step 5: Run Editing
```bash
python edit_manuscript.py
```

**Expected time**: 5-10 minutes total
**Expected cost**: ~$0.03-0.10

### Step 6: Download Results
1. Results will be in `edited_sections/`
2. Download via web terminal file browser
3. Stop the pod to avoid charges

## Alternative: Build Custom Docker Image

If you want a pre-configured environment:

### Build Image
```bash
docker build -f Dockerfile.runpod -t manuscript-editor .
```

### Push to Docker Hub
```bash
docker tag manuscript-editor yourusername/manuscript-editor
docker push yourusername/manuscript-editor
```

### Deploy on RunPod
1. Use "Custom Image" template
2. Image: `yourusername/manuscript-editor`
3. Deploy and run

## Cost Breakdown

### GPU Options
| GPU | Cost/Hour | Speed | Est. Time | Total Cost |
|-----|-----------|-------|-----------|------------|
| RTX 4090 | $0.39 | 200 tok/s | 5-10 min | $0.03-0.07 |
| RTX 3090 | $0.29 | 150 tok/s | 7-12 min | $0.03-0.06 |
| A40 | $0.79 | 250 tok/s | 4-8 min | $0.05-0.10 |

**Recommendation**: RTX 4090 (best speed/cost ratio)

## Troubleshooting

### Out of Memory
If you get OOM errors:
```python
# In instella_client.py, add:
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",
    torch_dtype=torch.float16,  # Use FP16 instead of BF16
    load_in_8bit=True,  # Enable 8-bit quantization
    trust_remote_code=True
)
```

### Slow Upload
Zip files before uploading:
```bash
tar -czf manuscript_files.tar.gz edit_manuscript.py langchain_manuscript_analyzer.py instella_client.py life/manuscript/
```

Then upload `manuscript_files.tar.gz` and extract on RunPod:
```bash
tar -xzf manuscript_files.tar.gz
```

## Expected Results

After 5-10 minutes, you should have:
- `edited_sections/introduction_v2.tex`
- `edited_sections/theory_v2.tex`
- `edited_sections/methods_v2.tex`
- `edited_sections/results_v2.tex`
- `edited_sections/discussion_v2.tex`
- `edited_sections/conclusion_v2.tex`

Each section will be RAG-augmented with context from the entire manuscript for consistency.

## Next Steps After Editing

1. Download edited sections
2. Review and compare with originals
3. Integrate into main manuscript
4. Run consistency checks with RAG tools
5. Submit to journal!
