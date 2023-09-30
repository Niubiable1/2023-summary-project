from typing import Any

import data
import maps
import random
import text


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
    + is_active() -> bool
    + is_passive() -> bool
    + is_charged() -> bool
    + prompt_choice(agent: str, map: Map, current_room: Room) -> Any
    + update(agent: str, map: Map, current_room: Room)
    + use(agent: str, map: Map, current_room: Room, choice)
    + reset()
    """
    name: str
    cooldown: int
    def __init__(self, timer: int = 0):
        self.timer = timer

    def is_active(self) -> bool:
        """Returns True if the ability must be manually invoked, otherwise False"""
        raise NotImplementedError

    def is_passive(self) -> bool:
        """Returns True if the ability is automatically triggered, otherwise False"""
        raise NotImplementedError

    def is_charged(self) -> bool:
        assert self.timer >= 0
        return self.timer == 0

    def prompt_choice(self, agent: str, map: maps.Map, current_room: data.Room) -> Any:
        """Prompts the player to make a choice depending on the ability's effect."""
        raise NotImplementedError

    def update(self) -> None:
        self.timer -= 1
        if self.timer < 0:
            self.timer = 0

    def use(self, agent: str, map: maps.Map, current_room: data.Room, choice) -> None:
        """Applies the ability's effect, based on the player's choice from prompt_choice()."""
        raise NotImplementedError

    def reset(self) -> None:
        self.timer = self.cooldown


class Escape(Ability):
    name = "Escape"
    cooldown = 999
    def is_active(self) -> bool:
        return False

    def is_passive(self) -> bool:
        return True

    def prompt_choice(self, agent: str, map: maps.Map, current_room: data.Room):
        """This ability picks a random room to teleport to.
        It does not actually prompt the player.
        """
        if not self.is_charged():
            return None
        player = current_room.give_char(agent)
        current_room.take_char(player)
        if current_room.has_char("Reyna") and player.hp < 300:
            return random.choice(current_room.paths())
        elif current_room.has_char("Creature") and player.hp < 30:
            return random.choice(current_room.paths())
    
    def use(self, agent: str, map: maps.Map, current_room: data.Room, choice):
        print("You were about to die. You used dash to escape.")
        print(f"You are now in {choice}.")
        self.reset()
        next_room = map.get_room(choice)
        player = current_room.give_char(agent)
        next_room.take_char(player)


class Scan(Ability):
    name = "Scan"
    cooldown = 2
    def is_active(self) -> bool:
        return True

    def is_passive(self) -> bool:
        return False

    def prompt_choice(self, agent: str, map: maps.Map, current_room: data.Room) -> str | None:
        return text.prompt_valid_choice(
            current_room.paths(),
            "You can scan the following rooms: ",
            cancel=True
        )
    
    def use(self, agent: str, map: maps.Map, current_room: data.Room, choice: str) -> None:
        room = map.get_room(choice)
        ustatus = room.has_char("Creature")
        ostatus = room.has_obj("Orb")
        if ustatus and ostatus:
            print(f"{room.name} has both utility and an orb.")
        elif ustatus and not ostatus:
            print(f"{room.name} has utility.")
        elif not ustatus and ostatus:
            print(f"{room.name} has an orb.")
        else:
            print(f"{room.name} is empty.")
        self.reset()


class Teleport(Ability):
    name = "Teleport"
    cooldown = 5
    def is_active(self) -> bool:
        return True

    def is_passive(self) -> bool:
        return False

    def prompt_choice(self, agent: str, map: maps.Map, current_room: data.Room) -> str | None:
        return text.prompt_valid_choice(
            map.room_names(),
            "You can move to the following rooms: ",
            cancel=True
        )
        
    def use(self, agent: str, map: maps.Map, current_room: data.Room, choice: str) -> None:
        next_room = map.get_room(choice)
        player = current_room.give_char(agent)
        next_room.take_char(player)
        self.reset()


class Block(Ability):
    name = "Block"
    cooldown = 3
    def is_active(self) -> bool:
        return True

    def is_passive(self) -> bool:
        return False

    def prompt_choice(self, agent: str, map: maps.Map, current_room: data.Room) -> str | None:
        return text.prompt_valid_choice(
            current_room.paths(),
            "You can block the following rooms: ",
            cancel=True
        )
    
    def use(self, agent: str, map: maps.Map, current_room: data.Room, choice: str) -> None:
        # TODO: encapsulate path blocking
        current_room._paths.remove(choice)
        target = map.get_room(choice)
        # TODO: encapsulate path blocking
        target._paths.remove(current_room.name)
        self.reset()
        print(f"{choice} is successfully blocked.")
        print(text.divider)

