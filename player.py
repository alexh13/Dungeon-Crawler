import map

#
# PLAYER STATE CONSTANTS, no code should change these values
#
LOOKING_UP = '^'
LOOKING_DOWN = 'v'
LOOKING_LEFT = '<'
LOOKING_RIGHT = '>'
LOOKING_DEAD = 'X'
SLINGSHOT_DISTANCE = 4
SLINGSHOT_MAX_DAMAGE = 3


#
# PLAYER STATE
#
playerX = None
playerY = None
playerSymbol = None
playerInventory = {}


#
# PLAYER FUNCTIONS
#
def getLookingAtLocation(currentX, currentY, currentSymbol):
    if currentSymbol == LOOKING_LEFT:
        lookingAtX = currentX - 1
        lookingAtY = currentY
    elif currentSymbol == LOOKING_RIGHT:
        lookingAtX = currentX + 1
        lookingAtY = currentY
    elif currentSymbol == LOOKING_UP:
        lookingAtX = currentX
        lookingAtY = currentY - 1
    elif currentSymbol == LOOKING_DOWN:
        lookingAtX = currentX
        lookingAtY = currentY + 1
    else:
        lookingAtX = currentX
        lookingAtY = currentY
    return lookingAtX, lookingAtY


def doPlayerHit(hitpoints):
    playerhealth = playerInventory.get(map.MAP_SQUARE_HEALTH)
    remaininghealth = playerhealth - hitpoints
    if remaininghealth < 0:
        remaininghealth = 0
    playerInventory[map.MAP_SQUARE_HEALTH] = remaininghealth
    return remaininghealth


def playerIsAlive():
    return playerInventory.get(map.MAP_SQUARE_HEALTH, 0) > 0


def getPlayerSymbol():
    global playerSymbol
    if playerIsAlive():
        result = playerSymbol
    else:
        result = LOOKING_DEAD
    return result


def inventoryAdd(item):
    if item == map.MAP_SQUARE_HEALTH:
        playerInventory[item] = playerInventory.get(item, 0) + 1
    if item == map.MAP_SQUARE_KEY:
        playerInventory[item] = playerInventory.get(item, 0) + 1
    if item == map.MAP_SQUARE_PEBBLE:
        playerInventory[item] = playerInventory.get(item, 0) + 1
    if item == map.MAP_SQUARE_PLANK:
        playerInventory[item] = playerInventory.get(item, 0) + 1
    if item == map.MAP_SQUARE_ROPE:
        playerInventory[item] = playerInventory.get(item, 0) + 1
    if item == map.MAP_SQUARE_PEBBLES:
        playerInventory[item] = playerInventory.get(map.MAP_SQUARE_PEBBLE) + 2
    if item == map.MAP_SQUARE_SLINGSHOT:
        playerInventory[item] = playerInventory.get(item, 0) + 1
        if playerInventory[map.MAP_SQUARE_SLINGSHOT] > 1:
            playerInventory[map.MAP_SQUARE_SLINGSHOT] = 1
    return playerInventory


def inventoryHas(item, count=1):
    return playerInventory.get(item, 0) >= count


def inventoryUse(item, count=1):
    success = False

    if item in [map.MAP_SQUARE_HEALTH, map.MAP_SQUARE_KEY, map.MAP_SQUARE_PEBBLE, map.MAP_SQUARE_PLANK, map.MAP_SQUARE_ROPE]:
        if playerInventory.get(item, 0) > 0:
            playerInventory[item] = playerInventory.get(item, 0) - count
            success = True
    elif item == map.MAP_SQUARE_SLINGSHOT:
        if playerInventory.get(item, 0) > 0:
            success = True

    return success


def inventorySet(newInventoryItemsDict):
    for (key, value) in newInventoryItemsDict.items():
        playerInventory[key] = value


