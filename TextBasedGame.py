'''
Author: Jon Ormond
Created: October 14th, 2021
Description: Adventure Quest, a text based game.
             Created for Project Two of the IT-140 class at SNHU.
Version: 1.0
'''

# Import OS module to access the Get_Terminal_Size function for console line count
import os
# Import Random module for use in the fight function random number generation
import random

def main():
    '''main(): Main game loop, provides the main dispaly output, and accepts and routes the user commands.'''
    # Set variables used in the game
    user_input = ""
    current_room = "Castle"
    winning_inventory = ["Opal", "Emerald", "Ruby", "Sapphire", "Diamond", "Pearl"]
    
    # Display game open text and get hero name and skill set
    intro() 
    
    # Start main game loop
    # Although set up as an infinite loop, there are exit points within
    # the main loop based on completion of the game or at the request
    # of the user.
    while True:
        
        # There are a few "immediate effect" conditions so
        # at the begining of this loop we need to check if
        # we meet any of those conditions and act accordingly.

        # Immediate Condition 1: Hero is at the castle with all the gems (i.e. player wins!)
        if current_room == "Castle" and all(things in hero.inventory for things in winning_inventory):
            # Display winning messages
            print('You\'ve entered the castle with all the gems and the king is\ndelighted to see you! He calls his court into the main\nthrone room and exclaims in his loudest kingly-est voice,\n')
            print(f'"Oh brave hero, you have returned from your periless\njourney and I see you have returned my precious gems. I am\nso thankful that I dub you knight {hero.name}, protector of the')
            print(f'realm and most high {hero.skill_set}. You will hence forth be known\nas such to all people in my lands. I also bequeath to you\nthe diamond that you have returned, a token of my gratitude."\n')
            print('The crowd erupts in applause as the king rises and walks out\nof the room with all the gems save the shining diamond which he\ntosses to you. With diamond in hand, you head out of the castle')
            print('doors and into the sunshine to start on your next big adventure!\n') 
            return # Exit game loop
        # Immediate Condition 2: Hero just walked off a cliff and died
        if current_room == "Cliff":
            # Display "cliff you died" messages
            print('You have just walked off the edge of an epic cliff, why\nwould you walk off a cliff? Unfortunately this was a fall\nfrom such a great height that you did not survive it. Your')
            print(f'adventure has ended in failure. Any songs about your life\nwill be more of a cautionary tale about a {hero.skill_set} named\n{hero.name} that couldn\'t fly, so sad.\n')
            return # Exit game loop
        if hero.life <= 0:
            # Display hero died in battle message
            print('You were warned this was a dangerous adventure, and while\nyou were not successful in your quest you were brave and\nvaliant. Bards will sing epic songs of your legendary tail.\n')
            return # Exit game loop
        
        # Display main location and character information screen
        main_display(current_room)
       
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
            # The user has changed their mind, don't process this input, just start the next iteration of the loop
            # Display a content break
            print(SECTION_BREAK)
            continue
        # Display a content break
        print(SECTION_BREAK)
                
        # Check for a verb-only command, if not then check user_input has at least two parts separated by a space
        if user_input.find(" ") < 1:
            # The "Instruction" verb doesn't need a noun, so check for "i"
            if user_input.lower()[0] == "i":
                user_verb = "i"
            else:
                print('{color.CYAN}Invalid input{color.END}: you must enter your command with a verb, a space, and a noun e.g. "move north"\n')
                continue
        else:
            # The input has a space, break the input into the first word as the verb, and second part as
            # the noun, maxsplit is used to ensure if the noun is two words, only the first word is split.
            # On the verb an extra [0] is used to only pull the first character of the verb.
            user_verb = user_input.split(" ",maxsplit=1)[0][0].lower()
            user_noun = user_input.split(" ",maxsplit=1)[1].lower()
        
        # Check to see if the hero is avoiding the monster
        if user_verb in ['m','g','u','d']:
            # Check to see if there is a monster in the room
            if "Monster" in atlas[current_room]:
                # There is a monster, and the hero is doing something other than fighting
                # Monster rolls for initiative
                monster_surprise_attack_roll = random.randint(1, 21)
                # If the monster rolls over 15, initiate one round of battle
                if monster_surprise_attack_roll > 15:
                    print(f'{color.YELLOW}Warning!{color.END}: the monster has made a surprise attack, prepare for battle!\n')
                    fight(current_room, atlas[current_room]["Monster"])
                         
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
            print(f'{color.CYAN}Invalid input{color.END}: the verb used was not recognized, please try again.\n')

