import requests
import logging
import os

class SteamAPI:
    """
    Fetches data from the Steam API for the user's owned games.
    """

    def __init__(self):
        """
        Initialise the Steam API with the user's API key and Steam ID.
        """
        self.api_key = os.getenv("STEAM_API_KEY")
        self.steam_id = os.getenv("STEAM_ID")
        self.base_url = "https://api.steampowered.com"
        self.logger = logging.getLogger(__name__)

    def fetch_games(self):
        """
        Fetch the user's owned games with playtime and names.
        """
        try:
            # Get basic game data
            url = f"{self.base_url}/IPlayerService/GetOwnedGames/v0001/"
            params = {
                "key": self.api_key,
                "steamid": self.steam_id,
                "format": "json",
            }
            response = requests.get(url, params=params)
            response.raise_for_status()

            games = response.json().get("response", {}).get("games", [])
            self.logger.debug(f"Raw API response for games: {games}")

            # Fetch game names for each appid
            enriched_games = []
            for game in games:
                appid = game.get("appid")
                if appid:
                    game_name = self.fetch_game_name(appid)
                    if game_name:
                        enriched_games.append({"name": game_name, **game})
                    else:
                        self.logger.warning(f"Could not fetch name for appid: {appid}")

            return enriched_games

        except Exception as e:
            self.logger.error(f"Error fetching games from Steam: {e}")
            return []

    def fetch_game_name(self, appid):
        """
        Fetch the name of a game using its appid.
        """
        try:
            url = f"{self.base_url}/ISteamApps/GetAppList/v2/"
            response = requests.get(url)
            response.raise_for_status()

            app_list = response.json().get("applist", {}).get("apps", [])
            game = next((app for app in app_list if app["appid"] == appid), None)
            return game["name"] if game else None

        except Exception as e:
            self.logger.error(f"Error fetching name for appid {appid}: {e}")
            return None
