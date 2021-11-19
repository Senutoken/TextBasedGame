'''
NAME: Guilherme Pereira
DESC: This program is a text based game with a puzzle and horror them to it. Players must find all items throughout
the ship, and some items are necessary to have in order to obtain the other items. If the player does not have all the
items before proceeding with the final room, the game will end and the player will lose. If the player obtains all the
items and makes it to the final room while the Engine Room is also on, the player will win.

STORY: A zombie menace has awoken deep within the bilge of a cruise ship and it has cut off the main power of the ship
as well as all the electricity onboard. All communication has been severed with control and the estimated arrival time
to dock is in a few hours. Due to fear of contamination spreading, all members of the ship have been asked to hide at
the foredeck of the ship where the zombie is last to reach from its current location. As captain, you have been
assigned to carry out a few critical tasks to ensure the threat is neutralized. This means:
1. You must retrieve all 6 items aboard the ship.
2. You must turn on the engine room's power.
3. You must defeat the zombie once all 6 items have been collected.
'''


### Dictionaries ###


# Move will change player position towards room
rooms = {
    "Foredeck": {"South": "Bridge"},
    "Bridge": {"North": "Foredeck", "West": "Captain's Quarters", "South": "Main Hall"},
    "Captain's Quarters": {"East": "Bridge"},
    "Main Hall": {"North": "Bridge", "West": "Cargo Hold", "East": "Cafeteria", "South": "Engine Room"},
    "Cargo Hold": {"East": "Main Hall"},
    "Cafeteria": {"West": "Main Hall"},
    "Engine Room": {"North": "Main Hall", "South": "Bilge"},
    "Bilge": {"North": "Engine Room"}
}

# Use will change room
# 1 = True. 0 = False. True means there is nothing else to use in the room"
# Values must add up to 8 to win the game
room_function = {
    "Foredeck": 1,
    "Bridge": 1,
    "Captain's Quarters": 0, # USE Captain's Key
    "Main Hall": 1,
    "Cargo Hold": 0, # USE Fuse
    "Cafeteria": 1,
    "Engine Room": 0, # USE Valve
    "Bilge": 1
}

# Inspect will retrieve items if they are set to FREE. If RESTRICTED is set, need another item to get.
collectibles = {
    "Foredeck": {"None": "N/A"},
    "Bridge": {"Captain's Key": "FREE"},
    "Captain's Quarters": {"Pistol": "Captain's Key"},
    "Main Hall": {"Flashlight": "FREE"},
    "Cargo Hold": {"Valve": "Fuse"},
    "Cafeteria": {"Ammunition": "FREE"},
    "Engine Room": {"Fuse": "Flashlight"},
    "Bilge": {"None": "N/A"}
}

# Description of rooms to be used if condition is not fulfilled (Inspect)
room_desc = {
    "Foredeck": "All the crewmen are huddled together to preserve warmth during the night's gale.\n"
                "They're counting on you to save their lives, and possibly the fate of others as well.",
    "Bridge": "Darkness and silence control the bridge.\n"
              "Dull flashes and jitters of monitors provide little life in this room.",
    "Captain's Quarters": "A small but warm lamp kindles on the corner of your desk; a haven on this ship.\n"
                          "A pistol is locked behind your locker. You might be able to open it with your keys",
    "Main Hall": "The magnitude of mystery and darkness now reside here.\n"
                 "Unknown eyes pierce through the hall, and stare at you from every direction.",
    "Cargo Hold": "A cold steel door rejects your passage to retrieve a spare valve.\n"
                  "There may be a spare fuse to open this door",
    "Cafeteria": "A place filled with full stomachs and laughter has now become distant memory.\n"
                 "You can't help but smell rotten flesh nearby.",
    "Engine Room": "Pipes and machines have ceased breathing. It is completely dark and difficult to see...\n"
                   "There's a spare fuse here but it's too dark to see. Need a light source.",
    "Bilge": "RAAAAUUUUGHHHH!!!"
}

# Description of rooms to be changed once respective conditions have been fulfilled
room_desc_update = {
    "Foredeck": "Although a beacon of light emits from the ship, a menace still lurks at the heart.\n"
                "Let's finish the job.",
    "Bridge": "The lights and power are back on and a nostalgic feeling comes back.\n"
              "Now is not the time to relax.",
    "Captain's Quarters": "The lamp shining warmly on your desk gives you a sense of hope.\n"
                          "Time to finish the job",
    "Main Hall": "The once dark hall is now filled with a brilliant light with captivating sculptures and paintings.\n"
                 "All of this just for you, an audience of one.",
    "Cargo Hold": "The steel door allows free passage now to and from the Cargo Hold.\n"
                  "You believe to hear creaking among the boxes, but it's only your imagination.",
    "Cafeteria": "While the lights may be on, the lack of people in the cafeteria gives you an uncanny feeling\n"
                 "I wonder what's on the menu tomorrow?",
    "Engine Room": {1: "While it's easier to see with the flashlight, the feeling of another presence does not escape you.\n"
                   "The valve to the main power is broken. There should be a replacement one in the cargo area.",
                    2: "Pipes and machines are now bellowing, powering up the ship to her full might\n"
                   "The final battle is just one door away."},
    "Bilge": "RAAAAUUUUGHHHH!!!"
}


