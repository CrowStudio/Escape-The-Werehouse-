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
    WALL_SWITCH  = "Z1"
    FLOOR_SWITCH = "Z2"

class ZoneTwo(BasicBoardElements):
    '''zone 2'''
    def __init__(self):
        super().__init__(ZONE_DATA)

    def blit_zone_element(self, element, pos, i):
        # Blit zone-specific sprites on top of the floor tiles
        if element == Zone2Tiles.WALL_SWITCH:
            self.game_board.blit(Sprite.FLOOR[i], pos)
            self.game_board.blit(Sprite.WALL_SWITCH, pos)
        elif element == Zone2Tiles.FLOOR_SWITCH:
            self.game_board.blit(Sprite.FLOOR[i], pos)
            self.game_board.blit(Sprite.FLOOR_SWITCH, pos)

    def blit_level(self):
        super().blit_basic_elements(blit_zone_element = self.blit_zone_element)