'''Jon Ormond'''
# Required Tasks
# TODO: Review all text, and instructions for completeness
# TODO: UAT

# Optional Tasks
# TODO: in fight(), check for a single hit point of damage make print statement "point" instead of "points" for hero and monster damage
# TODO: on the item and monster display, check for a leading vowel and switch between "a" and "an" as appropriate
# TODO: Complete chance for fight subroutine if monster present, cut if needed
# TODO: Add "chance for fight" subroutine to Move, Look, Get, Drop, Use subroutines (or maybe to main loop)

# Import JSON module to work with the json data files
import json
# Import OS module to access the Get_Terminal_Size function for console line count
import os
# Import Random module for use in the fight function random number generation
import random

def main():
    '''main()'''
    # Set variables used in the game
    user_input = ""
    current_room = "Library" # TODO: Change back to "Castle" before Prod
    winning = ["Opal", "Emerald", "Ruby", "Sapphire", "Diamond", "Pearl"]
    
    # Display game open text and get hero name and skill set
    # TODO: un-remark intro() line before Prod
    # intro() 
    
    # Start main game loop
    # Although set up as an infinite loop, there are exit points within
    # the main loop based on completion of the game or at the request
    # of the user.
    while True:
        
        # There are a few "immediate effect" conditions so
        # at the begining of this loop we need to check if
        # we meet any of those conditions and act accordingly.

        # Immediate Condition 1: Hero is at the castle with all the gems (i.e. player wins!)
        if current_room == "Castle" and all(things in hero.inventory for things in winning):
            hero_wins()
            return
        # Immediate Condition 2: Hero just walked off a cliff and died
        elif current_room == "Cliff":
            hero_cliff()
            return
        elif hero.life <= 0:
            print('You were warned this was a dangerous adventure, and while\nyou were not successful in your quest you were brave and\nvaliant. Bards will sing epic songs of your legendary tail.\n')
            return
        
        # The main purpose of this loop is to display the standard
        # output screen of information and accept and route the
        # user command. The display output is aligned thusly:
        # 
        # Current location description
        # (optional) Any items in the room
        # (optional) Any monsters in the room
        #
        # The hero's inventory
        # The hero's weapon
        # The hero's health
        #
        # The possible directions and what is in that direction
        # 
        # A reminder of the verbs
        # An input prompt for a command
        #

        # Show the description of the current room from the map dictionary
        print(atlas[current_room]['Description'])

        # Show any items
        if len(atlas[current_room]['Items']) > 0:
            display_items = 'You see a '
            for item in atlas[current_room]['Items']:
                display_items += color.GREEN + item + color.END + ', '
            display_items = display_items[:-2] + ' there for the taking.'
            print(display_items)

        # Show any monsters
        if 'Monster' in atlas[current_room]:
            print('Oh no! There is a big scary ' + color.RED + atlas[current_room]['Monster'] + color.END + ' in here with you!!')

        # Show the hero's current inventory list
        if "Empty" not in hero.inventory:
            inventory_items = '\nYour Inventory: '
            for item in hero.inventory:
                inventory_items += color.GREEN + item + color.END + ', '
            inventory_items = inventory_items[:-2]
            print(inventory_items)
        else:
            print('\nYour Inventory: Empty')

        # Show the hero's current equipped weapon
        if hero.weapon != "Fists":
            print('Your Weapon: ' + color.GREEN + hero.weapon + color.END)
        else:
            print('Your Weapon: Fists')
            
        # Show the hero's remaining life
        if hero.life > 80:
            life_color = color.GREEN
        elif hero.life > 30:
            life_color = color.YELLOW
        else:
            life_color = color.RED + color.BOLD
        print('Your health: ' + life_color + str(hero.life) + color.END +' out of ' + str(hero.life_max) +'\n')
        
        # Show the possible directions available from this location
        # Start with a begining of the line in a variable and add each valid direction to the string
        directions = "Possible Directions: you see "
        # Check each the map dictionary for the current room and see if the cardinal direction exists
        if 'North' in atlas[current_room]:
            # If this direction exists, append this direction, nicely formated with an ending comma to the directions string
            directions +='a ' + atlas[current_room]['North'] + ' to the ' + color.CYAN + 'North' + color.END + ', '
        if 'East' in atlas[current_room]:
            directions +='a ' + atlas[current_room]['East'] + ' to the ' + color.CYAN + 'East' + color.END + ', '
        if 'South' in atlas[current_room]:
            directions +='a ' + atlas[current_room]['South'] + ' to the ' + color.CYAN + 'South' + color.END + ', '
        if 'West' in atlas[current_room]:
            directions +='a ' + atlas[current_room]['West'] + ' to the ' + color.CYAN + 'West' + color.END + ', '
        # The last direction appended will have a trailing comma and a space, so we need to trim those two characters off
        # and add a period
        directions = directions[:-2] + "."
        # Print the available directions for this location
        print(directions, '\n\n')
        # Print a reminder of the available verbs for the user to use
        print('(Verbs: Move, Look, Get, Use, Drop, Fight, or Instructions)')
        # Get the users command
        user_input = input('Please enter a command (verb noun): ')
        # Check if the user just wants to end the game
        # Change the input to lower case, and split off anything after the verb if the user added a noun
        if user_input.lower().split(' ')[0] in ['quit','exit','bye','goodbye','later']:
            # Double check as this eliminates any progress made in the game
            temp = input('You have asked to quit the game! Are you sure? Y/n ') or 'y'
            # Eval the users second answer
            if temp[0].lower() == 'y':
                # Yes, they want to quit, break this main game loop, and the script heads to the ending text.
                break
            else:
                # The user has changed their mind, don't process this input, just start the next iteration of the loop
                # Display a content break
                print(SECTION_BREAK)
                continue
        # Display a content break
        print(SECTION_BREAK)
                
        # Check for a verb-only command, if not then check user_input has at least two parts separated by a space
        if user_input.find(" ") < 1:
            if user_input.lower()[0] in ["i", "t", "r"]:
                user_verb = user_input.split(" ",maxsplit=1)[0][0].lower()
                user_noun = "none"
            else:
                print(color.CYAN + color.BOLD + 'Invalid input' + color.END + ': you must enter your command with a verb, a space, and a noun e.g. "move north"\n')
                continue
        else:
            # The input has a space, break the input into the first word as the verb, and second part as the noun
            # maxsplit is used to ensure if the noun is two word, only the first word is split.
            # on the verb an extra [0] is used to only pull the first character of the verb.
            user_verb = user_input.split(" ",maxsplit=1)[0][0].lower()
            user_noun = user_input.split(" ",maxsplit=1)[1].lower()
        
        # Based on the verb, decide which action function to call
        # User wants to move
        if user_verb == 'm':
            current_room = move(current_room, user_noun)
        # User wants to look at an item
        elif  user_verb == 'l':
            look_item(current_room, user_noun)
        # User wants to get an item
        elif  user_verb == 'g':
            get_item(current_room, user_noun)
        # User wants to use an item
        elif  user_verb == 'u':
            use_item(current_room, user_noun)
        # User wants to drop an item
        elif  user_verb == 'd':
            drop_item(current_room, user_noun)
        # User wants to fight a monster
        elif  user_verb == 'f':
            fight(current_room, user_noun)
        # Users wants to read the game instructions
        elif  user_verb == 'i':
            instructions()
        # if we've gotten this far, the verb letter wasn't recognized
        else:
            print(color.CYAN + color.BOLD + 'Invalid input' + color.END + ': the verb used was not recognized, please try again.\n')
   
