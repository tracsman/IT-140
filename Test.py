# Get input and assign to variables
#first_name = input()
#generic_location = input()
#whole_number = input()
#plural_noun = input()

# Display output
#print(first_name, 'went to', generic_location, 'to buy', whole_number, 'different types of', plural_noun)


import json

map_file = "Map.json"
monster_file = "Monsters.json"
item_file = "Items.json"


print("Loading Map File......", end="")
with open("Map.json", "r") as read_file:
    map = json.load(read_file)
    print("Done")

print("Loading Monster File..", end="")
with open("Map.json", "r") as read_file:
    map = json.load(read_file)
    print("Done")

print("Loading Items File....", end="")
with open("Map.json", "r") as read_file:
    map = json.load(read_file)
    print("Done")
print()
print("-=-=-=-=-=-=-=-")
print()
print (map['0']['Description']) 
