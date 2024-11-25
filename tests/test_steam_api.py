import unittest
from unittest.mock import patch
from src.steam_api import SteamAPI
import requests

class TestSteamAPI(unittest.TestCase):
    def setUp(self):
        """
        Set up the SteamAPI instance for testing.
        """
        self.steam_api = SteamAPI(verbose=True)  # Enable verbose mode for detailed debug output during tests

    @patch("src.steam_api.requests.get")
    def test_fetch_games_success(self, mock_get):
        # Mock the response for fetch_games
        mock_get.return_value.json.return_value = {
            "response": {
                "games": [
                    {"appid": 1, "playtime_forever": 120},
                    {"appid": 2, "playtime_forever": 45}
                ]
            }
        }
        games = self.steam_api.fetch_games()
        self.assertEqual(len(games), 2)

    @patch("src.steam_api.requests.get")
    def test_fetch_games_failure(self, mock_get):
        """
        Test fetch_games with an API failure.
        """
        mock_get.side_effect = requests.exceptions.HTTPError("Simulated failure")  # Simulate an HTTP error
        with patch.object(self.steam_api, '_load_cache', return_value=None):  # Ensure cache doesn't interfere
            games = self.steam_api.fetch_games()
            self.assertEqual(games, [])  # Should return an empty list

    @patch("src.steam_api.requests.get")
    def test_fetch_games_with_cache(self, mock_get):
        cached_data = [{'name': 'Unnamed Game', 'appid': 1, 'playtime_forever': 120}, {'name': 'Unnamed Game', 'appid': 2, 'playtime_forever': 45}]
        with patch.object(self.steam_api, '_load_cache', return_value=cached_data):
            games = self.steam_api.fetch_games()
            self.assertEqual(len(games), 2)  # Check that two games are returned from cache
            mock_get.assert_not_called()  # Ensure no API call is made

            # Call again to test cache usage without hitting the API
            cached_games = self.steam_api.fetch_games()
            self.assertEqual(len(cached_games), 2)  # Confirm cached data is used
            mock_get.assert_not_called()  # Confirm no new API call
