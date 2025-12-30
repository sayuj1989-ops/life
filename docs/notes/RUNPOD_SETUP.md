# RunPod GPU Deployment for Manuscript Editing

## Overview
Deploy Instella-3B on RunPod GPU for fast manuscript editing (100x+ speedup vs CPU).

## RunPod Setup Options

### Option 1: RunPod Serverless (Recommended)
- **Cost**: ~$0.20-0.40/hour (GPU time only)
- **Speed**: ~100-200 tokens/sec on GPU
- **Estimated time**: 5-10 minutes total for all sections
- **Total cost**: ~$0.05-0.10 for full manuscript

### Option 2: RunPod Pods (Persistent)
- **Cost**: ~$0.40-0.80/hour (continuous)
- **Speed**: Same as serverless
- **Use case**: Multiple editing iterations

## Quick Start

### 1. Install RunPod SDK
```bash
pip install runpod
```

### 2. Set API Key
```bash
export RUNPOD_API_KEY="your-api-key-here"
```

### 3. Deploy & Run
```bash
python runpod_manuscript_editor.py
```

## Files Needed on RunPod

### Docker Image Requirements
- Python 3.11
- PyTorch with CUDA
- Transformers library
- Instella model (amd/Instella-3B-Long-Instruct)

### Upload to RunPod
- `edit_manuscript.py`
- `langchain_manuscript_analyzer.py`
- `instella_client.py`
- `life/manuscript/sections/*.tex`
- `chroma_db/` (vector store)

## Deployment Strategy

### Dockerfile for RunPod
```dockerfile
FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel

# Install dependencies
RUN pip install transformers accelerate bitsandbytes langchain chromadb

# Copy scripts
COPY edit_manuscript.py /app/
COPY langchain_manuscript_analyzer.py /app/
COPY instella_client.py /app/

# Download Instella model (cached)
RUN python -c "from transformers import AutoModelForCausalLM; AutoModelForCausalLM.from_pretrained('amd/Instella-3B-Long-Instruct')"

WORKDIR /app
CMD ["python", "edit_manuscript.py"]
```

### Alternative: Use RunPod Template
- Search RunPod templates for "transformers" or "LLM"
- Upload scripts via RunPod web interface
- Run via terminal

## Cost Estimate

### GPU Options
- **RTX 4090**: $0.39/hour, ~200 tokens/sec
- **RTX 3090**: $0.29/hour, ~150 tokens/sec
- **A40**: $0.79/hour, ~250 tokens/sec

### Manuscript Editing Time
- 6 sections × 2000 tokens = 12,000 tokens
- At 200 tokens/sec: ~60 seconds generation
- Total with overhead: ~5-10 minutes
- **Cost**: $0.03-0.10 total

## Next Steps

1. Create RunPod account (if needed)
2. Get API key from RunPod dashboard
3. Choose deployment method (Serverless vs Pods)
4. Run deployment script