def main_display(current_room):
    '''main_display(current_room): Used to show location information and current character attributes.'''
    # The main purpose of this loop is to display the standard
    # output screen of information, then accept and route the
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

    # Note: Python has a map function and although I could have called
    # the map variable "map" I deciced to call it "atlas" to avoid
    # reusing the word map.
    # Show the description of the current room from the atlas dictionary
    print(atlas[current_room]['Description'])

    # Show any items in the room
    if len(atlas[current_room]['Items']) > 0:
        display_items = 'You see a '
        # Player can drop additional items in a room, so the items
        # container must be a list.
        # iterate through the list and display items in the room
        for item in atlas[current_room]['Items']:
            display_items += f'{color.GREEN}{item}{color.END}, '
        # items will have an unneeded ", " at the end, strip that off
        display_items = display_items[:-2] + ' there for the taking.'
        print(display_items)

    # Show any monsters
    if 'Monster' in atlas[current_room]:
        print(f'Oh no! There is a big scary {color.RED}{atlas[current_room]["Monster"]}{color.END} in here with you!!')

    # Show the hero's current inventory list
    if "Empty" not in hero.inventory:
        inventory_items = '\nYour Inventory: '
        # iterate through the list and display items in inventory
        for item in hero.inventory:
            inventory_items += f'{color.GREEN}{item}{color.END}, '
        # items will have an unneeded ", " at the end, strip that off
        inventory_items = inventory_items[:-2]
        print(inventory_items)
    else:
        print('\nYour Inventory: Empty')

    # Show the hero's current equipped weapon
    if hero.weapon != "Fists":
        print(f'Your Weapon: {color.GREEN}hero.weapon{color.END}')
    else:
        print('Your Weapon: Fists')
        
    # Show the hero's remaining life
    # Get a color to provide visual impact to the hero's health level
    if hero.life >= 80:
        life_color = color.GREEN
    elif hero.life > 30:
        life_color = color.YELLOW
    else:
        life_color = color.RED
    # Display the hero's health with the right color and show the max life possible
    print(f'Your health: {life_color}{str(hero.life)}{color.END} out of {str(hero.life_max)}\n')
    
    # Show the possible directions available from this location
    # Start with a begining of the line in a variable and add each valid direction to the string
    directions = "Possible Directions: you see "
    # Check each the map dictionary for the current room and see if the cardinal direction exists
    if 'North' in atlas[current_room]:
        # If this direction exists, append this direction, nicely formated with an ending comma to the directions string
        directions +=f'a {atlas[current_room]["North"]} to the {color.CYAN}North{color.END}, '
    if 'East' in atlas[current_room]:
        directions +=f'a {atlas[current_room]["East"]} to the {color.CYAN}East{color.END}, '
    if 'South' in atlas[current_room]:
        directions +=f'a {atlas[current_room]["South"]} to the {color.CYAN}South{color.END}, '
    if 'West' in atlas[current_room]:
        directions +=f'a {atlas[current_room]["West"]} to the {color.CYAN}West{color.END}, '
    # The last direction appended will have a trailing comma and a space, so we need to trim those two characters off
    # and add a period
    directions = directions[:-2] + "."
    # Print the available directions for this location
    print(directions, '\n\n')
    # Print a reminder of the available verbs for the user to use
    print('(Verbs: Move, Look, Get, Use, Drop, Fight, or Instructions)')

def move(current_room, direction):
    '''move(current_room, direction): processes the move request from the main game loop and moves player to a new location'''
    # Check for single character direction, if so, expand to full cardinal direction name
    if direction.lower() == 'n':
        direction = "North"
    elif direction.lower() == 'e':
        direction = "East"
    elif direction.lower() == 's':
        direction = "South"
    elif direction.lower() == 'w':
        direction = "West"
    # ensure the direction is capitalized to match the atlas keys
    direction = direction.capitalize()
    # Check if direction is not valid for this location
    if direction not in atlas[current_room]:
        # set new room to be the current room, i.e. don't change locations
        new_room = current_room
        # Display error message
        print(f'{color.CYAN}Invalid input{color.END}: invalid direction entered for this room, please try again.\n')
    else:
        # Direction is valid, so update the new room with the value from the direction key in the current room dictionary
        new_room = atlas[current_room][direction]
        print(f'{color.GREEN}Success{color.END}: You have moved to a new location!\n')
    return new_room
    
def look_item(current_room, item_to_see):
    '''look_item(current_room, item_to_see): displays information about a item in the current location or in the hero's inventory.'''
    # Ensure the item is capitalized to match the items keys
    item_to_see = item_to_see.title()
    # Does this item not exist anywhere in the world?
    if item_to_see not in items:
        # Maybe they are looking at a monster?
        if "Monster" in atlas[current_room] and item_to_see == atlas[current_room]["Monster"]:
            print(f'{color.GREEN}Success{color.END}: {monsters[item_to_see]["Description"]}\n')
            return
        # Invalid item requested, display error
        print(f'{color.CYAN}Invalid input{color.END}: item does not exist, please try again.\n')
        return
    # If noun is hero weapon or item in inventory or in room items then display item
    if item_to_see in atlas[current_room]["Items"] or item_to_see == hero.weapon or item_to_see in hero.inventory:
        print(f'{color.GREEN}Success{color.END}: {items[item_to_see]["Description"]}\n')
    else:
        # The item does exist somewhere in the world, but not here or on the hero
        print(f'{color.CYAN}Invalid input{color.END}: item not found here, please try again.\n')
        
