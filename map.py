import random
import utility

#
# MAP CONSTANTS, no code should change these values
#
MAP_SQUARE_CHASM = 'O'
MAP_SQUARE_EMPTY = ' '
MAP_SQUARE_HEALTH = '+'
MAP_SQUARE_KEY = 'k'
MAP_SQUARE_LOCK = '@'
MAP_SQUARE_PEBBLE = '.'
MAP_SQUARE_PEBBLES = ':'
MAP_SQUARE_PLANK = '='
MAP_SQUARE_PLANK_SET = 'I'
MAP_SQUARE_ROCK = '#'
MAP_SQUARE_ROPE = '&'
MAP_SQUARE_ROPE_TIED = '~'
MAP_SQUARE_SLINGSHOT = 'Y'

#
# MAP STATE, not constant but value should only be set inside map.py
#
MAP_WIDTH = 1
MAP_HEIGHT = 1
MAP = [[MAP_SQUARE_EMPTY]]

#
# FILE STATE, not constant but value should only be set inside map.py
#
FILE_START_LOCATION_X = None
FILE_START_LOCATION_Y = None
FILE_START_LOOKING_DIRECTION = None
FILE_INVENTORY = {}
FILE_WEREWOLF_START_X = None
FILE_WEREWOLF_START_Y = None
FILE_WEREWOLF_START_HEALTH = None
FILE_WEREWOLF_START_STUN_COUNT = None


#
# MAP FUNCTIONS
#
def getMapSquare(x, y):
    result = MAP_SQUARE_ROCK
    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
        result = MAP[y][x]
    return result


def setMapSquare(x, y, currentValue, newValue):
    result = False
    if 0 <= x < MAP_WIDTH and \
            0 <= y < MAP_HEIGHT and \
            getMapSquare(x, y) == currentValue:
        MAP[y][x] = newValue
        result = True
    return result


def clearMapSquare(x, y, currentValue):
    return setMapSquare(x, y, currentValue, MAP_SQUARE_EMPTY)


def isOpenSpace(x, y):
    openSpace = getMapSquare(x, y)
    if openSpace in [MAP_SQUARE_EMPTY, MAP_SQUARE_PLANK_SET, MAP_SQUARE_ROPE_TIED]:
        result = True
    else:
        result = False
    return result


def canSeePast(x, y):
    seePast = isOpenSpace(x, y)
    if seePast in [MAP_SQUARE_EMPTY, MAP_SQUARE_CHASM, MAP_SQUARE_PEBBLE, MAP_SQUARE_PEBBLES, MAP_SQUARE_PLANK,
                   MAP_SQUARE_PLANK_SET, MAP_SQUARE_ROPE, MAP_SQUARE_ROPE_TIED, MAP_SQUARE_SLINGSHOT]:
        result = True
    else:
        result = False
    return result


def printMapRow(centerX, centerY, rowOffset, screenRadius, locationTuplesToSymbolsDict):
    row = centerY - screenRadius + rowOffset
    for col in range(centerX - screenRadius, centerX + screenRadius + 1):
        characterToPrint = locationTuplesToSymbolsDict.get((col, row), getMapSquare(col, row))
        print(characterToPrint, end='')


def loadGame(fileName):
    global MAP, MAP_WIDTH, MAP_HEIGHT
    global FILE_START_LOCATION_X, FILE_START_LOCATION_Y, FILE_START_LOOKING_DIRECTION
    global FILE_WEREWOLF_START_X, FILE_WEREWOLF_START_Y, FILE_WEREWOLF_START_HEALTH, FILE_WEREWOLF_START_STUN_COUNT
    success = False
    try:
        with open(fileName, 'r') as file:
            firstLine = file.readline()  # reads first line of text in file
            gameConfig = firstLine.split()  # splits first line and returns a list
            mapWidth = int(gameConfig[0])  # returns the list value as an int
            mapHeight = int(gameConfig[1])
            playerLocationX = int(gameConfig[2])
            playerLocationY = int(gameConfig[3])
            lookingDirection = gameConfig[4]  # leave this value as a string
            werewolfX = int(gameConfig[5])
            werewolfY = int(gameConfig[6])
            werewolfHealth = int(gameConfig[7])
            werewolfStunCount = int(gameConfig[8])

            if mapWidth > 0 and mapHeight > 0:
                tempMap = []
                charactersRead = 0
                while charactersRead < mapWidth * mapHeight:
                    buffer = file.readline()
                    if buffer.endswith('\n'):
                        buffer = buffer[:-1]
                    tempMap.append(list(buffer))
                    charactersRead += len(buffer)

                if charactersRead == mapWidth * mapHeight:
                    MAP = tempMap
                    MAP_WIDTH = mapWidth
                    MAP_HEIGHT = mapHeight
                    FILE_START_LOCATION_X = playerLocationX
                    FILE_START_LOCATION_Y = playerLocationY
                    FILE_START_LOOKING_DIRECTION = lookingDirection
                    FILE_WEREWOLF_START_X = werewolfX
                    FILE_WEREWOLF_START_Y = werewolfY
                    FILE_WEREWOLF_START_HEALTH = werewolfHealth
                    FILE_WEREWOLF_START_STUN_COUNT = werewolfStunCount

                    while True:
                        try:
                            for line in file:
                                line = line.strip()
                                if line == '':
                                    break
                                line = line.split(' ')
                                item = line[0]
                                amount = line[1]
                                FILE_INVENTORY[item] = int(amount)
                            break

                        except Exception as e:
                            print("Error reading from file: " + str(e))
                            break

                    success = True
    except Exception as error:
        print(f'\nERROR: {error}\n')

    return success


