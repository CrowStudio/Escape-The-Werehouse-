import pygame
import json
import os
from game_board.blitter import Blitter
from game_board.basic_tile import BasicTile

# Set paths for level data
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ZONE_1_PATH = os.path.join(DIR_PATH, 'level_maps', 'zone_1_maps.json')

# Load the game maps
with open(ZONE_1_PATH, 'r') as file:
    ZONE_DATA = json.load(file)

class ZoneOne(Blitter):
    '''zone 1'''
    def __init__(self):
        super().__init__(ZONE_DATA, BasicTile)
        self.basic_tile = BasicTile

    def check_zone_element_state(self, element, game_state, player_pos=None, boxes_pos=None):
        element_type = element[0]
        # Basic tiles are OK
        if element_type in self.basic_tile.mapping:
            return True

    def blit_zone_element(self, element, pos, i, game_state):
        pass

    def blit_level_elements(self, game_state):
        super().blit_level_elements(game_state, blit_zone_element = self.blit_zone_element)

    def blit_status_bar(self, game_state):
        super().blit_status_bar(game_state)

    def validate_move(self, new_x, new_y):
        return super().validate_move(new_x, new_y, check_zone_element_state=self.check_zone_element_state)

    def validate_push(self, push_x, push_y):
        return super().validate_push(push_x, push_y, check_zone_element_state=self.check_zone_element_state)