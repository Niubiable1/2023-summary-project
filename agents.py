import data


class Agent(data.Character):
    """Represents an agent in the game.

    Each agent has an ability which may affect the game map.
    The ability has a cooldown
    Agents are buffed or injured depending on the game situation.
    Game over is determined by the game and not by agent HP.

    Attributes
    ----------
    + name: str
    + ability: str
    + hp: int
    + cooldown: int
    

    Methods
    -------
    + buff(amt: int) -> None
    + injure(amt: int) -> None
    """
    name: str
    ability: str
    def __init__(self, hp: int):
        self.hp = hp
        self.cooldown = 0

    def buff(self, amt: int) -> None:
        self.hp += amt

    def charge(self, time: int = 1) -> None:
        self.cooldown -= time
        # Cooldown cannot be < 0
        if self.cooldown < 0:
            self.cooldown = 0

    def injure(self, amt: int) -> None:
        self.hp -= amt

    def is_charged(self) -> bool:
        return self.cooldown == 0

    def reset_cooldown(self, time: int) -> None:
        assert time > 0
        self.cooldown = time


class Jett(Agent):
    name = "Jett"
    ability = "Escape"


class Sova(Agent):
    name = "Sova"
    ability = "Scan"


class Omen(Agent):
    name = "Omen"
    ability = "Teleport"


class Sage(Agent):
    name = "Sage"
    ability = "Block"


def create(name: str, hp: int) -> Agent:
    name = name.lower()
    if name == "jett":
        return Jett(hp)
    if name == "sova":
        return Sova(hp)
    if name == "omen":
        return Omen(hp)
    if name == "sage":
        return Sage(hp)
    raise ValueError(f"{name}: invalid agent name")
    