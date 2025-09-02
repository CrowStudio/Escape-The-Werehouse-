import pygame
import json
import os
from game_board.basic_blitting import BasicBoardElements

# Set paths for level data
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ZONE_1_PATH = os.path.join(DIR_PATH, 'level_maps', 'zone_1_maps.json')

# Load the game maps
with open(ZONE_1_PATH, 'r') as file:
    ZONE_DATA = json.load(file)

class ZoneOne(BasicBoardElements):
    '''zone 1'''
    def __init__(self):
        super().__init__(ZONE_DATA)

    def blit_level(self, game_state):
        super().blit_basic_elements(game_state)

    def check_boxes_with_zone_element(self, game_State, box_num, bx, by):
        return False