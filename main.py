from src.categoriser import GameCategoriser
from src.config import OUTPUT_FORMAT
from src.hltb_api import HowLongToBeatAPI
from src.steam_api import SteamAPI
import os
from dotenv import load_dotenv
import argparse

def main():
    """
    Main script for categorising real Steam games.
    """
    # Load environment variables
    load_dotenv()
    steam_id = os.getenv("STEAM_ID")
    api_key = os.getenv("STEAM_API_KEY")

    if not steam_id or not api_key:
        print("Error: Missing Steam ID or API key in the .env file.")
        return

    # Parse arguments
    parser = argparse.ArgumentParser(description="Steam Game Categoriser")
    parser.add_argument("--verbose", action="store_true", help="Enable detailed debug output")
    args = parser.parse_args()

    verbose = args.verbose

    # Initialise categoriser and APIs
    categoriser = GameCategoriser(verbose=verbose)
    steam_api = SteamAPI()
    hltb_api = HowLongToBeatAPI()

    # Fetch games
    print("Fetching games from Steam...")
    try:
        games = steam_api.fetch_games()
        if not games:
            print("No games found. Please check your Steam ID and API key.")
            return
    except Exception as e:
        print(f"Error fetching games from Steam: {e}")
        return

    # Categorise games
    print("Categorising games...")
    for game in games:
        game_name = game.get("name")
        try:
            playtime = hltb_api.get_game_time(game_name)
            categoriser.categorise_game(game_name, playtime)
        except Exception as e:
            error_message = f"Failed to categorise game '{game_name}' due to error: {e}"
            print(f"Error: {error_message}")
            with open("skipped_games.log", "a") as log_file:
                log_file.write(f"{error_message}\n")

    # Display results
    print("\nCategories:")
    for category, game_list in categoriser.categories.items():
        print(f"{category}: {len(game_list)} games")
        for game in game_list:
            print(f"  - {game}")

    categoriser.display_summary()

if __name__ == "__main__":
    main()
