# Tile type enumeration
class BasicTile:
    SIZE            = 100 # Pixel width/height of the squared basic tile
    NUM_COLS        = 6   # Number of tiles for the X axis, default 6
    NUM_ROWS        = 6   # Number of tiles for the Y axis, default 6
    BOARD_WIDTH     = SIZE * NUM_COLS                   # Default 600
    HEIGHT_OFFSET   = 40                                # +40 pixels to compensate for info bar at top
    BOARD_HEIGHT    = (SIZE * NUM_ROWS) + HEIGHT_OFFSET # Default 600 + 40

    START       = 0
    PIT1        = 1
    PIT2        = 2
    PIT3        = 3
    PIT4        = 4
    PIT_WALL    = 5  # Pit as Wall - not able to put box in it
    FLOOR       = 6
    WALL        = 7
    EXIT        = 8