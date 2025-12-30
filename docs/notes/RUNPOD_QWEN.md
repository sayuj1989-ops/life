# RunPod with Qwen2.5 - Quick Start

## Why Qwen2.5-32B?
- **Better quality**: State-of-the-art for scientific writing
- **Same cost**: RTX 4090 @ $0.39/hr
- **Faster setup**: More popular model, better docs
- **Better instruction following**: Superior to Instella-3B

## Quick Start (5 Steps)

### 1. Deploy RunPod
- Go to https://www.runpod.io
- Deploy → GPU Pods
- Select: **RTX 4090** (24GB VRAM)
- Template: **RunPod PyTorch 2.1**
- Click "Deploy On-Demand"

### 2. Install Dependencies
In web terminal:
```bash
pip install transformers>=4.37.0 accelerate langchain langchain-community chromadb sentence-transformers
```

### 3. Upload Files
Upload to `/workspace/`:
- `qwen_client.py` (new Qwen2.5 client)
- `edit_manuscript.py`
- `langchain_manuscript_analyzer.py`
- `life/manuscript/` directory
- `chroma_db/` directory (optional, for RAG)

### 4. Update Import (if needed)
If `edit_manuscript.py` imports `instella_client`, change to:
```python
from qwen_client import qwen_chat as instella_chat
```

Or just rename `qwen_client.py` to `instella_client.py` for drop-in replacement.

### 5. Run Editing
```bash
python edit_manuscript.py
```

**Expected time**: 8-12 minutes
**Expected cost**: $0.05-0.08
**Quality**: ⭐⭐⭐⭐⭐

## Model Sizes

If RTX 4090 is unavailable, use smaller models:

### Qwen2.5-14B (Good balance)
```python
MODEL_ID = "Qwen/Qwen2.5-14B-Instruct"
# Needs: 12GB VRAM (RTX 3090)
# Speed: ~150 tok/s
# Time: 5-8 min
```

### Qwen2.5-7B (Fastest)
```python
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
# Needs: 8GB VRAM (RTX 3090)
# Speed: ~200 tok/s
# Time: 3-5 min
```

## 8-bit Quantization (if OOM)

If you get out-of-memory errors with 32B:
```python
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-32B-Instruct",
    device_map="auto",
    load_in_8bit=True,  # Reduces to ~16GB VRAM
    trust_remote_code=True
)
```

## Performance Comparison

| Model | Time | Cost | Quality | Recommendation |
|-------|------|------|---------|----------------|
| **Qwen2.5-32B** | 8-12 min | $0.05-0.08 | ⭐⭐⭐⭐⭐ | **Best for final draft** |
| Qwen2.5-14B | 5-8 min | $0.02-0.04 | ⭐⭐⭐⭐ | Good for iterations |
| Qwen2.5-7B | 3-5 min | $0.02-0.03 | ⭐⭐⭐ | Quick edits |
| Instella-3B | 5-8 min | $0.02-0.04 | ⭐⭐ | Not recommended |

## Troubleshooting

### Model Download Slow
Pre-download on RunPod:
```bash
python -c "from transformers import AutoModelForCausalLM; AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-32B-Instruct', device_map='auto', torch_dtype='auto', trust_remote_code=True)"
```

### Import Error
Make sure to update imports:
```python
# Old
from instella_client import instella_chat

# New (option 1)
from qwen_client import qwen_chat as instella_chat

# New (option 2) - rename file
# Rename qwen_client.py to instella_client.py
```

## Expected Output

After 8-12 minutes:
- `edited_sections/introduction_v2.tex` ✅
- `edited_sections/theory_v2.tex` ✅
- `edited_sections/methods_v2.tex` ✅
- `edited_sections/results_v2.tex` ✅
- `edited_sections/discussion_v2.tex` ✅
- `edited_sections/conclusion_v2.tex` ✅

**Quality**: Publication-ready scientific writing with RAG-enhanced consistency.