def get_item(current_room, requested_item):
    '''get_item(current_room, requested_item): adds an item to the hero's inventory'''
    # Ensure the item is capitalized to match the items keys
    requested_item = requested_item.title()
    item_found = False
    # Loop through each item in the current room items list
    for item in atlas[current_room]["Items"]:
        # Evaluate if this item matches the requested item
        if item == requested_item:
            item_found = True
            # Check to see if the inventory is full and therefor show error message that the item isn't added.
            if (hero.weapon == 'Fists' and len(hero.inventory) >= hero.inventory_max) or (hero.weapon != 'Fists' and len(hero.inventory) >= hero.inventory_max - 1):
                print(f'{color.CYAN}Inventory Full{color.END}: You can\'t carry any more. To get this item')
                print(f'{" "*16}you must first drop your weapon or another')
                print(f'{" "*16}inventory item to make room for it.\n')
            else:
                # Item is found, there is room in the inventory
                # Remove the item from the room items list
                atlas[current_room]["Items"].remove(item)
                # Add the item to the hero's inventory list
                hero.inventory.append(item)
                # If the hero's list was empty, that list entry needs to be removed
                if 'Empty' in hero.inventory:
                    hero.inventory.remove('Empty')
                # Display success message
                print(f'{color.GREEN}Success{color.END}: You have added an item to your inventory!\n')
    
    # If the item wasn't found, display error message
    if not item_found:
        print(f'{color.CYAN}Invalid Object{color.END}: I can\'t find that item!\n')
    
def use_item(current_room, item_to_use):
    '''use_item(current_room, item_to_use): allows the hero to equip a weapon or consume a health increasing item.'''
    # Ensure the item is capitalized to match the items keys
    item_to_use = item_to_use.title()
    # Does this item not exist anywhere in the world?
    if item_to_use not in items:
        # Invalid item requested, display error
        print(f'{color.CYAN}Invalid input{color.END}: item does not exist, please try again.\n')
        return
    # If item type is a weapon, and the hero is using fists as the weapon, then equip the item
    if item_to_use in hero.inventory and items[item_to_use]['Item Type'] == 'Weapon' and hero.weapon == "Fists":
        # Set this item as the hero's weapon
        hero.weapon = item_to_use
        # Remove the item from the hero's inventory list
        hero.inventory.remove(item_to_use)
        # If the hero's inventory is now empty, update the list with "Empty"
        if len(hero.inventory) == 0:
            hero.inventory.append('Empty')
        # Display success message
        print(f'{color.GREEN}Success{color.END}: you have equipped a new weapon!\n')
        
    # If item type is a weapon, and the hero is using another weapon, then equip the item and swap the old weapon to inventory
    elif item_to_use in hero.inventory and items[item_to_use]['Item Type'] == 'Weapon':
        # Remove the item from the hero's inventory
        hero.inventory.remove(item_to_use)
        # Add the current weapon to the hero's inventory
        hero.inventory.append(hero.weapon)
        # Add the item as the hero's newly equipped weapon
        hero.weapon = item_to_use
        # Display success message
        print(f'{color.GREEN}Success{color.END}: you have equipped a new weapon and your old one is in your inventory!\n')

    # If item type is health, add to health up to max (but not over)
    elif item_to_use in hero.inventory and items[item_to_use]['Item Type'] == 'Health':
        # Calc hero life + health boost
        hero.life += items[item_to_use]['Restore Points']
        # Remove item from hero's inventory
        hero.inventory.remove(item_to_use)
        # If the hero's inventory is now empty, update the list with "Empty"
        if len(hero.inventory) == 0:
            hero.inventory.append('Empty')
        # Check if this pushed the hero's life over the max life
        if hero.life > hero.life_max:
            # Reset life to max value
            hero.life = hero.life_max
            # Display health maxed message
            print(f'{color.GREEN}Success{color.END}: you feel energy and health surging in your body, your health is maxed!\n')
        else:
            # Display health increased message
            print(f'{color.GREEN}Success{color.END}: you feel energy and health surging in your body, your health is increased!\n')
    # If type is a gem, tell the player to save it for the king
    elif item_to_use in hero.inventory and items[item_to_use]['Item Type'] == 'Gem':
        print(f'{color.CYAN}Invalid input{color.END}: you can\'t use that, you\'re saving it for the King, please try again.\n')
    # If type is a regular item, display an error message
    elif item_to_use in hero.inventory and items[item_to_use]['Item Type'] == 'Item':
        print(f'{color.CYAN}Invalid input{color.END}: this item can\'t be used, it just looks pretty, please try again.\n')
    # If item is in the current room, but not in inventory, display error stating you have to get the item first
    elif item_to_use in atlas[current_room]["Items"]:
        print(f'{color.CYAN}Invalid input{color.END}: the item must be in your inventory before it can be used, please try again.\n')
    # Anything else display "I don't know how to use that" message
    else:
        print(f'{color.CYAN}Invalid input{color.END}: that item can\'t be used, please try again.\n')
    
