import unittest
from src.categoriser import GameCategoriser

class TestGameCategoriser(unittest.TestCase):
    def setUp(self):
        """
        Set up the GameCategoriser instance for testing.
        """
        self.categoriser = GameCategoriser()

    def test_categorise_quick_bites(self):
        """
        Test categorising a game under 'Quick Bites (<2h)'.
        """
        self.categoriser.categorise_game("Short Game", 1.5)
        self.assertIn("Short Game", self.categoriser.categories["Quick Bites (<2h)"])

    def test_categorise_long_game(self):
        """
        Test categorising a game under 'Epic (>40h)'.
        """
        self.categoriser.categorise_game("Epic Game", 50)
        self.assertIn("Epic Game", self.categoriser.categories["Epic (>40h)"])

    def test_multiplayer_endless(self):
        """
        Test categorising a game as 'Multiplayer/Endless' when playtime is None.
        """
        self.categoriser.categorise_game("Endless Game", None)
        self.assertIn("Endless Game", self.categoriser.categories["Multiplayer/Endless"])