### Global Variables ###


current_room = "Foredeck"
move_counter = 0 # Total moves in the game.
item_counter = 0 # How many total items have been retrieved
room_counter = 0 # How many rooms are fully functional
fixed_engine_room = False
quit_game = False
inventory = []


### Debugging Purpose Functions ###

'''
# Keeps track of variables throughout game. Not part of final game

def DisplayStats():
    global room_counter
    global item_counter
    global fixed_engine_room

    counter = 0

    print("Items collected:" + str(item_counter) + "/6")

    for value in room_function.values():
        counter += value
        print(value)
    room_counter = counter
    print("Rooms functioning:" + str(room_counter) + "/8")

    print("Fixed engine room = ", fixed_engine_room)

# Grants player with completion status. Not part of final game

def Cheat():
    global inventory
    global room_counter
    global room_function
    global fixed_engine_room


    full_inventory = ["Captain's Key", "Pistol", "Flashlight", "Ammunition", "Valve", "Fuse"]


    for key, value in room_function.items():
        room_function[key] = 1
        print(room_function[key])
    room_counter = value

    room_function["Engine Room"] = 0

    inventory = full_inventory

    #fixed_engine_room = True

    #for room, desc in room_desc_update.items():
    #   room_desc[room] = desc
'''

### General Game Functions ###


# The first function to be displayed.
def WelcomeMessage():
    print("<< Welcome to The Menace of Mary Celeste >>")
    print("\n< If you are ever lost, type: 'options' or 'help' to see available commands >")
    print("< In order to win this game, you must complete the following tasks: >")
    print("1) You must retrieve all 6 items aboard the ship")
    print("2) You must have the engine room turned on")
    print("3) You must defeat the zombie with all 6 items in your inventory")
    print("\n< NOTE: You will lose if you enter the bilge before retrieving all items and having the engine room on >")
    print("\n<< Good luck, captain! >>")
    print("\n<<< ============================================================================================= >>>\n")

# A function that provides players with a list of options
def HelpMessage():
    print("<< List of commands to type >>")
    print("'Move': Choose to move either north, south, east, or west.")
    print("'Use': Use an item in a certain room")
    print("'Inspect': Examine the room for items")
    print("'Map': Examine the layout of the ship!")
    print("'Exit': Ends the game")

# Display map through ASCII art!
def DisplayMap():
    # 40 lines of whitespace
    print("                                        \n"
          "                                        \n"
          "               __________               \n"
          "              | Foredeck |              \n"
          "               ----------               \n"
          "                   ||                   \n"
          "  __________   __________               \n"
          " |C.Quarters| |  Bridge  |              \n"
          "  ----------   ----------               \n"
          "                   ||                   \n"
          "  __________   __________   __________  \n"
          " |Cargo Hold| |Main Hall | |Cafeteria | \n"
          "  ----------   ----------   ----------  \n"
          "                   ||                   \n"
          "               __________               \n"
          "              |Eng. Room |              \n"
          "               ----------               \n"
          "                   ||                   \n"
          "               __________               \n"
          "              |  Bilge   |              \n"
          "               ----------               \n"
          "                                        \n"
        )

# The menu that shows up after every action, displaying the player's status.
def Menu():
    global current_room
    global item_counter
    global quit_game

    item_counter = len(inventory)

    print("\n< ================================================================================================== >")
    print("You are currently in:", current_room)
    print("Current inventory:", sorted(inventory))
    print("< ================================================================================================== >\n")
    command = input("Enter command:\n")
    print("\n")

    Commands(command)

def Commands(command):
    global quit_game
    global current_room

    if command.lower() == "move":
        player_direction = input("Type a direction to move:\n")
        Move(player_direction)
    elif command.lower() == "use":
        Use()
    elif command.lower() == "inspect":
        Inspect()
    elif command.lower() == "options" or command.lower() == "help":
        HelpMessage()
    elif command.lower() == "map":
        DisplayMap()
    elif command.lower() == "exit":
        current_room = "Exit"
        quit_game = True
    else:
        print("\n< Invalid Input. Please refer to command list. Type 'help' or 'options' to view the list. >\n")


## Action Functions ##


