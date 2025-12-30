import kagglehub

# Download latest version
print("Starting download...")
path = kagglehub.model_download("ashok205/nvidia-nemotron-3-nano-30b/pyTorch/pytorch-v1")

print("Path to model files:", path)
