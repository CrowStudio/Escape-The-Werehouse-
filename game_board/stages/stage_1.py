import pygame
import json
import os

class stage_1:
    '''stage 1'''
    def __inti__(self):
        # Set paths for level data

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.maps_stage_1_path = os.path.join(self. script_dir, 'level_maps\maps_stage_1.json')

        # Load the game maps
        with open(self.maps_stage_1_path, 'r') as file:
            self.stage_1_level_data = json.load(file)

        # Initiate variables to store levels from the JSON data
        self.stage_maps =[]

        self.map_title =[]

        self.active_boxes = []

        self.box_positions = []

        self.player_start = []

        self.player_direction = []

        self.active_exit = []

        self.level_score = []
        
        self.levle_maps
        
        # Add the game maps
        for level in self.stage_1_level_data['levels']:
            # Create the level map
            self.stage_maps.append([self.stage_1_level_data['game_board_elements'][item] for row in level['map'] for item in row])

            # Extract other level data
            self.map_title.append(level['title'])
            self.active_boxes.append(level['active_boxes'])

            # Convert box positions
            box_positions = []
            for pos in level['box_positions']:
                    box_positions.append(tuple(int(x * 100) for x in pos))
            self.box_positions.append(box_positions)

            # Convert player start position
            self.player_start.append(tuple(int(x * 100) for x in level['player_start']))

            self.player_direction.append(level['player_direction'])
            self.active_exit.append(level['exit_active'])
            self.score.append(level['score'])

            # Update the level variables
            self.level_maps.append(self.stage_maps)
            print(f'level_maps: {self.level_maps}')

            self.map_title.append(self.game_title)
            print(f'\nmap_title: {self.map_title}')

            self.active_boxes.append(self.game_active_boxes)
            print(f'\nactive_boxes: {self.active_boxes}')

            self.box_positions.append(self.game_positions)
            print(f'\npositions: {self.positions}')

            self.player_start.append(self.game_player_start)
            print(f'\nplayer_start: {self.player_start}')

            self.player_direction.append(self.game_player_direction)
            print(f'\nplayer_direction: {self.player_direction}')

            self.active_exit.append(self.game_active_exit)
            print(f'\nactive_exit: {self.active_exit}')

            self.level_score.append(self.game_score)
            print(f'\nlevel_score: {self.level_score}')