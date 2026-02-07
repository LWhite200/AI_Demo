"""
===========================
TASKS TEMPLATE
===========================

- Prompts the user
- Sends input to AI
- Prints AI response cleanly
"""

from agent import ask_ai

def main():
    print("🎲 Welcome to the AI Agent Demo!")
    print("You can type anything (a question or statement) and the AI will respond.")
    print("Type 'exit' or 'quit' to end the demo.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        print("🤖 AI is thinking...\n")
        response = ask_ai(user_input)
        print(f"AI: {response}\n")

if __name__ == "__main__":
    main()
