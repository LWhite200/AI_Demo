"""
===========================
AGENT TEMPLATE (DISTILGPT2)
===========================

- Loads the AI once with a friendly message
- Generates longer, coherent responses
- Tidy terminal output
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# -----------------------------
# Tiny, CPU-friendly model
# -----------------------------
MODEL_NAME = "distilgpt2"

print("🤖 Loading AI model. This may take a few seconds...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
print("✅ AI model loaded! Ready to chat.\n")

def ask_ai(prompt, max_new_tokens=60):
    """
    Generate a response to the user's input.
    - max_new_tokens increased to 60 for better responses
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():  # fast, no gradients
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
    generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated[len(prompt):].strip().split("\n")[0]  # first line only
