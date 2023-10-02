class Action:
    """Encapsulates the possible actions a character can take in the game"""
    def __init__(self, data=None) -> None:
        self.data = data

class Move(Action):
    """Move to a given location on the map.
    The location must be stated in data under the key "room".
    """

class Stay(Action):
    """Stay in the current room"""

class UseAbility(Action):
    """Use the player's active ability."""