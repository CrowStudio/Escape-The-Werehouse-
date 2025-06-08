import pygame
import json
import os
from game_board.basic_tile import BasicTile

# Set paths for level data
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
STAGE_1_PATH = os.path.join(DIR_PATH, 'level_maps\stage_1_maps.json')

# Load the game maps
with open(STAGE_1_PATH, 'r') as file:
    STAGE_DATA = json.load(file)

class StageOne():
    '''stage 1'''
    def __init__(self):
        # Initiate variables to store levels from the JSON data
        self.stage_maps =[]
        self.map_title =[]
        self.active_boxes = []
        self.box_positions = []
        self.player_start = []
        self.player_direction = []
        self.active_exit = []
        self.level_score = []
        
        # Add the game maps
        for level in STAGE_DATA['levels']:
            # Create the level map
            self.stage_maps.append([STAGE_DATA['game_board_elements'][item] for row in level['map'] for item in row])

            # Extract other level data
            self.map_title.append(level['title'])
            self.active_boxes.append(level['active_boxes'])

            # Convert box positions
            box_positions = []
            for pos in level['box_positions']:
                box_positions.append(tuple(int(x * BasicTile.SIZE) for x in pos))
            self.box_positions.append(box_positions)

            # Convert player start position
            self.player_start.append(tuple(int(x * BasicTile.SIZE) for x in level['player_start']))

            self.player_direction.append(level['player_direction'])
            self.active_exit.append(level['exit_active'])
            self.level_score.append(level['score'])