from data import Character, Room


class Action:
    """Encapsulates the possible actions a character can take in the game"""
    def __init__(self, actor: Actor, data=None) -> None:
        self.character = actor
        self.data = data


class Move(Action):
    """Move to a given location on the map.
    The location must be stated in data under the key "room".
    """


class Stay(Action):
    """Stay in the current room"""


class UseAbility(Action):
    """Use the player's active ability."""


class DoNothing(Action):
    """Take no action"""


class Actor(Character):
    """An Actor is a Character capable of performing actions.

    The chosen action must be a valid action.

    Methods
    -------
    + select_action(room: Room) -> Action
    """
    def select_action(self, room: Room) -> "Action":
        return DoNothing(self, data={"room", room}
