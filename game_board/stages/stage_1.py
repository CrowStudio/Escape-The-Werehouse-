import pygame
import json
import os
from game_board.blitting import BoardElements

# Set paths for level data
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
STAGE_1_PATH = os.path.join(DIR_PATH, 'level_maps\stage_1_maps.json')

# Load the game maps
with open(STAGE_1_PATH, 'r') as file:
    STAGE_DATA = json.load(file)

class StageOne(BoardElements):
    '''stage 1'''
    def __init__(self):
        super().__init__(self, STAGE_DATA)

    def blit_level(self):
        super().blit_basic_elements()