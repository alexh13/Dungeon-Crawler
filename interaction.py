import random
import map
import player
import utility
import werewolf

#
# KEYBOARD CONSTANTS, no code should change these values
#
KEYBOARD_UP = 'w'
KEYBOARD_DOWN = 's'
KEYBOARD_LEFT = 'a'
KEYBOARD_RIGHT = 'd'
KEYBOARD_LOOK = 'l'
KEYBOARD_TAKE = 't'
KEYBOARD_USE = 'u'
KEYBOARD_QUIT = 'Q'
KEYBOARD_LOAD_GAME = 'L'
KEYBOARD_SAVE_GAME = 'S'
KEYBOARD_HELP = 'h'


#
# INTERACTION STATE
#
lastMessage = ''


#
# INTERACTION FUNCTIONS
#
def readCharacterInput():
    validInputs = [
        KEYBOARD_UP,
        KEYBOARD_DOWN,
        KEYBOARD_LEFT,
        KEYBOARD_RIGHT,
        KEYBOARD_LOOK,
        KEYBOARD_TAKE,
        KEYBOARD_USE,
        KEYBOARD_QUIT,
        KEYBOARD_LOAD_GAME,
        KEYBOARD_SAVE_GAME,
        KEYBOARD_HELP
    ]
    while True:
        userInput = input()
        if len(userInput) > 1:
            userInput = userInput[0]
        if userInput in validInputs:
            break
        print('Bad input. Try again.')
    return userInput


def doCommand(command):
    if command == KEYBOARD_UP:
        player.playerSymbol = player.LOOKING_UP
        if map.isOpenSpace(player.playerX, player.playerY - 1):
            player.playerY -= 1
    elif command == KEYBOARD_DOWN:
        player.playerSymbol = player.LOOKING_DOWN
        if map.isOpenSpace(player.playerX, player.playerY + 1):
            player.playerY += 1
    elif command == KEYBOARD_LEFT:
        player.playerSymbol = player.LOOKING_LEFT
        if map.isOpenSpace(player.playerX - 1, player.playerY):
            player.playerX -= 1
    elif command == KEYBOARD_RIGHT:
        player.playerSymbol = player.LOOKING_RIGHT
        if map.isOpenSpace(player.playerX + 1, player.playerY):
            player.playerX += 1
    elif command == KEYBOARD_LOOK:
        doLook(player.playerX, player.playerY, player.playerSymbol)
    elif command == KEYBOARD_TAKE:
        doTake(player.playerX, player.playerY, player.playerSymbol)
    elif command == KEYBOARD_USE:
        doUse(player.playerX, player.playerY, player.playerSymbol)
    elif command == KEYBOARD_LOAD_GAME:
        doLoadGame()
        werewolf.skipWerewolfsTurn = True
    elif command == KEYBOARD_SAVE_GAME:
        doSaveGame()
        werewolf.skipWerewolfsTurn = True
    elif command == KEYBOARD_HELP:
        doShowHelp()
        werewolf.skipWerewolfsTurn = True


def doLook(x, y, lookingDirection):
    global lastMessage
    lookingAtX, lookingAtY = player.getLookingAtLocation(x, y, lookingDirection)
    mapSquare = map.getMapSquare(lookingAtX, lookingAtY)
    descriptionDict = {
        map.MAP_SQUARE_CHASM: "The chasm in front of you is too wide to jump across. Perhaps there's another "
                              "way across?",
        map.MAP_SQUARE_EMPTY: "You see nothing of interest.",
        map.MAP_SQUARE_KEY: "There is a shiny key on the ground. But what is it for?",
        map.MAP_SQUARE_LOCK: "The door in front of you is locked.",
        map.MAP_SQUARE_PEBBLE: "You see a large pebble on the ground. Stepping on it would hurt.",
        map.MAP_SQUARE_PEBBLES: "You see two large pebbles on the ground. Stepping on them would hurt.",
        map.MAP_SQUARE_PLANK: "There is a long plank of wood on the ground. You wonder how it got there.",
        map.MAP_SQUARE_PLANK_SET: "The two sides of the chasm are bridged by a long plank of wood.",
        map.MAP_SQUARE_ROPE: "Someone left a long stretch of rope just lying around. How irresponsible.",
        map.MAP_SQUARE_ROPE_TIED: "A rope dangles above the chasm in front of you. You can just barely reach it.",
        map.MAP_SQUARE_ROCK: "The rock wall in front of you is dusty with age. Try not to sneeze.",
        map.MAP_SQUARE_SLINGSHOT: "A weapon! Use it to shoot pebbles at your enemy."
    }
    lastMessage = descriptionDict.get(mapSquare, "You're not sure what it is. You've never seen anything like it "
                                                 "before.")


