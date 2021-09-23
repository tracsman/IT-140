import random
import json

# Color class for adding color to the print output
# Idea from https://appdividend.com/2021/06/14/how-to-print-bold-python-text
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

SECTION_BREAK = '\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n'

def main():
    # Load data files to create dictionaries
    # Define filename/location
    map_file = "Map.json"
    monster_file = "Monsters.json"
    item_file = "Items.json"
    
    # Load map file
    print("\nLoading Map File......", end="")
    with open(map_file, "r") as read_file:
        map = json.load(read_file)
        print("Done")

    # Load Monster file
    print("Loading Monster File..", end="")
    with open(monster_file, "r") as read_file:
        monsters = json.load(read_file)
        print("Done")

    # Load Items file
    print("Loading Items File....", end="")
    with open(item_file, "r") as read_file:
        items = json.load(read_file)
        print("Done")
    
    # Set variables used in the game
    user_input = ""
    #hero_list = intro()
    hero_list = ["Bubba", "Fighter"]  # TODO: Remove before production
    hero_name = hero_list[0]
    hero_class = hero_list[1]
    hero_inventory = ["Empty"]
    hero_weapon = "Fists"
    hero_life = 100
    current_room_index = "0" # TODO: reset to 0 before production
    
    # Display intro message from the King
    print(SECTION_BREAK)
    print('Hello {} brave {}!!\n'.format(hero_name, hero_class))
    print('Thank you for taking on this foolhardy.... er... I mean... uh')
    print('valiant! yes, valiant quest! My kingdom has been overrun by evil')
    print('doers and my treasury plundered. Please get my precious gemstones')
    print('back. There are six in all. When you have collected them please')
    print('return to me here in the castle.\n')
    print('Best of luck!\n')
    print(SECTION_BREAK)
            
    # Start main game loop
    while True:
        # Display the standard output screen information:
        # 
        # Current location description
        # Any items in the room
        # Any monsters in the room
        #
        # The hero's inventory
        # The hero's weapon
        # The hero's health
        #
        # The possible directions and whats in that direction
        # 
        # A reminder of the verbs
        # An input prompt for a command
        #
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
        print('\nYour Inventory:', hero_inventory)
        # Show the hero's current equipped weapon
        print('Your Weapon:', hero_weapon)
        # Show the hero's remaining life
        print('Your health: {} out of 100\n'.format(hero_life))
        # Show the possible directions available from this location
        # Start with a beging of the line in a variable and add each valid direction to the string
        directions = "Possible Directions: you see "
        # Check each the dictionary for the current room index, and see if the cardinal direction exists
        if 'North' in map[current_room_index]:
            # If this direction exists, append this direction, nicely formated with an ending comma to the directions string
            # Note: that the map object is being called twice in the format statement, once to pull the index number from the
            #       requested direction of the current room to be used as the index to get the name of the intended room.
            directions +='a {} to the North, '.format(map[map[current_room_index]['North']]['Name'])
        if 'East' in map[current_room_index]:
            directions +='a {} to the East, '.format(map[map[current_room_index]['East']]['Name'])
        if 'South' in map[current_room_index]:
            directions +='a {} to the South, '.format(map[map[current_room_index]['South']]['Name'])
        if 'West' in map[current_room_index]:
            directions +='a {} to the West, '.format(map[map[current_room_index]['West']]['Name'])
        # The last direction appended will have a trailing comma and a space, so we need to trim those two characters off
        directions = directions[:-2]
        # Print the available directions for this location
        print(directions, '\n\n')
        # Print a reminder of the available verbs for the user to use
        print('(Verbs: Move, Look, Get, Use, Drop, Fight, or Instructions)')
        # Get the users command
        user_input = input('Please enter a command (verb noun): ')
        # Check if the user just wants to end the game
        if user_input.lower() in ['quit','exit','bye','goodbye','later']:
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
            look()
        elif  user_verb == 'g':
            get()
        elif  user_verb == 'u':
            use()
        elif  user_verb == 'd':
            drop()
        elif  user_verb == 'f':
            fight()
        elif  user_verb == 'i':
            instructions()
        else:
            print(color.CYAN + color.BOLD + 'Invalid input' + color.END + ': the verb used was not recognized, please try again.\n')

def move(room_index, direction):
    print('move func{}'.format(direction))
    new_room_index = 0
    return new_room_index
    
def look():
    print('look')
        
def get():
    print('get')
    
def use():
    print('use')
    
def drop():
    print('drop')
    
def fight():
    print('fight')
    
def instructions():
    print('instructions')
    
def intro():
    # Display game intro and instructions
    print('Flowers, pomp, and circumstance.')
    
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

