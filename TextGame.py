# Required Tasks
# TODO: Update hero globals to a hero class (make sure that works the way you think it does)
# TODO: Complete Fight subroutine
# TODO: Add castle gem check and story ending if gems are all in hero_inventory
# TODO: Complete Intructions subroutine
# TODO: Complete data descriptions for Map - 0 - 11 complete (I think)
# TODO: Complete data descriptions for Items
# TODO: Complete data descriptions for Monsters
# TODO: remove the 'r' reload option from the main loop verb options
# TODO: UAT

# Optional Tasks
# TODO: on the item and monster display, check for a leading vowel and switch between "a" and "an" as appropriate
# TODO: Complete chance for fight subroutine if monster present, cut if needed
# TODO: Add "chance for fight" subroutine to Move, Look, Get, Drop, Use subroutines (or maybe to main loop)
# TODO: add the Cliff you dead logic, cut if needed

import random
import json

# Color class for adding color to print output
# From https://appdividend.com/2021/06/14/how-to-print-bold-python-text
# (c) Krunal Lathiya, June 14, 2021
# Defines a color class and adds constant values for each color/effect
class color:
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

# Define a constant for use in separating the output for better readability
SECTION_BREAK = '\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n'

def main():
    # Load data files to create dictionaries
    # Note: these dictionaries are created as global variables so that
    #       they can be accessed by any functions called from this loop.
    #       However, any changes to these global dictionaries in a sub
    #       function will create a locally scoped dictionary (same name
    #       and initial values) and are local in nature to that function.
    #       Any changes won't be preserved when returning control to the
    #       main loop, therefore if a called function will make changes
    #       that need to be reflected in the main loop, that global
    #       variable has to be declared in the called function with the
    #       global keyword to ensure the change is affected in the global
    #       and not the local scope.
    #
    
    # Define filename/location
    map_file = "Map.json"
    monster_file = "Monsters.json"
    item_file = "Items.json"
    
    # Load map file
    print("\nLoading Map File......", end="")
    with open(map_file, "r") as read_file:
        global map
        map = json.load(read_file)
        print("Done")

    # Load Monster file
    print("Loading Monsters File..", end="")
    with open(monster_file, "r") as read_file:
        global monsters
        monsters = json.load(read_file)
        print("Done")

    # Load Items file
    print("Loading Items File....", end="")
    with open(item_file, "r") as read_file:
        global items
        items = json.load(read_file)
        print("Done")
    
    # Set variables used in the game
    user_input = ""
    #hero_list = intro()
    hero_list = ["Bubba", "Fighter"]  # TODO: reset to intro() before production
    hero_name = hero_list[0]
    hero_class = hero_list[1]
    global inventory_limit
    inventory_limit = 10
    hero_inventory = ["Empty"]
    # hero_inventory = ["1","2","3"]    # TODO: reset to "Empty" before production
    global hero_weapon
    hero_weapon = "Fists"
    # hero_weapon = "Fists"                 # TODO: reset to "Fists" before production
    global hero_life_max
    hero_life_max = 100
    global hero_life
    # hero_life = hero_life_max
    hero_life = 25                    # TODO: reset to hero_life_max before production
    current_room_index = "4"          # TODO: reset to 0 before production
    
    # Display intro message from the King
    print(SECTION_BREAK)
    print('Greetings {}, brave {}!!\n'.format(hero_name, hero_class))
    print('Thank you for taking on this foolhardy.... er... I mean... uh')
    print('valiant! yes, valiant quest! My kingdom has been overrun by evil')
    print('doers and my treasury plundered. Please retreive my precious')
    print('gemstones. There are six in all. When you have collected them,')
    print('please return to me here in the castle.\n')
    print('Best of luck!')
    print(SECTION_BREAK)
            
    # Start main game loop
    # Although set up as an infinite loop, there are exit points within
    # the main loop based on completion of the game or at the request
    # of the user.
    while True:
        # The main purpose of this loop is to display the standard
        # output screen information and accept and handoff the user
        # command. The display output is aligned thusly:
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
        print(map[current_room_index]['Description'])

        # Show any items
        if len(map[current_room_index]['Items']) > 0:
            display_items = 'You see a '
            for item in map[current_room_index]['Items']:
                display_items += color.GREEN + items[item]['Name'] + color.END + ', '
            display_items = display_items[:-2] + ' there for the taking.'
            print(display_items)

        # Show any monsters
        if 'Monster' in map[current_room_index]:
            print('Oh no! There is a big scary ' + color.RED + monsters[map[current_room_index]['Monster']]["Name"] + color.END + ' in here with you!!')

        # Show the hero's current inventory list
        if "Empty" not in hero_inventory:
            inventory_items = '\nYour Inventory: '
            for item in hero_inventory:
                inventory_items += color.GREEN + items[item]['Name'] + color.END + ', '
            inventory_items = inventory_items[:-2]
            print(inventory_items)
        else:
            print('\nYour Inventory: Empty')

        # Show the hero's current equipped weapon
        if hero_weapon != "Fists":
            print('Your Weapon: ' + color.GREEN + items[hero_weapon]["Name"] + color.END)
        else:
            print('Your Weapon: Fists')
            
        # Show the hero's remaining life
        if hero_life > 80:
            life_color = color.GREEN
        elif hero_life > 30:
            life_color = color.YELLOW
        else:
            life_color = color.RED + color.BOLD
        print('Your health: ' + life_color + str(hero_life) + color.END +' out of 100\n')
        
        # Show the possible directions available from this location
        # Start with a beging of the line in a variable and add each valid direction to the string
        directions = "Possible Directions: you see "
        # Check each the map dictionary for the current room index and see if the cardinal direction exists
        if 'North' in map[current_room_index]:
            # If this direction exists, append this direction, nicely formated with an ending comma to the directions string
            # Note: the map dictionary is being called twice (nested) in the format statement, once to pull the index number
            #       from the requested direction of the current room to be used as the index to get the name of the intended
            #       room.
            directions +='a ' + map[map[current_room_index]['North']]['Name'] + ' to the ' + color.CYAN + 'North' + color.END + ', '
        if 'East' in map[current_room_index]:
            directions +='a ' + map[map[current_room_index]['East']]['Name'] + ' to the ' + color.CYAN + 'East' + color.END + ', '
        if 'South' in map[current_room_index]:
            directions +='a ' + map[map[current_room_index]['South']]['Name'] + ' to the ' + color.CYAN + 'South' + color.END + ', '
        if 'West' in map[current_room_index]:
            directions +='a ' + map[map[current_room_index]['West']]['Name'] + ' to the ' + color.CYAN + 'West' + color.END + ', '
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
                
        # Check to ensure user_input has at least two parts separated by a space
        if user_input.find(" ") < 1:
            print(color.CYAN + color.BOLD + 'Invalid input' + color.END + ': you must enter your command with a verb, a space, and a noun e.g. "move north"\n')
            continue
        # The input has a space, break the input into the first word as the verb, and second part as the noun
        # maxsplit is used to ensure if the noun is two word, only the first word is split.
        # on the verb an extra [0] is used to only pull the first character of the verb.
        user_verb = user_input.split(" ",maxsplit=1)[0][0].lower()
        user_noun = user_input.split(" ",maxsplit=1)[1].lower()
        
        # Based on the verb, decide which subfunction to call
        if user_verb == 'm':
            current_room_index = move(current_room_index, user_noun)
        elif  user_verb == 'l':
            look_item(current_room_index, hero_weapon, hero_inventory, user_noun)
        elif  user_verb == 'g':
            hero_inventory = get_item(current_room_index, user_noun, hero_weapon, hero_inventory)
        elif  user_verb == 'u':
            hero_inventory = use_item(current_room_index, hero_inventory, user_noun)
        elif  user_verb == 'd':
            hero_inventory = drop_item(current_room_index, hero_inventory, user_noun)
        elif  user_verb == 'f':
            fight(current_room_index)
        elif  user_verb == 'i':
            instructions()
        elif  user_verb == 'r':
            # Load map file
            print("\nReloading Map File......", end="")
            with open(map_file, "r") as read_file:
                map = json.load(read_file)
                print("Done")

            # Load Monster file
            print("Reloading Monsters File..", end="")
            with open(monster_file, "r") as read_file:
                monsters = json.load(read_file)
                print("Done")

            # Load Items file
            print("Reloading Items File....", end="")
            with open(item_file, "r") as read_file:
                items = json.load(read_file)
                print("Done")
            print(SECTION_BREAK)
        else:
            print(color.CYAN + color.BOLD + 'Invalid input' + color.END + ': the verb used was not recognized, please try again.\n')