def drop_item(current_room, item_to_drop):
    '''drop_item(current_room, item_to_drop): drops an item from the hero's inventory and adds it to the items list for the current location.'''
    # Ensure the item is capitalized to match the items keys
    item_to_drop = item_to_drop.title()
    # Does this item not exist anywhere in the world?
    if item_to_drop not in items:
        # Invalid item requested, display error
        print(f'{color.CYAN}Invalid input{color.END}: item does not exist, please try again.\n')
    # If equipped weapon, drop and add to room inventory
    elif hero.weapon == item_to_drop:
        # Change equipped weapon to Fists (no weapon)
        hero.weapon = "Fists"
        # Add the item to the current location items list
        atlas[current_room]["Items"].append(item_to_drop)
        # Display success message
        print(f'{color.GREEN}Success{color.END}: you have dropped your equipped weapon, back to bare knuckles for you!\n')
    # If item in inventory drop and add to room inventory
    elif item_to_drop in hero.inventory:
        # Remove item from hero's inventory
        hero.inventory.remove(item_to_drop)
        # If the hero's inventory is now empty, update the list with "Empty"
        if len(hero.inventory) == 0:
            hero.inventory.append('Empty')
        # Add item to the current room inventory list
        atlas[current_room]["Items"].append(item_to_drop)
        # Display success message
        print(f'{color.GREEN}Success{color.END}: you have dropped an item, it feels nice not to carry around so much weight!\n')
    # Invalid data
    else:
        print(f'{color.CYAN}Invalid input{color.END}: you can\'t drop what you don\'t have, please try again.\n')

def fight(current_room, monster):
    '''fight(current_room, monster): processes one round of battle between the hero and a monster.'''
    # Ensure the monster is capitalized to match the monsters keys
    monster = monster.title()
    # If monster isn't in the current room, display error and return to main loop
    if "Monster" not in atlas[current_room]:
        print(f'{color.CYAN}Invalid input{color.END}: there is no monster here\n')
        return
    if monster != atlas[current_room]["Monster"]:
        print(f'{color.CYAN}Invalid input{color.END}: no such monster here for you to fight\n')
        return

    # Battle Logic (for both hero and Monster)
    # Roll for initiative, roll damage, calculate total with weapon multiplier
    #     Attack Roll is 1 - 20: This provides an Attack Role effect based on the Attack Roll with < 5 missed, >= 5 hits, >= 10 double damage, >= 15 triple damage
    #     Damage roll is 1 - 12
    #     Total_Damage = Int(Damage_Roll * (1 + (Weapon_Multiplier/100)) * attack_roll_effect)
    #
    #     e.g. (min)     Int(      5     * (1 + (     10          /100)) *          0        ) =  0 total damage
    #     e.g            Int(      6     * (1 + (     30          /100)) *          2        ) = 15 total damage
    #     e.g. (max)     Int(     12     * (1 + (     40          /100)) *          3        ) = 50 total damage
    #
    
    # Start battle
    # Hero Attack Phase
    # Get random number for attack roll
    hero_attack_roll = random.randint(1, 21)
    # Calculate attack roll effect (multiplier)
    if hero_attack_roll >= 15:
        hero_attack_roll_effect = 3
    else:
        hero_attack_roll_effect = int(hero_attack_roll / 5)
    # Get random number for damage roll
    hero_damage_roll = random.randint(1, 13)
    # Get weapon damage multiplier
    hero_damage_multiplier = items[hero.weapon]["Multiplier"] if hero.weapon != "Fists" else 0
    # Calc total damage
    hero_damage = int(hero_damage_roll * (1 + (hero_damage_multiplier/100)) * hero_attack_roll_effect)
    # Display attack results
    if hero_attack_roll < 5:
        # Hero missed
        print(f'{color.RED}Hero Attack Failed{color.END}: you tried really hard, but you completely missed the monster!\n')
    else:
        # Hero hit
        print(f'{color.GREEN}Hero Attack successful{color.END}: you have landed a powerful blow of {hero_damage} damage {"point" if hero_damage ==1 else "points"}.\n')
    # Reduce monster life by damage amount
    monsters[monster]["Life"] -= hero_damage
    # Check if monster died (life <= 0)
    if monsters[monster]["Life"] <= 0:
        # Remove moster dictionary entry from the current room
        atlas[current_room].pop("Monster")
        # Monster is dead, display victory message
        print(f'{color.GREEN}You win!{color.END}: you triumphed over this terrible monster. You truly are a hero!\n')
        # Since the monster is dead, the monster phase isn't needed, so return back to the main game loop
        return

    # Monster Attack Phase
    # Get random number for attack roll
    monster_attack_roll = random.randint(1, 21)
    # Calculate attack roll effect (multiplier)
    if monster_attack_roll >= 15:
        monster_attack_roll_effect = 3
    else:
        monster_attack_roll_effect = int(monster_attack_roll / 5)
    # Get random number for damage roll
    monster_damage_roll = random.randint(1, 13)
    # Get monster damage multiplier
    monster_damage_multiplier = monsters[monster]["Multiplier"]
    # Calc total damage
    monster_damage = int(monster_damage_roll * (1 + (monster_damage_multiplier/100)) * monster_attack_roll_effect)
    # Display attack results
    if monster_attack_roll < 5:
        # Monster missed
        spaces = len(monster)
        print(f'{color.GREEN}{monster} Attack Failed{color.END}: the monster attacked ferociously but you danced\n{" "*(16 + spaces)}out of the way and the monster completely missed!\n')
    else:
        # Monster hit
        print(f'{color.RED}{monster} Attack successful{color.END}: the {monster} has landed a powerful blow of {monster_damage} damage {"point" if monster_damage ==1 else "points"}.\n')
    # Reduce Hero life by damage amount
    hero.life -= monster_damage
    # Check if hero died (life <= 0), then dispaly mortal blow message
    if hero.life <= 0:
        print(f'{color.RED}Mortal Blow!{color.END}: the evil {monster} as landed a mortal blow!\n')

