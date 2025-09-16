from game_board.elements.sprites import Sprite

# Tile type enumeration
class Zone2Tile:
    SIZE            = 100 # Pixel width/height of the squared basic tile
    NUM_COLS        = 6   # Number of tiles for the X axis, default 6
    NUM_ROWS        = 6   # Number of tiles for the Y axis, default 6
    BOARD_WIDTH     = SIZE * NUM_COLS                   # Default 600
    HEIGHT_OFFSET   = 40                                # +40 pixels to compensate for info bar at top
    BOARD_HEIGHT    = (SIZE * NUM_ROWS) + HEIGHT_OFFSET # Default 600 + 40

    # Zone (01-99),                 Element number (00-99),                 False(NA)/True (00-01),             Element Type (00-99)
    # 00 = basic elements           To keep track of multiple instanses     NA = no states, passive element     00 = START
    #                                                                                                           01 = PIT1
    #                                                                                                           02 = PIT2
    #                                                                                                           03 = PIT3
    #                                                                                                           04 = PIT4
    #                                                                                                           05 = BOTTOMLESS_PIT
    #                                                                                                           06 = WALL
    #                                                                                                           07 = FLOOR
    #                                                                                                           08 = EXIT
    #                                                                                                           09 = WALL_SWITCH_*
    #                                                                                                           10 = FLOOR_SWITCH_*
    #                                                                                                           11 = TRAP_DOOR_*
    #                                                                                                           12 = SLIDING_DOOR_*

    WALL_SWITCH_UP_1_1          = 102110110
    WALL_SWITCH_UP_2_1          = 102120110
    WALL_SWITCH_UP_1_0          = 102110010
    WALL_SWITCH_UP_2_0          = 102120010
    WALL_SWITCH_DOWN_1_1        = 102210110
    WALL_SWITCH_DOWN_2_1        = 102220110
    WALL_SWITCH_DOWN_1_0        = 102210010
    WALL_SWITCH_DOWN_2_0        = 102220010
    WALL_SWITCH_LEFT_1_1        = 102310110
    WALL_SWITCH_LEFT_2_1        = 102320110
    WALL_SWITCH_LEFT_1_0        = 102310010
    WALL_SWITCH_LEFT_2_0        = 102320010
    WALL_SWITCH_RIGHT_1_1       = 102410110
    WALL_SWITCH_RIGHT_2_1       = 102420110
    WALL_SWITCH_RIGHT_1_0       = 102410010
    WALL_SWITCH_RIGHT_2_0       = 102420010
    SLIDING_DOOR_HORIZONTAL_1_1 = 102510112
    SLIDING_DOOR_HORIZONTAL_2_1 = 102520112
    SLIDING_DOOR_HORIZONTAL_3_1 = 102530112
    SLIDING_DOOR_HORIZONTAL_4_1 = 102540112
    SLIDING_DOOR_HORIZONTAL_1_0 = 102510012
    SLIDING_DOOR_HORIZONTAL_2_0 = 102520012
    SLIDING_DOOR_HORIZONTAL_3_0 = 102530012
    SLIDING_DOOR_HORIZONTAL_4_0 = 102540012
    SLIDING_DOOR_VERTICAL_1_1   = 102610112
    SLIDING_DOOR_VERTICAL_2_1   = 102620112
    SLIDING_DOOR_VERTICAL_3_1   = 102630112
    SLIDING_DOOR_VERTICAL_4_1   = 102640112
    SLIDING_DOOR_VERTICAL_1_0   = 102610012
    SLIDING_DOOR_VERTICAL_2_0   = 102620012
    SLIDING_DOOR_VERTICAL_3_0   = 102630012
    SLIDING_DOOR_VERTICAL_4_0   = 102640012
    FLOOR_SWITCH_1_1            = 102710109
    FLOOR_SWITCH_2_1            = 102720109
    FLOOR_SWITCH_3_1            = 102730109
    FLOOR_SWITCH_4_1            = 102740109
    FLOOR_SWITCH_1_0            = 102710009
    FLOOR_SWITCH_2_0            = 102720009
    FLOOR_SWITCH_3_0            = 102730009
    FLOOR_SWITCH_4_0            = 102740009
    TRAP_DOOR_UP_1_1            = 102810111
    TRAP_DOOR_DOWN_1_1          = 102820111
    TRAP_DOOR_LEFT_1_1          = 102830111
    TRAP_DOOR_RIGHT_1_1         = 102840111
    TRAP_DOOR_UP_1_0            = 102810011
    TRAP_DOOR_DOWN_1_0          = 102820011
    TRAP_DOOR_LEFT_1_0          = 102830011
    TRAP_DOOR_RIGHT_1_0         = 102840011
    ACTIVATE_EXIT               = 102901009

    # Sprite mapping for zone elements
    sprite_mapping = {
        # Wall switches ON (NC):
        # UP
        WALL_SWITCH_UP_1_1: (
            (Sprite.WALL_SWITCH_UP_1_1[0], Sprite.WALL_SWITCH_UP_1_1[1]),
            'WS_U1_on'
        ),
        WALL_SWITCH_UP_2_1: (
            (Sprite.WALL_SWITCH_UP_2_1[0], Sprite.WALL_SWITCH_UP_2_1[1]),
            'WS_U2_on'
        ),
        # DOWN
        WALL_SWITCH_DOWN_1_1: (
            (Sprite.WALL_SWITCH_DOWN_1_1[0], Sprite.WALL_SWITCH_DOWN_1_1[1]),
            'WS_D1_on'
        ),
        WALL_SWITCH_DOWN_2_1: (
            (Sprite.WALL_SWITCH_DOWN_2_1[0], Sprite.WALL_SWITCH_DOWN_2_1[1]),
            'WS_D2_on'
        ),
        # LEFT
        WALL_SWITCH_LEFT_1_1: (
            (Sprite.WALL_SWITCH_LEFT_1_1[0], Sprite.WALL_SWITCH_LEFT_1_1[1]),
            'WS_L1_on'
        ),
        WALL_SWITCH_LEFT_2_1: (
            (Sprite.WALL_SWITCH_LEFT_2_1[0], Sprite.WALL_SWITCH_LEFT_2_1[1]),
            'WS_L2_on'
        ),
        # RIGHT
        WALL_SWITCH_RIGHT_1_1: (
            (Sprite.WALL_SWITCH_RIGHT_1_1[0], Sprite.WALL_SWITCH_RIGHT_1_1[1]),
            'WS_R1_on'
        ),
        WALL_SWITCH_RIGHT_2_1: (
            (Sprite.WALL_SWITCH_RIGHT_2_1[0], Sprite.WALL_SWITCH_RIGHT_2_1[1]),
            'WS_R2_on'
        ),

        # Wall switches OFF (NO):
        # UP
        WALL_SWITCH_UP_1_0: (
            (Sprite.WALL_SWITCH_UP_1_0[0], Sprite.WALL_SWITCH_UP_1_0[1]),
            'WS_U1_off'
        ),
        WALL_SWITCH_UP_2_0: (
            (Sprite.WALL_SWITCH_UP_2_0[0], Sprite.WALL_SWITCH_UP_2_0[1]),
            'WS_U2_off'
        ),
        # DOWN
        WALL_SWITCH_DOWN_1_0: (
            (Sprite.WALL_SWITCH_DOWN_1_0[0], Sprite.WALL_SWITCH_DOWN_1_0[1]),
            'WS_D1_off'
        ),
        WALL_SWITCH_DOWN_2_0: (
            (Sprite.WALL_SWITCH_DOWN_2_0[0], Sprite.WALL_SWITCH_DOWN_2_0[1]),
            'WS_D2_off'
        ),
        # LEFT
        WALL_SWITCH_LEFT_1_0: (
            (Sprite.WALL_SWITCH_LEFT_1_0[0], Sprite.WALL_SWITCH_LEFT_1_0[1]),
            'WS_L1_off'
        ),
        WALL_SWITCH_LEFT_2_0: (
            (Sprite.WALL_SWITCH_LEFT_2_0[0], Sprite.WALL_SWITCH_LEFT_2_0[1]),
            'WS_L2_off'
        ),
        # RIGHT
        WALL_SWITCH_RIGHT_1_0: (
            (Sprite.WALL_SWITCH_RIGHT_1_0[0], Sprite.WALL_SWITCH_RIGHT_1_0[1]),
            'WS_R1_off'
        ),
        WALL_SWITCH_RIGHT_2_0: (
            (Sprite.WALL_SWITCH_RIGHT_2_0[0], Sprite.WALL_SWITCH_RIGHT_2_0[1]),
            'WS_R2_off'
        ),


        # Sliding doors OPEN (NO):
        # HORIZONTAL
        SLIDING_DOOR_HORIZONTAL_1_1: (
            (Sprite.SLIDING_DOOR_HORIZONTAL_1_1[0], Sprite.SLIDING_DOOR_HORIZONTAL_1_1[1]),
            'SD_H1_1_normally_open'
        ),
        SLIDING_DOOR_HORIZONTAL_2_1: (
            (Sprite.SLIDING_DOOR_HORIZONTAL_2_1[0], Sprite.SLIDING_DOOR_HORIZONTAL_2_1[1]),
            'SD_H2_1_normally_open'
        ),
        SLIDING_DOOR_HORIZONTAL_3_1: (
            (Sprite.SLIDING_DOOR_HORIZONTAL_3_1[0], Sprite.SLIDING_DOOR_HORIZONTAL_3_1[1]),
            'SD_H3_1_normally_open'
        ),
        SLIDING_DOOR_HORIZONTAL_4_1: (
            (Sprite.SLIDING_DOOR_HORIZONTAL_4_1[0], Sprite.SLIDING_DOOR_HORIZONTAL_4_1[1]),
            'SD_H4_1_normally_open'
        ),
        # VERTICAL
        SLIDING_DOOR_VERTICAL_1_1: (
            (Sprite.SLIDING_DOOR_VERTICAL_1_1[0], Sprite.SLIDING_DOOR_VERTICAL_1_1[1]),
            'SD_V1_1_normally_open'
        ),
        SLIDING_DOOR_VERTICAL_2_1: (
            (Sprite.SLIDING_DOOR_VERTICAL_2_1[0], Sprite.SLIDING_DOOR_VERTICAL_2_1[1]),
            'SD_V2_1_normally_open'
        ),
        SLIDING_DOOR_VERTICAL_3_1: (
            (Sprite.SLIDING_DOOR_VERTICAL_3_1[0], Sprite.SLIDING_DOOR_VERTICAL_3_1[1]),
            'SD_V3_1_normally_open'
        ),
        SLIDING_DOOR_VERTICAL_4_1: (
            (Sprite.SLIDING_DOOR_VERTICAL_4_1[0], Sprite.SLIDING_DOOR_VERTICAL_4_1[1]),
            'SD_V4_1_normally_open'
        ),

        # Sliding doors CLOSED (NC):
        # HORIZONTAL
        SLIDING_DOOR_HORIZONTAL_1_0: (
            (Sprite.SLIDING_DOOR_HORIZONTAL_1_0[0], Sprite.SLIDING_DOOR_HORIZONTAL_1_0[1]),
            'SD_H1_0_normally_closed'
        ),
        SLIDING_DOOR_HORIZONTAL_2_0: (
            (Sprite.SLIDING_DOOR_HORIZONTAL_2_0[0], Sprite.SLIDING_DOOR_HORIZONTAL_2_0[1]),
            'SD_H2_0_normally_closed'
        ),
        SLIDING_DOOR_HORIZONTAL_3_0: (
            (Sprite.SLIDING_DOOR_HORIZONTAL_3_0[0], Sprite.SLIDING_DOOR_HORIZONTAL_3_0[1]),
            'SD_H3_0_normally_closed'
        ),
        SLIDING_DOOR_HORIZONTAL_4_0: (
            (Sprite.SLIDING_DOOR_HORIZONTAL_4_0[0], Sprite.SLIDING_DOOR_HORIZONTAL_4_0[1]),
            'SD_H4_0_normally_closed'
        ),
        # VERTICAL
        SLIDING_DOOR_VERTICAL_1_0: (
            (Sprite.SLIDING_DOOR_VERTICAL_1_0[0], Sprite.SLIDING_DOOR_VERTICAL_1_0[1]),
            'SD_V1_0_normally_closed'
        ),
        SLIDING_DOOR_VERTICAL_2_0: (
            (Sprite.SLIDING_DOOR_VERTICAL_2_0[0], Sprite.SLIDING_DOOR_VERTICAL_2_0[1]),
            'SD_V2_0_normally_closed'
        ),
        SLIDING_DOOR_VERTICAL_3_0: (
            (Sprite.SLIDING_DOOR_VERTICAL_3_0[0], Sprite.SLIDING_DOOR_VERTICAL_3_0[1]),
            'SD_V3_0_normally_closed'
        ),
        SLIDING_DOOR_VERTICAL_4_0: (
            (Sprite.SLIDING_DOOR_VERTICAL_4_0[0], Sprite.SLIDING_DOOR_VERTICAL_4_0[1]),
            'SD_V4_0_normally_closed'
        ),

        # Floor switches ON (NC):
        FLOOR_SWITCH_1_1: (
            (Sprite.FLOOR_SWITCH_1_1[0], Sprite.FLOOR_SWITCH_1_1[1]),
            'FS1_on'
        ),
        FLOOR_SWITCH_2_1: (
            (Sprite.FLOOR_SWITCH_2_1[0], Sprite.FLOOR_SWITCH_2_1[1]),
            'FS2_on'
        ),
        FLOOR_SWITCH_3_1: (
            (Sprite.FLOOR_SWITCH_3_1[0], Sprite.FLOOR_SWITCH_3_1[1]),
            'FS3_on'
        ),
        FLOOR_SWITCH_4_1: (
            (Sprite.FLOOR_SWITCH_4_1[0], Sprite.FLOOR_SWITCH_4_1[1]),
            'FS4_on'
        ),

        # Floor switches OFF (NO):
        FLOOR_SWITCH_1_0: (
            (Sprite.FLOOR_SWITCH_1_0[0], Sprite.FLOOR_SWITCH_1_0[1]),
            'FS1_off'
        ),
        FLOOR_SWITCH_2_0: (
            (Sprite.FLOOR_SWITCH_2_0[0], Sprite.FLOOR_SWITCH_2_0[1]),
            'FS2_off'
        ),
        FLOOR_SWITCH_3_0: (
            (Sprite.FLOOR_SWITCH_3_0[0], Sprite.FLOOR_SWITCH_3_0[1]),
            'FS3_off'
        ),
        FLOOR_SWITCH_4_0: (
            (Sprite.FLOOR_SWITCH_4_0[0], Sprite.FLOOR_SWITCH_4_0[1]),
            'FS4_off'
        ),

        # Trap doors OPEN (NO):
        TRAP_DOOR_UP_1_1: (
            (Sprite.TRAP_DOOR_UP_1_1[0], Sprite.TRAP_DOOR_UP_1_1[1]),
            'TD_U1_1_normally_open'
        ),
        TRAP_DOOR_DOWN_1_1: (
            (Sprite.TRAP_DOOR_DOWN_1_1[0], Sprite.TRAP_DOOR_DOWN_1_1[1]),
            'TD_d1_1_normally_open'
        ),
        TRAP_DOOR_LEFT_1_1: (
            (Sprite.TRAP_DOOR_LEFT_1_1[0], Sprite.TRAP_DOOR_LEFT_1_1[1]),
            'TD_L1_1_normally_open'
        ),
        TRAP_DOOR_RIGHT_1_1: (
            (Sprite.TRAP_DOOR_RIGHT_1_1[0], Sprite.TRAP_DOOR_RIGHT_1_1[1]),
            'TD_R1_1_normally_open'
        ),

        # Trap doors CLOSED (NC):
        TRAP_DOOR_UP_1_0: (
            (Sprite.TRAP_DOOR_UP_1_0[0], Sprite.TRAP_DOOR_UP_1_0[1]),
            'TD_U1_0_normally_closed'
        ),
        TRAP_DOOR_DOWN_1_0: (
            (Sprite.TRAP_DOOR_DOWN_1_0[0], Sprite.TRAP_DOOR_DOWN_1_0[1]),
            'TD_D1_0_normally_closed'
        ),
        TRAP_DOOR_LEFT_1_0: (
            (Sprite.TRAP_DOOR_LEFT_1_0[0], Sprite.TRAP_DOOR_LEFT_1_0[1]),
            'TD_L1_0_normally_closed'
        ),
        TRAP_DOOR_RIGHT_1_0: (
            (Sprite.TRAP_DOOR_RIGHT_1_0[0], Sprite.TRAP_DOOR_RIGHT_1_0[1]),
            'TD_R1_0_normally_closed'
        ),

        # Switch to activate EXIT
        ACTIVATE_EXIT: (
            (Sprite.ACTIVATE_EXIT[0], Sprite.ACTIVATE_EXIT[1]),
            'activate_exit'
        )
    }

    # State mapping of zone elements
    state_mapping = {
        # Wall switches ON (NC):
        # UP
        WALL_SWITCH_UP_1_1: ('WS_U1_on', 'SD_H1_0_normally_closed',  'wall switch up 1_1', 'latching'),
        WALL_SWITCH_UP_2_1: ('WS_U2_on', 'SD_H2_0_normally_closed',  'wall switch up 2_1', 'latching'),
        # DOWN
        WALL_SWITCH_DOWN_1_1: ('WS_D1_on', 'SD_H1_0_normally_closed', 'wall switch down 1_1', 'latching'),
        WALL_SWITCH_DOWN_2_1: ('WS_D2_on', 'SD_H2_0_normally_closed', 'wall switch down 2_1', 'latching'),
        # LEFT
        WALL_SWITCH_LEFT_1_1: ('WS_L1_on', 'SD_V1_0_normally_closed', 'wall switch left 1_1', 'latching'),
        WALL_SWITCH_LEFT_2_1: ('WS_L2_on', 'SD_V2_0_normally_closed', 'wall switch left 2_1', 'latching'),
        # RIGHT
        WALL_SWITCH_RIGHT_1_1: ('WS_R1_on', 'SD_V1_0_normally_closed', 'wall switch right 1_1', 'latching'),
        WALL_SWITCH_RIGHT_2_1: ('WS_R2_on', 'SD_V2_0_normally_closed', 'wall switch right 2_1', 'latching'),


        # Wall switches OFF (NO):
        # UP
        WALL_SWITCH_UP_1_0: ('WS_U1_off', 'SD_H1_1_normally_open',  'wall switch up 1_0', 'latching'),
        WALL_SWITCH_UP_2_0: ('WS_U2_off', 'SD_H2_1_normally_open',  'wall switch up 2_0', 'latching'),
        # DOWN
        WALL_SWITCH_DOWN_1_0: ('WS_D1_off', 'SD_H1_1_normally_open', 'wall switch down 1_0', 'latching'),
        WALL_SWITCH_DOWN_2_0: ('WS_D2_off', 'SD_H2_1_normally_open', 'wall switch down 2_0', 'latching'),
        # LEFT
        WALL_SWITCH_LEFT_1_0: ('WS_L1_off', 'SD_V1_1_normally_open', 'wall switch left 1_0', 'latching'),
        WALL_SWITCH_LEFT_2_0: ('WS_L2_off', 'SD_V2_1_normally_open', 'wall switch left 2_0', 'latching'),
        # RIGHT
        WALL_SWITCH_RIGHT_1_0: ('WS_R1_off', 'SD_V1_1_normally_open', 'wall switch right 1_0', 'latching'),
        WALL_SWITCH_RIGHT_2_0: ('WS_R2_off', 'SD_V2_1_normally_open', 'wall switch right 2_0', 'latching'),


        # Sliding doors OPEN (NO):
        # HORIZONTAL
        SLIDING_DOOR_HORIZONTAL_1_1: ('SD_H1_1_normally_open', 'horizontal sliding door 1_1'),
        SLIDING_DOOR_HORIZONTAL_2_1: ('SD_H2_1_normally_open', 'horizontal sliding door 2_1'),
        SLIDING_DOOR_HORIZONTAL_3_1: ('SD_H3_1_normally_open', 'horizontal sliding door 3_1'),
        SLIDING_DOOR_HORIZONTAL_4_1: ('SD_H4_1_normally_open', 'horizontal sliding door 4_1'),
        # VERTICAL
        SLIDING_DOOR_VERTICAL_1_1: ('SD_V1_1_normally_open', 'vertical sliding door 1_1'),
        SLIDING_DOOR_VERTICAL_2_1: ('SD_V2_1_normally_open', 'vertical sliding door 2_1'),
        SLIDING_DOOR_VERTICAL_3_1: ('SD_V3_1_normally_open', 'vertical sliding door 3_1'),
        SLIDING_DOOR_VERTICAL_4_1: ('SD_V4_1_normally_open', 'vertical sliding door 4_1'),

        # Sliding doors CLOSED (NC):
        # HORIZONTAL
        SLIDING_DOOR_HORIZONTAL_1_0: ('SD_H1_0_normally_closed', 'horizontal sliding door 1_0'),
        SLIDING_DOOR_HORIZONTAL_2_0: ('SD_H2_0_normally_closed', 'horizontal sliding door 2_0'),
        SLIDING_DOOR_HORIZONTAL_3_0: ('SD_H3_0_normally_closed', 'horizontal sliding door 3_0'),
        SLIDING_DOOR_HORIZONTAL_4_0: ('SD_H4_0_normally_closed', 'horizontal sliding door 4_0'),
        # VERTICAL
        SLIDING_DOOR_VERTICAL_1_0: ('SD_V1_0_normally_closed', 'vertical sliding door 1_0'),
        SLIDING_DOOR_VERTICAL_2_0: ('SD_V2_0_normally_closed', 'vertical sliding door 2_0'),
        SLIDING_DOOR_VERTICAL_3_0: ('SD_V3_0_normally_closed', 'vertical sliding door 3_0'),
        SLIDING_DOOR_VERTICAL_4_0: ('SD_V4_0_normally_closed', 'vertical sliding door 4_0'),

        # Floor switches ON (NO):
        FLOOR_SWITCH_1_1: ('FS1_on', 'TD_U1_1_normally_open', 'floor switch_1_1', 'momentary'),
        FLOOR_SWITCH_2_1: ('FS2_on', 'TD_D1_1_normally_open', 'floor switch_2_1', 'momentary'),
        FLOOR_SWITCH_3_1: ('FS3_on', 'TD_L1_1_normally_open', 'floor switch_3_1', 'momentary'),
        FLOOR_SWITCH_4_1: ('FS4_on', 'TD_R1_1_normally_open', 'floor switch_4_1', 'momentary'),
        # Floor switches OFF (NC):
        FLOOR_SWITCH_1_0: ('FS1_off', 'TD_U1_0_normally_closed', 'floor switch_1_0', 'momentary'),
        FLOOR_SWITCH_2_0: ('FS2_off', 'TD_D1_0_normally_closed', 'floor switch_2_0', 'momentary'),
        FLOOR_SWITCH_3_0: ('FS3_off', 'TD_L1_0_normally_closed', 'floor switch_3_0', 'momentary'),
        FLOOR_SWITCH_4_0: ('FS4_off', 'TD_R1_0_normally_closed', 'floor switch_4_0', 'momentary'),

        # Trap doors OPEN (NO)
        TRAP_DOOR_UP_1_1:('TD_U1_1_normally_open','trap door 1_1'),
        TRAP_DOOR_DOWN_1_1:('TD_D1_1_normally_open','trap door 1_1'),
        TRAP_DOOR_LEFT_1_1:('TD_L1_1_normally_open','trap door 1_1'),
        TRAP_DOOR_RIGHT_1_1:('TD_R1_1_normally_open','trap door 1_1'),

        # Trap doors CLOSED (NC)
        TRAP_DOOR_UP_1_0:('TD_U1_0_normally_closed','trap door 1_0'),
        TRAP_DOOR_DOWN_1_0:('TD_D1_0_normally_closed','trap door 1_0'),
        TRAP_DOOR_LEFT_1_0:('TD_L1_0_normally_closed','trap door 1_0'),
        TRAP_DOOR_RIGHT_1_0:('TD_R1_0_normally_closed','trap door 1_0'),

        ACTIVATE_EXIT:('activate_exit', 'exit', 'activate exit', 'momentary')
    }