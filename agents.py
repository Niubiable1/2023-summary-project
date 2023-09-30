import ability
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
    + hp: int
    + cooldown: int
    

    Methods
    -------
    + buff(amt: int) -> None
    + get_ability() -> Ability
    + injure(amt: int) -> None
    + update() -> None
    """
    name: str
    def __init__(self, hp: int):
        self.hp = hp
        self.cooldown = 0

    def buff(self, amt: int) -> None:
        self.hp += amt

    def get_ability(self) -> ability.Ability:
        raise NotImplementedError

    def injure(self, amt: int) -> None:
        self.hp -= amt

    def update(self):
        for ability_ in self._abilities:
            ability_.update()


class Jett(Agent):
    name = "Jett"
    def __init__(self, hp: int):
        super().__init__(hp)
        self._abilities = [ability.Escape()]

    def get_ability(self) -> ability. Ability:
        return self._abilities[0]


class Sova(Agent):
    name = "Sova"
    def __init__(self, hp: int):
        super().__init__(hp)
        self._abilities = [ability.Scan()]

    def get_ability(self) -> ability. Ability:
        return self._abilities[0]


class Omen(Agent):
    name = "Omen"
    def __init__(self, hp: int):
        super().__init__(hp)
        self._abilities = [ability.Teleport()]

    def get_ability(self) -> ability. Ability:
        return self._abilities[0]


class Sage(Agent):
    name = "Sage"
    def __init__(self, hp: int):
        super().__init__(hp)
        self._abilities = [ability.Block()]

    def get_ability(self) -> ability. Ability:
        return self._abilities[0]


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
    