def move(current_room, direction):
    '''move(current_room, direction)'''
    # Check for single character direction, if so, expand to full cardinal direction name
    if direction.lower() == 'n':
        direction = "North"
    elif direction.lower() == 'e':
        direction = "East"
    elif direction.lower() == 's':
        direction = "South"
    elif direction.lower() == 'w':
        direction = "West"
    direction = direction.capitalize()
    if direction not in atlas[current_room]:
        new_room = current_room
        print(color.CYAN + color.BOLD + 'Invalid input' + color.END + ': invalid direction entered for this room, please try again.\n')
    else: 
        new_room = atlas[current_room][direction]
        print(color.GREEN + 'Success' + color.END + ': You have moved to a new location!\n')
    return new_room
    
def look_item(current_room, item_to_see):
    '''look_item(current_room, look_item)'''
    item_to_see = item_to_see.title()
    if item_to_see not in items:
        print(color.CYAN + 'Invalid input' + color.END + ': item does not exist, please try again.\n')
        return
    # If noun is hero weapon or item in inventory or in room items display item
    if item_to_see in atlas[current_room]["Items"] or item_to_see == hero.weapon or item_to_see in hero.inventory:
        print(color.GREEN + 'Success' + color.END + ': ' + items[item_to_see]['Description'] + '\n')
    else:
        # Else "You can't see that from here!"
        print(color.CYAN + 'Invalid input' + color.END + ': item not found here, please try again.\n')
        
