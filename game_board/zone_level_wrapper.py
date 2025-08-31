import pygame
from game_board.zones.zone_1 import ZoneOne

class ZoneLevelWrapper:
    def __init__(self):
        self.zones = [ZoneOne()]
        self.current_zone_index = 0
        self.current_zone = self.zones[self.current_zone_index]
