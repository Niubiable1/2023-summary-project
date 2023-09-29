


class Character:
    """
    A Character class for each character

    Attribrute:
    hp : Health points of the character

    Method:
    - get_hp
    """
    name: str

    def __init__(self, hp: int):
        self.hp = hp

    def get_hp(self) -> int:
        """returns hp value of player"""
        return self.hp


class Player(Character):
    """
    A sub class of Character class

    Attributes:
    agent : Name of agent
    
    Methods:
     - get_agent
     - set_hp
    """

    def __init__(self, hp: int, agent: str):
        super().__init__(hp)
        self.agent = agent

    def get_agent(self) -> str:
        """Returns name of agent chosen"""
        return self.agent

    def set_hp(self, creature: bool, buff: bool) -> None:
        """
        Increases hp by 50 if buff found, and
        decreases it by 30 if creature found, no return value
        """
        if creature:
            self.hp -= 30
        if buff:
            self.hp += 50


class Agent:
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


def create_agent(name: str, hp: int) -> Agent:
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
