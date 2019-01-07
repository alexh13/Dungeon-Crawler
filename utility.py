def sign(x):
    a = x
    if a == 0:
        return 0
    elif a > 0:
        return 1
    elif a < 0:
        return -1


def manhattanDistance(firstX, firstY, secondX, secondY):
    # Returns the "Manhattan distance" between two points:
    #    The difference in their x-coordinates plus the difference in their y-coordinates.
    #    This is the equivalent to picking two squares on a chessboard and counting the
    #    number of squares between them (without diagonals).
    return abs(firstX - secondX) + abs(firstY - secondY)

