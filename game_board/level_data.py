import json
import os
from game_board.basic_tile import BasicTile

# Set paths for level data
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TUTORIAL_PATH = os.path.join(DIR_PATH, 'zones','level_maps', 'tutorial_maps.json')

# Load the tutorial maps
with open(TUTORIAL_PATH, 'r') as file:
    TUTORIAL_DATA = json.load(file)

class LevelData():
    def __init__(self, ZONE_DATA):
        print("LevelData instance created")  # Debug statement

        # Initiate variables to store levels from the JSON data
        self.tutorial_maps = []
        self.zone_maps = []
        self.level_maps = []

        self.tutorial_title = []
        self.game_title = []
        self.map_title = []

        self.tutorial_active_boxes = []
        self.game_active_boxes = []
        self.active_boxes = []

        self.tutorial_positions = []
        self.game_positions = []
        self.positions = []

        self.tutorial_player_start = []
        self.game_player_start = []
        self.player_start = []

        self.tutorial_player_direction = []
        self.game_player_direction = []
        self.player_direction = []

        self.tutorial_active_exit = []
        self.game_active_exit = []
        self.active_exit = []

        self.game_score = []
        self.level_score = []

        # Always add the tutorial maps
        for level in TUTORIAL_DATA['levels']:
            # Create the level map
            self.tutorial_maps.append([TUTORIAL_DATA['game_board_elements'][item] for row in level['map'] for item in row])
            # Extract other level data
            self.tutorial_title.append(level['title'])
            self.tutorial_active_boxes.append(level['active_boxes'])

            # Convert box positions
            box_positions = []
            for pos in level['box_positions']:
                    box_positions.append(tuple(int(x * BasicTile.SIZE) for x in pos))
            self.tutorial_positions.append(box_positions)

            # Convert player start position
            self.tutorial_player_start.append(tuple(int(x * BasicTile.SIZE) for x in level['player_start']))

            self.tutorial_player_direction.append(level['player_direction'])
            self.tutorial_active_exit.append(level['exit_active'])

        # Add the zone maps
        for level in ZONE_DATA['levels']:
            # Create the level map
            self.zone_maps.append([ZONE_DATA['game_board_elements'][item] for row in level['map'] for item in row])

            # Extract other level data
            self.game_title.append(level['title'])
            self.game_active_boxes.append(level['active_boxes'])

            # Convert box positions
            box_positions = []
            for pos in level['box_positions']:
                    box_positions.append(tuple(int(x * BasicTile.SIZE) for x in pos))
            self.game_positions.append(box_positions)

            # Convert player start position
            self.game_player_start.append(tuple(int(x * BasicTile.SIZE) for x in level['player_start']))

            self.game_player_direction.append(level['player_direction'])
            self.game_active_exit.append(level['exit_active'])
            self.game_score.append(level['score'])

        # Update the level variables
        self.level_maps.append(self.tutorial_maps)
        self.level_maps.append(self.zone_maps)
        print(f'level_maps: {self.level_maps}')

        self.map_title.append(self.tutorial_title)
        self.map_title.append(self.game_title)
        print(f'\nmap_title: {self.map_title}')

        self.active_boxes.append(self.tutorial_active_boxes)
        self.active_boxes.append(self.game_active_boxes)
        print(f'\nactive_boxes: {self.active_boxes}')

        self.positions.append(self.tutorial_positions)
        self.positions.append(self.game_positions)
        print(f'\npositions: {self.positions}')

        self.player_start.append(self.tutorial_player_start)
        self.player_start.append(self.game_player_start)
        print(f'\nplayer_start: {self.player_start}')

        self.player_direction.append(self.tutorial_player_direction)
        self.player_direction.append(self.game_player_direction)
        print(f'\nplayer_direction: {self.player_direction}')

        self.active_exit.append(self.tutorial_active_exit)
        self.active_exit.append(self.game_active_exit)
        print(f'\nactive_exit: {self.active_exit}')

        self.level_score.append(self.game_score)
        print(f'\nlevel_score: {self.level_score}')