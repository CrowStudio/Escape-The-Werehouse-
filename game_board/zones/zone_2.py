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

        self.element_mapping = {
            # Simple elements: (sprite, None)
            Zone2Tiles.WALL_SWITCH_UP_1: (Sprite.WALL_SWITCH_UP_1[0], None),
            Zone2Tiles.WALL_SWITCH_DOWN_1: (Sprite.WALL_SWITCH_DOWN_1[0], None),
            Zone2Tiles.WALL_SWITCH_LEFT_1: (Sprite.WALL_SWITCH_LEFT_1[0], None),
            Zone2Tiles.WALL_SWITCH_RIGHT_1: (Sprite.WALL_SWITCH_RIGHT_1[0], None),
            # State-dependent elements: ((closed_sprite, open_sprite), state_attribute)
            Zone2Tiles.SLIDING_DOOR_HORIZONTAL_1: (
                (Sprite.SLIDING_DOOR_HORIZONTAL_1[0], Sprite.SLIDING_DOOR_HORIZONTAL_1[1]),
                'SD_H1_closed'
            ),
            Zone2Tiles.SLIDING_DOOR_VERTICAL_1: (
                (Sprite.SLIDING_DOOR_VERTICAL_1[0], Sprite.SLIDING_DOOR_VERTICAL_1[1]),
                'SD_V1_closed'
            ),
        }

    def blit_zone_element(self, element, pos, i, game_state):
        # Blit the floor tile
        self.game_board.blit(Sprite.FLOOR[i], pos)

        # Look up the element in the mapping
        if element in self.element_mapping:
            sprite_data, state_attr = self.element_mapping[element]

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

    def is_zone_element_valid(self, element, game_state):
        if element[0] in [Zone2Tiles.WALL_SWITCH_UP_1, Zone2Tiles.WALL_SWITCH_DOWN_1, Zone2Tiles.WALL_SWITCH_LEFT_1, Zone2Tiles.WALL_SWITCH_RIGHT_1]:
            print('wall switch present')
            return True
        elif element[0] in Zone2Tiles.SLIDING_DOOR_VERTICAL_1 and game_state.SD_V1_closed == False:
            print('Vertical sliding door open')
            return True
        elif element[0]== Zone2Tiles.SLIDING_DOOR_HORIZONTAL_1 and game_state.SD_H1_closed == False:
            print('Horizontal sliding door open')
            return True
        elif element[0] == Zone2Tiles.SLIDING_DOOR_VERTICAL_1 and game_state.SD_V1_closed == True:
            print('Vertical sliding door  closed')
            return False
        elif element[0]== Zone2Tiles.SLIDING_DOOR_HORIZONTAL_1 and game_state.SD_H1_closed == True:
            print('Horizontal sliding door  closed')
            return False

    def validate_move(self, new_x, new_y, game_state):
        return super().validate_move(new_x, new_y, game_state, is_zone_element_valid=self.is_zone_element_valid)

    def validate_push(self, push_x, push_y, game_state):
        return super().validate_push(push_x, push_y, game_state, is_zone_element_valid=self.is_zone_element_valid)

    def check_boxes_with_zone_element(self, game_State, box_num, bx, by):
        return False