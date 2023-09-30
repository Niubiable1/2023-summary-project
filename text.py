from typing import Any

divider = "====================================================="

intro = f"""Welcome to Valorant.
        
Your team all got killed by the Ranked Demon Reyna on the enemy team, 
you need to clutch. 

The Reyna will certainly one tap you the second you get into an encounter so the only way you're going to win this is by picking up enough shields (total 300hp) to not instantly die. 

Shield orbs can be found randomly throughout the map, and add 50hp to your character. 

There is still enemy utility scattered around the map, each piece you encounter will deduct 30hp from your character. 

You also have an agent ability, which will hopefully give you an edge over this no-lifer. Using an ability does not pass your turn. 

You are on attack, so you have a time limit of 50 rounds to find and kill Reyna in order to win.

Remember, CLUTCH OR GAE!!

{divider}"""

agent = f"""CHOOSE YOUR AGENT:
 
[1] Jett: Dash into an adjacent room if you would otherwise die (does not refresh)
    
[2] Sova: Scan an adjacent room for information (cooldown: 2 turn)
    
[3] Omen: Move to any room on the map (cooldown: 5 turns)
    
[4] Sage: Block a path from your current room to an adjacent one permanently (cooldown: 3 turns)
{divider}"""

victory = """
         _________ _______ _________ _______  _______          
|\     /|\__   __/(  ____ \\\__   __/(  ___  )(  ____ )|\     /|
| )   ( |   ) (   | (    \/   ) (   | (   ) || (    )|( \   / )
| |   | |   | |   | |         | |   | |   | || (____)| \ (_) / 
( (   ) )   | |   | |         | |   | |   | ||     __)  \   /  
 \ \_/ /    | |   | |         | |   | |   | || (\ (      ) (   
  \   /  ___) (___| (____/\   | |   | (___) || ) \ \__   | |   
   \_/   \_______/(_______/   )_(   (_______)|/   \__/   \_/   
"""

defeat = """
 ______   _______  _______  _______  _______ _________
(  __  \ (  ____ \(  ____ \(  ____ \(  ___  )\__   __/
| (  \  )| (    \/| (    \/| (    \/| (   ) |   ) (   
| |   ) || (__    | (__    | (__    | (___) |   | |   
| |   | ||  __)   |  __)   |  __)   |  ___  |   | |   
| |   ) || (      | (      | (      | (   ) |   | |   
| (__/  )| (____/\| )      | (____/\| )   ( |   | |   
(______/ (_______/|/       (_______/|/     \|   )_(   
"""

timeout = """You have run out of time, the round is over."""


def prompt_valid_choice(options: list, message: str, cancel: bool) -> Any:
        """Prompts the player to pick a valid choice.
        
        - options is a list of choices given to the player
        - message is a description of the choice to be made
        - cancel is whether or not an option to cancel the choice should be available
        
        Returns a number corresponding to an option, or -1 if action is cancelled
        """
        print(message)
        for i, a in enumerate(options, start=1):
            print(f"{i}. {a}")
        prompt = "Pick a number (or 'c' to cancel): " if cancel else "Pick a number: "
        while True:  
            choice = input(prompt)
            if choice.lower() == 'c':
                print(divider)
                return None
            if not choice.isdecimal():
                print("Invalid input")
                continue
            index = int(choice) - 1
            if 0 <= index < len(options):
                print(divider)
                return options[index]