def doTake(x, y, lookingDirection):
    global lastMessage
    itemX, itemY = player.getLookingAtLocation(x, y, lookingDirection)
    mapSquare = map.getMapSquare(itemX, itemY)
    descriptionDict = {
        map.MAP_SQUARE_KEY: "You pick up the key.",
        map.MAP_SQUARE_PEBBLE: "You pick up a pebble.",
        map.MAP_SQUARE_PEBBLES: "You pick up a couple pebbles.",
        map.MAP_SQUARE_PLANK: "You pick up a plank of wood.",
        map.MAP_SQUARE_ROPE: "You pick up a long rope.",
        map.MAP_SQUARE_SLINGSHOT: "You pick up a slingshot."
    }
    if mapSquare in descriptionDict:
        lastMessage = descriptionDict[mapSquare]
        player.inventoryAdd(mapSquare)
        map.clearMapSquare(itemX, itemY, mapSquare)
    else:
        lastMessage = "There is nothing to take."


def doUse(x, y, lookingDirection):
    global lastMessage
    itemToUse = input("What would you like to use?")
    itemToUse = itemToUse[0]
    if itemToUse == map.MAP_SQUARE_SLINGSHOT \
            and player.inventoryHas(map.MAP_SQUARE_SLINGSHOT) \
            and not player.inventoryHas(map.MAP_SQUARE_PEBBLE):
        lastMessage = "Can't use the slingshot without some ammunition."
        return
    elif not player.inventoryHas(itemToUse):
        lastMessage = "You don't have any."
        return

    # start with default message
    lastMessage = "You can't use that here."

    itemX, itemY = player.getLookingAtLocation(x, y, lookingDirection)
    mapSquare = map.getMapSquare(itemX, itemY)

    if mapSquare == map.MAP_SQUARE_CHASM and itemToUse == map.MAP_SQUARE_PLANK:
        player.inventoryUse(itemToUse)
        map.setMapSquare(itemX, itemY, mapSquare, map.MAP_SQUARE_PLANK_SET)
        lastMessage = "You lay the plank of wood over the chasm. It just barely touches both sides."
    elif mapSquare == map.MAP_SQUARE_CHASM and itemToUse == map.MAP_SQUARE_ROPE:
        player.inventoryUse(itemToUse)
        map.setMapSquare(itemX, itemY, mapSquare, map.MAP_SQUARE_ROPE_TIED)
        lastMessage = "Standing on the tips of your toes, you reach up and tie the rope to a beam above you."
    elif mapSquare == map.MAP_SQUARE_LOCK and itemToUse == map.MAP_SQUARE_KEY:
        player.inventoryUse(itemToUse)
        map.clearMapSquare(itemX, itemY, mapSquare)
        lastMessage = "You turn the key. Hard. Just as the lock opens you feel the key snap in half."
    elif mapSquare == map.MAP_SQUARE_CHASM and itemToUse == map.MAP_SQUARE_PEBBLE:
        player.inventoryUse(itemToUse)
        lastMessage = "You drop a pebble into the chasm, counting the seconds until it hits the bottom. You hear " \
                      "nothing."
    elif mapSquare == map.MAP_SQUARE_CHASM and itemToUse == map.MAP_SQUARE_PEBBLE:
        player.inventoryUse(itemToUse)
        lastMessage = "You drop a pebble into the chasm, counting the seconds until it hits the bottom. You hear " \
                      "nothing."
    elif itemToUse == map.MAP_SQUARE_SLINGSHOT:
        if player.playerIsLookingAt(werewolf.werewolfX, werewolf.werewolfY) \
                and utility.manhattanDistance(player.playerX, player.playerY, werewolf.werewolfX, werewolf.werewolfY)\
                <= player.SLINGSHOT_DISTANCE:
            player.inventoryUse(map.MAP_SQUARE_PEBBLE)
            damage = random.randint(1, player.SLINGSHOT_MAX_DAMAGE)
            werewolf.doWerewolfHit(damage)
            lastMessage = "You hit the werewolf! "
            if werewolf.werewolfIsAlive():
                lastMessage += "He is temporarily stunned. The werewolf took "
                lastMessage += str(damage)
                lastMessage += [" point of damage.", " points of damage."][int(damage > 1)]

            else:
                lastMessage += "You have killed the werewolf."
        else:
            pebbleDestinationX, pebbleDestinationY = player.getFarthestActionableLocation(player.SLINGSHOT_DISTANCE,
                                                                                          True)
            distanceShot = utility.manhattanDistance(player.playerX, player.playerY, pebbleDestinationX,
                                                     pebbleDestinationY)
            if distanceShot > 0:
                player.inventoryUse(map.MAP_SQUARE_PEBBLE)
                map.setMapSquare(pebbleDestinationX, pebbleDestinationY, map.MAP_SQUARE_EMPTY, map.MAP_SQUARE_PEBBLE)
                lastMessage = "The pebble you shot lands "
                lastMessage += str(distanceShot)
                """
                Replace the 0 in the following line of code with code that will choose the correct element in the list
                before it. This decision should be based on the value of distanceShot.
                """
                lastMessage += [" square away.", " squares away."][int(distanceShot) > 1]
            else:
                lastMessage = "There is nothing to shoot your slingshot at."