def get_item(current_room, requested_item):
    '''get_item(current_room, requested_item)'''
    requested_item = requested_item.title()
    item_found = False
    for item in atlas[current_room]["Items"]:
        if item == requested_item:
            item_found = True
            if (hero.weapon == 'Fists' and len(hero.inventory) >= hero.inventory_max) or (hero.weapon != 'Fists' and len(hero.inventory) >= hero.inventory_max - 1):
                print(color.CYAN + 'Inventory Full' + color.END + ': You can\'t carry any more. To get this item')
                print('                you must first drop your weapon or another')
                print('                inventory item to make room for it.\n')
            else:
                atlas[current_room]["Items"].remove(item)
                hero.inventory.append(item)
                if 'Empty' in hero.inventory:
                    hero.inventory.remove('Empty')
                print(color.GREEN + 'Success' + color.END + ': You have added an item to your inventory!\n')

    if not item_found:
        print(color.CYAN + 'Invalid Object' + color.END + ': I can\'t find that item!\n')
    
def use_item(current_room, item_to_use):
    '''use_item(current_room, use_item)'''
    item_to_use = item_to_use.title()
    if item_to_use not in items:
        print(color.CYAN + 'Invalid input' + color.END + ': item does not exist, please try again.\n')
        return
    # If type is weapon equip, swap if needed
    if item_to_use in hero.inventory and items[item_to_use]['Item Type'] == 'Weapon' and hero.weapon == "Fists":
        hero.weapon = item_to_use
        hero.inventory.remove(item_to_use)
        if len(hero.inventory) == 0:
            hero.inventory.append('Empty')
        print(color.GREEN + 'Success' + color.END + ': you have equipped a new weapon!\n')
    elif item_to_use in hero.inventory and items[item_to_use]['Item Type'] == 'Weapon':
        hero.inventory.remove(item_to_use)
        hero.inventory.append(hero.weapon)
        hero.weapon = item_to_use
        print(color.GREEN + 'Success' + color.END + ': you have equipped a new weapon and your old one is in your inventory!\n')
    # Else If type is health, add to health to max (but not over)
    elif item_to_use in hero.inventory and items[item_to_use]['Item Type'] == 'Health':
        # Calc hero life + health boost
        hero.life += int(items[item_to_use]['Restore Points'])
        hero.inventory.remove(item_to_use)
        if len(hero.inventory) == 0:
            hero.inventory.append('Empty')
        if hero.life > hero.life_max:
            hero.life = hero.life_max
            print(color.GREEN + 'Success' + color.END + ': you feel energy and health surging in your body, your health is maxed!\n')
        else:
            print(color.GREEN + 'Success' + color.END + ': you feel energy and health surging in your body, your health is increased!\n')
    # Else If type is a gem, tell the player to save it for the king
    elif item_to_use in hero.inventory and items[item_to_use]['Item Type'] == 'Gem':
        print(color.CYAN + 'Invalid input' + color.END + ': you can\'t use that, you\'re saving it for the King, please try again.\n')
    # Else If type is a regular item, display an error message
    elif item_to_use in hero.inventory and items[item_to_use]['Item Type'] == 'Item':
        print(color.CYAN + 'Invalid input' + color.END + ': this item can\'t be used, it just looks pretty, please try again.\n')
    elif item_to_use in atlas[current_room]["Items"]:
        print(color.CYAN + 'Invalid input' + color.END + ': the item must be in your inventory before it can be used, please try again.\n')
    # Anything else "I don't know how to use that"
    else:
        print(color.CYAN + 'Invalid input' + color.END + ': that item can\'t be used, please try again.\n')
    return
    
