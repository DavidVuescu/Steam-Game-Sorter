from src.steam_api import SteamAPI
from src.hltb_api import HowLongToBeatAPI
from src.categoriser import GameCategoriser
from src.config import OUTPUT_FORMAT

def main():
    """
    Main script for fetching, categorising, and displaying Steam games.
    """
    # Initialise components
    steam_api = SteamAPI()
    hltb_api = HowLongToBeatAPI()
    categoriser = GameCategoriser()

    # Fetch games
    print("Fetching games from Steam...")
    games = steam_api.fetch_games()

    if not games:
        print("No games found. Please check your Steam API key and Steam ID.")
        return

    # Categorise games
    print("Categorising games based on playtime...")
    for game in games:
        playtime = hltb_api.get_game_time(game["name"])
        categoriser.categorise_game(game["name"], playtime)

    # Display results
    if OUTPUT_FORMAT == "console":
        print("\nCategories:")
        for category, game_list in categoriser.categories.items():
            print(f"{category}: {len(game_list)} games")
            for game in game_list:
                print(f"  - {game}")
    elif OUTPUT_FORMAT == "json":
        import json
        print(json.dumps(categoriser.categories, indent=4))
    elif OUTPUT_FORMAT == "csv":
        import csv
        with open("categories.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            for category, game_list in categoriser.categories.items():
                writer.writerow([category] + game_list)

if __name__ == "__main__":
    main()
