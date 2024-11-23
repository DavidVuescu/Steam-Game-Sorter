import unittest
from unittest.mock import patch
from src.steam_api import SteamAPI

class TestSteamAPI(unittest.TestCase):
    def setUp(self):
        """
        Set up the SteamAPI instance for testing.
        """
        self.steam_api = SteamAPI()

    @patch("src.steam_api.requests.get")  # Mock requests.get
    def test_fetch_games_success(self, mock_get):
        """
        Test fetch_games with a successful API response.
        """
        # Definition of mock response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "response": {
                "games": [
                    {"appid": 1, "name": "Half-Life 2"},
                    {"appid": 2, "name": "Portal"},
                ]
            }
        }

        # Call the method
        games = self.steam_api.fetch_games()

        # Assertions
        self.assertEqual(len(games), 2)
        self.assertEqual(games[0]["name"], "Half-Life 2")

    @patch("src.steam_api.requests.get")  # Mock requests.get
    def test_fetch_games_failure(self, mock_get):
        """
        Test fetch_games with an API failure.
        """
        # Simulate a server error
        mock_get.return_value.status_code = 500

        # Call the method
        games = self.steam_api.fetch_games()

        # Assertions
        self.assertEqual(games, [])  # Should return an empty list
