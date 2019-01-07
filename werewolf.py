import random
import map
import utility


#
# WEREWOLF CONSTANTS, no code should change these values
#
WEREWOLF_SYMBOL_NORMAL = 'W'
WEREWOLF_SYMBOL_STUNNED = 'w'
WEREWOLF_SYMBOL_DEAD = 'm'
WEREWOLF_MAX_DAMAGE = 5
WEREWOLF_POST_DAMAGE_TELEPORT_DISTANCE = 6
WEREWOLF_PICTURE_WIDTH = 36
WEREWOLF_PICTURE_HEIGHT = 12
WEREWOLF_PICTURE = [
    "             /\\",
    "            ( ;`~v/~~~ ;._",
    "         ,/'\"/^) ' < o\\  '\".~'\\\\\\--,",
    "       ,/\",/W  u '`. ~  >,._..,   )'",
    "      ,/'  w  ,U^v  ;//^)/')/^\\;~)'",
    "   ,/\"'/   W` ^v  W |;         )/'",
    " ;''  |  v' v`\" W }  \\\\",
    "\"    .'\\    v  `v/^W,) '\\)\\.)\\/)",
    "         `\\   ,/,)'   ''')/^\"-;'",
    "              \\",
    "               '\". _",
    "                    \\" ]

#
# WEREWOLF STATE
#
werewolfX = None
werewolfY = None
werewolfHealth = 0
werewolfStunnedCount = 0
skipWerewolfsTurn = False


#
# WEREWOLF FUNCTIONS
#
def werewolfIsAlive():
    if werewolfHealth > 0:
        return True
    else:
        return False


def werewolfIsStunned():
    if werewolfStunnedCount > 0:
        return True
    else:
        return False


def getWerewolfSymbol():
    symbol = None

    if werewolfIsAlive() and werewolfIsStunned():
        symbol = WEREWOLF_SYMBOL_STUNNED
    elif werewolfIsAlive()and not werewolfIsStunned():
        symbol = WEREWOLF_SYMBOL_NORMAL
    elif not werewolfIsAlive():
        symbol = WEREWOLF_SYMBOL_DEAD

    return symbol


def doWerewolfHit(hitpoints):
    global werewolfHealth, werewolfStunnedCount
    werewolfStunnedCount = werewolfStunnedCount + 2
    werewolfHealth = werewolfHealth - hitpoints
    if werewolfHealth < 0:
        werewolfHealth = 0
    return werewolfHealth


def doWerewolfNextMove(playerX, playerY):

    global werewolfX, werewolfY, skipWerewolfsTurn, werewolfStunnedCount
    if not werewolfIsAlive():
        return

    # if you should skip the werewolf's turn, set skipWerewolfsTurn to False and do not execute the rest of this
    # function

    if skipWerewolfsTurn is True:
        skipWerewolfsTurn = False
        return

    # if the werewolf is stunned, subtract 1 from the stun count and do not execute the rest of this function

    if werewolfIsStunned():
        werewolfStunnedCount = werewolfStunnedCount - 1
        return

    deltaX = playerX - werewolfX  # distance from werewolf to player in X direction
    deltaY = playerY - werewolfY  # distance from werewolf to player in Y direction

    possibleNextX = werewolfX + utility.sign(deltaX)  # one square closer to player in X direction
    possibleNextY = werewolfY + utility.sign(deltaY)  # one square closer to player in Y direction

    xDirectionMovePossible = (deltaX != 0 and isOpenSpaceForWerewolf(possibleNextX, werewolfY))
    yDirectionMovePossible = (deltaY != 0 and isOpenSpaceForWerewolf(werewolfX, possibleNextY))

    if xDirectionMovePossible and not yDirectionMovePossible:
        werewolfX = possibleNextX
    elif not xDirectionMovePossible and yDirectionMovePossible:
        werewolfY = possibleNextY
    elif xDirectionMovePossible and yDirectionMovePossible:
        if abs(deltaX) > abs(deltaY):
            werewolfX = possibleNextX
        elif abs(deltaX) < abs(deltaY):
            werewolfY = possibleNextY
        else:
            # expression that randomly produces True or False with equal probability
            randomlyPickX = random.choice([True, False])
            if randomlyPickX:
                werewolfX = possibleNextX
            else:
                werewolfY = possibleNextY


def isOpenSpaceForWerewolf(x, y):
    # - the werewolf can walk through squares that are empty or have key, pebble, pebbles, plank, set plank, or rope
    # - return True or False because on this description of location (x, y)
    #
    whatsInSpace = map.getMapSquare(x, y)
    if whatsInSpace in [map.MAP_SQUARE_EMPTY,
                        map.MAP_SQUARE_KEY,
                        map.MAP_SQUARE_PEBBLE,
                        map.MAP_SQUARE_PEBBLES,
                        map.MAP_SQUARE_PLANK,
                        map.MAP_SQUARE_PLANK_SET,
                        map.MAP_SQUARE_ROPE]:
        return True
    else:
        return False

