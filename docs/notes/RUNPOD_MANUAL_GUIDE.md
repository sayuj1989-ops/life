# Manual RunPod Deployment Guide - Manuscript Editing

## Quick Start (20-30 minutes)

You have the deployment link open: https://console.runpod.io/deploy?gpu=RTX+4090&count=1&template=runpod-torch-v280

---

## Step 1: Deploy the Pod (5 minutes)

1. **Click the deployment link** (already open in your browser)
2. **Configure the pod:**
   - GPU: RTX 4090 (already selected) ✅
   - Template: RunPod PyTorch 2.8.0 (already selected) ✅
   - Volume: 50 GB (increase to 100 GB for model cache)
   - Expose HTTP Ports: Add `8888` (for Jupyter, optional)
   
3. **Deploy:**
   - Click "Deploy On-Demand" or "Deploy Spot" (spot is 3-6x cheaper)
   - Wait 2-3 minutes for pod to start

---

## Step 2: Connect to Pod (2 minutes)

Once pod is running:

1. Click **"Connect"** button
2. Choose **"Start Web Terminal"** or **"Connect via SSH"**
3. You'll see a terminal interface

---

## Step 3: Upload Files (5 minutes)

In the RunPod web terminal, create a working directory:

```bash
mkdir -p /workspace/manuscript_editing
cd /workspace/manuscript_editing
```

**Upload these files from your local machine:**

### Method A: Via RunPod File Browser
1. Click the folder icon in RunPod interface
2. Navigate to `/workspace/manuscript_editing`
3. Upload these files:
   - `qwen_client.py`
   - `edit_manuscript_cloud.py`
   - `requirements_cloud.txt`
   - The entire `life/manuscript/` directory

### Method B: Via SCP (if you prefer command line)

On your **local machine**, run:

```bash
# Get the pod's SSH connection string from RunPod dashboard
# It will look like: ssh root@<pod-id>.runpod.io -p <port>

# Then upload files:
scp -P <port> qwen_client.py root@<pod-id>.runpod.io:/workspace/manuscript_editing/
scp -P <port> edit_manuscript_cloud.py root@<pod-id>.runpod.io:/workspace/manuscript_editing/
scp -P <port> requirements_cloud.txt root@<pod-id>.runpod.io:/workspace/manuscript_editing/
scp -r -P <port> life/manuscript root@<pod-id>.runpod.io:/workspace/manuscript_editing/
```

---

## Step 4: Install Dependencies (5-10 minutes)

In the RunPod terminal:

```bash
cd /workspace/manuscript_editing

# Install Python dependencies
pip install -r requirements_cloud.txt

# Pre-download Qwen2.5-32B model (this takes 5-10 minutes)
python3 -c "
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_ID = 'Qwen/Qwen2.5-32B-Instruct'
print(f'Downloading {MODEL_ID}...')

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map='auto',
    torch_dtype='auto',
    trust_remote_code=True
)
print('Model downloaded and cached!')
"
```

**While waiting**, you can verify GPU:
```bash
nvidia-smi
```

You should see RTX 4090 with 24GB VRAM.

---

## Step 5: Run Manuscript Editing (8-12 minutes)

```bash
cd /workspace/manuscript_editing

# Create output directory
mkdir -p edited_sections

# Run the editor
python3 edit_manuscript_cloud.py \
    --manuscript-dir life/manuscript \
    --style "Nature Communications"
```

**Monitor progress:**
- You'll see each section being processed
- Total time: ~8-12 minutes for all sections

---

## Step 6: Download Results (3 minutes)

### Method A: Via RunPod File Browser
1. Navigate to `/workspace/manuscript_editing/edited_sections/`
2. Select all files
3. Click "Download"

### Method B: Via SCP

On your **local machine**:

```bash
# Create local output directory
mkdir -p /Users/mac/LIFE/edited_sections_runpod

# Download results
scp -r -P <port> root@<pod-id>.runpod.io:/workspace/manuscript_editing/edited_sections/* \
    /Users/mac/LIFE/edited_sections_runpod/
```

---

## Step 7: Terminate Pod (1 minute)

**IMPORTANT:** Don't forget to terminate the pod to stop charges!

1. Go to RunPod dashboard
2. Find your pod
3. Click **"Terminate"**

---

## Expected Costs

| Component | Time | Rate | Cost |
|-----------|------|------|------|
| Setup + Upload | 5 min | $0.39/hr | $0.03 |
| Model Download | 8 min | $0.39/hr | $0.05 |
| Editing | 10 min | $0.39/hr | $0.06 |
| Download | 3 min | $0.39/hr | $0.02 |
| **Total** | **26 min** | - | **$0.17** |

**With Spot Instance:** ~$0.05 total (3-6x cheaper)

---

## Troubleshooting

### "Out of Memory"
```bash
# Use 8-bit quantization
# Edit qwen_client.py, change line 11-16 to:
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",
    load_in_8bit=True,  # Add this line
    trust_remote_code=True,
)
```

### "Model download too slow"
- This is normal for first run (60GB download)
- Takes 5-10 minutes depending on connection
- Subsequent runs use cached model

### "Files not found"
```bash
# Verify files are uploaded:
ls -lh /workspace/manuscript_editing/
ls -lh /workspace/manuscript_editing/life/manuscript/
```

---

## Quick Reference Commands

```bash
# Check GPU
nvidia-smi

# Check disk space
df -h

# Monitor editing progress
tail -f /workspace/manuscript_editing/editing.log

# List output files
ls -lh /workspace/manuscript_editing/edited_sections/
```

---

## After This Works

Once you've successfully edited your manuscript manually, consider setting up SkyPilot for future runs:

1. Get RunPod API key: https://console.runpod.io/user/settings
2. Run: `runpod config`
3. Future edits: `./sky_edit.sh launch` (one command!)

---

## Files You Need to Upload

From `/Users/mac/LIFE/`:
- ✅ `qwen_client.py` (3.3 KB)
- ✅ `edit_manuscript_cloud.py` (6.9 KB)
- ✅ `requirements_cloud.txt` (0.5 KB)
- ✅ `life/manuscript/` directory (entire folder)

**Total upload size:** ~2-5 MB (depending on manuscript size)

---

**Ready to start?** Click that deployment link and follow the steps above!

**Estimated total time:** 20-30 minutes  
**Estimated cost:** $0.17 (on-demand) or $0.05 (spot)