def instructions():
    '''instructions(): Displays the full game instructions with screen breaks based on console line height.'''
    # Get number of lines of the console
    console_lines = os.get_terminal_size()[1]
    i = 1
    # Load instructions into a list
    message = []
    message.append("Instructions for Adventure Quest, a text-based adventure!\n")
    message.append("Goal: Collect six gems hidden around the 23 locations in")
    message.append("      the game, then return to the Castle.\n")
    message.append("Basic Commands:")
    message.append("  Generally you need to enter a verb and noun to control the hero.")
    message.append("  The verbs are:")
    message.append("  Move  - to move between locations in the world")
    message.append("  Look  - to get more information about an item you see or have")
    message.append("  Get   - to add an item you see to your inventory")
    message.append("  Use   - to consume food or a potion to restore health or to equip")
    message.append("          a weapon in your inventory for use in battle")
    message.append("  Drop  - to drop an item in your inventory, it will then appear in")
    message.append("          the list of items you see in that location")
    message.append("  Fight - used to engage a monster in battle")
    message.append("  Instructions - enter this to print these instructions")
    message.append("  Quit  - use to exit the game, WARNING: you will lose all progress")
    message.append("          made in this session\n")
    message.append("Each of the above verbs may be abbreviated to a single character")
    message.append("e.g. Instead of the whole word \"Move\", you can simple use \"m\"")
    message.append("(the exception is \"Quit\", that must always be typed fully)\n")
    message.append("The verb is followed by a noun, the noun is the object or direction")
    message.append("you wish to act upon.\n")
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
    message.append("  Quit - 'Quit' (cannot be abbreviated)\n")
    message.append("Noun restrictions:")
    message.append("  - the object you wish to interact with must be in the")
    message.append("    current location to 'look' or 'get'.")
    message.append("  - the object you wish to interact with must be in your")
    message.append("    inventory to 'look', 'get', 'use', or 'drop'.\n")
    message.append("Inventory restrictions:")
    message.append("  You hero is limited to carry only 10 items, this includes")
    message.append("  an equipped weapon. This means if you have a weapon")
    message.append("  equipped you can only carry nine items in your inventory.\n")
    message.append("Monster information:")
    message.append("  You will encounter Monsters on your journey through the")
    message.append("  world. When present in a location with a Monster, a warning")
    message.append("  will pop up informing you of the Monster type. You may take")
    message.append("  other actions while in the room with the Monster such as")
    message.append("  'get', 'look', 'use', or 'move'. Any action (verb) other than")
    message.append("  'Fight' will result in a chance that the Monster will attack")
    message.append("  you. If the Monster successfully attacks, you will automatically")
    message.append("  enter the fight phase of the game for one round of battle.")
    message.append("  While fighting you will see the hero health and Monster health")
    message.append("  after each round of attacks. You can choose to run ('Move') at")
    message.append("  any time (although that choice does give the monster a chance")
    message.append("  to attack before you leave!). You can continue fighting until")
    message.append("  either the hero or the monster is dead (when life is zero).")
  
    print()
    # Loop through message list printing each line
    for line in message:
        print(line)
        i += 1
        # If the output gets within 6 lines of the max console height, pause and wait for the user.
        if i >= console_lines - 6:
            response = input("\nPress ENTER to continue (or Q, ENTER to return to the game)...") or "continue"
            print()
            # If the user enters Q, stop showing instructions and return to the main game loop
            if response.lower()[0] == 'q':
                print(SECTION_BREAK)
                return
            # Print some spaces from previous input
            print("\n\n")
            # Reset screen line counter back to 1
            i = 1
    # At end of instructions list, tell user they are at the end
    response = input("\nEnd of instructions\nPress ENTER to continue...")
    print(SECTION_BREAK)

def intro():
    '''intro(): Displays game welcome statements, collects hero name and class.'''
    # Display game intro
    print(SECTION_BREAK)
    print('Hello intrepid adventurer!\n')
    print('You are about to embark on an epic quest, if you are\nfamiliar with text based games you may be able to jump right\nin. If you need some guidance on the structure and commands\nyou can enter \'instructions\' at the main game prompt for\nmore information on how to play. However first I need to ask\nyou two questions and then we can begin!\n' )
    
    # Get name for the hero character
    hero.name = ""
    # Loop until the users gives the hero at least a single character name
    while len(hero.name) < 1:
        hero.name = input('What is your name brave hero? ')
    
    # Get hero's skill set
    good_input = False
    while not good_input:
        hero.skill_set = ""
        # Loop until some input provided
        while len(hero.skill_set) < 1:
            hero.skill_set = input('Pick a class to play ([F]ighter, [C]leric, or [R]ouge): ')
        # Set input to lower case and slice just the first character for evaluation
        hero.skill_set = hero.skill_set.lower()[0]
        # Look through the valid skill sets and set skill_set accordingly
        if hero.skill_set == 'f':
            hero.skill_set = 'Fighter'
        elif  hero.skill_set == 'c':
            hero.skill_set = 'Cleric'
        elif  hero.skill_set == 'r':
            hero.skill_set = 'Rouge'
        else:
            # No valid skill set was entered, loop back and have the user try again
            continue
        # Set boolean to true which will break out of the while loop and continue
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
    print('doers and my treasury plundered. Please retrieve my precious')
    print('gemstones. There are six in all. When you have collected them,')
    print('please return to me here in the castle.\n')
    print('Best of luck!"\n\n')
    input("Press ENTER to continue...")
    print(SECTION_BREAK)

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
    life = 100
    life_max = 100
    inventory = ["Empty"]
    inventory_max = 10