def drop_item(current_room, item_to_drop):
    '''drop_item(current_room, drop_item)'''
    item_to_drop = item_to_drop.title()
    if item_to_drop not in items:
        print(color.CYAN + 'Invalid input' + color.END + ': item does not exist, please try again.\n')
    # If weapon drop add to room inventory
    elif hero.weapon == item_to_drop:
        hero.weapon = "Fists"
        atlas[current_room]["Items"].append(item_to_drop)
        print(color.GREEN + 'Success' + color.END + ': you have dropped your equipped weapon, back to bare knuckles for you!\n')
    # else if in inventory drop and add to room inventory
    elif item_to_drop in hero.inventory:
        hero.inventory.remove(item_to_drop)
        if len(hero.inventory) == 0:
            hero.inventory.append('Empty')
        atlas[current_room]["Items"].append(item_to_drop)
        print(color.GREEN + 'Success' + color.END + ': you have dropped an item, it feels nice not to carry around so much weight!\n')
    # Invalid data
    else:
        print(color.CYAN + 'Invalid input' + color.END + ': you can\'t drop what you don\'t have, please try again.\n')

def fight(current_room, monster):
    '''fight(current_room)'''
    monster = monster.title()
    if monster not in atlas[current_room]["Monster"]:
        print(color.CYAN + 'Invalid input' + color.END + ': no such monster here for you to fight\n')
        return

    # Battle Logic (for both hero and Monster)
    # Roll for initiative, roll damage, calculate total with weapon multiplier
    #     Attack Roll is 1 - 20: This provided an Attack Role effect based on the Attack Roll with < 5 missed, >= 5 hits, >= 10 double damage, >= 15 triple damage
    #     Damage roll is 1 - 12
    #     Total_Damage = Damage_Roll * (1 + (Weapon_Multiplier/100)) * attack_roll_effect
    #
    #     e.g. (min)           5     * (1 + (     10          /100)) *          0         =  0.0 total damage
    #     e.g                  6     * (1 + (     30          /100)) *          2         = 15.6 total damage
    #     e.g. (max)          12     * (1 + (     40          /100)) *          3         = 50.4 total damage
    #
    
    # Start battle
    # Hero Attack Phase
    hero_attack_roll = random.randint(1, 21)
    if hero_attack_roll >= 15:
        hero_attack_roll_effect = 3
    elif hero_attack_roll >= 10:
        hero_attack_roll_effect = 2
    elif hero_attack_roll >= 5:
        hero_attack_roll_effect = 1
    else:
        hero_attack_roll_effect = 0
    hero_damage_roll = random.randint(1, 13)
    hero_damage_multiplier = int(items[hero.weapon]["Multiplier"]) if hero.weapon != "Fists" else 0
    hero_damage = int(hero_damage_roll * (1 + (hero_damage_multiplier/100)) * hero_attack_roll_effect)
    # Display attack results
    if hero_attack_roll < 5:
        print(color.RED + 'Hero Attack Failed' + color.END + ': you tried really hard, but you completely missed the monster!\n')
    else:
        print(color.GREEN + 'Hero Attack successful' + color.END + f': you have landed a powerful blow of {hero_damage} damage points.\n')
    # Check monster life
    monsters[monster]["Life"] -= hero_damage
    if monsters[monster]["Life"] <= 0:
        print(color.GREEN + 'You win!' + color.END + ': you triumphed over this terrible monster. You truly are a hero!\n')
        atlas[current_room].pop("Monster")
        return

    # Monster Attack Phase
    monster_attack_roll = random.randint(1, 21)
    if monster_attack_roll >= 15:
        monster_attack_roll_effect = 3
    elif monster_attack_roll >= 10:
        monster_attack_roll_effect = 2
    elif monster_attack_roll >= 5:
        monster_attack_roll_effect = 1
    else:
        monster_attack_roll_effect = 0
    monster_damage_roll = random.randint(1, 13)
    monster_damage_multiplier = int(monsters[monster]["Multiplier"])
    monster_damage = int(monster_damage_roll * (1 + (monster_damage_multiplier/100)) * monster_attack_roll_effect)
    # Display attack results
    if monster_attack_roll < 5:
        print(color.GREEN + f'{monster} Attack Failed' + color.END + ': the monster attacked ferociously but you danced\n                      out of the way and the monster completely missed!\n')
    else:
        print(color.RED + f'{monster} Attack successful' + color.END + f': the {monster} has landed a powerful blow of {monster_damage} damage points.\n')
    # Check Hero life
    hero.life -= monster_damage
    if hero.life <= 0:
        print(color.RED + 'Mortal Blow!' + color.END + f': the evil {monster} as landed a mortal blow!\n')