def move(room_index, direction):
    direction = direction.capitalize()
    if direction not in map[room_index]:
        new_room_index = room_index
        print(color.CYAN + color.BOLD + 'Invalid input' + color.END + ': invalid direction entered for this room, please try again.\n')
    else: 
        new_room_index = map[room_index][direction]
        print(color.GREEN + 'Success' + color.END + ': You have moved to a new location!\n')
    return new_room_index
    
def look_item(current_room_index, hero_weapon, hero_inventory, look_item):
    look_item = look_item.title()
    look_item_found = False
    # Find look_item_index
    for item_index in items:
        if look_item == items[item_index]["Name"]:
            look_item_index = item_index
            look_item_found = True
    if not look_item_found:
        print(color.CYAN + 'Invalid input' + color.END + ': item does not exist, please try again.\n')
        return
    # If noun is hero weapon or item in inventory or in room items display item
    if look_item_index in map[current_room_index]["Items"] or look_item_index == hero_weapon or look_item_index in hero_inventory:
        print(color.GREEN + 'Success' + color.END + ': ' + items[look_item_index]['Description'] + '\n')
    else:
        # Else "You can't see that from here!"
        print(color.CYAN + 'Invalid input' + color.END + ': item not found here, please try again.\n')
        
def get_item(room_index, requested_item, hero_weapon, hero_inventory):
    requested_item = requested_item.title()
    item_found = False
    global map
    for item_index in map[room_index]["Items"]:
        if items[item_index]['Name'] == requested_item:
            item_found = True
            if (hero_weapon == 'Fists' and len(hero_inventory) >= inventory_limit) or (hero_weapon != 'Fists' and len(hero_inventory) >= inventory_limit - 1):
                print(color.CYAN + 'Inventory Full' + color.END + ': You can\'t carry any more. To get this item')
                print('                you must first drop your weapon or another')
                print('                inventory item to make room for it.\n')
            else:  
                map[room_index]["Items"].remove(item_index)
                hero_inventory.append(item_index)
                if 'Empty' in hero_inventory:
                    hero_inventory.remove('Empty')
                print(color.GREEN + 'Success' + color.END + ': You have added an item to your inventory!\n')  
    if not item_found:
            print(color.CYAN + 'Invalid Object' + color.END + ': I can\'t find that item!\n')
    return hero_inventory
    
