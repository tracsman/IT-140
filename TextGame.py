import random

def main():
    user_input = ""
    hero_list = intro()
    hero_name = hero_list[0]
    hero_class = hero_list[1]
    hero_inventory = ["Empty"]
    hero_weapon = "Fists"
    hero_life = 100
    current_room_index = "0"
        
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print()
    print('Hello {} brave {}!!'.format(hero_name, hero_class))
    print('Thank you for taking on this foolhardy.... er... I mean... uh')
    print('valiant! yes, valiant quest! My kingdom has been overrun by evil')
    print('doers and my treasury plundered. Please get my precious gemstones')
    print('back. There are six in all. When you have collected them please')
    print('return to me here in the castle.')
    print()
    print('Best of luck!')
    print()
    while True:
        print()
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print()
        print('You are in the Great Hall')
        print('Your Inventory:', hero_inventory)
        print('Your Weapon:', hero_weapon)
        print('Your health: {} out of 100'.format(hero_life))
        print()
        print('Possible Directions: Path (North), Manor (South)')
        print()
        print('(Verbs: Move, Look, Get, Use, Drop, Attack, Instructions)')
        user_input = input('Please enter a command (verb noun): ')
        if user_input.lower() in ['quit','exit','bye','goodbye','later']:
            temp = input('You have asked to quit the game! Are you sure? Y/n ') or 'y'
            if temp[0].lower() == 'y':
                break
            else:
                continue
        print('parse input')
        

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
            hero_class = input('Pick a class to play ([F]ighter, [C]leric, [R]ouge): ')
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

def init():
    print('Doin that loady stuff')
    print('Loading maps')
    print('Loading items')
    print('Loading monsters')
    print()

init()

main()

print("All Done")


