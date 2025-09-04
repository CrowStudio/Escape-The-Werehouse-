import pygame
import json
import os
from game_board.basic_blitting import BasicBoardElements
from game_board.elements.sprites import Sprite

# Set paths for level data
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ZONE_2_PATH = os.path.join(DIR_PATH, 'level_maps', 'zone_2_maps.json')

# Load the game maps
with open(ZONE_2_PATH, 'r') as file:
    ZONE_DATA = json.load(file)

# Tile type enumeration
class Zone2Tiles:
    WALL_SWITCH_UP_1_1          = "Z1U_1_1"
    WALL_SWITCH_UP_1_0          = "Z1U_1_0"
    WALL_SWITCH_UP_2_1          = "Z1U_2_1"
    WALL_SWITCH_UP_2_0          = "Z1U_2_0"
    WALL_SWITCH_DOWN_1_1        = "Z2D_1_1"
    WALL_SWITCH_DOWN_1_0        = "Z2D_1_0"
    WALL_SWITCH_DOWN_2_1        = "Z2D_2_1"
    WALL_SWITCH_DOWN_2_0        = "Z2D_2_0"
    WALL_SWITCH_LEFT_1_1        = "Z3L_1_1"
    WALL_SWITCH_LEFT_1_0        = "Z3L_1_0"
    WALL_SWITCH_LEFT_2_1        = "Z3L_2_1"
    WALL_SWITCH_LEFT_2_0        = "Z3L_2_0"
    WALL_SWITCH_RIGHT_1_1       = "Z4R_1_1"
    WALL_SWITCH_RIGHT_1_0       = "Z4R_1_0"
    WALL_SWITCH_RIGHT_2_1       = "Z4R_2_1"
    WALL_SWITCH_RIGHT_2_0       = "Z4R_2_0"
    SLIDING_DOOR_HORIZONTAL_1_1 = "Z5H_1_1"
    SLIDING_DOOR_HORIZONTAL_1_0 = "Z5H_1_0"
    SLIDING_DOOR_HORIZONTAL_2_1 = "Z5H_2_1"
    SLIDING_DOOR_HORIZONTAL_2_0 = "Z5H_2_0"
    SLIDING_DOOR_VERTICAL_1_1   = "Z6V_1_1"
    SLIDING_DOOR_VERTICAL_1_0   = "Z6V_1_0"
    SLIDING_DOOR_VERTICAL_2_1   = "Z6V_2_1"
    SLIDING_DOOR_VERTICAL_2_0   = "Z6V_2_0"
    FLOOR_SWITCH_1              = "Z7_1"
    FLOOR_SWITCH_2              = "Z7_2"
    FLOOR_SWITCH_3              = "Z7_3"
    FLOOR_SWITCH_4              = "Z7_4"
    TRAP_DOOR_1                 = "Z8_1"
    TRAP_DOOR_2                 = "Z8_2"
    TRAP_DOOR_3                 = "Z8_3"
    TRAP_DOOR_4                 = "Z8_4"
    ACTIVATE_EXIT_1             = "Z9_1"

