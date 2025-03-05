from game_board.blitting import BoardElements
from game_board.elements.gfx import debug

# Constants
TILE_SIZE = 100

# Tile type enumeration
class TileType:
    START = 0
    FLOOR = 1
    WALL = 2
    PIT1 = 3
    PIT2 = 4
    PIT3 = 5
    PIT4 = 6
    PIT_WALL = 7
    EXIT = 8

__all__ = ['BoardElements', 'TileType', 'TILE_SIZE', 'debug']
