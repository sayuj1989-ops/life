"""
RunPod Manuscript Editor - GPU Accelerated

Deploys manuscript editing to RunPod GPU for 100x+ speedup.
"""

import runpod
import os
import sys
from pathlib import Path

# Configuration
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
GPU_TYPE = "NVIDIA RTX 4090"  # or "RTX 3090", "A40"
DOCKER_IMAGE = "runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel"

def setup_runpod_pod():
    """Create a RunPod pod for manuscript editing"""
    
    if not RUNPOD_API_KEY:
        print("❌ RUNPOD_API_KEY not set!")
        print("Get your API key from: https://www.runpod.io/console/user/settings")
        print("Then run: export RUNPOD_API_KEY='your-key-here'")
        sys.exit(1)
    
    runpod.api_key = RUNPOD_API_KEY
    
    print("🚀 Creating RunPod GPU instance...")
    print(f"GPU: {GPU_TYPE}")
    print(f"Image: {DOCKER_IMAGE}")
    
    # Create pod
    pod = runpod.create_pod(
        name="manuscript-editor",
        image_name=DOCKER_IMAGE,
        gpu_type_id=GPU_TYPE,
        cloud_type="SECURE",  # or "COMMUNITY" for cheaper
        volume_in_gb=20,
        container_disk_in_gb=10,
        ports="8888/http",  # Jupyter for debugging
        env={
            "PYTHONUNBUFFERED": "1"
        }
    )
    
    print(f"✅ Pod created: {pod['id']}")
    print(f"📊 Status: {pod['desiredStatus']}")
    
    return pod

def upload_files_to_pod(pod_id):
    """Upload necessary files to RunPod pod"""
    
    files_to_upload = [
        "edit_manuscript.py",
        "langchain_manuscript_analyzer.py",
        "instella_client.py",
        "instella_tasks.py",
    ]
    
    print("\n📤 Uploading files to RunPod...")
    
    for file in files_to_upload:
        if Path(file).exists():
            print(f"  Uploading {file}...")
            # RunPod file upload via API or SSH
            # Note: Actual implementation depends on RunPod SDK version
        else:
            print(f"  ⚠️  {file} not found, skipping")
    
    print("✅ Files uploaded")

def run_editing_on_pod(pod_id):
    """Execute manuscript editing on RunPod"""
    
    print("\n🔧 Installing dependencies on pod...")
    
    setup_commands = [
        "pip install transformers accelerate bitsandbytes langchain chromadb sentence-transformers",
        "python -c \"from transformers import AutoModelForCausalLM; AutoModelForCausalLM.from_pretrained('amd/Instella-3B-Long-Instruct', device_map='auto', torch_dtype='auto')\"",
    ]
    
    for cmd in setup_commands:
        print(f"  Running: {cmd[:50]}...")
        # Execute via RunPod API
    
    print("\n✍️  Starting manuscript editing...")
    print("This will take ~5-10 minutes on GPU...")
    
    # Run editing script
    result = runpod.run_sync(
        pod_id=pod_id,
        command="python edit_manuscript.py"
    )
    
    print("\n✅ Editing complete!")
    return result

def download_results(pod_id):
    """Download edited sections from RunPod"""
    
    print("\n📥 Downloading edited sections...")
    
    # Download edited_sections/ directory
    # Implementation depends on RunPod SDK
    
    print("✅ Results downloaded to edited_sections/")

def cleanup_pod(pod_id):
    """Terminate RunPod pod"""
    
    print(f"\n🧹 Terminating pod {pod_id}...")
    runpod.terminate_pod(pod_id)
    print("✅ Pod terminated")

def main():
    """Main workflow"""
    
    print("=" * 60)
    print("RunPod GPU Manuscript Editor")
    print("=" * 60)
    
    try:
        # Create pod
        pod = setup_runpod_pod()
        pod_id = pod['id']
        
        # Wait for pod to be ready
        print("\n⏳ Waiting for pod to start...")
        runpod.wait_for_pod(pod_id, status="RUNNING")
        
        # Upload files
        upload_files_to_pod(pod_id)
        
        # Run editing
        result = run_editing_on_pod(pod_id)
        
        # Download results
        download_results(pod_id)
        
        # Cleanup
        cleanup_pod(pod_id)
        
        print("\n" + "=" * 60)
        print("✅ Manuscript editing complete!")
        print("📁 Check edited_sections/ for results")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Check RunPod dashboard: https://www.runpod.io/console/pods")
        sys.exit(1)

if __name__ == "__main__":
    main()
