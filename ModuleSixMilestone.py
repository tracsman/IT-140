'''
Author: Jon Ormond
Created: October 10th, 2021
Description: Simplified dragon text game, example of room movement.
             Created for week 6 of the IT-140 class at SNHU.
Version: 1.0
'''

# A dictionary for the simplified dragon text game
# The dictionary links a room to other rooms.
rooms = {
        'Great Hall': {'South': 'Bedroom'},
        'Bedroom': {'North': 'Great Hall', 'East': 'Cellar'},
        'Cellar': {'West': 'Bedroom'}
    }

# Set the great hall as the starting point of the game
current_room = "Great Hall"

# Display a welcome message and possible commands
print()
print()
print("Dragon Text Adventure Game")
print("Possible commands: go South, go North, go East, go West, exit")
print("  ----------------------------------------------")
print()

# Main Game Loop
# Although an infinite loop, an exit command will break the loop to end the game
while True:
    # Show user current room
    print(f'You are currently in the {current_room}.')
    # Get user command, note that the input is formatted in title case
    # to ensure the commands and evaluations are case insensitive from
    # the user input.
    user_command = input("Enter a command: ").title()
    # Add a spacer to separate the past verbage and current command output
    print("  ----------------------------------------------")
    print()
    # Check if user input DOES NOT match a valid command
    if user_command not in ["Go North", "Go South", "Go East", "Go West", "Exit"]:
        # Unrecognized command, display error, display valid commands again
        print("That command word is not recognized, please enter a valid command.")
        print("Possible commands: go South, go North, go East, go West, exit")
        # Go back to the top of the loop and get new input
        continue
    # Check if user wants to exit the game
    if user_command == 'Exit':
        # Set current room to exit, although irrelevant to this script,
        # it is specifically called out in the requirements.
        current_room = 'exit'
        # Let the user know they have requested to end the game
        print('You have requested to end the game.')
        # Break out of the main game loop
        break
    # Command is valid, strip off "go"
    user_command = user_command.split()[1]
    # Check if the direction is NOT in the current room possible directions
    if user_command not in rooms[current_room]:
        # Display error message that this direction is an invalid choice for this room
        print('That direction is invalid for the room you are in, try a different direction.')
        # Go back to the top of the loop and get new input
        continue
    # Valid direction
    # Set the current room to the room in the dictionary for the direction requested
    current_room = rooms[current_room][user_command]

# Display ending message
print("Thanks for playing, we hope you had fun!")
print()