# Function that moves the player
def Move(direction):
    global move_counter
    global quit_game # only True if player's current room is the bilge.
    global current_room

    move_counter += 1 # Player used MOVE.
    direction = direction.lower().capitalize() # Converting 'direction' variable to target format

    if direction in rooms[current_room]:
        # Direction exists. Move to that room.
        for key, location in rooms[current_room].items():
            # Match player's 'key' with room key
            if direction == key:
                # Move player to that room
                print("\nMoving", direction)
                current_room = location

                if current_room == "Bilge":
                    quit_game = True
    else:
        # Direction does not exist in that room.
        print("Direction does not exist")

# Function that inspects room for items or hints
def Inspect():
    global move_counter
    global current_room
    global collectibles

    move_counter += 1
    print("You inspect your surroundings...\n")

    for location, pair in collectibles.items():
        for item, restriction in pair.items():
            if current_room == location and restriction == "N/A": # Target item reached
                print(room_desc[location])
                print("\nThere is no item to be obtained")
                break
            elif current_room == location and restriction == "FREE": # Target item reached, get item
                print(room_desc[location])
                print("\nObtained:", item)
                inventory.append(item)
                restriction = "N/A"
                pair[item] = restriction
                break
            elif current_room == location and restriction != "FREE" and restriction != "N/A":
                print(room_desc[location])
                print("\n" + str(item) + " is unobtainable at this moment.")
            else: # Target item not reached, continue iterating
                continue
            break
        continue

# Function that uses items to get other items
def Use():
    global move_counter
    global collectibles
    global current_room
    global room_desc
    global room_function
    global fixed_engine_room

    move_counter += 1

    # Unlock item in room
    for location, pair in collectibles.items():
        for item, restriction in pair.items():
            if current_room == location and item in inventory: # Item already exists in player's inventory.
                print("\nYou already have the item for this room.")
                break
            elif current_room == "Engine Room" and "Valve" in inventory and not fixed_engine_room: # Event 2
                print("< Turning on Power >")
                room_function[current_room] = 1
                fixed_engine_room = True
                for location, description in room_desc_update.items():
                    room_desc[location] = description # Updates every description for all rooms.
                room_desc[current_room] = room_desc_update[current_room][2]
                break
            elif current_room == location and restriction in inventory: # Paired item is found. Set locked item to FREE.
                print("\nYou used the " + str(restriction) + ". " + str(item) +
                      " is now obtainable. Type 'Inspect' to retrieve " + str(item))
                restriction = "FREE"
                pair[item] = restriction
                room_desc[location] = room_desc_update[location]  # Room changed, change description
                if current_room == "Engine Room" and not fixed_engine_room:
                    room_desc[location] = room_desc_update[location][1]
                    break
                room_function[location] = 1
                break
            elif current_room == location and restriction == "FREE": # Item in room is free to obtain
                print("\nAn item is located somewhere in this room. Type 'Inspect' to retrieve it.")
                break
            elif current_room == location and restriction == "N/A": # No item needs to be "Used" in the room
                print("\nThere is no item to be used here")
                break
            elif current_room == location and restriction not in inventory: # Need specific item to get tool.
                print("\nRequired item to get " + str(item) + " is not in your inventory")
                break
            else:
                continue

## Execution Game Functions ##


# Function that determines whether the player has won or lost
def Result():
    global item_counter # Must be 6 in order to win
    global room_counter # Must be 8 in order to win
    global fixed_engine_room # Must be true in order to win

    for value in room_function.values():
        room_counter += value
    print(room_counter)

    if current_room == "Bilge" and item_counter == 6:
        if room_counter == 8 and fixed_engine_room == True:
            print("\n<<< CONGRATULATIONS >>>\n"
                  "\nYou won!\n"
                  "You completed all your tasks, gathered every item, fixed every room, turned on the power, and killed"
                  " the zombie!\n"
                  "You're a hero!\n")
        elif room_counter == 8 and not fixed_engine_room:
            print("\n>>> GAME OVER <<<\n"
                  "\nYou forgot to turn on the lights! The zombie delivered a fatal blow and knocked you out\n")
        else:
            print("\n>>> GAME OVER <<<\n"
                  "\nYour tasks were not fully completed.\n"
                  "Without the necessary equipment or power, the zombie overpowered you\n")
    else:
        print("\n>>> GAME OVER <<<\n"
              "You were unprepared and the zombie managed to escape\n")

    Stats()

# Print player stats by the end of the game.
def Stats():
    global item_counter
    global room_counter

    print("\n<< ============================================ >>\n")
    print("<< Player Stats >>")
    print("Total number of moves used:", move_counter) # Using MOVE, USE, or INSPECT adds 1 to the counter.
    print("Items collected: " + str(item_counter) + "/6")
    print("Rooms fixed: " + str(room_counter) + "/8")
    print("\n<< ============================================ >>\n")

# Function that runs most of the game's functions.
def Game():
    WelcomeMessage()
    while not quit_game:
        Menu()
    Result()


## Program Execution ##


if __name__ == '__main__':
    Game()

#TODO: Use changes description for engine room. Fix that