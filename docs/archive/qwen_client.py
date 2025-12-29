# qwen_client.py
from typing import List, Dict, Generator, Optional
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "Qwen/Qwen2.5-32B-Instruct"  # Best for scientific writing

print(f"Loading Qwen model: {MODEL_ID} ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",
    torch_dtype="auto",  # BF16 on modern GPUs
    trust_remote_code=True,
)
model.eval()

MAX_CONTEXT_TOKENS = 32000  # Qwen2.5 supports 32K context


def _build_messages(system: str, messages: List[Dict[str, str]]) -> List[Dict]:
    """Build Qwen2.5 chat messages"""
    chat = []
    if system:
        chat.append({"role": "system", "content": system})
    chat.extend(messages)
    return chat


def qwen_chat(
    system: str,
    messages: List[Dict[str, str]],
    max_new_tokens: int = 2048,
    temperature: float = 0.3,
    stream: bool = False,
) -> str | Generator[str, None, None]:
    """
    High-level chat wrapper for Qwen2.5-32B-Instruct.
    """
    chat_messages = _build_messages(system, messages)
    
    # Apply chat template
    text = tokenizer.apply_chat_template(
        chat_messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    inputs = tokenizer(
        text, 
        return_tensors="pt", 
        truncation=True,
        max_length=MAX_CONTEXT_TOKENS
    ).to(model.device)

    if not stream:
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=0.9,
                repetition_penalty=1.1,
            )
        
        # Decode only the generated tokens
        input_length = inputs.input_ids.shape[1]
        generated_tokens = outputs[0][input_length:]
        return tokenizer.decode(generated_tokens, skip_special_tokens=True)

    # Streaming mode
    from transformers import TextIteratorStreamer
    import threading
    
    streamer = TextIteratorStreamer(
        tokenizer, 
        skip_prompt=True, 
        skip_special_tokens=True
    )
    
    generation_kwargs = dict(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=0.9,
        repetition_penalty=1.1,
        streamer=streamer,
    )

    thread = threading.Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    def gen():
        for token in streamer:
            yield token

    return gen()


def summarize_text(text: str, goal: str = "scientific") -> str:
    """Summarize text with Qwen2.5"""
    system = (
        "You are a scientific summarizer for a neurosurgeon working on "
        "Biological Counter-Curvature and spinal modes. Preserve equations, "
        "notation, and key hypotheses. Be concise but technically precise."
    )
    msg = {
        "role": "user",
        "content": f"Summarize the following text with a focus on {goal} details:\n\n{text}",
    }
    return qwen_chat(system, [msg], max_new_tokens=1024, temperature=0.2)


# Backward compatibility aliases
instella_chat = qwen_chat  # So existing code still works
