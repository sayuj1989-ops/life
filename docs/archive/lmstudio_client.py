"""
LM Studio Client
Provides a Qwen/Instella-compatible chat interface for local LM Studio inference.
"""

import requests
import json
from typing import List, Dict, Generator, Optional
import os

# Default to local LM Studio server
BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
TIMEOUT = 600  # Seconds (increased for local inference)

def lmstudio_chat(
    system: str,
    messages: List[Dict[str, str]],
    max_new_tokens: int = 2048,
    temperature: float = 0.7,
    stream: bool = False,
    model: str = "qwen/qwen3-8b"  # Default but often ignored by LM Studio in single-model mode
) -> str | Generator[str, None, None]:
    """
    Chat wrapper for LM Studio local server.
    Mimics the signature of qwen_client.qwen_chat.
    """
    
    # Construct full message history including system prompt
    full_messages = []
    if system:
        full_messages.append({"role": "system", "content": system})
    full_messages.extend(messages)
    
    payload = {
        "model": model,
        "messages": full_messages,
        "temperature": temperature,
        "max_tokens": max_new_tokens,
        "stream": stream
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        if stream:
            return _stream_response(payload, headers)
        else:
            response = requests.post(
                f"{BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
            
    except requests.exceptions.RequestException as e:
        return f"Error connecting to LM Studio: {str(e)}"

def _stream_response(payload: Dict, headers: Dict) -> Generator[str, None, None]:
    """Helper to yield tokens from streaming response"""
    try:
        with requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=TIMEOUT
        ) as response:
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            delta = data["choices"][0]["delta"]
                            if "content" in delta:
                                yield delta["content"]
                        except json.JSONDecodeError:
                            continue
    except Exception as e:
        yield f"[Error: {str(e)}]"

if __name__ == "__main__":
    # Simple test
    print("Testing connection to LM Studio...")
    test_msg = [{"role": "user", "content": "Hello, are you ready for research?"}]
    response = lmstudio_chat("You are a helpful assistant.", test_msg, max_new_tokens=100)
    print(f"Response: {response}")