def use_item(current_room_index, hero_inventory, use_item):
    use_item = use_item.title()
    use_item_found = False
    # Find use_item_index
    for item_index in items:
        if use_item == items[item_index]["Name"]:
            use_item_index = item_index
            use_item_found = True
    if not use_item_found:
        print(color.CYAN + 'Invalid input' + color.END + ': item does not exist, please try again.\n')
        return hero_inventory
    # If type is weapon equip, swap if needed
    if use_item_index in hero_inventory and items[use_item_index]['Item Type'] == 'Weapon':
        global hero_weapon
        if hero_weapon == "Fists":
            hero_weapon = use_item_index
            hero_inventory.remove(use_item_index)
            if len(hero_inventory) == 0:
                hero_inventory.append('Empty')
            print(color.GREEN + 'Success' + color.END + ': you have equipped a new weapon!\n')
        else:
            hero_inventory.remove(use_item_index)
            hero_inventory.append(hero_weapon)
            hero_weapon = use_item_index
            print(color.GREEN + 'Success' + color.END + ': you have equipped a new weapon and your old one is in your inventory!\n')
    # Else If type is health, add to health to max (but not over)
    elif use_item_index in hero_inventory and items[use_item_index]['Item Type'] == 'Health':
        # Calc hero life + health boost
        global hero_life
        hero_life += int(items[use_item_index]['Restore Points'])
        hero_inventory.remove(use_item_index)
        if len(hero_inventory) == 0:
            hero_inventory.append('Empty')
        if hero_life > hero_life_max:
            hero_life = hero_life_max
            print(color.GREEN + 'Success' + color.END + ': you feel energy and health surging in your body, your health is maxed!\n')
        else:
            print(color.GREEN + 'Success' + color.END + ': you feel energy and health surging in your body, your health is increased!\n')
    # Else If type is a gem, tell the player to save it for the king
    elif use_item_index in hero_inventory and items[use_item_index]['Item Type'] == 'Gem':
        print(color.CYAN + 'Invalid input' + color.END + ': you can\'t use that, you\'re saving it for the King, please try again.\n')
    # Else If type is a regular item, display an error message
    elif use_item_index in hero_inventory and items[use_item_index]['Item Type'] == 'Item':
        print(color.CYAN + 'Invalid input' + color.END + ': this item can\'t be used, it just looks pretty, please try again.\n')
    elif use_item_index in map[current_room_index]["Items"]:
        print(color.CYAN + 'Invalid input' + color.END + ': the item must be in your inventory before it can be used, please try again.\n')
    # Anything else "I don't know how to use that"
    else:
        print(color.CYAN + 'Invalid input' + color.END + ': that item can\'t be used, please try again.\n')
    return hero_inventory
    
