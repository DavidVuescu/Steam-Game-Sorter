import unittest
from src.categoriser import GameCategoriser

class TestGameCategoriser(unittest.TestCase):
    def setUp(self):
        self.categoriser = GameCategoriser(verbose=True)

    def test_valid_categorisation(self):
        test_data = [
            ("Quick Game", 1, "Quick Bites (<2h)"),
            ("Short Game", 3, "Short (2-5h)"),
            ("Medium Game", 10, "Medium (5-15h)"),
            ("Long Game", 20, "Long (15-40h)"),
            ("Epic Game", 100, "Epic (>40h)"),
        ]
        for name, playtime, expected_category in test_data:
            self.categoriser.categorise_game(name, playtime)
            self.assertIn(name, self.categoriser.categories[expected_category])

    def test_invalid_playtime(self):
        invalid_playtimes = [-1, "five", {"time": 5}, [10], True]
        for invalid_playtime in invalid_playtimes:
            with self.subTest(playtime=invalid_playtime):
                with self.assertRaises(ValueError):
                    self.categoriser.categorise_game("Invalid Game", invalid_playtime)

    def test_multiplayer_endless(self):
        self.categoriser.categorise_game("Endless Game", None)
        self.assertIn("Endless Game", self.categoriser.categories["Multiplayer/Endless"])

    def test_summary(self):
        self.categoriser.categorise_game("Valid Game", 5)
        with self.assertRaises(ValueError):
            self.categoriser.categorise_game("Invalid Game", -1)
        self.categoriser.categorise_game("Multiplayer Game", None)
        self.assertEqual(self.categoriser.categorised_games, 2)
        self.assertEqual(self.categoriser.skipped_games, 1)

    def test_category_bounds(self):
        self.categoriser.categorise_game("Lower Bound", 0)
        self.categoriser.categorise_game("Upper Bound", 40)
        self.assertIn("Lower Bound", self.categoriser.categories["Quick Bites (<2h)"])
        self.assertIn("Upper Bound", self.categoriser.categories["Epic (>40h)"])

    def test_edge_cases(self):
        edge_cases = [
            ("Negative Extreme", -9999, False),
            ("String Playtime", "123", False),
        ]
        for name, playtime, should_raise in edge_cases:
            if should_raise:
                with self.assertRaises(ValueError):
                    self.categoriser.categorise_game(name, playtime)

