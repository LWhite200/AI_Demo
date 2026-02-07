import sqlite3
import os
from colorama import Fore, init

init(autoreset=True)
DB_FILE = "boardgames.db"

def create_database():
    if os.path.exists(DB_FILE):
        print(Fore.BLUE + "📂 Database already exists. Skipping creation.\n")
        return

    print(Fore.CYAN + "📂 Creating board game database...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        description TEXT,
        category TEXT,
        keywords TEXT
    )
    """)

    games = [
        ("Catan", "Trade, build, and settle an island", "Strategy", "strategy,trade,build"),
        ("Monopoly", "Buy properties and bankrupt opponents", "Economic", "economic,property,money"),
        ("Pandemic", "Work together to cure diseases worldwide", "Cooperative", "cooperative,team,virus,disease"),
        ("Ticket to Ride", "Build train routes across the map", "Family", "family,train,route"),
        ("Chess", "Classic strategy game of capture", "Strategy", "strategy,chess,classic"),
        ("Dixit", "Guess the story from abstract images", "Creative", "creative,story,imagination"),
        ("Carcassonne", "Tile placement strategy with medieval cities", "Strategy", "strategy,tile,placement"),
        ("Exploding Kittens", "A fun, fast-paced card game", "Party", "party,fun,fast,card"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO games (name, description, category, keywords) VALUES (?, ?, ?, ?)",
        games
    )
    conn.commit()
    conn.close()
    print(Fore.GREEN + "✅ Database created!\n")


def get_games():
    if not os.path.exists(DB_FILE):
        create_database()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, description, category, keywords FROM games")
    rows = cursor.fetchall()
    conn.close()
    games = []
    for r in rows:
        games.append({
            "name": r[0],
            "description": r[1],
            "category": r[2],
            "keywords": [k.strip().lower() for k in r[3].split(",")]
        })
    return games

if __name__ == "__main__":
    create_database()
