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

- self.player_pos: room object
the room the player is currently in

- self.reyna_pos: room object
the room the monster is currently in


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

        self.player_pos = self.map.get_room(rooms[0])
        self.reyna_pos = self.map.get_room(rooms[-1])

    def desc(self) -> None:
        """
        describe the current room, presence of objects,
        available paths, current hp and ability usage options
        """
        print(f"There are {self.roundsleft} rounds left.")
        print(f"You are in {self.player_pos.name}.")
        print(f"You have {self.player.hp} hp.\n")

        if self.reyna_pos.name in self.player_pos.paths():
            print(
                f"You hear footsteps nearby...Reyna is in {self.reyna_pos.name}\n."
            )

        print("You can move to the following rooms: ")
        paths = self.player_pos.paths()
        for path in paths:
            print(path)
        print()
        if self.player.get_ability().is_charged():
            print("ABILITY READY!")
        else:
            print(
                f"{self.player.cooldown} turns until you can use your ability."
            )
        print(divider)

    def ability(self) -> None:
        """
        uses the player's ability based on
        the agent they selected
        """
        if self.player.get_ability().is_charged():
            if isinstance(self.player, data.Sova):
                choice = self.prompt(self.player_pos.paths(),
                                     "You can scan the following rooms: ",
                                     True)
                if choice != -1:
                    self.sova(choice)
            elif isinstance(self.player, data.Omen):
                choice = self.prompt(self.map.room_names(),
                                     "You can move to the following rooms: ",
                                     True)
                if choice != -1:
                    self.omen(choice)
            elif isinstance(self.player, data.Sage):
                choice = self.prompt(self.player_pos.paths(),
                                     "You can block the following rooms: ",
                                     True)
                if choice != -1:
                    self.sage(choice)
            else:
                print("Jett's ability cannot be manually activated\n")
        else:
            print("ABILITY NOT READY YET!")

    def jett(self) -> None:
        """
        if player is about to die, moves player
        to an adjacent room of the player's choice
        and avoid death
        """
        paths = self.player_pos.paths()
        outcome = random.choice(paths)
        print("You were about to die. You used dash to escape.")
        print(f"You are now in {outcome}.")
        self.player.get_ability().reset()
        self.player_pos = self.map.get_room(outcome)
        self.update()

    def sova(self, choice: int) -> None:
        """
        takes in a chosen room as a number
        return creature presence and orb presence in a room adjacent to the player's
        """
        paths = self.player_pos.paths()
        room = self.map.get_room(paths[choice])
        ustatus = room.has_char("Creature")
        ostatus = room.has_obj("Orb")
        if ustatus == True and ostatus == True:
            print(f"{room.name} has both utility and an orb.")
        elif ustatus == True and ostatus == False:
            print(f"{room.name} has utility.")
        elif ustatus == False and ostatus == True:
            print(f"{room.name} has an orb.")
        else:
            print(f"{room.name} is empty.")
        self.player.get_ability().reset()

    def omen(self, choice: int) -> None:
        """
        takes in a chosen room as a number
        moves player to chosen room
        triggers update
        """
        room = self.map.get_room(self.map.room_names()[choice])
        self.player_pos = room
        self.player.get_ability().reset()
        self.update()

    def sage(self, choice: int) -> None:
        """
        takes in choice of room as a number
        removes path between current room and chosen room permanently
        """
        paths = self.player_pos.paths()
        blocked = paths[choice]
        paths.remove(blocked)
        # TODO: encapsulate path blocking
        self.player_pos._paths = paths

        temp = self.map.get_room(blocked)
        paths = temp.paths()
        paths.remove(self.player_pos.name)
        # TODO: encapsulate path blocking
        temp._paths = paths

        self.player.get_ability().reset()
        print(f"{blocked} is successfully blocked.")
        print(divider)

    def move(self, choice: int) -> int:
        """
        takes in a chosen room as a number
        moves player to chosen room
        """
        room = self.player_pos.paths()[choice]
        self.player_pos = self.map.get_room(room)

    def reyna_turn(self) -> None:
        """
        Moves reyna to a room adjacent to her current
        room randomly
        """
        paths = self.reyna_pos.paths()
        move = random.choice(paths)
        self.reyna_pos = self.map.get_room(move)

    def update(self) -> None:
        """
        adjust player hp based on presence of orbs, 
        creatures, and reyna
        returns None
        """
        if self.reyna_pos == self.player_pos:
            print("\nReyna has found you!")
            if self.player.hp >= 300:
                self.win = True
                print("Somehow, you manage to win the gunfight.")
                self.gameover = True
            elif isinstance(self.player, data.Jett) and self.player.get_ability().is_charged():
                self.jett()
            else:
                self.gameover = True
                print(
                    "Reyna annihilates you before you can even register her presence."
                )
        else:
            if self.player_pos.has_char("Creature"):
                creature = self.player_pos.give_char("Creature")
                if self.player.hp <= 30:
                    if isinstance(self.player, data.Jett) and self.player.get_ability().is_charged():
                        self.jett()
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
            if self.player_pos.has_obj("Orb"):
                orb = self.player_pos.give_obj("Orb")
                print(f"There is a shield orb in this room, you gain {orb.buff} hp.\n")
                self.player.buff(orb.buff)

    def run(self):
        """
        run the game
        """
        self.intro()
        agent_name = self.agent_select(
            self.prompt(self.agent_names, self.agent_descriptions, False))
        self.map_select(self.prompt(self.maps, "Choose a map", False))
        self.initialise(agent_name)
        self.countdown()

        while not self.gameover:
            self.desc()
            advance = False
            while not advance:
                action = self.prompt(["Move", "Stay", "Ability"],
                                     "You can do the following: ", False)
                if action == 0:
                    choice = self.prompt(self.player_pos.paths(),
                                         "Where do you want to go?", True)
                    if choice == -1:
                        pass
                    else:
                        self.move(choice)
                        advance = True
                elif action == 1:
                    advance = True
                    print(
                        f"You stay in {self.player_pos.name} for this turn."
                    )
                elif action == 2:
                    self.ability()
                    if self.gameover == True:
                        break
                    else:
                        self.desc()
            self.player.update()
            if self.gameover == True:
                break
            else:
                self.update()
            if self.gameover == True:
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
