from game_board.blitting import BoardElements
from game_board.elements.gfx import debug

# Constants
TILE_SIZE = 100

# Tile type enumeration
class TileType:
    START = 0
    PIT1 = 1
    PIT2 = 2
    PIT3 = 3
    PIT4 = 4
    PIT_WALL = 5  # Pit as Wall - not able to put box in it
    FLOOR = 6
    WALL = 7
    EXIT = 8

__all__ = ['BoardElements', 'TileType', 'TILE_SIZE', 'debug']
