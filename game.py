# Built-in imports
import random
import time

# Local imports
import ability
import action
import agents
import data
import enemy
import maps
import objects
import text


class Game:
    """Class that creates an instance of the game

    Attributes
    ----------
    + gameover: Bool
      Whether or not the game is over
    + win: Bool
      Whether or not the player won
    - roundsleft: int
      Number of turns before game ends
    - map: Map
      A map encapsulating rooms
    - player: player object
      An object containing attributes related to the player
    
    Methods
    -------
    + intro() -> None
    + countdown() -> None
    + initialise(agent_name: str) -> None
    + desc() -> None
    + use_active_ability(player, room) -> None
    + trigger_passive_ability(player, room) -> None
    + move(character, choice: str) -> None
    + encounter(player, creature) -> None
    + interact(player, object) -> None
    + handle_encounter(room) -> None
    + handle_interaction(room) -> None
    + select_action(character, room) -> Action
    + do_action(action) -> bool
    + update() -> None
    + run() -> None
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

    def use_active_ability(self, player: agents.Agent, room: data.Room) -> None:
        """Uses the player's ability based on
        the agent they selected
        """
        if not isinstance(player, agents.Agent):
            return
        room = self.map.locate_char(player.name)
        ability_ = player.get_ability()
        if not ability_.is_active():
            print("{ability_.name} cannot be manually activated\n")
            return
        if not ability_.is_charged():
            print("ABILITY NOT READY YET!")
            return
        choice = ability_.prompt_choice(player.name, self.map, room)
        if choice:
            ability_.use(player.name, self.map, room, choice)
            
    def trigger_passive_ability(self, player: agents.Agent, room: data.Room) -> None:
        """Triggers the player's ability based on
        the agent they selected
        """
        ability_ = player.get_ability()
        if not ability_.is_passive():
            return
        if not ability_.is_charged():
            return
        choice = ability_.prompt_choice(player.name, self.map, room)
        if choice:
            ability_.use(player.name, self.map, room, choice)

    def move(self, character: data.Character, choice: str) -> None:
        """Takes in a chosen room as a number
        moves player to chosen room
        """
        current_room = self.map.locate_char(character.name)
        next_room = self.map.get_room(choice)
        current_room.give_char(character.name)
        next_room.take_char(character)

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

    def select_action(self, character: data.Character, room: data.Room) -> action.Action | None:
        if isinstance(character, agents.Agent):
            return self.user_select(character, room)
        if isinstance(character, enemy.Boss):
            return self.reyna_select(character, room)

    def user_select(self, player: agents.Agent, current_room: data.Room) -> action.Action | None:
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
                current_room.paths(),
                "Where do you want to go?",
                cancel=True
            )
            if not choice:
                return None
            return action.Move(player, {"room": choice})
        if choice == "Stay":
            return action.Stay(player, {"room": choice})
        if choice == "Ability":
            return action.UseAbility(player, {"room": choice})
        raise ValueError(f"{choice}: invalid action")

    def reyna_select(self, character: data.Character, current_room: data.Room) -> action.Action:
        """Select a move for Reyna"""
        reyna_room = self.map.locate_char(character.name)
        paths = reyna_room.paths()
        next_room = self.map.get_room(random.choice(paths))
        return action.Move(character, {"room": next_room})

    def do_action(self, choice: action.Action | None) -> bool:
        """Carry out the effects of the chosen action.
        If the actions constitute a turn, return True, otherwise False.
        """
        if choice is None:
            return False
        if isinstance(choice, action.Move):
            self.move(choice.character, choice.data["room"])
            return True
        if isinstance(choice, action.Stay):
            print(
                f"You stay in {choice.data['room']} for this turn."
            )
            return True
        if isinstance(choice, action.UseAbility):
            if isinstance(choice.character, agents.Agent):
                self.use_active_ability(choice.character, choice.data["room"])
            elif isinstance(choice.character, enemy.Boss):
                print(f"{choice.character.name} has no abilities")
            return False
        raise TypeError(f"{choice}: unhandled action")

    def update(self, character: data.Character) -> None:
        """
        adjust player hp based on presence of orbs, 
        creatures, and reyna.
        Triggers any passive abilities.
        returns None
        """
        room = self.map.locate_char(character.name)
        # Trigger any passive abilities, if valid
        if isinstance(character, agents.Agent):
            self.trigger_passive_ability(character, room)
        # Jett should have escaped by now, if he can use his ability
        # Should test
        self.handle_encounter(room)
        self.handle_interaction(room)

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

        while self.roundsleft and not self.gameover:
            for character in [self.player, self.reyna]:
                
                end_turn = False
                while not end_turn:
                    room = self.map.locate_char(character.name)
                    self.desc()
                    choice = self.select_action(character, room)
                    end_turn = self.do_action(choice)
                character.update()
                self.update(character, room)
            self.roundsleft -= 1
            if self.roundsleft == 0:
                print(text.timeout)

        if self.win:
            print(text.victory)
        else:
            print(text.defeat)
