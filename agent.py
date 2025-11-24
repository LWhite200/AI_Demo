"""
Simple Gemini Research & Summarization Agent
------------------------------------------------
This agent performs:
1. Web search for a topic
2. Summarization of search results using Gemini
3. Combines summaries into a final report
4. Saves report as a Markdown file
"""

import os
import re
from rich.console import Console

# Optional: install ddgs and google-generativeai
from ddgs import DDGS
import google.generativeai as genai
from config import GEMINI_API_KEY

console = Console()

# -----------------------------
# Gemini API setup
# -----------------------------
if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
    raise ValueError("Please set your GEMINI_API_KEY in config.py!")

genai.configure(api_key=GEMINI_API_KEY)

# -----------------------------
# Utility Functions
# -----------------------------
def sanitize_filename(text: str) -> str:
    """
    Converts a topic string into a safe filename (first 2 words, safe characters)
    """
    words = text.split()[:2]
    base = "_".join(words)
    return re.sub(r'[\\/*?:"<>|]', "_", base)

# -----------------------------
# Search & Summarization
# -----------------------------
def search_topic(topic: str, max_results: int = 5):
    """
    Search the web for short text snippets using DuckDuckGo
    """
    console.print(f"🔎 Searching the web for: [bold]{topic}[/bold]")
    snippets = [r.get("body") for r in DDGS().text(topic, max_results=max_results) if r.get("body")]
    if not snippets:
        console.print("[red]No snippets found. Try another topic or check your connection.[/red]")
    return snippets

def summarize_text(text: str, model_name: str = "models/gemini-flash-latest") -> str:
    """
    Summarize text using Gemini API
    """
    if not text.strip():
        return "(No content found to summarize.)"
    
    model = genai.GenerativeModel(model_name)
    response = model.start_chat(history=[]).send_message(
        f"Summarize this clearly into key points:\n{text}"
    )
    return response.text

# -----------------------------
# Agent Pipeline
# -----------------------------
def research_agent(topic: str):
    """
    Full pipeline:
    1. Search topic
    2. Summarize each snippet
    3. Merge summaries
    4. Save as Markdown report
    """
    console.rule(f"[bold blue]Research Agent: {topic}[/bold blue]")

    snippets = search_topic(topic)
    if not snippets:
        return

    console.print(f"📄 Found {len(snippets)} snippets. Summarizing...")
    partial_summaries = []
    for i, snippet in enumerate(snippets, 1):
        console.print(f"\n[cyan]Summarizing snippet {i}...[/cyan]")
        summary = summarize_text(snippet)
        partial_summaries.append(summary)

    combined_text = "\n\n".join(partial_summaries)
    console.print("\n🧠 Combining summaries into a final report...")
    final_summary = summarize_text(combined_text)

    safe_name = sanitize_filename(topic)
    output_path = f"report_{safe_name}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Research Report: {topic}\n\n{final_summary}")

    console.print(f"\n✅ Done! Report saved as [green]{output_path}[/green]\n")

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    console.print("Welcome to the Gemini Research & Summary Agent!\n", style="bold green")
    topic = input("Enter a topic to research: ").strip()
    if topic:
        research_agent(topic)
    else:
        console.print("No topic entered. Exiting.", style="red")