def instructions():
    '''instructions()'''
    # Get number of lines of the console
    console_lines = os.get_terminal_size()[1]
    i = 1
    message = []
    message.append("Instructions for this Text Based Adventure!")
    message.append("")
    message.append("Goal: Collect six gems hidden around the 23 locations in the")
    message.append("      game, then return to the Castle.")
    message.append("")
    message.append("Basic Commands:")
    message.append("  Generally you need to enter a verb and noun to control the hero.")
    message.append("  The verbs are:")
    message.append("  Move  - to move between locations in the world")
    message.append("  Look  - to get more information about an item you see or have")
    message.append("  Get   - to add an item you see to your inventory")
    message.append("  Use   - to consume food or a potion to restore health or to equip")
    message.append("          a weapon in your inventory for use in battle")
    message.append("  Drop  - to drop an item in your inventory, it will appear in the")
    message.append("          the list of items you see in that location")
    message.append("  Fight - used to engage a monster in battle")
    message.append("  Instructions - use this to print these instructions")
    message.append("  Quit  - use to exit the game, WARNING: you will lose all progress")
    message.append("          made in this session")
    message.append("")
    message.append("Each of the above verbs may be abbreviated to a single character")
    message.append("e.g. Instead of the whole word \"Move\", you can simple use \"m\"")
    message.append("(the exception is \"Quit\", that must always be typed fully)")
    message.append("")
    message.append("The verb is followed by a noun, the noun is the object or direction")
    message.append("you wish to act upon.")
    message.append("")
    message.append("Examples:")
    message.append("  Move - 'Move North' or 'm north' or 'm n'")
    message.append("         (directions are the only nouns you may abbreviate)")
    message.append("  Look - 'Look Dagger' or 'l dagger'")
    message.append("  Get - 'Get Dagger' or 'g dagger'")
    message.append("  Use (weapon) - 'Use Dagger' or ' u dagger'")
    message.append("  Use (food) - 'Use Apple' or 'u apple'")
    message.append("  Drop - 'Drop Dagger' or 'd dagger'")
    message.append("  Fight - 'Fight Zombie' or 'f zombie'")
    message.append("  Instructions - 'instructions' or 'i'")
    message.append("  Quit - 'Quit' (can not be abbreviated)")
    message.append("")
    message.append("Noun restrictions:")
    message.append("  - the object you wish to interact with must be in the room")
    message.append("    to 'look' or 'get'.")
    message.append("  - the object you wish to interact with must be in your")
    message.append("    inventory to 'look', 'get', 'use', or 'drop'")
    message.append("")
    message.append("Inventory restrictions:")
    message.append("  You hero is limited to carry only 10 items, this includes")
    message.append("  a weapon. This means if you have a weapon equipped you can")
    message.append("  only carry nine items.")
    message.append("")
    message.append("Monster information:")
    message.append("  You will encounter Monsters on your journey through the")
    message.append("  world. When present in a location with a Monster a warning")
    message.append("  will pop up informing you of the Monster type. You may take")
    message.append("  other actions while in the room with the Monster such as")
    message.append("  'get', 'look', 'use', or 'move'. Any action (verb) other than")
    message.append("  'Fight' will result in a chance that the Monster will attack")
    message.append("  you. If the Monster successfully attacks, you will automatically")
    message.append("  enter the fight phase of the game. While fighting you will")
    message.append("  see the hero health and Monster health after each round of")
    message.append("  attacks. You can choose to run ('Move') at any time (although")
    message.append("  that choice does give the monster a chance to attack before")
    message.append("  you leave!). You can continue fighting until either the hero")
    message.append("  or the monster is dead (when life is zero)")
    
    print()
    for line in message:
        print(line)
        i += 1
        if i >= console_lines - 3:
            response = input("\nPress ENTER to continue (or Q, ENTER to return to the game)...") or "continue"
            print()
            if response.lower()[0] == 'q':
                print(SECTION_BREAK)
                return
            else:
                print("\n\n")
                i = 1
    response = input("\nEnd of instructions\nPress ENTER to continue...")
    print(SECTION_BREAK)

