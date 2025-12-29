# Instella Integration Status

**Last Updated:** 2025-11-27  
**Model:** AMD Instella-3B-Long-Instruct (128k context)  
**Status:** � Operational - Phase 0 Complete, Executing Mission

---

## Phase 0 Complete ✅

**Test Results (2025-11-27):**
- ✅ Model loads successfully (~12 seconds with cached weights)
- ✅ Inference runs correctly
- ✅ Response: "Instella is ready!"
- ✅ All imports working
- 📊 Load time: ~12s (cached), inference: ~2-3s for 20 tokens

**System Info:**
- Device: CPU (meta device offloading for memory efficiency)
- PyTorch: Using auto device_map
- Context limit: 120k tokens configured

**Status:** Ready for Phase 1 (summarization)

---

## Summary

The Instella-3B-Long-Instruct integration is **fully configured** with comprehensive orchestration tools. The infrastructure supports:

- ✅ Long-context chat interface (128k tokens)
- ✅ Streaming and non-streaming modes
- ✅ Role-based prompting (planner/drafter/reviewer)
- ✅ Automated summarization, rewriting, and review workflows
- ✅ Antigravity mission document for autonomous agent execution

**Current Status:** Ready for Phase 0 testing (model load + inference verification).

**Known Issue:** Initial model download is ~6GB and may take 10-20 minutes on first run. Subsequent loads will be much faster (~1-2 min) as weights are cached.

---

## What's Been Completed ✅

### 1. Environment Setup
- ✅ Python 3.11 virtual environment at `/Users/mac/LIFE/.venv`
- ✅ Dependencies installed: `transformers>=4.47.0`, `accelerate`, `torch`, `sentencepiece`
- ✅ GPU/CPU auto-detection with `device_map="auto"`
- ✅ Mixed precision support (bfloat16 on CUDA, float32 fallback)

### 2. Core Instella Infrastructure
- ✅ **`instella_client.py`**: 
  - Chat-style wrapper with system/user/assistant roles
  - Long-context support (MAX_CONTEXT_TOKENS = 120,000)
  - Streaming support via TextIteratorStreamer
  - Temperature and sampling control
  - Automatic chat template application
  
- ✅ **`instella_tasks.py`**: 
  - `summarize_file(path, goal)` – with automatic chunking for large files
  - `rewrite_section(title, content, style)` – journal-targeted rewrites
  - `reviewer_pass(section_title, content)` – critical reviewer analysis
  - `read_text_file(path)` – UTF-8 safe file reading

### 3. Orchestration Scripts
- ✅ **`rewrite_driver.py`**: CLI for section rewrites (existing simple version)
- ✅ **`reviewer_pass_driver.py`**: CLI for reviewer passes (existing simple version)
- ✅ **`summarize_manuscript.py`**: Batch summarization tool
- ✅ **`refine_outline.py`**: Outline refinement with Instella
- ✅ **`consistency_check.py`**: Cross-section consistency analysis
- ✅ **`run_rewrites.sh`**: Batch processing script

### 4. Planning & Mission Documents
- ✅ **`MANUSCRIPT_PLAN_BCC_INSTELLA.md`**: Repository map and project structure
- ✅ **`INSTELLA_ANTIGRAVITY_MISSION.md`**: **NEW** – Complete 7-phase mission for autonomous agents
  - Phase 0: Verify setup
  - Phase 1: Repo mapping & summarization
  - Phase 2: Refine outline
  - Phase 3: Section rewrites
  - Phase 4: Reviewer passes
  - Phase 5: Consistency checks
  - Phase 6: Abstract & conclusion polish
  - Phase 7: Final integration
- ✅ **`TARGET_OUTLINE_BCC.md`**: Target manuscript structure

---

## Next Steps: Phase 0 Verification 🚀

### Quick Test (Recommended First Step)

Run this to verify Instella loads and can generate text:

```bash
cd /Users/mac/LIFE
source .venv/bin/activate  # Activate virtual environment

# Quick 20-token test
python -c "
from instella_client import instella_chat
print('Testing Instella...')
response = instella_chat(
    system='You are a helpful assistant.',
    messages=[{'role': 'user', 'content': 'Say hello in one sentence.'}],
    max_new_tokens=20,
    temperature=0.3
)
print(f'Response: {response}')
"
```

**Expected behavior:**
1. Model loads (first time: 1-2 min, downloads ~6GB if not cached)
2. Inference runs (~5-10 seconds for 20 tokens)
3. Returns a brief greeting

### If Test Passes ✅

Proceed to **Phase 1** of `INSTELLA_ANTIGRAVITY_MISSION.md`:
```bash
# Summarize all draft sections
python summarize_manuscript.py
```

### If Test Fails ❌

**Common issues:**

1. **Import errors** → Check dependencies:
   ```bash
   pip install --upgrade "transformers>=4.47.0" accelerate torch sentencepiece
   ```

