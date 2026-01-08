"""
Client for Google Deep Research API.
Handles authentication, task creation, and result polling.
"""

import os
import time
import json
from pathlib import Path
from typing import Dict, Optional, Any, Callable, Union

try:
    from google import genai
    from google.genai.types import Interaction, InteractionStatus
    GOOGLE_GENAI_AVAILABLE = True
except ImportError:
    GOOGLE_GENAI_AVAILABLE = False


class GoogleResearchClient:
    """Checkpoints and manages Google Deep Research tasks."""

    def __init__(self, api_key: Optional[str] = None):
        if not GOOGLE_GENAI_AVAILABLE:
            raise ImportError(
                "google-genai package is not installed. "
                "Please install it with: pip install google-genai"
            )
        
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY is not set. "
                "Please set it in environment variables or pass it to the constructor."
            )
            
        self.client = genai.Client(api_key=self.api_key)
        self.agent_model = "deep-research-pro-preview-12-2025"

    def start_research(self, query: str) -> str:
        """
        Start a new research task.
        
        Args:
            query: The research topic or question.
            
        Returns:
            The interaction ID.
        """
        interaction = self.client.interactions.create(
            agent=self.agent_model,
            input=query,
            background=True
        )
        return interaction.id

    def get_status(self, interaction_id: str) -> Any:
        """Get the current status of an interaction."""
        return self.client.interactions.get(interaction_id)

    def poll_results(
        self, 
        interaction_id: str, 
        max_wait_time: int = 600, 
        poll_interval: int = 10,
        status_callback: Optional[Callable[[str, int], None]] = None
    ) -> Dict[str, Any]:
        """
        Poll for research results until completion or timeout.
        
        Args:
            interaction_id: The ID of the research task.
            max_wait_time: Maximum time to wait in seconds.
            poll_interval: Time between checks in seconds.
            status_callback: Optional function(status_state, elapsed_time) called on each poll.
            
        Returns:
            Dictionary containing status and result (if successful).
            
        Raises:
            TimeoutError: If research takes longer than max_wait_time.
            RuntimeError: If research fails.
        """
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            status = self.get_status(interaction_id)
            
            if status_callback:
                status_callback(status.state, elapsed_time)
            
            if status.state == "COMPLETED":
                return {
                    "status": "COMPLETED",
                    "result": status.result,
                    "interaction_id": interaction_id,
                    "elapsed_time": elapsed_time
                }
            
            elif status.state == "FAILED":
                # Convert error object to string if possible, or keep as is
                error_msg = getattr(status, "error", "Unknown error")
                raise RuntimeError(f"Research failed: {error_msg}")
            
            time.sleep(poll_interval)
            elapsed_time += poll_interval
            
        raise TimeoutError(f"Research did not complete within {max_wait_time} seconds")

    def save_result(self, result_data: Dict[str, Any], output_dir: Union[str, Path], filename_prefix: str = "research"):
        """
        Save research results to disk.
        
        Args:
            result_data: The dictionary returned by poll_results.
            output_dir: Directory to save files.
            filename_prefix: Prefix for output filenames.
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save raw JSON
        json_file = output_path / f"{filename_prefix}.json"
        with open(json_file, "w") as f:
            json.dump(result_data, f, indent=2)
            
        # Save Markdown report
        md_file = output_path / f"{filename_prefix}.md"
        content = result_data.get("result", "")
        
        # Add metadata header
        header = f"""# Research Report: {filename_prefix}
Date: {time.strftime('%Y-%m-%d %H:%M:%S')}
Interaction ID: {result_data.get('interaction_id')}
Elapsed Time: {result_data.get('elapsed_time')}s

---

"""
        with open(md_file, "w") as f:
            f.write(header + content)
            
        return {"json": str(json_file), "markdown": str(md_file)}
