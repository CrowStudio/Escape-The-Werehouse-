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
    WALL_SWITCH_UP_1          = "Z1-U1"
    WALL_SWITCH_DOWN_1        = "Z1-D1"
    WALL_SWITCH_LEFT_1        = "Z1-L1"
    WALL_SWITCH_RIGHT_1       = "Z1-R1"
    FLOOR_SWITCH_1            = "Z2-1"
    TRAP_DOOR_1               = "Z3-1"
    SLIDING_DOOR_HORIZONTAL_1 = "Z4-H1"
    SLIDING_DOOR_VERTICAL_1   = "Z4-V1"

class ZoneTwo(BasicBoardElements):
    '''zone 2'''
    def __init__(self):
        super().__init__(ZONE_DATA)

        # Sprite mapping for zone elements
        self.sprite_mapping = {
            Zone2Tiles.WALL_SWITCH_UP_1: (
                (Sprite.WALL_SWITCH_UP_1[0], Sprite.WALL_SWITCH_UP_1[1]),
                'WS_U1_off'
            ),
            Zone2Tiles.WALL_SWITCH_DOWN_1: (
                (Sprite.WALL_SWITCH_DOWN_1[0], Sprite.WALL_SWITCH_DOWN_1[1]),
                'WS_D1_off'
            ),
            Zone2Tiles.WALL_SWITCH_LEFT_1: (
                (Sprite.WALL_SWITCH_LEFT_1[0]), (Sprite.WALL_SWITCH_LEFT_1[1]),
                 'WS_L1_off'
            ),
            Zone2Tiles.WALL_SWITCH_RIGHT_1: (
                (Sprite.WALL_SWITCH_RIGHT_1[0], Sprite.WALL_SWITCH_RIGHT_1[1]),
                'WS_R1_off'
            ),
            Zone2Tiles.SLIDING_DOOR_HORIZONTAL_1: (
                (Sprite.SLIDING_DOOR_HORIZONTAL_1[0], Sprite.SLIDING_DOOR_HORIZONTAL_1[1]),
                'SD_H1_closed'
            ),
            Zone2Tiles.SLIDING_DOOR_VERTICAL_1: (
                (Sprite.SLIDING_DOOR_VERTICAL_1[0], Sprite.SLIDING_DOOR_VERTICAL_1[1]),
                'SD_V1_closed'
            )
        }

        # State mapping of zone elements
        self.state_mapping = {
            # Wall switches: Always valid
            Zone2Tiles.WALL_SWITCH_UP_1: ('WS_U1_off', 'SD_H1_closed',  'wall switch present'),
            Zone2Tiles.WALL_SWITCH_DOWN_1: ('WS_D1_off', 'SD_H1_closed', 'wall switch present'),
            Zone2Tiles.WALL_SWITCH_LEFT_1: ('WS_L1_off', 'SD_V1_closed', 'wall switch present'),
            Zone2Tiles.WALL_SWITCH_RIGHT_1: ('WS_R1_off', 'SD_V1_closed', 'wall switch present'),

            # Sliding doors: State attribute and message prefix
            Zone2Tiles.SLIDING_DOOR_VERTICAL_1: ('SD_V1_closed', 'Vertical sliding door'),
            Zone2Tiles.SLIDING_DOOR_HORIZONTAL_1: ('SD_H1_closed', 'Horizontal sliding door'),
        }

    def check_zone_element_state(self, element, game_state):
        '''Check if a zone element is valid based on its type and game state.'''
        element_type = element[0]

        # Look up the element in the mapping
        if element_type in self.state_mapping:
            entry = self.state_mapping[element_type]

            if isinstance(entry, tuple) and len(entry) == 3:
                # Wall switches: Always valid
                switch_state, door_state, message = entry
                print(message)
                # Invert the state of swithc
                switch_value = getattr(game_state, switch_state)
                setattr(game_state, switch_state, not switch_value)

                door_value = getattr(game_state, door_state)
                setattr(game_state, door_state, not door_value)
                return True
            else:
                # Sliding doors: Check game state
                state_attr, message_prefix = entry
                closed = getattr(game_state, state_attr)

                if not closed:
                    print(f"{message_prefix} open")
                    return True
                else:
                    print(f"{message_prefix} closed")
                    return False

        # Default case: Element not in mapping
        print(f"Warning: Unknown element {element_type} in check_zone_element_state")
        return False

    def blit_zone_element(self, element, pos, i, game_state):
        # Blit the floor tile
        self.game_board.blit(Sprite.FLOOR[i], pos)

        # Look up the element in the sprite mapping
        if element in self.sprite_mapping:
            sprite_data, state_attr = self.sprite_mapping[element]

            if state_attr:
                # Use getattr to check the game state for doors
                closed = getattr(game_state, state_attr)
                sprite = sprite_data[0] if closed else sprite_data[1]
            else:
                # Use the sprite directly for switches
                sprite = sprite_data

            self.game_board.blit(sprite, pos)

    def blit_level(self, game_state):
        super().blit_basic_elements(game_state, blit_zone_element = self.blit_zone_element)

    def validate_move(self, new_x, new_y, game_state):
        return super().validate_move(new_x, new_y, game_state, check_zone_element_state=self.check_zone_element_state)

    def validate_push(self, push_x, push_y, game_state):
        return super().validate_push(push_x, push_y, game_state, check_zone_element_state=self.check_zone_element_state)

    def check_boxes_with_zone_elements(self, game_state, box_num, bx, by):
        return False