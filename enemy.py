import data


class Creature(data.Character):
    """Represents a creature of unknown type."""
    name = "Creature"
    hp = 30
    def __init__(self, dmg: int):
        self.dmg = dmg


class Boss(data.Character):
    """Represents a boss to be defeated"""
    def __init__(self, name: str, hp: int, dmg: int):
        self.name = name
        self.hp = hp
        self.dmg = dmg