def printInventoryRow(row, displayWidth):
    success = False

    extraSpaceWidth = 1
    symbolWidth = max(0, min(2, displayWidth))
    numberWidth = max(0, min(4, displayWidth - symbolWidth))
    nameWidth = max(0, displayWidth - (numberWidth + symbolWidth + extraSpaceWidth))

    if row == 1:
        count = playerInventory.get(map.MAP_SQUARE_KEY, 0)
        if count > 0:
            print(str(count).rjust(numberWidth),
                  ' ',
                  map.MAP_SQUARE_KEY.ljust(symbolWidth),
                  'Key'.ljust(nameWidth),
                  sep='',
                  end='')
            success = True
    elif row == 2:
        count = playerInventory.get(map.MAP_SQUARE_ROPE, 0)
        if count > 0:
            print(str(count).rjust(numberWidth),
                  ' ',
                  map.MAP_SQUARE_ROPE.ljust(symbolWidth),
                  'Rope'.ljust(nameWidth),
                  sep='',
                  end='')
            success = True
    elif row == 3:
        count = playerInventory.get(map.MAP_SQUARE_PLANK, 0)
        if count > 0:
            print(str(count).rjust(numberWidth),
                  ' ',
                  map.MAP_SQUARE_PLANK.ljust(symbolWidth),
                  'Wood Plank'.ljust(nameWidth),
                  sep='',
                  end='')
            success = True
    elif row == 4:
        hasSlingshot = inventoryHas(map.MAP_SQUARE_SLINGSHOT)
        count = playerInventory.get(map.MAP_SQUARE_PEBBLE, 0)
        if hasSlingshot:
            print(str(count).rjust(numberWidth),
                  ' ',
                  map.MAP_SQUARE_SLINGSHOT.ljust(symbolWidth),
                  'Slingshot'.ljust(nameWidth),
                  sep='',
                  end='')
            success = True
        elif count > 0:
            print(str(count).rjust(numberWidth),
                  ' ',
                  map.MAP_SQUARE_PEBBLE.ljust(symbolWidth),
                  'Pebble'.ljust(nameWidth),
                  sep='',
                  end='')
            success = True
    elif row == 5:
        count = playerInventory.get(map.MAP_SQUARE_HEALTH, 0)
        print(str(count).rjust(numberWidth),
              ' ',
              map.MAP_SQUARE_HEALTH.ljust(symbolWidth),
              'Health'.ljust(nameWidth),
              sep='',
              end='')
        success = True

    return success


def getFarthestActionableLocation(maxActionDistance, mustBeEmpty):
    global playerX, playerY
    locationX, locationY = playerX, playerY
    nextX, nextY = None, None
    farthestEmptyX, farthestEmptyY = playerX, playerY
    for i in range(maxActionDistance):
        # The farthest actionable location is the square (defined by locationX and locationY)
        # that is the farthest location the player can affect. This location may not necessarily
        # be empty. Use farthestEmptyX and farthestEmptyY to keep track of the farthest empty
        # actionable location you have found so far. Either way, the farthest actionable location
        # must be directly in front of the player, whichever direction that may be. The player
        # must be able to see this location, meaning that the player must be able to see past
        # every square between the player's location and the farthest actionable location. Take
        # into account the maxActionDistance provided.
        nextX, nextY = getLookingAtLocation(locationX, locationY, playerSymbol)
        if map.canSeePast(nextX, nextY):
            locationX, locationY = nextX, nextY
            if map.getMapSquare(nextX, nextY) == map.MAP_SQUARE_EMPTY:
                farthestEmptyX, farthestEmptyY = nextX, nextY
        else:
            break

    if mustBeEmpty:
        locationX, locationY = farthestEmptyX, farthestEmptyY

    return locationX, locationY


def playerIsLookingAt(x, y):
    isVisible = map.twoLocationsAreVisibleToEachOther(x, y, playerX, playerY)
    canSeeUp = (playerSymbol == LOOKING_UP and y < playerY)
    canSeeDown = (playerSymbol == LOOKING_DOWN and y > playerY)
    canSeeLeft = (playerSymbol == LOOKING_LEFT and x < playerX)
    canSeeRight = (playerSymbol == LOOKING_RIGHT and x > playerX)
    return isVisible and (canSeeUp or canSeeDown or canSeeLeft or canSeeRight)

