import pygame
import json
import os
from game_board.blitting import BoardElements

# Set paths for level data
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ZONE_1_PATH = os.path.join(DIR_PATH, 'level_maps', 'zone_1_maps.json')

# Load the game maps
with open(ZONE_1_PATH, 'r') as file:
    ZONE_DATA = json.load(file)

class ZoneOne(BoardElements):
    '''zone 1'''
    def __init__(self):
        super().__init__(ZONE_DATA)

    def blit_level(self):
        super().blit_basic_elements()
