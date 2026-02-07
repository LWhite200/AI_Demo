# ===============================
# AI AGENT: FOLLOW-UP QUESTION MODEL
# ===============================
# This module demonstrates a small AI component that could generate
# follow-up questions if the agent is unsure about the user's intent.

from transformers import AutoTokenizer, AutoModelForCausalLM
from colorama import Fore, init

init(autoreset=True)  # Ensure terminal colors reset automatically

print(Fore.CYAN + "🤖 Loading tiny AI model for follow-ups...")

# MODEL SELECTION:
# 'distilgpt2' is a very small, CPU-friendly language model.
# In a real AI agent, this would be used to generate dynamic prompts or
# clarifying questions when the agent is unsure.
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print(Fore.GREEN + "✅ AI model loaded!\n")


def ask_ai(prompt, max_new_tokens=50):
    """
    This function demonstrates a simplified AI agent process:
    
    1. Receive a 'prompt' (user input + context)
    2. Encode the prompt into tokens the model understands
    3. Generate text (follow-up question) based on the prompt
    4. Decode the output back into human-readable text
    5. Return only the first line for clarity
    
    In a real agent:
    - The prompt provides context and instructions
    - The model generates next steps for the agent to ask or act
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        pad_token_id=tokenizer.eos_token_id  # Ensure proper sentence ending
    )
    # Return first line only, simulating a concise follow-up question
    return tokenizer.decode(outputs[0], skip_special_tokens=True).split("\n")[0]
