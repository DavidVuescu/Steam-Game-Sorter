import requests
import os
from dotenv import load_dotenv

class SteamAPI:
    """
    Handles interactions with the Steam Web API.
    Requires an API key and Steam ID for authentication.
    """

    def __init__(self):
        """
        Load Steam API key and Steam ID from the .env file.
        """
        load_dotenv()  # Load environment variables from .env
        self.api_key = os.getenv("STEAM_API_KEY")
        self.steam_id = os.getenv("STEAM_ID")

        if not self.api_key or not self.steam_id:
            print("WARNING: Steam API key or Steam ID is missing. "
                  "Ensure your .env file is correctly configured.")

    def fetch_games(self):
        """
        Fetch the list of owned games for the given Steam ID.
        :return: List of games with app IDs and names, or an error message
        """
        if not self.api_key or not self.steam_id:
            print("ERROR: API key or Steam ID not found. Please configure the .env file.")
            return []

        url = (
            f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
            f"?key={self.api_key}&steamid={self.steam_id}&format=json"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad HTTP status codes
            games = response.json().get("response", {}).get("games", [])
            return [{"app_id": game["appid"], "name": game["name"]} for game in games]
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Failed to fetch games. {e}")
            return []