# Define a constant for use in separating the output for better readability
SECTION_BREAK = '\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n'

# Define the atlas (map) dictionary
# Key is the location name
# Values (as nested dictionary key-value pairs):
#   Description - String
#   North - Optional String of a location name (Key)
#   East - Optional String of a location name (Key)
#   South - Optional String of a location name (Key)
#   West - Optional String of a location name (Key)
#   Items - Required List of strings, empty list ([]) is allowed (Foreign Keys from Items dictionary)
#   Monster - Optional String of monster name (Foreign Key in Monsters dictionary)
atlas = {'Castle': {'Description': "You are in the King's grand castle with lots of granite\nstones, marble floors, and tapestries. So many tapestries!\nThere appears to be only one way out, it's to the East\noutside where you see a path leading to a large statue.", 'East': 'Statue', 'Items': []},
         'Statue': {'Description': "You are on a path in an open wooded area, next to the path\nis a statue of the King. It's kind of creepy, where ever you\nmove the eyes seem to follow you... creepy! To the North\nlooks like the gates to a town, to the East the path\ncontinues through the forest.", 'North': 'Town Gate', 'East': 'Path', 'West': 'Castle', 'Items': ['Dagger']},
         'Path': {'Description': 'You are on a path in a dark wooded area with the trees\nclosing in. You can see a path with a statue to the west\nand perhaps a house beyond the trees to the East.', 'East': 'Manor Promenade', 'West': 'Statue', 'Items': ['Club']},
         'Well': {'Description': "You are in an open field with on old water well. The well\nhas a rotted rope and a broken bucket to the side of it. The\nwell doesn't appear to have been used in ages. To the South\nof the field is a large manor with many rooms, and to the\nNorth the field ends at a mountain face with what looks like\na foreboding cave.", 'North': 'Dungeon Entrance', 'South': 'Manor Promenade', 'Items': ['Opal']},
         'Manor Promenade': {'Description': 'You are standing on the lawn of a great manor. Down the\ngravel promenade, the manor is quite grand with a formal\nfountain court and garden leading to the main doors of the\nmanor. To the North you see a large open field, to the East\nis the fountain court and garden of the house, to the West\n a path leads into a dark forest.', 'North': 'Well', 'East': 'Fountain', 'West': 'Path', 'Items': ['Old Shoe']},
         'Fountain': {'Description': 'Before you is a long garden leading to a country manor\nwith impeccably maintained topiary bushes in many fanciful\nshapes and gravel pathways. Your eyes are drawn to the\nimmense fountain with water spouting horses, and cherubs\npouring water from vases. Quite the bucolic scene. To the\nEast is the main entrance of the house, to the West is a\nlong promenade across the house property.', 'East': 'Library', 'West': 'Manor Promenade', 'Items': ['Silver Shilling']},
         'Dining Room': {'Description': "You've entered into a formal dining room (you are really\nunderdressed!). The table is set with the finest China on\ndisplay. On a sideboard in the room you see bottles of\nliquor and elixirs, I'm sure they are purely for medicinal\npurposes. To the East and South are closed doors leading\nto other rooms.", 'East': 'Bedroom', 'South': 'Kitchen', 'Items': ['Potion']},
         'Kitchen': {'Description': 'Through the door and see you are in a dingy, dirty kitchen.\nEverything seems to be in disarray with pots and pans\non the floor, garbage in the corners, plates of uneaten\nfood, and I mean come on, what is that smell?!? To the North,\nEast, and South are sets of closed doors.', 'North': 'Dining Room', 'East': 'Servants Room', 'South': 'Library', 'Items': ['Apple'], 'Monster': 'Zombie'},
         'Library': {'Description': 'You are standing in the Library of the manor, although\nornate and quite grand you feel a sense of dread and\ndiscomfort. The house is quiet, too quiet. The hairs\nstanding on the back of your neck tell you that something\nevil is lurking in the shadows of this house. To the North\nand East are a sets of closed doors, to the West is the\nmain door outside to the fountain court.', 'North': 'Kitchen', 'East': 'Great Hall', 'West': 'Fountain', 'Items': ['Short Sword']},
         'Bedroom': {'Description': "This room is a bedroom, but I don't think a nap is in order,\nyou hear ghastly wailing coming from somewhere, and wait...\nis something rustling in the bed sheets? I sure hope not.\nThe only ways out of this bedroom are closed doors to the\nWest and South.", 'South': 'Servants Room', 'West': 'Dining Room', 'Items': ['Emerald'], 'Monster': 'Banshee'},
         'Servants Room': {'Description': "A table, two chairs, a few simple beds, this looks like the\nhousehold staff's quarters. A little tight, but comfortable\nenough. There are doors to the North, South, and West.\nTake your pick!", 'North': 'Bedroom', 'South': 'Great Hall', 'West': 'Kitchen', 'Items': ['Lance']},
         'Great Hall': {'Description': "You have entered the Great Hall. Family crests, classic\nweapons of yore, and a vast table down the center of this\nimpressive room. With so many dour portraits of old men on\nthe walls, whoever decorated this room wasn't shy about\nbragging about the family history. West is the doorway\nto the Library, to the North is a closed door.", 'North': 'Servants Room', 'West': 'Library', 'Items': ['Ruby']},
         'Passage Way': {'Description': 'Damp hewn rock surrounds you in along a narrow corridor.\nBits of detritus and refuse where the walls meet the floor.\nThe subtle wafting odor of long standing mildew. Best to\njust keep moving! To the East is deepening darkness, to the\nSouth the dim hope of daylight.', 'East': 'Torture Room', 'South': 'Dungeon Entrance', 'Items': ['Potion']},
         'Dungeon Entrance': {'Description': 'At the edge of a clearing, a cliff wall stands about the height\nof a tall tree. Next to a large boulder appears to be an\nentrance to a cave or.. no wait, not a cave but a dungeon!\nContinue North to enter the dungeon, South to an open\nfield with a Well.', 'North': 'Passage Way', 'South': 'Well', 'Items': ['Leg Bone']},
         'Torture Room': {'Description': 'A sense of dread and terror fill your senses, the hair on\nthe back your neck stands as if in a lightning storm. Very\nbad things have happened in this room. There are various\nimplements of torture laying about the room and some really\ndisgusting stains on the floor. To the East is a door with\nbright metal fittings, to the West only darkness.', 'East': 'Treasure Room', 'West': 'Passage Way', 'Items': ['Crossbow']},
         'Treasure Room': {'Description': "You enter a room that, unlike the other rooms in this\nterrible place, is relatively clean and well appointed. No\nmore rough walls and floor, although dusty you see fine\nwooden tables and polished stone walls. In the center of the\nroom stands a small plinth. To the East is a door, but\nsomething isn't right about it, you really don't want to\nopen that door. You can also return to the torture room to\nthe West.", 'East': 'Pit of Despair', 'West': 'Torture Room', 'Items': ['Sapphire']},
         'Pit of Despair': {'Description': "You enter a room dominated by a torture rack, but with the\naddition of vacuum pumps a water driven wheel and other\ninconceivable contraptions, it appears far worse than a\nnormal rack. A lot of life has been lost in this room. Is\nthere a slithering sound? I don't like this place. Go West\nas soon as possible, it's your only way out of here!", 'West': 'Treasure Room', 'Items': ['Diamond'], 'Monster': 'Giant Python'},
         'Butcher Shop': {'Description': "Scraps of fetid meat are scattered around the shop, facing\nthis stench you're really wishing someone would invent\nrefrigeration right about now, this place is nasty! There's\nreally nothing for you here, you can head back East to the\ntown square.", 'East': 'Town Square', 'Items': ['Leg Bone']},
         'Ale House': {'Description': 'Mmmmm beer, ooh or maybe mead, so many choices! But it looks\nlike someone (or something) has been here before you. You\nsee smashed kegs, tables, chairs. Not sure if there much\nleft in here to imbibe. The only way out appears to be South\nback to the town square.', 'South': 'Town Square', 'Items': ['Wooden Crate'], 'Monster': 'Ogre'},
         'Town Square': {'Description': "You find yourself in the town square, you see interesting\nshops and establishments all around you, but where are the\npeople? It's awfully quiet, perhaps too quiet? To the West\nappears to be a Butcher Shop, to the North an Ale House, to\nthe East a Fish Market, or you can leave the town through\nthe gates to the South.", 'North': 'Ale House', 'East': 'Fish Market', 'South': 'Town Gate', 'West': 'Butcher Shop', 'Items': ['Bow']},
         'Town Gate': {'Description': 'Before you stands a large archway filled with two metal-\nbanded wooden gates. An entrance to a town! Will you go\nNorth and enter the town or proceed South to the path\nwith a Statue?', 'North': 'Town Square', 'South': 'Statue', 'West': 'Cliff', 'Items': ['5 Vellum Sheets']},
         'Fish Market': {'Description': "What is that smell?! Oh, it is a fish market so I guess it\ngoes with the territory. But this seems worse than normal,\nI don't think this is today's catch, or even this week's\ncatch! But there could be something useful here, maybe...\nor not. Head West to get back to the town square.", 'West': 'Town Square', 'Items': ['Pearl']},
         'Cliff': {'Items': []}
         }
