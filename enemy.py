import random

import action
import data


class Creature(action.Actor):
    """Represents a creature of unknown type."""
    name = "Creature"
    hp = 30
    def __init__(self, dmg: int):
        self.dmg = dmg

    def select_action(self, room: data.Room) -> action.Action | None:
        """Prompt the user to select an action.
        Return the chosen action.
        """
        return action.DoNothing(self, {"room": choice})


class Boss(action.Actor):
    """Represents a boss to be defeated"""
    def __init__(self, name: str, hp: int, dmg: int):
        self.name = name
        self.hp = hp
        self.dmg = dmg

    def select_action(self, room: data.Room) -> action.Action | None:
        """Decide on and return an action."""
        next_room = random.choice(room.paths())
        return action.Move(self, {"room": next_room})