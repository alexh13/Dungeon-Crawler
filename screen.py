import interaction
import map
import player
import werewolf


#
# SCREEN CONSTANTS AND SETTINGS, no code should change these values
#
SCREEN_MAP_RADIUS = 3
SCREEN_MAP_WIDTH_HEIGHT = SCREEN_MAP_RADIUS * 2 + 1
SCREEN_INVENTORY_WIDTH = 22
SCREEN_PICTURE_WIDTH = SCREEN_MAP_WIDTH_HEIGHT + SCREEN_INVENTORY_WIDTH + 1  # 3 for the frame chars


#
# SCREEN FUNCTIONS
#
def clearScreen():
    print('\n' * 100)


def printScreen():
    locationTuplesToSymbolsDict = {
        (player.playerX, player.playerY): player.getPlayerSymbol(),
        (werewolf.werewolfX, werewolf.werewolfY): werewolf.getWerewolfSymbol()
    }

    FRAME_TOP_CORNER = ','
    FRAME_MIDDLE_CORNER = '+'
    FRAME_BOTTOM_CORNER = '\''
    FRAME_SIDE_HORIZONTAL = '-'
    FRAME_SIDE_VERTICAL = '|'

    if map.twoLocationsAreVisibleToEachOther(player.playerX, player.playerY, werewolf.werewolfX, werewolf.werewolfY):
        leftMargin = (SCREEN_PICTURE_WIDTH - werewolf.WEREWOLF_PICTURE_WIDTH) // 2
        rightMargin = SCREEN_PICTURE_WIDTH - werewolf.WEREWOLF_PICTURE_WIDTH - leftMargin

        # draw top of frame
        print(FRAME_TOP_CORNER + FRAME_SIDE_HORIZONTAL * SCREEN_PICTURE_WIDTH + FRAME_TOP_CORNER)

        # draw werewolf picture
        for i in range(werewolf.WEREWOLF_PICTURE_HEIGHT):
            print(FRAME_SIDE_VERTICAL,
                  ' ' * leftMargin,
                  werewolf.WEREWOLF_PICTURE[i].ljust(werewolf.WEREWOLF_PICTURE_WIDTH),
                  ' ' * rightMargin,
                  FRAME_SIDE_VERTICAL, sep='')

        # draw middle of frame
        print(FRAME_MIDDLE_CORNER,
              FRAME_SIDE_HORIZONTAL * SCREEN_MAP_WIDTH_HEIGHT,
              FRAME_MIDDLE_CORNER,
              FRAME_SIDE_HORIZONTAL * SCREEN_INVENTORY_WIDTH,
              FRAME_MIDDLE_CORNER, sep='')
    else:
        # draw top of frame
        print(FRAME_TOP_CORNER,
              FRAME_SIDE_HORIZONTAL * SCREEN_MAP_WIDTH_HEIGHT,
              FRAME_TOP_CORNER,
              FRAME_SIDE_HORIZONTAL * SCREEN_INVENTORY_WIDTH,
              FRAME_TOP_CORNER, sep='')

    # draw frame, map, and inventory
    for row in range(SCREEN_MAP_WIDTH_HEIGHT):
        print(FRAME_SIDE_VERTICAL, end='')
        map.printMapRow(player.playerX, player.playerY, row, SCREEN_MAP_RADIUS, locationTuplesToSymbolsDict)
        print(FRAME_SIDE_VERTICAL, end='')
        if not player.printInventoryRow(row, SCREEN_INVENTORY_WIDTH):
            print(' ' * SCREEN_INVENTORY_WIDTH, end='')
        print(FRAME_SIDE_VERTICAL)

    # draw bottom of frame
    print(FRAME_BOTTOM_CORNER,
          FRAME_SIDE_HORIZONTAL * SCREEN_MAP_WIDTH_HEIGHT,
          FRAME_BOTTOM_CORNER,
          FRAME_SIDE_HORIZONTAL * SCREEN_INVENTORY_WIDTH,
          FRAME_BOTTOM_CORNER, sep='')

    # messaging below frame
    print(f'\n{interaction.lastMessage}\n\nYou are at ({player.playerX},{player.playerY}). Enter a command: ', end='')
