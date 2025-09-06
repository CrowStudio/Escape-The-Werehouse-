from game_board.elements.sprites import Sprite

# Tile type enumeration
class Zone2Tiles:
    WALL_SWITCH_UP_1_1          = "Z1U_1_1"
    WALL_SWITCH_UP_2_1          = "Z1U_2_1"
    WALL_SWITCH_UP_1_0          = "Z1U_1_0"
    WALL_SWITCH_UP_2_0          = "Z1U_2_0"
    WALL_SWITCH_DOWN_1_1        = "Z2D_1_1"
    WALL_SWITCH_DOWN_2_1        = "Z2D_2_1"
    WALL_SWITCH_DOWN_1_0        = "Z2D_1_0"
    WALL_SWITCH_DOWN_2_0        = "Z2D_2_0"
    WALL_SWITCH_LEFT_1_1        = "Z3L_1_1"
    WALL_SWITCH_LEFT_2_1        = "Z3L_2_1"
    WALL_SWITCH_LEFT_1_0        = "Z3L_1_0"
    WALL_SWITCH_LEFT_2_0        = "Z3L_2_0"
    WALL_SWITCH_RIGHT_1_1       = "Z4R_1_1"
    WALL_SWITCH_RIGHT_2_1       = "Z4R_2_1"
    WALL_SWITCH_RIGHT_1_0       = "Z4R_1_0"
    WALL_SWITCH_RIGHT_2_0       = "Z4R_2_0"
    SLIDING_DOOR_HORIZONTAL_1_1 = "Z5H_1_1"
    SLIDING_DOOR_HORIZONTAL_2_1 = "Z5H_2_1"
    SLIDING_DOOR_HORIZONTAL_1_0 = "Z5H_1_0"
    SLIDING_DOOR_HORIZONTAL_2_0 = "Z5H_2_0"
    SLIDING_DOOR_VERTICAL_1_1   = "Z6V_1_1"
    SLIDING_DOOR_VERTICAL_2_1   = "Z6V_2_1"
    SLIDING_DOOR_VERTICAL_1_0   = "Z6V_1_0"
    SLIDING_DOOR_VERTICAL_2_0   = "Z6V_2_0"
    FLOOR_SWITCH_1_1            = "Z7_1_1"
    FLOOR_SWITCH_2_1            = "Z7_2_1"
    FLOOR_SWITCH_1_0            = "Z7_1_0"
    FLOOR_SWITCH_2_0            = "Z7_2_0"
    TRAP_DOOR_1_1               = "Z8_1_1"
    TRAP_DOOR_2_1               = "Z8_2_1"
    TRAP_DOOR_1_0               = "Z8_1_0"
    TRAP_DOOR_2_0               = "Z8_2_0"
    ACTIVATE_EXIT               = "Z9"

    # Sprite mapping for zone elements
    sprite_mapping = {
        # Wall switches ON:
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

        # Wall switches OFF:
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
        WALL_SWITCH_RIGHT_2_0: (
            (Sprite.WALL_SWITCH_RIGHT_2_0[0], Sprite.WALL_SWITCH_RIGHT_2_0[1]),
            'WS_R2_off'
        ),
        WALL_SWITCH_RIGHT_1_0: (
            (Sprite.WALL_SWITCH_RIGHT_1_0[0], Sprite.WALL_SWITCH_RIGHT_1_0[1]),
            'WS_R1_off'
        ),


        # Sliding doors OPEN:
        # HORIZONTAL
        SLIDING_DOOR_HORIZONTAL_1_1: (
            (Sprite.SLIDING_DOOR_HORIZONTAL_1_1[0], Sprite.SLIDING_DOOR_HORIZONTAL_1_1[1]),
            'SD_H1_1_normally_open'
        ),
        SLIDING_DOOR_HORIZONTAL_2_1: (
            (Sprite.SLIDING_DOOR_HORIZONTAL_2_1[0], Sprite.SLIDING_DOOR_HORIZONTAL_2_1[1]),
            'SD_H2_1_normally_open'
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

        # Sliding doors CLOSED:
        # HORIZONTAL
        SLIDING_DOOR_HORIZONTAL_1_0: (
            (Sprite.SLIDING_DOOR_HORIZONTAL_1_0[0], Sprite.SLIDING_DOOR_HORIZONTAL_1_0[1]),
            'SD_H1_0_normally_closed'
        ),
        SLIDING_DOOR_HORIZONTAL_2_0: (
            (Sprite.SLIDING_DOOR_HORIZONTAL_2_0[0], Sprite.SLIDING_DOOR_HORIZONTAL_2_0[1]),
            'SD_H2_0_normally_closed'
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

        # Floor switches ON:
        FLOOR_SWITCH_1_1: (
            (Sprite.FLOOR_SWITCH_1_1[0], Sprite.FLOOR_SWITCH_1_1[1]),
            'FS1_on'
        ),
        FLOOR_SWITCH_2_1: (
            (Sprite.FLOOR_SWITCH_2_1[0], Sprite.FLOOR_SWITCH_2_1[1]),
            'FS2_on'
        ),

        # Floor switches OFF:
        FLOOR_SWITCH_1_0: (
            (Sprite.FLOOR_SWITCH_1_0[0], Sprite.FLOOR_SWITCH_1_0[1]),
            'FS1_off'
        ),
        FLOOR_SWITCH_2_0: (
            (Sprite.FLOOR_SWITCH_2_0[0], Sprite.FLOOR_SWITCH_2_0[1]),
            'FS2_off'
        ),

        # Switch to activate EXIT
        ACTIVATE_EXIT: (
            (Sprite.ACTIVATE_EXIT[0], Sprite.ACTIVATE_EXIT[1]),
            'activate_exit'
        )
    }

    # State mapping of zone elements
    state_mapping = {
        # Wall switches ON:
        # UP
        WALL_SWITCH_UP_1_1: ('WS_U1_on', 'SD_H1_0_normally_closed',  'Wall switch present'),
        WALL_SWITCH_UP_2_1: ('WS_U2_on', 'SD_H2_0_normally_closed',  'Wall switch present'),
        # DOWN
        WALL_SWITCH_DOWN_1_1: ('WS_D1_on', 'SD_H1_0_normally_closed', 'Wall switch present'),
        WALL_SWITCH_DOWN_2_1: ('WS_D2_on', 'SD_H2_0_normally_closed', 'Wall switch present'),
        # LEFT
        WALL_SWITCH_LEFT_1_1: ('WS_L1_on', 'SD_V1_0_normally_closed', 'Wall switch present'),
        WALL_SWITCH_LEFT_2_1: ('WS_L2_on', 'SD_V2_0_normally_closed', 'Wall switch present'),
        # RIGHT
        WALL_SWITCH_RIGHT_1_1: ('WS_R1_on', 'SD_V1_0_normally_closed', 'Wall switch present'),
        WALL_SWITCH_RIGHT_2_1: ('WS_R2_on', 'SD_V2_0_normally_closed', 'Wall switch present'),


        # Wall switches OFF:
        # UP
        WALL_SWITCH_UP_1_0: ('WS_U1_off', 'SD_H1_1_normally_open',  'Wall switch present'),
        WALL_SWITCH_UP_2_0: ('WS_U2_off', 'SD_H2_1_normally_open',  'Wall switch present'),
        # DOWN
        WALL_SWITCH_DOWN_1_0: ('WS_D1_off', 'SD_H1_1_normally_open', 'Wall switch present'),
        WALL_SWITCH_DOWN_2_0: ('WS_D2_off', 'SD_H2_1_normally_open', 'Wall switch present'),
        # LEFT
        WALL_SWITCH_LEFT_1_0: ('WS_L1_off', 'SD_V1_1_normally_open', 'Wall switch present'),
        WALL_SWITCH_LEFT_2_0: ('WS_L2_off', 'SD_V2_1_normally_open', 'Wall switch present'),
        # RIGHT
        WALL_SWITCH_RIGHT_1_0: ('WS_R1_off', 'SD_V1_1_normally_open', 'Wall switch present'),
        WALL_SWITCH_RIGHT_2_0: ('WS_R2_off', 'SD_V2_1_normally_open', 'Wall switch present'),


        # Sliding doors OPEN (NO):
        # HORIZONTAL
        SLIDING_DOOR_HORIZONTAL_1_1: ('SD_H1_1_normally_open', 'horizontal sliding door'),
        SLIDING_DOOR_HORIZONTAL_2_1: ('SD_H2_1_normally_open', 'horizontal sliding door'),
        # VERTICAL
        SLIDING_DOOR_VERTICAL_1_1: ('SD_V1_1_normally_open', 'vertical sliding door'),
        SLIDING_DOOR_VERTICAL_2_1: ('SD_V2_1_normally_open', 'vertical sliding door'),

        # Sliding doors CLOSED (NC):
        # HORIZONTAL
        SLIDING_DOOR_HORIZONTAL_1_0: ('SD_H1_0_normally_closed', 'horizontal sliding door'),
        SLIDING_DOOR_HORIZONTAL_2_0: ('SD_H2_0_normally_closed', 'horizontal sliding door'),
        # VERTICAL
        SLIDING_DOOR_VERTICAL_1_0: ('SD_V1_0_normally_closed', 'vertical sliding door'),
        SLIDING_DOOR_VERTICAL_2_0: ('SD_V2_0_normally_closed', 'vertical sliding door')
    }