from src.config import CATEGORY_RANGES

class GameCategoriser:
    """
    Categorises games based on playtime into defined tiers.
    """

    def __init__(self):
        """
        Initialise the categorisation structure.
        """
        self.categories = {category: [] for category in CATEGORY_RANGES.keys()}

    def categorise_game(self, game_name, playtime):
        """
        Categorise a game based on its playtime.
        :param game_name: Name of the game
        :param playtime: Completion time in hours (float)
        """
        if playtime is None:
            self.categories["Multiplayer/Endless"].append(game_name)
        else:
            for category, (min_time, max_time) in CATEGORY_RANGES.items():
                if min_time <= playtime < max_time:
                    self.categories[category].append(game_name)
                    break
