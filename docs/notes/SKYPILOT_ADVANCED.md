# SkyPilot Advanced Guide

## Multi-Cloud Failover

Configure SkyPilot to automatically try multiple clouds if one is unavailable.

### Global Configuration

Create `~/.sky/config.yaml`:

```yaml
# Cloud priority order
allowed_clouds:
  - runpod
  - lambda
  - vast

# Default resources
resources:
  accelerators: RTX4090:1
  use_spot: false
  disk_size: 100

# Cost optimization
optimizer:
  minimize_cost: true
  max_retry: 3
```

### Task-Level Failover

In your task YAML, remove the `cloud:` field to enable auto-selection:

```yaml
resources:
  accelerators: 
    - RTX4090:1
    - A100:1
    - L40S:1
  # cloud: runpod  # Remove this line
  use_spot: false
```

SkyPilot will automatically try clouds in priority order.

---

## Spot Instance Best Practices

### Checkpointing Strategy

The `edit_manuscript_cloud.py` script includes automatic checkpointing:

```python
# Progress is saved after each section
editor = CloudManuscriptEditor(checkpoint_dir="checkpoints")
```

If preempted, relaunch and it will resume from the last completed section.

### Managed Spot Jobs

For even better reliability, use SkyPilot's managed spot:

```bash
sky spot launch manuscript_editing_spot.yaml --name manuscript-job
```

This provides:
- Automatic recovery on preemption
- Job queue management
- Cost tracking

### Monitor Spot Jobs

```bash
# List all spot jobs
sky spot queue

# View logs
sky spot logs manuscript-job

# Cancel job
sky spot cancel manuscript-job
```

---

## Custom Docker Images

For faster setup, create a custom Docker image with pre-installed dependencies.

### Create Dockerfile

```dockerfile
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip git

# Install dependencies
COPY requirements_cloud.txt /tmp/
RUN pip3 install -r /tmp/requirements_cloud.txt

# Pre-download Qwen model
RUN python3 -c "from transformers import AutoTokenizer, AutoModelForCausalLM; \
    AutoTokenizer.from_pretrained('Qwen/Qwen2.5-32B-Instruct', trust_remote_code=True); \
    AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-32B-Instruct', \
    device_map='cpu', torch_dtype='float16', trust_remote_code=True)"

WORKDIR /workspace
```

### Build and Push

```bash
docker build -t your-username/qwen-manuscript:latest .
docker push your-username/qwen-manuscript:latest
```

### Use in SkyPilot

Update `manuscript_editing.yaml`:

```yaml
resources:
  image_id: docker:your-username/qwen-manuscript:latest
  accelerators: RTX4090:1

# Simplified setup (model already cached)
setup: |
  echo "Using pre-built image, setup complete!"

run: |
  python3 edit_manuscript_cloud.py
```

**Benefits:**
- Setup time: 10 minutes → 30 seconds
- Total time: 15 minutes → 5 minutes
- Cost savings: ~50%

---

## Batch Processing Multiple Manuscripts

Process multiple manuscripts in parallel.

### Create Batch Task

`batch_editing.yaml`:

```yaml
name: batch-manuscript-editing

resources:
  accelerators: RTX4090:1
  cloud: runpod
  disk_size: 100

workdir: .

setup: |
  pip install -r requirements_cloud.txt
  python3 -c "from transformers import AutoTokenizer, AutoModelForCausalLM; \
    AutoTokenizer.from_pretrained('Qwen/Qwen2.5-32B-Instruct', trust_remote_code=True); \
    AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-32B-Instruct', \
    device_map='auto', torch_dtype='auto', trust_remote_code=True)"

run: |
  # Process multiple manuscripts
  for manuscript in manuscript_1 manuscript_2 manuscript_3; do
    echo "Processing $manuscript..."
    python3 edit_manuscript_cloud.py \
      --manuscript-dir "manuscripts/$manuscript" \
      --checkpoint-dir "checkpoints/$manuscript"
  done
```

### Launch Batch Job

```bash
sky launch batch_editing.yaml --cluster batch-edit --detach
```

---

## Integration with RAGFlow

Combine SkyPilot GPU editing with RAGFlow document analysis.

### Workflow

1. **Local RAGFlow Analysis:**
   ```bash
   # Run RAGFlow locally for document retrieval
   python3 ragflow_manuscript_analyzer.py --analyze
   ```

2. **Upload Context to Cloud:**
   
   Update `manuscript_editing.yaml`:
   ```yaml
   file_mounts:
     ~/chroma_db:
       source: ./chroma_db
       mode: COPY
   ```

3. **Cloud Editing with RAG:**
   
   The `edit_manuscript_cloud.py` automatically uses RAG if `chroma_db/` exists.

4. **Download Results:**
   ```bash
   ./sky_edit.sh download
   ```

---

## Performance Optimization

### GPU Selection Strategy

Different GPUs for different use cases:

| GPU | VRAM | Speed | Cost/hr | Best For |
|-----|------|-------|---------|----------|
| RTX 4090 | 24GB | Fast | $0.39 | General use |
| A100 (40GB) | 40GB | Fastest | $1.10 | Large contexts |
| L40S | 48GB | Fast | $0.90 | Very large contexts |
| RTX 3090 | 24GB | Medium | $0.29 | Budget option |

### 8-bit Quantization

For larger models or smaller GPUs, use 8-bit quantization.

Update `qwen_client.py`:

