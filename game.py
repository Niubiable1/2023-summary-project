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
import text


class Game:
    """Class that creates an instance of the game

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
+ intro() -> None
+ countdown() -> None
+ self.initialise(agent_name: str) -> None
+ self.desc() -> None:
+ self.use_active_ability() -> None
+ self trigger_passive_ability() -> None
+ self.move(choice: int) -> int
+ self.reyna_turn() -> None
+ self.update() -> None
+ self.run()
    """

    def __init__(self):
        self.gameover = False
        self.roundsleft = 50
        self.win = False

    def intro(self) -> None:
        """Print intro message, instructions, etc.
        returns nothing 
        """
        print(text.intro)

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
        print(text.divider)

    def initialise(self, agent_name: str) -> None:
        """Scatters orbs and creatures through the map
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
        self.reyna = enemy.Boss("Reyna", hp=100, dmg=300)

        current_room = self.map.get_room(rooms[0])
        current_room.take_char(self.player)
        reyna_room = self.map.get_room(rooms[-1])
        reyna_room.take_char(self.reyna)

    def desc(self) -> None:
        """Describe the current room, presence of objects,
        available paths, current hp and ability usage options
        """
        current_room = self.map.locate_char(self.player.name)
        print(f"There are {self.roundsleft} rounds left.")
        print(f"You are in {current_room.name}.")
        print(f"You have {self.player.hp} hp.\n")

        for room_name in current_room.paths():
            if self.map.get_room(room_name).has_char("Reyna"):
                print(
                    f"You hear footsteps nearby...Reyna is in {room_name}\n."
                )
                break
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
        print(text.divider)

    def use_active_ability(self) -> None:
        """Uses the player's ability based on
        the agent they selected
        """
        current_room = self.map.locate_char(self.player.name)
        ability_ = self.player.get_ability()
        if not ability_.is_active():
            print("{ability_.name} cannot be manually activated\n")
            return
        if not ability_.is_charged():
            print("ABILITY NOT READY YET!")
            return
        choice = ability_.prompt_choice(self.player.name, self.map, current_room)
        if choice:
            ability_.use(self.player.name, self.map, current_room, choice)
            
    def trigger_passive_ability(self) -> None:
        """Triggers the player's ability based on
        the agent they selected
        """
        current_room = self.map.locate_char(self.player.name)
        ability_ = self.player.get_ability()
        if not ability_.is_passive():
            return
        if not ability_.is_charged():
            return
        choice = ability_.prompt_choice(self.player.name, self.map, current_room)
        if choice:
            ability_.use(self.player.name, self.map, current_room, choice)

    def move(self, choice: str) -> None:
        """Takes in a chosen room as a number
        moves player to chosen room
        """
        current_room = self.map.locate_char(self.player.name)
        next_room = self.map.get_room(choice)
        player = current_room.give_char(self.player.name)
        next_room.take_char(player)

    def reyna_turn(self) -> None:
        """Moves reyna to a room adjacent to her current
        room randomly
        """
        reyna_room = self.map.locate_char(self.reyna.name)
        paths = reyna_room.paths()
        next_room = self.map.get_room(random.choice(paths))
        reyna = reyna_room.give_char(self.reyna.name)
        next_room.take_char(reyna)

    def encounter(self, player: agents.Agent, creature: data.Character) -> None:
        """Apply effects of interacting creature"""
        if isinstance(creature, enemy.Boss):
            print(f"\n{creature.name} has found you!")
        player.injure(creature.dmg)
        if isinstance(creature, enemy.Creature):
            print(
                f"There is utility in this room, you lose {creature.dmg} hp handling it.\n"
            )
        if player.is_dead():
            self.gameover = True
            if isinstance(creature, enemy.Boss):
                print(
                    "Reyna annihilates you before you can even register her presence."
                )
            elif isinstance(creature, enemy.Creature):
                print("Unfortunately, it was enough to kill you.\n")
        else:
            self.win = True
            self.gameover = True
            print("Somehow, you manage to win the gunfight.")

    def interact(self, player: agents.Agent, object: data.Object) -> None:
        """Apply effects of interacting with object"""
        if isinstance(object, objects.Orb):
            print(f"There is a shield orb in this room, you gain {object.buff} hp.\n")
            player.buff(object.buff)

    def handle_encounter(self, room: data.Room) -> None:
        """Process any encounters between characters in the room."""
        for char in room.characters():
            # Creature is removed from room
            # TODO: Need to add back if creature is not dead
            creature = room.give_char(char)
            self.encounter(self.player, creature)

    def handle_interaction(self, room: data.Room) -> None:
        """Process any interactions between player and objects in the room."""
        for obj in room.objects():
            object = room.give_obj(obj)
            self.interact(self.player, object)

    def update(self) -> None:
        """
        adjust player hp based on presence of orbs, 
        creatures, and reyna.
        Triggers any passive abilities.
        returns None
        """
        current_room = self.map.locate_char(self.player.name)
        # Trigger any passive abilities, if valid
        self.trigger_passive_ability()
        # Jett should have escaped by now, if he can use his ability
        # Should test
        self.handle_encounter(current_room)
        self.handle_interaction(current_room)

    def user_select(self, current_room: data.Room) -> str:
        """Prompt the user to select an action.
        Return the chosen action.
        """
        action = text.prompt_valid_choice(
            ["Move", "Stay", "Ability"],
            "You can do the following: ",
            cancel=False
        )
        if action == "Move":
            choice = text.prompt_valid_choice(
                current_room.paths(),
                "Where do you want to go?",
                cancel=True
            )
            return choice
        return action

    def run(self):
        """run the game"""
        self.intro()
        agent_name = text.prompt_valid_choice(
            list(agents.SELECT.keys()),
            text.agent,
            cancel=False
        )
        choice = text.prompt_valid_choice(
            maps.available,
            "Choose a map",
            cancel=False
        )
        self.map = maps.make_map(choice)
        self.initialise(agent_name)
        self.countdown()

        while not self.gameover:
            current_room = self.map.locate_char(self.player.name)
            self.desc()
            advance = False
            while not advance:
                action = self.user_select(current_room)
                if action == "Stay":
                    advance = True
                    print(
                        f"You stay in {current_room.name} for this turn."
                    )
                elif action == "Ability":
                    self.use_active_ability()
                else:  # Move
                    if not choice:
                        pass
                    else:
                        advance = True
                        self.move(choice)
            if self.gameover:
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
                print(text.timeout)
                break
        if self.win:
            print(text.victory)
        else:
            print(text.defeat)
