import data


class Orb(data.Object):
    """Represents an orb.

    Buffs the player with its presence.
    """
    name = "Orb"
    def __init__(self, buff: int):
        self.buff = buff