2. **CUDA/GPU errors** → Model will fall back to CPU automatically (slower but functional)

3. **Out of memory** → Reduce context in `instella_client.py`:
   ```python
   MAX_CONTEXT_TOKENS = 60_000  # Lower from 120k
   ```

4. **Download timeout** → Pre-download the model:
   ```bash
   python -c "from transformers import AutoModelForCausalLM; AutoModelForCausalLM.from_pretrained('amd/Instella-3B-Long-Instruct', trust_remote_code=True)"
   ```

---

## Alternative: Use API-Based LLM (Faster) 🔄

If local Instella is too slow, consider swapping to OpenAI/Anthropic:

**Modify `instella_client.py`:**
```python
# At top of file, add:
USE_API = True  # Set to False to use local Instella
OPENAI_API_KEY = "your-key-here"

def instella_chat(system, messages, ...):
    if USE_API:
        # Use OpenAI API
        import openai
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "system", "content": system}] + messages,
            max_tokens=max_new_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
    else:
        # Use local Instella (existing code)
        ...
```

This gives you the same interface with much faster inference.

---

## Performance Expectations

**Local Instella-3B on CPU:**
- Model load: 1-2 minutes (first time), 20-30s (cached)
- Inference: ~10-20 tokens/second
- 2048 token generation: ~2-3 minutes

**Local Instella-3B on GPU (CUDA):**
- Model load: 30-60 seconds
- Inference: ~50-100 tokens/second
- 2048 token generation: ~30-60 seconds

**API-based (GPT-4/Claude):**
- No model load time
- Inference: ~30-50 tokens/second
- 2048 token generation: ~40-60 seconds
- Cost: ~$0.03-0.10 per rewrite (depending on model/length)

---

## Mission Execution Checklist

For Antigravity agents or manual execution:

- [ ] **Phase 0:** Verify Instella loads and runs (`INSTELLA_STATUS.md` updated with results)
- [ ] **Phase 1:** Summarize all `draft_*_BCC.md` files → `MANUSCRIPT_PLAN_BCC_INSTELLA.md`
- [ ] **Phase 2:** Refine `TARGET_OUTLINE_BCC.md` → `REFINED_OUTLINE_BCC.md`
- [ ] **Phase 3:** Rewrite all 6 sections → `draft_*_BCC_rewritten.md` files
- [ ] **Phase 4:** Reviewer passes → `REVIEW_NOTES_INSTELLA.md`
- [ ] **Phase 5:** Consistency check → `CONSISTENCY_REPORT_INSTELLA.md`
- [ ] **Phase 6:** Polish abstract & conclusion
- [ ] **Phase 7:** Final integration → `MANUSCRIPT_FULL_BCC_INSTELLA.md`

**Full mission details:** See `INSTELLA_ANTIGRAVITY_MISSION.md`

---

## Current System Info

**Model:** `amd/Instella-3B-Long-Instruct`  
**Context window:** 128k tokens (~400 pages of text)  
**Size:** 3B parameters (~6GB disk, ~12GB RAM when loaded)  
**License:** Research use (check Hugging Face for commercial terms)

**Python version:** 3.11  
**PyTorch version:** (check with `pip show torch`)  
**Transformers version:** ≥4.47.0

**Workspace:** `/Users/mac/LIFE`  
**Virtual env:** `/Users/mac/LIFE/.venv`

---

## Troubleshooting Resources

**If things break:**

1. Check model card: https://huggingface.co/amd/Instella-3B-Long-Instruct
2. Transformers docs: https://huggingface.co/docs/transformers
3. Issue tracker: https://github.com/huggingface/transformers/issues

**Quick diagnostics:**

```bash
# Check installed versions
pip list | grep -E "transformers|torch|accelerate"

# Test PyTorch
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"

# Check available disk space (model needs ~6GB)
df -h .

# Check available RAM
vm_stat | head -5  # macOS
# free -h  # Linux
```

---

**Status:** Ready for testing and mission execution  
**Blocker:** None (pending Phase 0 verification)  
**Risk level:** Low (fallback to API available if local inference fails)

*End of Status Document*
```

### Option 4: Continue with Existing Manuscript
The manuscript sections have already been drafted and integrated in the previous session. You can:
1. Review the existing sections in `life/manuscript/sections/`
2. Make manual edits based on the target outline
3. Compile and review the PDF

## Files Ready for Use
All the Instella infrastructure is in place and ready to use once the model loading issue is resolved:
- Client: `instella_client.py`
- Tasks: `instella_tasks.py`
- Scripts: `summarize_manuscript.py`, `refine_outline.py`, `rewrite_driver.py`, etc.

## Decision Required
Please choose how you'd like to proceed:
1. Switch to a faster local model
2. Use an API-based LLM instead
3. Wait for the full Instella model to download (may take 30+ minutes)
4. Skip Instella refinement and work with the existing manuscript
