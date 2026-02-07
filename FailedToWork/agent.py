# Gemini Research & Summarization Agent
# -------------------------------------
# This agent performs the following steps:
# 1. Searches the web for a given topic using DuckDuckGo
# 2. Summarizes the retrieved content using Gemini API
# 3. Combines all summaries into a single report
# 4. Displays the report in the terminal

import os
import re
from rich.console import Console  # For colored terminal output
from ddgs import DDGS  # DuckDuckGo search library
import google.generativeai as genai  # Google's Gemini AI API
from config import GEMINI_API_KEY  # API key from config file


# Create a console instance for formatted terminal output
console = Console()


# --- Gemini API Configuration Section
if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
    raise ValueError("Please set your GEMINI_API_KEY in config.py before running the agent.")


# Configures the Gemini API to make use of our key
genai.configure(api_key=GEMINI_API_KEY)


# --- Web Search Function
# This function searches the web using DuckDuckGo and returns text snippets
def search_topic(topic: str, max_results: int = 5):
    
    console.print(f"Searching for: {topic}")
    
    # Perform the search and extract the body text from each result
    # DDGS().text() returns search results, we filter to only include those with actual content
    snippets = [r.get("body") for r in DDGS().text(topic, max_results=max_results) if r.get("body")]
    
    # If no results found, show a message and return empty list
    if not snippets:
        console.print("No results found. Try a different topic or check your internet connection.")
    
    return snippets


# --- Text Summarization Function
# This function takes a block of text and returns a summarized version using Gemini
def summarize_text(text: str, model_name: str = "models/gemini-flash-latest") -> str:
    
    # Check if the text is empty or just whitespace (AI can be funny)
    if not text.strip():
        return "(No content available to summarize.)"
    
    # Initialize the Gemini model
    model = genai.GenerativeModel(model_name)
    
    # Send the text to Gemini with instructions to summarize it
    # We're starting a new chat each time (empty history)
    response = model.start_chat(history=[]).send_message(
        f"Summarize the following text into clear key points in a format for terminal display:\n{text}"
    )
    
    return response.text # Return the AI-generated summary


# --- Main Research Pipeline
# This is the main function that coordinates the entire research process
def research_agent(topic: str):
    
    console.rule(f"Research Agent: {topic}") 


    # Step 1: Search the web for the topic
    snippets = search_topic(topic)
    
    if not snippets:
        return

    console.print(f"Found {len(snippets)} results. Summarizing each snippet...")


    # Step 2: Summarize each search result individually
    partial_summaries = []  # This will store all the individual summaries
    
    # Loop through each search result and create a summary
    for i, snippet in enumerate(snippets, 1):
        console.print(f"Summarizing snippet {i}...")
        summary = summarize_text(snippet)  # Get summary for this specific result
        partial_summaries.append(summary)  # Add to our collection


    # Step 3: Combine all individual summaries into one big text block
    combined_text = "\n\n".join(partial_summaries)
    console.print("Combining all summaries into the final report...")

    
    # Step 4: Create a final comprehensive summary from all the individual summaries
    model = genai.GenerativeModel("models/gemini-flash-latest")
    
    # Ask Gemini to create a final report based on all the summarized research
    final_response = model.start_chat(history=[]).send_message(
        f"Based on the following research summaries about '{topic}', create a comprehensive final report with clear key points and practical advice. Format for terminal display:\n\n{combined_text}"
    )
    final_summary = final_response.text


    # Step 5: Display the final report in the terminal
    console.print(f"\n[bold cyan]Research Report: {topic}[/bold cyan]")  # Colored header
    console.print(final_summary)  # The actual report content
    console.print("[green]Research complete![/green]")  # Success message


# --- Program Entry Point
if __name__ == "__main__":

    console.print("Welcome to the Gemini Research & Summarization Agent")

    exit_program = False

    # Loop to allow multiple search queries from user.
    while not exit_program:

        topic = input("Enter a topic to research: ").strip()
        
        if topic and topic != "0":
            research_agent(topic)
        elif topic == "0":
            console.print(f"Goodbye. Shutting down...")
            exit_program = True
        else:
            console.print("No topic entered. Exiting.")
            exit_program = True