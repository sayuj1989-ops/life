# instella_client.py
from typing import List, Dict, Generator, Optional
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TextIteratorStreamer,
)

MODEL_ID = "amd/Instella-3B-Long-Instruct"  # long-context instruct variant

print(f"Loading Instella model: {MODEL_ID} ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",
    torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
    trust_remote_code=True,
)
model.eval()

# You can tweak this if you want to hard-cap the context
MAX_CONTEXT_TOKENS = 120_000


def _build_prompt(system: str, messages: List[Dict[str, str]]) -> str:
    """
    messages: list of {"role": "user"|"assistant", "content": "..."}
    """
    chat = []
    if system:
        chat.append({"role": "system", "content": system})
    chat.extend(messages)
    return tokenizer.apply_chat_template(
        chat,
        tokenize=False,
        add_generation_prompt=True,
    )


def instella_chat(
    system: str,
    messages: List[Dict[str, str]],
    max_new_tokens: int = 2048,
    temperature: float = 0.3,
    stream: bool = False,
) -> str | Generator[str, None, None]:
    """
    High-level chat wrapper for Instella-3B-Long-Instruct.
    Use `stream=True` for token-by-token streaming (generator).
    """
    prompt = _build_prompt(system, messages)
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True,
                       max_length=MAX_CONTEXT_TOKENS).to(model.device)

    if not stream:
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=0.9,
            )
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Optional: strip the prompt part if template echoes it
        # Note: This simple strip might need adjustment depending on exact template behavior
        if text.startswith(prompt):
             return text[len(prompt):].strip()
        # Fallback if prompt is not exactly at start (e.g. special tokens)
        # For now, return full text or try to split by header if known. 
        # But usually decode(skip_special_tokens=True) removes the prompt structure if it's special tokens.
        # Actually, generate returns the *continuation* usually if we don't pass inputs? 
        # No, generate returns full sequence including input by default.
        # Let's trust the user's snippet logic or improve it. 
        # The user's snippet: return text[len(prompt):].strip()
        # But prompt has special tokens that might not be in text if skip_special_tokens=True.
        # Safer approach:
        input_length = inputs.input_ids.shape[1]
        generated_tokens = outputs[0][input_length:]
        return tokenizer.decode(generated_tokens, skip_special_tokens=True)

    # Streaming mode
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    generation_kwargs = dict(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=0.9,
        streamer=streamer,
    )

    import threading
    thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    def gen():
        for token in streamer:
            yield token

    return gen()


def summarize_text(text: str, goal: str = "scientific") -> str:
    system = (
        "You are a scientific summariser for a neurosurgeon working on "
        "Biological Counter-Curvature and spinal modes. Preserve equations, "
        "notation, and key hypotheses. Be concise but technically precise."
    )
    msg = {
        "role": "user",
        "content": f"Summarise the following text with a focus on {goal} details:\n\n{text}",
    }
    return instella_chat(system, [msg], max_new_tokens=1024, temperature=0.2)
