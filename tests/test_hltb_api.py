from unittest.mock import patch, MagicMock
import unittest
from src.hltb_api import HowLongToBeatAPI

class TestHowLongToBeatAPI(unittest.TestCase):
    def setUp(self):
        """
        Set up the HowLongToBeatAPI instance for testing.
        """
        self.hltb_api = HowLongToBeatAPI()

    @patch("src.hltb_api.HowLongToBeat.search")  # Mock the search method
    def test_get_game_time_found(self, mock_search):
        """
        Test get_game_time with a valid game name.
        """
        # Mock the HowLongToBeatEntry object with a main_story attribute
        mock_result = MagicMock()
        mock_result.main_story = 5.0
        mock_search.return_value = [mock_result]

        # Call the method
        time = self.hltb_api.get_game_time("Portal")

        # Assertions
        self.assertEqual(time, 5.0)

    @patch("src.hltb_api.HowLongToBeat.search")  # Mock the search method
    def test_get_game_time_not_found(self, mock_search):
        """
        Test get_game_time with a non-existent game name.
        """
        # Simulate no results found
        mock_search.return_value = []

        # Call the method
        time = self.hltb_api.get_game_time("NonExistentGame")

        # Assertions
        self.assertIsNone(time)
