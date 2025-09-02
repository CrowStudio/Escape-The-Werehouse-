import pygame
from game_board.zones.zone_1 import ZoneOne
from game_board.zones.zone_2 import ZoneTwo

class ZoneLevelWrapper:
    def __init__(self):
        self.zones = [ZoneOne(), ZoneTwo()]
        self.current_zone_index = 1
        self.current_zone = self.zones[self.current_zone_index]