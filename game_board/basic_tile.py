# Tile type enumeration
class BasicTile:
    SIZE = 100      # Pixel width of the squared basic tile
    NUM_COLS  = 6   # Number of tiles for the X axis
    NUM_ROWS  = 6   # Number of tiles for the Y axis

    START = 0
    PIT1 = 1
    PIT2 = 2
    PIT3 = 3
    PIT4 = 4
    PIT_WALL = 5  # Pit as Wall - not able to put box in it
    FLOOR = 6
    WALL = 7
    EXIT = 8