# ===============================
# AI AGENT: BOARD GAME RECOMMENDER
# ===============================
# This script demonstrates an AI agent interacting with a human:
# - It remembers user input
# - Accesses a knowledge base (database)
# - Provides recommendations
# - Uses follow-ups if uncertain

from colorama import Fore, Style, init
from boardgame_db import create_database, get_games

init(autoreset=True)

# PRE-PROGRAMMED FOLLOW-UP QUESTIONS
# These are used when the agent cannot confidently determine the recommendation.
# They simulate the 'clarifying questions' part of an AI agent.
FOLLOW_UPS = [
    "Do you prefer a strategy, party, cooperative, or family game?",
    "Do you want the game to be competitive or cooperative?",
    "How long do you want the game to last: short or long?",
]


def match_game(user_input, games, exclude=[]):
    """
    This function demonstrates the agent's reasoning process:
    
    - Looks for keywords in user input to match against known games
    - Excludes games already recommended (memory)
    
    This is similar to an AI agent searching a knowledge base
    and deciding what action to take next.
    """
    user_input = user_input.lower()
    for game in games:
        if game["name"] in exclude:
            continue  # Remember: AI avoids repeating previous suggestions
        for kw in game["keywords"]:
            if kw in user_input:
                return game["name"]
    return None


def recommend_game():
    """
    Main AI agent loop:
    
    1. Greets the user
    2. Creates/loads the database (knowledge base)
    3. Asks initial question
    4. Tries to determine the recommendation using keywords
    5. If unsure, asks pre-programmed follow-ups (simulating reasoning)
    6. Once a game is selected, asks for confirmation
    7. If the user rejects, continues reasoning/follow-ups
    """
    print(Fore.MAGENTA + "🎲 Welcome to the Board Game Recommendation AI!")
    print("I will help you find the perfect board game for your preferences.\n")

    # Knowledge base initialization
    create_database()
    games = get_games()

    question = "Describe the type of game you want to play today:"
    follow_up_index = 0
    recommended = []  # Memory of previously suggested games

    while True:
        # ------------------------------
        # 1️⃣ Gather user input
        # ------------------------------
        answer = input(Fore.YELLOW + question + "\n> " + Style.RESET_ALL)
        print(Fore.BLUE + "✏️ Got it!\n")  # Feedback for the human user

        # ------------------------------
        # 2️⃣ Reasoning step: try to match a game
        # ------------------------------
        game = match_game(answer, games, exclude=recommended)

        # ------------------------------
        # 3️⃣ Follow-up reasoning
        # ------------------------------
        if not game:
            if follow_up_index < len(FOLLOW_UPS):
                # Agent asks next clarifying question
                question = FOLLOW_UPS[follow_up_index]
                follow_up_index += 1
                continue
            else:
                # Agent fallback if no confident recommendation
                game = "Catan: fallback"

        # ------------------------------
        # 4️⃣ Output recommendation & ask for confirmation
        # ------------------------------
        recommended.append(game)  # AI memory: do not repeat
        confirm = input(Fore.CYAN + f"🤖 Recommendation: {game}\nIs this the game you wanted? (yes/no)\n> " + Style.RESET_ALL).strip().lower()

        if confirm in ["yes", "y"]:
            print(Fore.GREEN + Style.BRIGHT + f"🎉 Great! Enjoy playing {game}! 🎉\n")
            break  # Task complete
        else:
            print(Fore.MAGENTA + "Okay, let's try another option...\n")
            # Continue reasoning → next follow-up question
            if follow_up_index < len(FOLLOW_UPS):
                question = FOLLOW_UPS[follow_up_index]
                follow_up_index += 1
            else:
                # No follow-ups left → let user choose from remaining options
                unmatched = [g["name"] for g in games if g["name"] not in recommended]
                if unmatched:
                    question = f"Let's try one of these: {', '.join(unmatched)}. Which one do you prefer?"
                else:
                    print(Fore.GREEN + Style.BRIGHT + "🎉 No more options, ending recommendation.\n")
                    break


if __name__ == "__main__":
    recommend_game()