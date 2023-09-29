# Cannot import game.py!


class Ability:
    """Abilities are used by Agents.

    An ability can change the map or reveal information.
    An ability has a cooldown timer.
    After use, the timer resets.
    The ability can only be used again after the timer counts down to zero.

    Attributes
    ----------
    + name: str
    + cooldown: int
    + timer: int

    Methods
    -------
    + is_charged() -> bool
    + update()
    + use()
    + reset()
    """
    name: str
    cooldown: int
    def __init__(self, timer: int = 0):
        self.timer = timer

    def is_charged(self) -> bool:
        assert self.timer >= 0
        return self.timer == 0

    def update(self) -> None:
        self.timer -= 1
        if self.timer < 0:
            self.timer = 0

    def use(self, map):
        raise NotImplementedError

    def reset(self) -> None:
        self.timer = self.cooldown


class Escape(Ability):
    name = "Escape"
    cooldown = 999
    def use(self, map):
        pass


class Scan(Ability):
    name = "Scan"
    cooldown = 2
    def use(self, map):
        pass


class Teleport(Ability):
    name = "Teleport"
    cooldown = 5
    def use(self, map):
        pass


class Block(Ability):
    name = "Block"
    cooldown = 3
    def use(self, map):
        pass
