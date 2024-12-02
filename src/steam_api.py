import requests
import logging
import os
import json
from pathlib import Path
from datetime import datetime, timedelta


class SteamAPI:
    """
    Fetches data from the Steam API for the user's owned games.
    """

    CACHE_EXPIRY_DAYS = 7  # Cache expiry in days

    def __init__(self, verbose=False):
        self.api_key = os.getenv("STEAM_API_KEY")
        self.steam_id = os.getenv("STEAM_ID")
        self.base_url = "https://api.steampowered.com"
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)

        # Set up logging based on the verbose flag
        if self.verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        # Define the cache folder path
        self.cache_dir = Path.home() / "Documents" / "Steam Games Sorter" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _load_cache(self, filename):
        """
        Load cached data if it exists and is valid.
        """
        cache_file = self.cache_dir / filename
        if cache_file.exists():
            with open(cache_file, "r") as file:
                cache_data = json.load(file)
                cache_date = datetime.fromisoformat(cache_data.get("date", ""))
                if datetime.now() - cache_date < timedelta(days=self.CACHE_EXPIRY_DAYS):
                    self.logger.debug(f"Using cached data from {cache_file}")
                    return cache_data.get("data")
                else:
                    self.logger.debug(f"Cache expired for {cache_file}")
        return None

    def _save_cache(self, filename, data):
        """
        Save data to the cache.
        """
        cache_file = self.cache_dir / filename
        with open(cache_file, "w") as file:
            json.dump({"date": datetime.now().isoformat(), "data": data}, file)
        self.logger.debug(f"Data cached in {cache_file}")

    def fetch_games(self):
        """
        Fetch owned games and their metadata.
        """
        try:
            cache_filename = f"{self.steam_id}_games.json"
            cached_games = self._load_cache(cache_filename)
            if cached_games:
                self.logger.debug(f"Using cached games data.")
                return cached_games

            # Fetch games from Steam API
            url = f"{self.base_url}/IPlayerService/GetOwnedGames/v0001/"
            params = {"key": self.api_key, "steamid": self.steam_id, "format": "json"}
            response = requests.get(url, params=params)
            response.raise_for_status()

            games = response.json().get("response", {}).get("games", [])
            app_ids = [game["appid"] for game in games]

            # Fetch app list (game names) and enrich data
            app_list = self.fetch_app_list()
            enriched_games = [
                {"name": app_list.get(game["appid"], "Unnamed Game"), **game}
                for game in games
            ]

            # Cache the enriched games
            self._save_cache(cache_filename, enriched_games)
            return enriched_games
        except Exception as e:
            self.logger.error(f"Error fetching games from Steam: {e}")
            return []

    def fetch_app_list(self):
        """
        Fetch or load app list (game names) and cache it.
        """
        try:
            cache_filename = "applist.json"
            cached_app_list = self._load_cache(cache_filename)
            if cached_app_list:
                self.logger.debug(f"Using cached app list.")
                return {app["appid"]: app["name"] for app in cached_app_list}

            # Fetch full app list from Steam API
            url = f"{self.base_url}/ISteamApps/GetAppList/v2/"
            response = requests.get(url)
            response.raise_for_status()

            app_list = response.json().get("applist", {}).get("apps", [])
            self._save_cache(cache_filename, app_list)
            return {app["appid"]: app["name"] for app in app_list}
        except Exception as e:
            self.logger.error(f"Error fetching app list: {e}")
            return {}