class ZoneTwo(BasicBoardElements):
    '''zone 2'''
    def __init__(self):
        super().__init__(ZONE_DATA)

        # Sprite mapping for zone elements
        self.sprite_mapping = {
            # Wall switches:
            Zone2Tiles.WALL_SWITCH_UP_1_1: (
                (Sprite.WALL_SWITCH_UP_1_1[0], Sprite.WALL_SWITCH_UP_1_1[1]),
                'WS_U1_on'
            ),
            Zone2Tiles.WALL_SWITCH_UP_1_0: (
                (Sprite.WALL_SWITCH_UP_1_0[0], Sprite.WALL_SWITCH_UP_1_0[1]),
                'WS_U1_off'
            ),
            Zone2Tiles.WALL_SWITCH_DOWN_1_1: (
                (Sprite.WALL_SWITCH_DOWN_1_1[0], Sprite.WALL_SWITCH_DOWN_1_1[1]),
                'WS_D1_on'
            ),
            Zone2Tiles.WALL_SWITCH_DOWN_1_0: (
                (Sprite.WALL_SWITCH_DOWN_1_0[0], Sprite.WALL_SWITCH_DOWN_1_0[1]),
                'WS_D1_off'
            ),
            Zone2Tiles.WALL_SWITCH_LEFT_1_1: (
                (Sprite.WALL_SWITCH_LEFT_1_1[0], Sprite.WALL_SWITCH_LEFT_1_1[1]),
                 'WS_L1_on'
            ),
            Zone2Tiles.WALL_SWITCH_LEFT_1_0: (
                (Sprite.WALL_SWITCH_LEFT_1_0[0], Sprite.WALL_SWITCH_LEFT_1_0[1]),
                 'WS_L1_off'
            ),
            Zone2Tiles.WALL_SWITCH_RIGHT_1_1: (
                (Sprite.WALL_SWITCH_RIGHT_1_1[0], Sprite.WALL_SWITCH_RIGHT_1_1[1]),
                'WS_R1_on'
            ),
            Zone2Tiles.WALL_SWITCH_RIGHT_1_0: (
                (Sprite.WALL_SWITCH_RIGHT_1_0[0], Sprite.WALL_SWITCH_RIGHT_1_0[1]),
                'WS_R1_off'
            ),

            # Sliding doors:
            Zone2Tiles.SLIDING_DOOR_HORIZONTAL_1_1: (
                (Sprite.SLIDING_DOOR_HORIZONTAL_1_1[0], Sprite.SLIDING_DOOR_HORIZONTAL_1_1[1]),
                'SD_H1_1_closed'
            ),
            Zone2Tiles.SLIDING_DOOR_HORIZONTAL_1_0: (
                (Sprite.SLIDING_DOOR_HORIZONTAL_1_0[0], Sprite.SLIDING_DOOR_HORIZONTAL_1_0[1]),
                'SD_H1_0_closed'
            ),
            Zone2Tiles.SLIDING_DOOR_VERTICAL_1_1: (
                (Sprite.SLIDING_DOOR_VERTICAL_1_1[0], Sprite.SLIDING_DOOR_VERTICAL_1_1[1]),
                'SD_V1_1_closed'
            ),
            Zone2Tiles.SLIDING_DOOR_VERTICAL_1_0: (
                (Sprite.SLIDING_DOOR_VERTICAL_1_0[0], Sprite.SLIDING_DOOR_VERTICAL_1_0[1]),
                'SD_V1_0_closed'
            )
        }

        # State mapping of zone elements
        self.state_mapping = {
            # Wall switches:
            Zone2Tiles.WALL_SWITCH_UP_1_1: ('WS_U1_on', 'SD_H1_1_closed',  'Wall switch present'),
            Zone2Tiles.WALL_SWITCH_UP_1_0: ('WS_U1_off', 'SD_H1_0_closed',  'Wall switch present'),

            Zone2Tiles.WALL_SWITCH_DOWN_1_1: ('WS_D1_on', 'SD_H1_1_closed', 'Wall switch present'),
            Zone2Tiles.WALL_SWITCH_DOWN_1_0: ('WS_D1_off', 'SD_H1_0_closed', 'Wall switch present'),

            Zone2Tiles.WALL_SWITCH_LEFT_1_1: ('WS_L1_on', 'SD_V1_1_closed', 'Wall switch present'),
            Zone2Tiles.WALL_SWITCH_LEFT_1_0: ('WS_L1_off', 'SD_V1_0_closed', 'Wall switch present'),

            Zone2Tiles.WALL_SWITCH_RIGHT_1_1: ('WS_R1_on', 'SD_V1_1_closed', 'Wall switch present'),
            Zone2Tiles.WALL_SWITCH_RIGHT_1_0: ('WS_R1_off', 'SD_V1_0_closed', 'Wall switch present'),

            # Sliding doors:
            Zone2Tiles.SLIDING_DOOR_HORIZONTAL_1_1: ('SD_H1_1_closed', 'horizontal sliding door'),
            Zone2Tiles.SLIDING_DOOR_HORIZONTAL_1_0: ('SD_H1_0_closed', 'horizontal sliding door'),

            Zone2Tiles.SLIDING_DOOR_VERTICAL_1_1: ('SD_V1_1_closed', 'vertical sliding door'),
            Zone2Tiles.SLIDING_DOOR_VERTICAL_1_0: ('SD_V1_0_closed', 'vertical sliding door')
        }

    def check_zone_element_state(self, element, game_state):
        '''Check if a zone element is valid based on its type and game state.'''
        element_type = element[0]

        # Look up the element in the mapping
        if element_type in self.state_mapping:
            entry = self.state_mapping[element_type]

            # Wall switches:
            if isinstance(entry, tuple) and len(entry) == 3:
                switch_state, door_state, message = entry
                print(message)
                # Invert the state of switch
                switch_value = getattr(game_state, switch_state)
                setattr(game_state, switch_state, not switch_value)
                print('Activating' if not getattr(game_state, switch_state) else 'Disengaging')

                door_value = getattr(game_state, door_state)
                setattr(game_state, door_state, not door_value)
                print('Opening sliding door' if not getattr(game_state, door_state) else 'Closing sliding door')
                return True
            else:  # Sliding doors:
                door_state, message = entry
                closed = getattr(game_state, door_state)

                if not closed:
                    print('Passing the', message)
                    return True
                else:
                    print('The', message, 'is closed!')
                    return False

        # Default case: Element not in mapping
        print(f"Warning: Unknown element {element_type} in check_zone_element_state")
        return False

    def blit_zone_element(self, element, pos, i, game_state):
        # Blit the floor tile
        self.game_board.blit(Sprite.FLOOR[i], pos)
        # Look up the element in the sprite mapping
        if element in self.sprite_mapping:
            sprite_tuple, state_attr = self.sprite_mapping[element]
            # Get the state of the element from game_state
            element_state = getattr(game_state, state_attr)

            # Select the appropriate sprite based on the element state
            if isinstance(sprite_tuple, tuple) and len(sprite_tuple) == 2:
                # Use the first sprite if element_state is True, else use the second sprite
                sprite = sprite_tuple[1] if element_state else sprite_tuple[0]
            else:
                # Fallback: Use the sprite directly if it's not a tuple
                sprite = sprite_tuple

            # Blit the selected sprite
            self.game_board.blit(sprite, pos)

    def blit_level(self, game_state):
        super().blit_basic_elements(game_state, blit_zone_element = self.blit_zone_element)

    def validate_move(self, new_x, new_y, game_state):
        return super().validate_move(new_x, new_y, game_state, check_zone_element_state=self.check_zone_element_state)

    def validate_push(self, box_data, push_x, push_y, game_state):
        return super().validate_push(box_data, push_x, push_y, game_state, check_zone_element_state=self.check_zone_element_state, check_boxes_with_zone_elements=self.check_boxes_with_zone_elements)

    def check_boxes_with_zone_elements(self, game_state, box_num, push_x, push_y, bx, by):
        box_positions = []
        # Check if the box is being pushed onto a zone element
        for element in self.elements:
            if element[1] == (push_x, push_y):
                print('Checking for zone element at: ', element[1], 'bx:', bx, 'bx:', by)
                if element[0] in [
                    Zone2Tiles.WALL_SWITCH_UP_1_1, Zone2Tiles.WALL_SWITCH_UP_1_0,
                    Zone2Tiles.WALL_SWITCH_DOWN_1_1, Zone2Tiles.WALL_SWITCH_DOWN_1_0,
                    Zone2Tiles.WALL_SWITCH_LEFT_1_1, Zone2Tiles.WALL_SWITCH_LEFT_1_0,
                    Zone2Tiles.WALL_SWITCH_RIGHT_1_1, Zone2Tiles.WALL_SWITCH_RIGHT_1_0,
                    Zone2Tiles.SLIDING_DOOR_HORIZONTAL_1_1, Zone2Tiles.SLIDING_DOOR_HORIZONTAL_1_0,
                    Zone2Tiles.SLIDING_DOOR_VERTICAL_1_1, Zone2Tiles.SLIDING_DOOR_VERTICAL_1_0,
                    self.basic_tile.WALL, self.basic_tile.PIT_WALL
                ]:
                    # Check if there is already a box on the zone element
                    if self.box1 and box_num != 1: box_positions.append((self.b1x, self.b1y))
                    if self.box2 and box_num != 2: box_positions.append((self.b2x, self.b2y))
                    if self.box3 and box_num != 3: box_positions.append((self.b3x, self.b3y))
                    if self.box4 and box_num != 4: box_positions.append((self.b4x, self.b4y))

                    # If another box is already on the zone element, do not trigger it
                    for box_pos in box_positions:
                        print('box positions',box_positions)
                        if box_pos == (bx, by):
                            print(f"Box {box_num} cannot trigger zone element, another box is already on it.")
                            return False
                        # Trigger the zone element
                        return True