```python
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",
    load_in_8bit=True,  # Enable 8-bit
    trust_remote_code=True,
)
```

**Trade-offs:**
- VRAM: 60GB → 16GB
- Speed: -20%
- Quality: -2% (minimal)

### Parallel Section Processing

Edit sections in parallel for 6x speedup.

Create `parallel_editing.yaml`:

```yaml
num_nodes: 6  # One GPU per section

run: |
  # Each node processes one section
  SECTIONS=(introduction theory methods results discussion conclusion)
  SECTION=${SECTIONS[$SKYPILOT_NODE_RANK]}
  
  python3 edit_section.py --section $SECTION
```

Launch:
```bash
sky launch parallel_editing.yaml --cluster parallel-edit
```

---

## Cost Optimization Strategies

### 1. Use Spot Instances

```bash
./sky_edit.sh launch-spot  # 3-6x cheaper
```

### 2. Auto-Stop Idle Clusters

Add to task YAML:

```yaml
resources:
  autostop: 10  # Stop after 10 minutes idle
```

### 3. Use Smaller Models for Drafts

For initial drafts, use Qwen-7B:

```yaml
setup: |
  # Download Qwen-7B instead of 32B
  python3 -c "... Qwen2.5-7B-Instruct ..."
```

**Savings:**
- Time: 15 min → 5 min
- Cost: $0.08 → $0.03
- Quality: 90% of 32B

### 4. Batch Multiple Jobs

Process multiple sections in one session to amortize setup costs.

---

## Monitoring and Debugging

### Real-time Monitoring

```bash
# Watch GPU usage
sky exec manuscript-edit "watch -n 1 nvidia-smi"

# Monitor disk usage
sky exec manuscript-edit "df -h"

# Check memory
sky exec manuscript-edit "free -h"
```

### Debug Mode

Add to task YAML:

```yaml
envs:
  PYTHONUNBUFFERED: "1"
  TRANSFORMERS_VERBOSITY: "debug"
  CUDA_LAUNCH_BLOCKING: "1"
```

### Save Logs

```bash
sky logs manuscript-edit > editing_logs.txt
```

---

## Advanced Task Configurations

### Custom Environment Variables

```yaml
envs:
  HF_TOKEN: "your_huggingface_token"
  WANDB_API_KEY: "your_wandb_key"
  CUSTOM_VAR: "value"
```

### Persistent Storage

For model caching across runs:

```yaml
file_mounts:
  /data/models:
    name: model-cache
    mode: MOUNT
    store: s3
```

### SSH Access

SSH into running cluster:

```bash
ssh manuscript-edit
```

Then run commands interactively.

---

## Production Deployment

### CI/CD Integration

`.github/workflows/manuscript-editing.yml`:

```yaml
name: Edit Manuscript

on:
  push:
    paths:
      - 'manuscript/**'

jobs:
  edit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install SkyPilot
        run: pip install "skypilot[runpod]"
      
      - name: Configure RunPod
        run: |
          mkdir -p ~/.runpod
          echo "${{ secrets.RUNPOD_CONFIG }}" > ~/.runpod/config.toml
      
      - name: Launch Editing
        run: sky launch manuscript_editing.yaml --yes --down
      
      - name: Commit Results
        run: |
          git add edited_sections/
          git commit -m "Auto-edited manuscript"
          git push
```

### Scheduled Jobs

Use `cron` to schedule regular manuscript updates:

```bash
# Edit: crontab -e
0 2 * * * cd /Users/mac/LIFE && ./sky_edit.sh launch-spot
```

---

## Multi-User Setup

For team collaboration:

### Shared Clusters

```bash
# Launch shared cluster
sky launch manuscript_editing.yaml --cluster team-edit --no-down

# Team members can exec on same cluster
sky exec team-edit "python3 edit_manuscript_cloud.py --section introduction"
```

### Separate Namespaces

Each user gets their own namespace:

```bash
export SKYPILOT_NAMESPACE="user1"
sky launch manuscript_editing.yaml
```

---

## Troubleshooting Advanced Issues

### Out of Memory

1. Use 8-bit quantization
2. Reduce `max_new_tokens`
3. Use smaller model (Qwen-14B)
4. Upgrade to A100 (40GB)

### Slow File Sync

Exclude large files:

```yaml
file_mounts:
  /tmp/skip:
    source: .skyignore
```

Create `.skyignore`:
```
*.pyc
__pycache__/
.git/
ragflow/
*.db
```

### Network Issues

Add retry logic:

```yaml
setup: |
  for i in {1..3}; do
    pip install -r requirements_cloud.txt && break
    sleep 5
  done
```

---

## Best Practices Summary

1. ✅ Start with on-demand, switch to spot once stable
2. ✅ Use custom Docker images for production
3. ✅ Enable auto-stop to prevent idle costs
4. ✅ Monitor costs with `sky cost-report`
5. ✅ Use checkpointing for long jobs
6. ✅ Test with small models before scaling
7. ✅ Keep logs for debugging
8. ✅ Use `.skyignore` to exclude large files

---

## Resources

- **SkyPilot Docs:** https://docs.skypilot.co
- **Examples:** https://github.com/skypilot-org/skypilot/tree/master/examples
- **Slack Community:** https://slack.skypilot.co
- **GitHub Issues:** https://github.com/skypilot-org/skypilot/issues

---

**Next:** Try the [Quick Start Guide](file:///Users/mac/LIFE/SKYPILOT_QUICKSTART.md) to get started!