# Define the monsters dictionary
# Key is the monster name
# Values (as nested dictionary key-value pairs):
#   Description - String
#   Life - Integer
#   Multiplier - Integer
monsters = {'Zombie': {'Description': "Stinky, undead, shambling, and clothed in mouldering scraps,\nwhat's not to love? Actually a lot, this zombie really wants\nto eat your brains!", 'Life': 30, 'Multiplier': 20},
            'Banshee': {'Description': "Glowing translucent from a light that seems to come from\nwithin, this female wraith is seeking revenge and isn't\nparticular about from whom she exacts it.\nIt's fight or flight time!", 'Life': 50, 'Multiplier': 60},
            'Giant Python': {'Description': "It's giant, it's snaky, but you know, once you get to know\nit, it's not that difficult to deal with. But best to kill\nit just to be on the safe side.", 'Life': 15, 'Multiplier': 0},
            'Ogre': {'Description': 'This thing is angry, no I mean like berserker level angry,\nand did I mention huge? This hulking giant may best be just\nleft alone, running away may be the wiser course of action\nhere.', 'Life': 60, 'Multiplier': 100}
            }
# Define the items dictionary
# Key is the item name
# Values (as nested dictionary key-value pairs):
#   Item Type - String, valid values: "Gem", "Weapon", "Health", and "Item"
#   Description - String
#   Multiplier - Optional Integer (for Item Type weapon only)
#   Restore Points - Optional Integer (for Item Type health only)
items = {'Opal': {'Item Type': 'Gem', 'Description': 'Swirling iridescent colors mesmerize in this amazing\nspecimen of Opal.'},
         'Emerald': {'Item Type': 'Gem', 'Description': 'The deepest green with a slight hue of blue, this is\ndefinitely a gemstone for the king!'},
         'Ruby': {'Item Type': 'Gem', 'Description': "Blood red and seaming to shine with a light of its own,\nit's so pretty maybe the King won't miss if it isn't returned!"},
         'Sapphire': {'Item Type': 'Gem', 'Description': 'The very definition of blue, this sapphire draws the eye\nwith a radiance rivaled by few other gemstones.'},
         'Diamond': {'Item Type': 'Gem', 'Description': "It's just carbon, but damn that's some sexy carbon.\nThe king of all gemstones, if there was one item you'd covet\nfrom this quest, wow this is it!"},
         'Pearl': {'Item Type': 'Gem', 'Description': 'Ok, technically not a gemstone but who are you to\ncorrect the king. Still for oyster snot, this is a pretty\namazing piece of work. As iridescent and lustrous as any\nof the other gems.'},
         'Dagger': {'Item Type': 'Weapon', 'Description': 'Basically a smallish knife with edges on both sides\nof the blade. Easy to wield with one hand.', 'Multiplier': 20},
         'Club': {'Item Type': 'Weapon', 'Description': 'Solid wood, smaller at the holding end, bigger at the\nbusiness end, you know, a club!', 'Multiplier': 25},
         'Bow': {'Item Type': 'Weapon', 'Description': 'Curved wood about an arms width in length with a taut\nsinew cord. This weapon can do some serious ranged damage.', 'Multiplier': 30},
         'Short Sword': {'Item Type': 'Weapon', 'Description': 'A one-handed weapon best for quick stabbing damage. Much\nbetter than a dagger but still a close in weapon.', 'Multiplier': 30},
         'Lance': {'Item Type': 'Weapon', 'Description': "A long wooden pole with a pointy bit at one end. Place\nthe pointy bit in your enemy and you win! Although not the most\npowerful weapon, it's pretty close.", 'Multiplier': 35},
         'Crossbow': {'Item Type': 'Weapon', 'Description': 'A ranged weapon with enormous stopping power. Compact\nand shooting a metal tipped wooden bolt, this is the most\npowerful weapon you can yield.', 'Multiplier': 40},
         'Leg Bone': {'Item Type': 'Weapon', 'Description': "It's exactly what it sounds like. Mostly bone, a few\nbits of sinew. But hey, at least it's dry. In a pinch you could\nuse it as a weapon, better than your fists, but not by much.", 'Multiplier': 10},
         'Potion': {'Item Type': 'Health', 'Description': 'Reddish liquid that looks like a fine pinot noir, but\nsmells like south end of a north bound donkey. But it looks like\nit has tremendous restorative powers.', 'Restore Points': 30},
         'Apple': {'Item Type': 'Health', 'Description': 'Red and delicious, natures wonder. It may even make\nyou a little bit healthier.', 'Restore Points': 5},
         'Old Shoe': {'Item Type': 'Item', 'Description': "No not a pair of shoes, just one. And it's seen much\nbetter days. It looks like someone walked right out of it and\njust kept on walking. That is one disintegrating shoe."},
         'Wooden Crate': {'Item Type': 'Item', 'Description': 'If you have things you need shipped on the next ship to\nwherever, this could be the ticket. Sturdy wood, metal\nwrapped corners. As far as crates go, this is a masterpiece.'},
         'Silver Shilling': {'Item Type': 'Item', 'Description': "Shiny and silver, it's more than a pence, and a long\nway from a pound, but it's still nice to find free money!"},
         '5 Vellum Sheets': {'Item Type': 'Item', 'Description': 'The finest calfskin parchment, so precious and rare.\nThis would be the perfect medium to capture your epic adventure.\nIf you live through it perhaps you can find a scribe to\nwrite it all down!'}
         }

# Call the main function to start the main game loop
main()

# Display the exit message for all ending types
print("Thank you for playing Adventure Quest, we hope you enjoyed this game!\n\n")
