import sys
import pytest
from pathlib import Path

# Add repo root to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Add scripts directory to sys.path
scripts_dir = root_dir / "scripts"
if str(scripts_dir) not in sys.path:
    sys.path.append(str(scripts_dir))

# Add script subdirectories to sys.path for test discovery
for subdir in ["experiments", "pipeline", "data_management", "validation"]:
    s_path = scripts_dir / subdir
    if s_path.exists() and str(s_path) not in sys.path:
        sys.path.append(str(s_path))

# Add research/alphafold_countercurvature/src to sys.path
afcc_src_dir = root_dir / "research" / "alphafold_countercurvature" / "src"
if str(afcc_src_dir) not in sys.path:
    sys.path.append(str(afcc_src_dir))
