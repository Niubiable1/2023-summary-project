# Built-in imports
import random
import time

# Local imports
import ability
import agents
import data
import enemy
import maps
import objects
from text import divider, intro, agent, victory, defeat, timeout


class Game:
    """
Class that creates an instance of the game

Attributes
--------------------------------------------
- self.gameover: Bool
Whether or not the game is over

- self.win: Bool
Whether or not the player won

- self.roundsleft: int
Number of turns before game ends

- self.map: Map
A map encapsulating rooms

- self.player: player object
An object containing attributes related to the player

Methods
--------------------------------------------
+ self.intro(self) -> None:
+ self.countdown(self) -> None:
+ self.prompt(self, options: list, message: str, cancel: bool) -> int:
+ self.agent_select(self, choice: int) -> str:
+ self.map_select(self, choice: int) -> None:
+ self.initialise(self, agent_name: str) -> None:
+ self.desc(self) -> None:
+ self.ability(self) -> None:
- self.jett(self) -> None:
- self.sova(self, choice: int) -> None:
- self.omen(self, choice: int) -> None:
- self.sage(self, choice: int) -> None:
+ self.move(self, choice: int) -> int:
+ self.reyna_turn(self) -> None:
+ self.update(self) -> None:
+ self.run(self):
    """

    def __init__(self):
        self.gameover = False
        self.roundsleft = 50
        self.win = False

    def intro(self) -> None:
        """
        print intro message, instructions, etc.
        returns nothing 
        """
        print(intro)

    agent_descriptions = agent

    agent_names = ["Jett", "Sova", "Omen", "Sage"]
    maps = ["Ascent", "Haven", "Bind"]

    def countdown(self) -> None:
        """
        counts down to the start of the game
        """
        for i in range(5):
            print(f"{5-i}...")
            time.sleep(1)
        print("GAME STARTS NOW!!!!")
        time.sleep(1)
        print(divider)

    def prompt(self, options: list, message: str, cancel: bool) -> int:
        """
        Takes input from the player to pass on to other methods
        
        - options is a list of choices given to the player
        - message is a description of the choice to be made
        - cancel is whether or not an option to cancel the choice should be available
        
        Returns a number corresponding to an option, or -1 if action is cancelled
        """
        print(message)
        for i, a in enumerate(options):
            print(f"[{i+1}]: {a}")
        if cancel:
            print(f"[{len(options)+1}]: Cancel action")
        if cancel:
            accept = [str(x) for x in range(1, len(options) + 2)]
        else:
            accept = [str(x) for x in range(1, len(options) + 1)]
        choice = input("Pick a number: ")
        while choice not in accept:
            print("Invalid input")
            choice = input("Pick a number: ")
        print(divider)
        if int(choice) == len(options) + 1:
            return -1
        else:
            return int(choice) - 1

    def agent_select(self, choice: int) -> str:
        """
        takes in choice of agent as a number
        return agent name as string
        """
        agent_names = ["jett", "sova", "omen", "sage"]
        return agent_names[choice]

    def map_select(self, choice: int) -> None:
        """
        takes in choice of map as a number
        makes map 
        """
        if choice == 0:
            self.map = maps.make_map("ascent")
        elif choice == 1:
            self.map = maps.make_map("haven")
        elif choice == 2:
            self.map = maps.make_map("bind")

    def initialise(self, agent_name: str) -> None:
        """
        scatters orbs and creatures through the map
        creates player class
        sets cooldown for player
        sets starting positions for reyna and player
        """
        creatures = 5
        orbs = 8
        rooms = self.map.room_names()
        spawn_areas = rooms[1:-1]

        spawn_creatures = random.sample(spawn_areas, creatures)
        for room in spawn_creatures:
            self.map.get_room(room).take_char(enemy. Creature(dmg=30))

        spawn_orbs = random.sample(spawn_areas, orbs)
        for room in spawn_orbs:
            self.map.get_room(room).take_obj(objects.Orb(buff=50))

        self.player = agents.create(agent_name, hp=100)
        self.reyna = enemy.Boss("Reyna", hp=100)

        current_room = self.map.get_room(rooms[0])
        current_room.take_char(self.player)
        reyna_room = self.map.get_room(rooms[-1])
        reyna_room.take_char(self.reyna)

    def desc(self) -> None:
        """
        describe the current room, presence of objects,
        available paths, current hp and ability usage options
        """
        current_room = self.map.locate_char(self.player.name)
        reyna_room = self.map.locate_char(self.reyna.name)
        print(f"There are {self.roundsleft} rounds left.")
        print(f"You are in {current_room.name}.")
        print(f"You have {self.player.hp} hp.\n")

        if reyna_room.name in current_room.paths():
            print(
                f"You hear footsteps nearby...Reyna is in {reyna_room.name}\n."
            )

        print("You can move to the following rooms: ")
        paths = current_room.paths()
        for path in paths:
            print(path)
        print()
        if self.player.get_ability().is_charged():
            print("ABILITY READY!")
        else:
            print(
                f"{self.player.get_ability().timer} turns until you can use your ability."
            )
        print(divider)

    def ability(self) -> None:
        """
        uses the player's ability based on
        the agent they selected
        """
        current_room = self.map.locate_char(self.player.name)
        reyna_room = self.map.locate_char(self.reyna.name)
        ability_ = self.player.get_ability()
        if not ability_.is_charged():
            print("ABILITY NOT READY YET!")
            return
        if isinstance(self.player, agents.Sova):
            choice = ability_.prompt_choice(self.player.name, self.map, current_room)
            if choice:
                ability_.use(self.player.name, self.map, current_room, choice)
        elif isinstance(self.player.name, agents.Omen):
            choice = ability_.prompt_choice(self.player.name, self.map, current_room)
            if choice:
                ability_.use(self.player.name, self.map, current_room, choice)
        elif isinstance(self.player, agents.Sage):
            choice = ability_.prompt_choice(self.player.name, self.map, current_room)
            if choice:
                ability_.use(self.player.name, self.map, current_room, choice)
        else:
            print("Jett's ability cannot be manually activated\n")

    def jett(self) -> None:
        """
        if player is about to die, moves player
        to an adjacent room of the player's choice
        and avoid death
        """
        current_room = self.map.locate_char(self.player.name)
        paths = current_room.paths()
        outcome = random.choice(paths)
        print("You were about to die. You used dash to escape.")
        print(f"You are now in {outcome}.")
        self.player.get_ability().reset()
        next_room = self.map.get_room(outcome)
        player = current_room.give_char(self.player.name)
        next_room.take_char(player)
        self.update()

    def move(self, choice: int) -> int:
        """
        takes in a chosen room as a number
        moves player to chosen room
        """
        current_room = self.map.locate_char(self.player.name)
        reyna_room = self.map.locate_char(self.reyna.name)
        next_room = self.map.get_room(current_room.paths()[choice])
        player = current_room.give_char(self.player.name)
        next_room.take_char(player)

    def reyna_turn(self) -> None:
        """
        Moves reyna to a room adjacent to her current
        room randomly
        """
        current_room = self.map.locate_char(self.player.name)
        reyna_room = self.map.locate_char(self.reyna.name)
        paths = reyna_room.paths()
        next_room = self.map.get_room(random.choice(paths))
        reyna = current_room.give_char(self.reyna.name)
        next_room.take_char(reyna)

    def update(self) -> None:
        """
        adjust player hp based on presence of orbs, 
        creatures, and reyna
        returns None
        """
        current_room = self.map.locate_char(self.player.name)
        reyna_room = self.map.locate_char(self.reyna.name)
        if reyna_room.name == current_room.name:
            print("\nReyna has found you!")
            if self.player.hp >= 300:
                self.win = True
                print("Somehow, you manage to win the gunfight.")
                self.gameover = True
            elif isinstance(self.player, agents.Jett):
                ability = self.player.get_ability()
                if ability.is_charged():
                    choice = ability.prompt_choice(self.player.name, self.map, current_room)
                    if choice:
                         ability.use(self.player.name, self.map, current_room, choice)
            else:
                self.gameover = True
                print(
                    "Reyna annihilates you before you can even register her presence."
                )
        else:
            if current_room.has_char("Creature"):
                creature = current_room.give_char("Creature")
                if self.player.hp <= 30:
                    if isinstance(self.player, agents.Jett):
                        ability = self.player.get_ability()
                        if ability.is_charged():
                            choice = ability.prompt_choice(self.player.name, self.map, current_room)
                            if choice:
                                 ability.use(self.player.name, self.map, current_room, choice)
                    else:
                        print(
                            f"There is utility in this room, you lose {creature.dmg} hp handling it.\n"
                        )
                        print("Unfortunately, it was enough to kill you.\n")
                        self.gameover = True
                        return
                else:
                    print(
                        f"There is utility in this room, you lose {creature.dmg} hp handling it.\n"
                    )
                    self.player.injure(creature.dmg)
            if current_room.has_obj("Orb"):
                orb = current_room.give_obj("Orb")
                print(f"There is a shield orb in this room, you gain {orb.buff} hp.\n")
                self.player.buff(orb.buff)

    def run(self):
        """run the game"""
        self.intro()
        agent_name = self.agent_select(
            self.prompt(self.agent_names, self.agent_descriptions, False))
        self.map_select(self.prompt(self.maps, "Choose a map", False))
        self.initialise(agent_name)
        self.countdown()

        while not self.gameover:
            current_room = self.map.locate_char(self.player.name)
            reyna_room = self.map.locate_char(self.reyna.name)
            self.desc()
            advance = False
            while not advance:
                action = self.prompt(["Move", "Stay", "Ability"],
                                     "You can do the following: ", False)
                if action == 0:
                    choice = self.prompt(current_room.paths(),
                                         "Where do you want to go?", True)
                    if choice == -1:
                        pass
                    else:
                        self.move(choice)
                        advance = True
                elif action == 1:
                    advance = True
                    print(
                        f"You stay in {current_room.name} for this turn."
                    )
                elif action == 2:
                    self.ability()
                    if self.gameover == True:
                        break
                    else:
                        self.desc()
            self.player.update()
            if self.gameover:
                break
            else:
                self.update()
            if self.gameover:
                break
            else:
                self.reyna_turn()
                self.update()
            self.roundsleft = self.roundsleft - 1
            if self.roundsleft == 0:
                print(timeout)
                break
        if self.win:
            print(victory)
        else:
            print(defeat)
