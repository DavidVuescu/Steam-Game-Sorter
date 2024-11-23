from howlongtobeatpy import HowLongToBeat

class HowLongToBeatAPI:
    """
    Handles integration with the HowLongToBeat API for fetching game completion times.
    """

    def __init__(self):
        """
        Initialise the HowLongToBeat API wrapper.
        """
        self.hltb = HowLongToBeat()

    def get_game_time(self, game_name):
        """
        Fetch the main story completion time for a given game.
        :param game_name: Name of the game
        :return: Completion time in hours (float) or None if not found
        """
        results = self.hltb.search(game_name)
        if results:
            return results[0].main_story  # Main story time in hours
        return None
