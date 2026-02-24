from fastmcp import FastMCP
import os
import subprocess
from pathlib import Path

# Initialize FastMCP server
mcp = FastMCP("Life Research Server")

# Constants
BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
MANUSCRIPT_DIR = BASE_DIR / "manuscript"


@mcp.tool()
def read_manuscript_abstract() -> str:
    """
    Reads the abstract from the manuscript's main LaTeX file.
    Returns the content within the abstract environment or a snippet if not found.
    """
    main_tex = MANUSCRIPT_DIR / "main.tex"
    if not main_tex.exists():
        return "Manuscript file not found."

    try:
        # Check for sections/abstract.tex first
        abstract_tex = MANUSCRIPT_DIR / "sections" / "abstract.tex"
        if abstract_tex.exists():
            return abstract_tex.read_text(encoding="utf-8").strip()

        # Fallback to main.tex parsing
        content = main_tex.read_text(encoding="utf-8")
        start_marker = "\\begin{abstract}"
        end_marker = "\\end{abstract}"

        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)

        if start_idx != -1 and end_idx != -1:
            return content[start_idx + len(start_marker) : end_idx].strip()
        else:
            return "Abstract environment not found in main.tex or sections/abstract.tex."
    except Exception as e:
        return f"Error reading manuscript: {str(e)}"


@mcp.tool()
def list_experiments() -> list[str]:
    """
    Lists available experiment scripts in the scripts directory.
    Returns a list of filenames.
    """
    if not SCRIPTS_DIR.exists():
        return ["Scripts directory not found."]

    scripts = [f.name for f in SCRIPTS_DIR.glob("*.py") if f.is_file()]
    return sorted(scripts)


@mcp.tool()
def run_experiment(script_name: str) -> str:
    """
    Runs a specified experiment script from the scripts directory.

    Args:
        script_name: The name of the script to run (e.g., 'experiment_minimal_elastica.py').

    Returns:
        The stdout and stderr of the execution.
    """
    script_path = SCRIPTS_DIR / script_name

    # Security check: ensure script is within SCRIPTS_DIR
    try:
        script_path = script_path.resolve()
        if not str(script_path).startswith(str(SCRIPTS_DIR.resolve())):
            return "Error: Script path traversal detected."
    except Exception as e:
        return f"Error resolving script path: {e}"

    if not script_path.exists():
        return f"Error: Script '{script_name}' not found."

    try:
        # Run the script using the current Python environment
        # We assume the environment running this server has necessary dependencies
        result = subprocess.run(
            ["python", str(script_path)],
            capture_output=True,
            text=True,
            check=False,  # Don't raise exception on non-zero exit code, just return output
            cwd=str(BASE_DIR),  # Run from base dir to ensure relative paths work
        )

        output = f"Exit Code: {result.returncode}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        return output
    except Exception as e:
        return f"Failed to execute script: {str(e)}"


if __name__ == "__main__":
    mcp.run()
