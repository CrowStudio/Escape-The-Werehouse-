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
    SIZE            = 100 # Pixel width/height of the squared basic tile
    NUM_COLS        = 6   # Number of tiles for the X axis, default 6
    NUM_ROWS        = 6   # Number of tiles for the Y axis, default 6
    BOARD_WIDTH     = SIZE * NUM_COLS                   # Default 600
    HEIGHT_OFFSET   = 40                                # +40 pixels to compensate for info bar at top
    BOARD_HEIGHT    = (SIZE * NUM_ROWS) + HEIGHT_OFFSET # Default 600 + 40

    WALL_SWITCH  = "Z1"
    FLOOR_SWITCH = "Z2"

# Generate a flat list in row-major order:
tiles = [
    (col * Zone2Tiles.SIZE, row * Zone2Tiles.SIZE)
    for row in range(Zone2Tiles.NUM_ROWS)
    for col in range(Zone2Tiles.NUM_COLS)
]

class ZoneTwo(BasicBoardElements):
    '''zone 2'''
    def __init__(self):
        super().__init__(ZONE_DATA)

    def __blit_zone_elements__(self):
        # Blit zone-specific sprites on top of the floor tiles
        for element, pos, _, _ in self.elements:
            if not isinstance(element, int):
                if element == Zone2Tiles.WALL_SWITCH:
                    self.game_board.blit(Sprite.WALL_SWITCH, pos)
                elif element == Zone2Tiles.FLOOR_SWITCH:
                    self.game_board.blit(Sprite.FLOOR_SWITCH, pos)

    def blit_level(self):
        super().blit_basic_elements()
        self.game_board.blit(Sprite.WALL_SWITCH, (0,0))
        self.__blit_zone_elements__()