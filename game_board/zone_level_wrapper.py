import pygame
from game_board.zones.zone_1 import ZoneOne
from game_board.zones.zone_2 import ZoneTwo

class ZoneLevelWrapper:
    def __init__(self):
        self.zone = [ZoneOne(), ZoneTwo()]
        self.no_of_zones = len(self.zone) -1  # to compensate for zone index that starts at 0
        self.current_zone_index = 1
        self.current_level_set = self.zone[self.current_zone_index]

    def switch_to_next_zone(self):
        self.current_zone_index += 1
        self.current_level_set = self.zone[self.current_zone_index]
        print(f"Entering zone {self.current_zone_index + 1}")