def saveGame(fileName, playerX, playerY, lookingDirection, inventoryItems, werewolfX, werewolfY, werewolfHealth,
             werewolfStunCount):
    success = False
    try:
        with open(fileName, 'w') as fileHandler:
            print(MAP_WIDTH, MAP_HEIGHT, playerX, playerY, lookingDirection, werewolfX, werewolfY, werewolfHealth,
                  werewolfStunCount, file=fileHandler)
            for i in range(MAP_HEIGHT):
                for w in range(MAP_WIDTH):
                    fileHandler.write(MAP[i][w])
                fileHandler.write('\n')
            for (itemName, amountItem) in inventoryItems.items:
                print(itemName, amountItem, file=fileHandler)
            success = True
    except Exception as error:
        print(f'\nERROR: {error}\n')

    return success


def loadDefaultMap():
    global MAP, MAP_WIDTH, MAP_HEIGHT
    global FILE_START_LOCATION_X, FILE_START_LOCATION_Y, FILE_START_LOOKING_DIRECTION, FILE_INVENTORY
    global FILE_WEREWOLF_START_X, FILE_WEREWOLF_START_Y, FILE_WEREWOLF_START_HEALTH, FILE_WEREWOLF_START_STUN_COUNT
    MAP_WIDTH = 5
    MAP_HEIGHT = 3
    MAP = [list('&.@:='), list('     '), list('OYO k')]
    FILE_START_LOCATION_X = 4
    FILE_START_LOCATION_Y = 1
    FILE_START_LOOKING_DIRECTION = '<'
    FILE_WEREWOLF_START_X = 0
    FILE_WEREWOLF_START_Y = 1
    FILE_WEREWOLF_START_HEALTH = 1
    FILE_WEREWOLF_START_STUN_COUNT = 0
    FILE_INVENTORY = {MAP_SQUARE_HEALTH: 5}


def getRandomEmptyLocation(playerX, playerY, minDistanceFromPlayer):
    numberOfEmptyLocations = 0
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            if MAP[row][col] == MAP_SQUARE_EMPTY and utility.manhattanDistance(playerX, playerY, col,
                                                                               row) >= minDistanceFromPlayer:
                numberOfEmptyLocations += 1

    emptyLocation = None
    if numberOfEmptyLocations > 0:
        stopAfterThisMany = random.randrange(numberOfEmptyLocations)
        numberOfEmptyLocations = 0
        for row in range(MAP_HEIGHT):
            for col in range(MAP_WIDTH):
                if MAP[row][col] == MAP_SQUARE_EMPTY and utility.manhattanDistance(playerX, playerY, col,
                                                                                   row) >= minDistanceFromPlayer:
                    if numberOfEmptyLocations == stopAfterThisMany:
                        emptyLocation = (col, row)
                        break
                    numberOfEmptyLocations += 1
            if emptyLocation is not None:
                break

    return emptyLocation


def twoLocationsAreVisibleToEachOther(firstX, firstY, secondX, secondY):
    areVisible = True
    if firstX == secondX:
        direction = utility.sign(secondY - firstY)
        for j in range(firstY + direction, secondY, direction):
            if not canSeePast(firstX, j):
                areVisible = False
                break
    elif firstY == secondY:
        direction = utility.sign(secondX - firstX)
        for i in range(firstX + direction, secondX, direction):
            if not canSeePast(i, firstY):
                areVisible = False
                break
    else:
        areVisible = False
    return areVisible
