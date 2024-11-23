import logging
from src.config import CATEGORY_RANGES

class GameCategoriser:
    def __init__(self, verbose=False):
        self.categories = {category: [] for category in CATEGORY_RANGES.keys()}
        self.skipped_games = 0
        self.categorised_games = 0
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
        if self.verbose:
            logging.basicConfig(level=logging.DEBUG)
        self.logger.debug(f"Initialising GameCategoriser with categories: {list(self.categories.keys())}")

    @staticmethod
    def is_valid_playtime(playtime):
        if isinstance(playtime, bool):
            logging.getLogger(__name__).error(f"Invalid playtime: {playtime}")
            return False
        if playtime is None:
            return True  # Allow None for multiplayer/endless
        if isinstance(playtime, (int, float)) and playtime >= 0:
            return True
        logging.getLogger(__name__).error(f"Invalid playtime: {playtime}")
        return False

    def categorise_game(self, game_name, playtime):
        """
        Categorise a game based on its playtime.
        """
        if not game_name:  # Skip games with empty names
            raise ValueError("Game name cannot be empty.")
        self.logger.debug(f"Categorising game '{game_name}' with playtime: {playtime}")

        if not self.is_valid_playtime(playtime):
            self.skipped_games += 1
            raise ValueError(f"Invalid playtime: {playtime}")

        if playtime is None:
            self.categories["Multiplayer/Endless"].append(game_name)
            self.categorised_games += 1
            return

        for category, bounds in CATEGORY_RANGES.items():
            if len(bounds) == 0:  # Multiplayer/Endless case
                continue
            min_time, max_time = bounds
            if min_time <= playtime < (float('inf') if max_time == 'inf' else max_time):
                self.categories[category].append(game_name)
                self.categorised_games += 1
                return

    def display_summary(self):
        print("\nSummary:")
        print(f"Categorised Games: {self.categorised_games}")
        print(f"Skipped Games: {self.skipped_games} (Invalid or Missing Data)")
        if self.verbose:
            self.logger.debug(f"Categories breakdown: {self.categories}")
