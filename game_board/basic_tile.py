# Tile type enumeration
class BasicTile:
    SIZE            = 100 # Pixel width/height of the squared basic tile
    NUM_COLS        = 6   # Number of tiles for the X axis, default 6
    NUM_ROWS        = 6   # Number of tiles for the Y axis, default 6
    BOARD_WIDTH     = SIZE * NUM_COLS                   # Default 600
    HEIGHT_OFFSET   = 40                                # +40 pixels to compensate for info bar at top
    BOARD_HEIGHT    = (SIZE * NUM_ROWS) + HEIGHT_OFFSET # Default 600 + 40

    # Zone (101-199),           Element number (00-99),                 False(NA)/True (00-01),             Element Type (00-99)
    # 101 = basic elements      To keep track of multiple instanses     NA = no states, passive element     00 = START
    #                                                                                                       01 = PIT1
    #                                                                                                       02 = PIT2
    #                                                                                                       03 = PIT3
    #                                                                                                       04 = PIT4
    #                                                                                                       05 = BOTTOMLESS_PIT
    #                                                                                                       06 = WALL
    #                                                                                                       07 = FLOOR
    #                                                                                                       08 = EXIT
    #                                                                                                       09 = WALL_SWITCH_*
    #                                                                                                       10 = FLOOR_SWITCH_*
    #                                                                                                       11 = TRAP_DOOR_*
    #                                                                                                       12 = SLIDING_DOOR_*

    START           = 101000000
    PIT1            = 101010101
    PIT2            = 101020102
    PIT3            = 101030103
    PIT4            = 101040104
    BOTTOMLESS_PIT  = 101050005
    FLOOR           = 101060006
    WALL            = 101070007
    EXIT            = 101080108

    mapping = [
            START,
            PIT1,
            PIT2,
            PIT3,
            PIT4,
            BOTTOMLESS_PIT,
            FLOOR,
            WALL,
            EXIT
    ]

    state_mapping = []