def drop_item(current_room_index, hero_inventory, drop_item):
    drop_item = drop_item.title()
    drop_item_found = False
    # Find drop_item_index
    for item_index in items:
        if drop_item == items[item_index]["Name"]:
            drop_item_index = item_index
            drop_item_found = True
    if not drop_item_found:
        print(color.CYAN + 'Invalid input' + color.END + ': item does not exist, please try again.\n')
        return hero_inventory
    # If weapon drop add to room inventory
    global hero_weapon
    global map
    if hero_weapon == drop_item_index:
        hero_weapon = "Fists"
        map[current_room_index]["Items"].append(drop_item_index)
        print(color.GREEN + 'Success' + color.END + ': you have dropped your equipped weapon, back to bare knuckles for you!\n')
    # else if in inventory drop and add to room inventory
    elif drop_item_index in hero_inventory:
        hero_inventory.remove(drop_item_index)
        if len(hero_inventory) == 0:
            hero_inventory.append('Empty')
        map[current_room_index]["Items"].append(drop_item_index)
        print(color.GREEN + 'Success' + color.END + ': you have dropped an item, it feels nice not to carry around so much weight!\n')
    # Invalid data
    else:
        print(color.CYAN + 'Invalid input' + color.END + ': you can\'t drop what you don\'t have, please try again.\n')
    return hero_inventory

def fight(current_room_index):
    # Get monster and hit points
    # Roll hero attack
    #     1 - 20: < 5 missed, >= 5 hits, >= 10 double damage, >= 15 triple damage
    #     1 - 12: Damage roll
    #     Total_Damage = Damage_Roll * (1 + (Weapon_Multiplier/100)) * attack_roll_effect
    #     e.g                  6     * (1 + (     30          /100)) *          2         = 15.6 total damage
    #     e.g. (max)          12     * (1 + (     40          /100)) *          3         = 50.4 total damage
    # Roll hero damage
    # Display attack results
    # Check monster life
    # Roll monster attack
    #    1 - 20: < 5 missed, >= 5 hits, >= 10 double damage, >= 15 triple damage
    #    1 - 12: Damage roll
    #    Total_Damage = Damage_Roll * (1 + (Monster_Multiplier/100)) * attack_roll_effect
    #     e.g                  6     * (1 + (      0          /100)) *          2         = 12.0 total damage
    #     e.g. (max)          12     * (1 + (     75          /100)) *          3         = 63.0 total damage
    # Roll monster damage
    # Display attack results
    # Check Hero life
    print('fight')
    
def instructions():
    print('instructions')
    print('Flowers, pomp, and circumstance.')
    
def intro():
    # Display game intro and instructions
    instructions()
    
    # Get name for the hero character
    hero_name = ""
    while len(hero_name) < 1:
        hero_name = input('What is your name brave hero? ')
    
    # Get hero's class
    good_input = False
    while (not good_input):
        hero_class = ""
        while len(hero_class) < 1:
            hero_class = input('Pick a class to play ([F]ighter, [C]leric, or [R]ouge): ')
        hero_class = hero_class.lower()[0]
        if hero_class == 'f':
            hero_class = 'Fighter'
        elif  hero_class == 'c':
            hero_class = 'Cleric'
        elif  hero_class == 'r':
            hero_class = 'Rouge'
        else:
            continue
        good_input = True
    return hero_name, hero_class

# End of Functions, script starts here
main()

print("All Done")