def intro():
    '''intro()'''
    # Display game intro
    print(SECTION_BREAK)
    print('Hello intrepid adventurer!\n')
    print('You are about to embark on an epic quest, if you are\nfamiliar with text based games you may be able to jump right\nin. If you need some guidance on the structure and commands\nyou can enter \'instructions\' at the main game prompt for\nmore information on how to play. However first I need to ask\nyou two question and then we can begin!\n' )
    
    # Get name for the hero character
    hero.name = ""
    while len(hero.name) < 1:
        hero.name = input('What is your name brave hero? ')
    
    # Get hero's class
    good_input = False
    while not good_input:
        hero.skill_set = ""
        while len(hero.skill_set) < 1:
            hero.skill_set = input('Pick a class to play ([F]ighter, [C]leric, or [R]ouge): ')
        hero.skill_set = hero.skill_set.lower()[0]
        if hero.skill_set == 'f':
            hero.skill_set = 'Fighter'
        elif  hero.skill_set == 'c':
            hero.skill_set = 'Cleric'
        elif  hero.skill_set == 'r':
            hero.skill_set = 'Rouge'
        else:
            continue
        good_input = True
    
    # We have the required info, now time to start the game
    # Display intro message from the King
    print(SECTION_BREAK)
    print('We find our hero in the castle of the king, in the main')
    print('throne room with all the pomp one would expect from a king')
    print('and his court. The king rises and addresses you,\n')
    print(f'"Greetings {hero.name}, brave {hero.skill_set}!!\n')
    print('Thank you for taking on this foolhardy.... er... I mean... uh')
    print('valiant! yes, valiant quest! My kingdom has been overrun by evil')
    print('doers and my treasury plundered. Please retreive my precious')
    print('gemstones. There are six in all. When you have collected them,')
    print('please return to me here in the castle.\n')
    print('Best of luck!"\n\n')
    input("Press ENTER to continue...")
    print(SECTION_BREAK)

def hero_wins():
    '''hero_wins()'''
    print('You\'ve entered the castle with all the gems and the king is\ndelighted to see you! He calls his court into the main\nthrone room and exclaims in his loudest kingly-est voice,\n')
    print('"Oh brave hero, you have returned from your periless\njourney and I see you have returned my precious gems. I am\nso thankful that I dub you knight ' + hero.name + ', protector of the')
    print('realm and most high ' + hero.skill_set +'. You will hence forth be known\nas such to all people in my lands. I also bequeath to you\nthe diamond that you have returned a token of my gratitude."\n')
    print('The crowd erupts in applause as the king rises and walks out\nof the room with all the gems save the shining diamond which he\ntosses to you. With diamond in hand, you head out of the castle')
    print('doors and into the sunshine to start on your next big adventure!\n') 

def hero_cliff():
    '''hero_cliff()'''
    print('You have just walked off the edge of an epic cliff, why\nwould you walk off a cliff? Unfortunately this was a fall\nfrom such a great height that you did not survive it. Your')
    print('adventure has ended in failure. Any songs about your life\nwill be more of a cautionary tale about a ' + hero.skill_set + ' named\n' + hero.name + ' that couldn\'t fly, so sad.\n')

def load_file(file):
    '''load_file'''
    print("Loading ", file, "File.....", end="")
    with open(file, "r", encoding='ascii') as read_file:
        dictionary = json.load(read_file)
    print(color.GREEN + "Done" + color.END)
    return dictionary

# End of Functions, script starts here

class color: # pylint: disable=too-few-public-methods
    '''class color: Defines a color class and adds constant values for each color/effect'''
    # Color class for adding color to print output
    # From https://appdividend.com/2021/06/14/how-to-print-bold-python-text
    # (c) Krunal Lathiya, June 14, 2021
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class hero: # pylint: disable=too-few-public-methods
    '''class hero: hold main attribute values for the games hero'''
    name = ""
    skill_set = ""
    weapon = "Fists"
    life = 75
    life_max = 100
    inventory = ["Short Sword"] # TODO: change to "Empty" before Prod
    inventory_max = 10

# Define a constant for use in separating the output for better readability
SECTION_BREAK = '\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n'

# Define filename/location and load dictionary variables from data files
map_file     = "Map.json"
monster_file = "Monsters.json"
item_file    = "Items.json"
atlas = dict(load_file(map_file))
monsters = dict(load_file(monster_file))
items = dict(load_file(item_file))

main()

print("Thank you for playing, we hope you enjoyed this adventure!\n\n")
