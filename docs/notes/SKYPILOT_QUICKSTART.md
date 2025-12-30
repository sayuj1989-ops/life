# SkyPilot Quick Start Guide

## What is SkyPilot?

SkyPilot automates GPU provisioning across multiple cloud providers, making it easy to run your Qwen2.5-32B manuscript editing on the cheapest available GPU with a single command.

**Benefits:**
- ✅ Single command to launch jobs
- ✅ Automatic GPU provisioning
- ✅ Cost optimization (auto-selects cheapest GPU)
- ✅ Spot instance support (3-6x savings)
- ✅ Auto-failover if GPU unavailable
- ✅ No manual file upload/download

---

## Installation

SkyPilot is already installed! Verify with:

```bash
cd /Users/mac/LIFE
source .venv/bin/activate
sky check
```

---

## Cloud Setup

### Option 1: RunPod (Recommended to Start)

1. **Get API Key:**
   - Go to https://www.runpod.io/console/user/settings
   - Generate API key

2. **Configure:**
   ```bash
   pip install runpod
   runpod config
   # Enter your API key when prompted
   ```

3. **Verify:**
   ```bash
   sky check
   # Should show "RunPod: enabled"
   ```

### Option 2: Lambda Cloud (Alternative)

1. **Get API Key:**
   - Go to https://cloud.lambdalabs.com/api-keys
   - Generate API key

2. **Configure:**
   ```bash
   mkdir -p ~/.lambda_cloud
   echo "api_key = YOUR_API_KEY_HERE" > ~/.lambda_cloud/lambda_keys
   ```

3. **Verify:**
   ```bash
   sky check
   # Should show "Lambda: enabled"
   ```

### Option 3: Vast.ai (Budget Option)

1. **Get API Key:**
   - Go to https://vast.ai/console/account/
   - Copy API key

2. **Configure:**
   ```bash
   pip install vastai
   mkdir -p ~/.config/vastai
   echo "YOUR_API_KEY" > ~/.config/vastai/vast_api_key
   ```

3. **Verify:**
   ```bash
   sky check
   # Should show "Vast: enabled"
   ```

---

## Quick Start: Edit Your Manuscript

### Step 1: Test the Setup (Optional but Recommended)

Run a quick test with Qwen-7B (smaller, faster):

```bash
./sky_edit.sh test
```

This will:
- Provision an RTX 4090 GPU
- Download Qwen-7B model
- Run a simple inference test
- Auto-terminate the cluster

**Expected time:** 5-8 minutes  
**Expected cost:** ~$0.03

### Step 2: Edit Your Manuscript

Launch the full manuscript editing job:

```bash
./sky_edit.sh launch
```

This will:
1. Find the cheapest available RTX 4090 or A100
2. Provision the GPU
3. Sync your local files to the cloud
4. Download Qwen2.5-32B model
5. Edit all manuscript sections
6. Save results to `edited_sections/`

**Expected time:** 10-15 minutes  
**Expected cost:** ~$0.08

### Step 3: Monitor Progress

In a new terminal, watch the logs:

```bash
./sky_edit.sh logs
```

### Step 4: Download Results

Results are automatically synced, but you can verify:

```bash
./sky_edit.sh status
ls -lh edited_sections/
```

### Step 5: Stop the Cluster

```bash
./sky_edit.sh stop
```

---

## Cost Savings: Spot Instances

For 3-6x cost savings, use spot instances:

```bash
./sky_edit.sh launch-spot
```

**Pros:**
- ~$0.02 per run (vs $0.08 on-demand)
- Automatic recovery if preempted

**Cons:**
- May be interrupted (rare for short jobs)
- Slightly longer total time if preempted

**Recommendation:** Use spot for batch processing, on-demand for urgent edits.

---

## Common Commands

```bash
# Launch editing job
./sky_edit.sh launch

# Launch with spot instances
./sky_edit.sh launch-spot

# Check status
./sky_edit.sh status

# View logs
./sky_edit.sh logs

# Show cost estimate
./sky_edit.sh cost

# Stop all clusters
./sky_edit.sh stop

# List all clusters
./sky_edit.sh clusters
```

---

## Troubleshooting

### "No clouds enabled"

Run `sky check` to see which clouds need configuration. Follow the setup instructions above for your preferred cloud.

### "No GPU available"

SkyPilot will automatically try alternative GPUs. If all are unavailable:
1. Wait a few minutes and retry
2. Try a different cloud provider
3. Use spot instances (more availability)

### "Model download slow"

First run takes 5-10 minutes to download Qwen2.5-32B (60GB). Subsequent runs use cached model and are much faster.

### "Job failed"

Check logs:
```bash
./sky_edit.sh logs
```

Common issues:
- Out of memory: Use 8-bit quantization (edit `manuscript_editing.yaml`)
- Missing files: Ensure `life/manuscript/` directory exists

---

## File Structure

```
/Users/mac/LIFE/
├── manuscript_editing.yaml          # Main task definition
├── manuscript_editing_spot.yaml     # Spot instance variant
├── test_qwen.yaml                   # Test task
├── requirements_cloud.txt           # Cloud dependencies
├── edit_manuscript_cloud.py         # Cloud-optimized editor
├── sky_edit.sh                      # Convenience wrapper
├── qwen_client.py                   # Qwen client
├── life/manuscript/                 # Your manuscript
└── edited_sections/                 # Output directory
```

---

## Next Steps

1. **Set up one cloud provider** (RunPod recommended)
2. **Run test job** to verify setup
3. **Edit your manuscript** with the full job
4. **Explore spot instances** for cost savings
5. **Read advanced guide** for multi-cloud setup

See [SKYPILOT_ADVANCED.md](file:///Users/mac/LIFE/SKYPILOT_ADVANCED.md) for:
- Multi-cloud failover
- Custom configurations
- Batch processing
- Integration with RAGFlow

---

## Support

- **SkyPilot Docs:** https://docs.skypilot.co
- **RunPod Docs:** https://docs.runpod.io
- **Lambda Docs:** https://docs.lambdalabs.com

**Quick Help:**
```bash
./sky_edit.sh help
sky --help
```