def doCheckForPlayerDamage():
    global lastMessage
    if player.playerX == werewolf.werewolfX and player.playerY == werewolf.werewolfY and werewolf.werewolfIsAlive():
        damage = random.randint(1, werewolf.WEREWOLF_MAX_DAMAGE)
        player.doPlayerHit(damage)

        if player.playerIsAlive():
            newWerewolfLocation = map.getRandomEmptyLocation(player.playerX, player.playerY,
                                                             werewolf.WEREWOLF_POST_DAMAGE_TELEPORT_DISTANCE)
            VERBS = ["scratched", "clawed", "kicked", "bitten"]
            verbToUse = random.choice(VERBS)

            lastMessage = "You have been "
            lastMessage += verbToUse
            lastMessage += " by the werewolf. He dealt "
            lastMessage += str(damage)
            lastMessage += " point"
            if damage > 1:
                lastMessage += "s"
            lastMessage += " of damage"
            if newWerewolfLocation is not None:
                lastMessage += " and has been teleported to a random location in the maze."
                werewolf.werewolfX, werewolf.werewolfY = newWerewolfLocation
            else:
                lastMessage += ". Unable to relocate werewolf."
        else:
            lastMessage = "You have been killed by a werewolf."


def doLoadGame(gameSlot=None, loadDefaultMapOnFailure=False):
    global lastMessage
    if gameSlot is None:
        gameSlot = input('\nType a number 0-9 and hit ENTER, or any other input to cancel. Input: ')
    if len(gameSlot) != 1 or not gameSlot.isnumeric():
        lastMessage = "Must enter 0-9 to load a saved game."
        return

    fileName = f"gameSlot{gameSlot}.txt"
    if not map.loadGame(fileName):
        lastMessage = "Could not load '"
        lastMessage += fileName
        lastMessage += "'. File is corrupt or does not exist."
        if loadDefaultMapOnFailure:
            lastMessage += " Loading default map."
            doLoadDefaultMap()
        return

    player.playerX = map.FILE_START_LOCATION_X
    player.playerY = map.FILE_START_LOCATION_Y
    if map.FILE_START_LOOKING_DIRECTION in [
            player.LOOKING_UP,
            player.LOOKING_DOWN,
            player.LOOKING_LEFT,
            player.LOOKING_RIGHT
        ]:
        player.playerSymbol = map.FILE_START_LOOKING_DIRECTION
    else:
        player.playerSymbol = player.LOOKING_UP

    player.inventorySet(map.FILE_INVENTORY)

    werewolf.werewolfX = map.FILE_WEREWOLF_START_X
    werewolf.werewolfY = map.FILE_WEREWOLF_START_Y
    werewolf.werewolfHealth = map.FILE_WEREWOLF_START_HEALTH
    werewolf.werewolfStunnedCount = map.FILE_WEREWOLF_START_STUN_COUNT

    lastMessage = f"Loaded game {gameSlot}."


def doSaveGame():
    global lastMessage
    gameSlot = input('\nType a number 0-9 and hit ENTER, or any other input to cancel. Input: ')
    if len(gameSlot) != 1 or not gameSlot.isnumeric():
        lastMessage = "Must enter 0-9 to load a saved game."
        return
    fileName = f"gameSlot{gameSlot}.txt"
    if not map.saveGame(fileName,
                        player.playerX,
                        player.playerY,
                        player.playerSymbol,
                        player.playerInventory,
                        werewolf.werewolfX,
                        werewolf.werewolfY,
                        werewolf.werewolfHealth,
                        werewolf.werewolfStunnedCount):
        lastMessage = f"Could not save '{fileName}'. Data is corrupt or writing files is not allowed."
        return

    lastMessage = f"Saved game to slot {gameSlot}."


def doLoadDefaultMap():
    map.loadDefaultMap()

    player.playerX = map.FILE_START_LOCATION_X
    player.playerY = map.FILE_START_LOCATION_Y
    if map.FILE_START_LOOKING_DIRECTION in [
            player.LOOKING_UP,
            player.LOOKING_DOWN,
            player.LOOKING_LEFT,
            player.LOOKING_RIGHT
        ]:
        player.playerSymbol = map.FILE_START_LOOKING_DIRECTION
    else:
        player.playerSymbol = player.LOOKING_UP

    player.inventorySet(map.FILE_INVENTORY)

    werewolf.werewolfX = map.FILE_WEREWOLF_START_X
    werewolf.werewolfY = map.FILE_WEREWOLF_START_Y
    werewolf.werewolfHealth = map.FILE_WEREWOLF_START_HEALTH
    werewolf.werewolfStunnedCount = map.FILE_WEREWOLF_START_STUN_COUNT


def doShowHelp():
    global lastMessage
    lastMessage = '\n   '.join(["Keyboard commands:",
                                KEYBOARD_UP + "  Go up.",
                                KEYBOARD_DOWN + "  Go down.",
                                KEYBOARD_LEFT + "  Go left.",
                                KEYBOARD_RIGHT + "  Go right.",
                                KEYBOARD_LOOK + "  Look.",
                                KEYBOARD_TAKE + "  Take item.",
                                KEYBOARD_USE + "  Use item.",
                                KEYBOARD_QUIT + "  Quit game.",
                                KEYBOARD_LOAD_GAME + "  Load game.",
                                KEYBOARD_SAVE_GAME + "  Save game.",
                                KEYBOARD_HELP + "  Display this menu."])

