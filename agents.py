import ability
import action
import data
import text


class Agent(action.Actor):
    """Represents an agent in the game.

    Each agent has an ability which may affect the game map.
    The ability has a cooldown
    Agents are buffed or injured depending on the game situation.
    Game over is determined by the game and not by agent HP.

    Attributes
    ----------
    + name: str
    + description: str
    + hp: int
    + cooldown: int
    

    Methods
    -------
    + buff(amt: int) -> None
    + get_ability() -> Ability
    + injure(amt: int) -> None
    + select_action(room) -> Action
    + update() -> None
    """
    name: str
    description: str
    def __init__(self, hp: int):
        self.hp = hp
        self.cooldown = 0

    def buff(self, amt: int) -> None:
        self.hp += amt

    def get_ability(self) -> ability.Ability:
        raise NotImplementedError

    def injure(self, amt: int) -> None:
        self.hp -= amt

    def select_action(self, room: data.Room) -> action.Action | None:
        """Prompt the user to select an action.
        Return the chosen action.
        """
        choice = text.prompt_valid_choice(
            ["Move", "Stay", "Ability"],
            "You can do the following: ",
            cancel=False
        )
        if choice == "Move":
            choice = text.prompt_valid_choice(
                room.paths(),
                "Where do you want to go?",
                cancel=True
            )
            if not choice:
                return None
            return action.Move(self, {"room": choice})
        if choice == "Stay":
            return action.Stay(self, {"room": choice})
        if choice == "Ability":
            return action.UseAbility(self, {"room": choice})
        raise ValueError(f"{choice}: invalid action")

    def update(self):
        for ability_ in self._abilities:
            ability_.update()


class Jett(Agent):
    name = "Jett"
    description = "Dash into an adjacent room if you would otherwise die (does not refresh)"
    def __init__(self, hp: int):
        super().__init__(hp)
        self._abilities = [ability.Escape()]

    def get_ability(self) -> ability. Ability:
        return self._abilities[0]


class Sova(Agent):
    name = "Sova"
    description = "Scan an adjacent room for information (cooldown: 2 turn)"
    def __init__(self, hp: int):
        super().__init__(hp)
        self._abilities = [ability.Scan()]

    def get_ability(self) -> ability. Ability:
        return self._abilities[0]


class Omen(Agent):
    name = "Omen"
    description = "Move to any room on the map (cooldown: 5 turns)"
    def __init__(self, hp: int):
        super().__init__(hp)
        self._abilities = [ability.Teleport()]

    def get_ability(self) -> ability. Ability:
        return self._abilities[0]


class Sage(Agent):
    name = "Sage"
    description = "Block a path from your current room to an adjacent one permanently (cooldown: 3 turns)"
    def __init__(self, hp: int):
        super().__init__(hp)
        self._abilities = [ability.Block()]

    def get_ability(self) -> ability. Ability:
        return self._abilities[0]


SELECT = {
    "Jett": Jett,
    "Sova": Sova,
    "Omen": Omen,
    "Sage": Sage,
}


def create(name: str, hp: int) -> Agent:
    if name in SELECT:
        return SELECT[name](hp)
    raise ValueError(f"{name}: invalid agent name")


