import data


class Creature(data.Character):
    """Represents a creature of unknown type."""
    name = "Creature"
    def __init__(self, dmg: int):
        self.dmg = dmg
