import pygame
import time
import math
import random
from random import randrange
from game_board.elements import gfx
import json
import os

TILE_SIZE = 100

# Set tile coordinate for X
x1 = 0
x2 = 100
x3 = 200
x4 = 300
x5 = 400
x6 = 500
# x7 = 600
# x8 = 700
# x9 = 800
# x10 = 900
# x11 = 1000
# x12 = 1100

# Set tile coordinate for Y
y1 = 0
y2 = 100
y3 = 200
y4 = 300
y5 = 400
y6 = 500
# y7 = 600
# y8 = 700
# y9 = 800
# y10 = 900
# y11 = 1000
# y12 = 1100

# Tile coordinates
t1r1 = (x1, y1); t2r1 = (x2, y1); t3r1 = (x3, y1); t4r1 = (x4, y1); t5r1 = (x5, y1); t6r1 = (x6, y1)
# t7r1 = (x7, y1); t8r1 = (x8, y1); t9r1 = (x9, y1); t10r1 = (x10, y1); t11r1 = (x11, y1); t12r1 = (x12, y1)
t1r2 = (x1, y2); t2r2 = (x2, y2); t3r2 = (x3, y2); t4r2 = (x4, y2); t5r2 = (x5, y2); t6r2 = (x6, y2)
# t7r2 = (x7, y2); t8r2 = (x8, y2); t9r2 = (x9, y2); t10r2 = (x10, y2); t11r2 = (x11, y2); t12r2 = (x12, y2)
t1r3 = (x1, y3); t2r3 = (x2, y3); t3r3 = (x3, y3); t4r3 = (x4, y3); t5r3 = (x5, y3); t6r3 = (x6, y3)
# t7r3 = (x7, y3); t8r3 = (x8, y3); t9r3 = (x9, y3); t10r3 = (x10, y3); t11r3 = (x11, y3); t12r3 = (x12, y3)
t1r4 = (x1, y4); t2r4 = (x2, y4); t3r4 = (x3, y4); t4r4 = (x4, y4); t5r4 = (x5, y4); t6r4 = (x6, y4)
# t7r4 = (x7, y4); t8r4 = (x8, y4); t9r4 = (x9, y4); t10r4 = (x10, y4); t11r4 = (x11, y4); t12r4 = (x12, y4)
t1r5 = (x1, y5); t2r5 = (x2, y5); t3r5 = (x3, y5); t4r5 = (x4, y5); t5r5 = (x5, y5); t6r5 = (x6, y5)
# t7r5 = (x7, y5); t8r5 = (x8, y5); t9r5 = (x9, y5); t10r5 = (x10, y5); t11r5 = (x11, y5); t12r5 = (x12, y5)
t1r6 = (x1, y6); t2r6 = (x2, y6); t3r6 = (x3, y6); t4r6 = (x4, y6); t5r6 = (x5, y6); t6r6 = (x6, y6)
# t7r6 = (x7, y6); t8r6 = (x8, y6); t9r6 = (x9, y6); t10r6 = (x10, y6); t11r6 = (x11, y6); t12r6 = (x12, y6)
# t1r7 = (x1, y7); t2r7 = (x2, y7); t3r7 = (x3, y7); t4r7 = (x4, y7); t5r7 = (x5, y7); t6r7 = (x6, y7)
# t7r7 = (x7, y7); t8r7 = (x8, y7); t9r7 = (x9, y7); t10r7 = (x10, y7); t11r7 = (x11, y7); t12r7 = (x12, y7)
# t1r8 = (x1, y8); t2r8 = (x2, y8); t3r8 = (x3, y8); t4r8 = (x4, y8); t5r8 = (x5, y8); t6r8 = (x6, y8)
# t7r8 = (x7, y8); t8r8 = (x8, y8); t9r8 = (x9, y8); t10r8 = (x10, y8); t11r8 = (x11, y8); t12r8 = (x12, y8)
# t1r9 = (x1, y9); t2r9 = (x2, y9); t3r9 = (x3, y9); t4r9 = (x4, y9); t5r9 = (x5, y9); t6r9 = (x6, y9)
# t7r9 = (x7, y9); t8r9 = (x8, y9); t9r9 = (x9, y9); t10r9 = (x10, y9); t11r9 = (x11, y9); t12r9 = (x12, y9)
# t1r10 = (x1, y10); t2r10 = (x2, y10); t3r10 = (x3, y10); t4r10 = (x4, y10); t5r10 = (x5, y10); t6r10 = (x6, y10)
# t7r10 = (x7, y10); t8r10 = (x8, y10); t9r10 = (x9, y10); t10r10 = (x10, y10); t11r10 = (x11, y10); t12r10 = (x12, y10)
# t1r11 = (x1, y11); t2r11 = (x2, y11); t3r11 = (x3, y11); t4r11 = (x4, y11); t5r11 = (x5, y11); t6r11 = (x6, y11)
# t7r11 = (x7, y11); t8r11 = (x8, y11); t9r11 = (x9, y11); t10r11 = (x10, y11); t11r11 = (x11, y11); t12r11 = (x12, y11)
# t1r12 = (x1, y12); t2r12 = (x2, y12); t3r12 = (x3, y12); t4r12 = (x4, y12); t5r12 = (x5, y12); t6r12 = (x6, y12)
# t7r12 = (x7, y12); t8r12 = (x8, y12); t9r12 = (x9, y12); t10r12 = (x10, y12); t11r12 = (x11, y12); t12r12 = (x12, y12)

# Game Board coordinates
tiles = (
    t1r1, t2r1, t3r1, t4r1, t5r1, t6r1, # t7r1, t8r1, t9r1, t10r1, t11r1, t12r1,
    t1r2, t2r2, t3r2, t4r2, t5r2, t6r2, # t7r2, t8r2, t9r2, t10r2, t11r2, t12r2,
    t1r3, t2r3, t3r3, t4r3, t5r3, t6r3, # t7r3, t8r3, t9r3, t10r3, t11r3, t12r3,
    t1r4, t2r4, t3r4, t4r4, t5r4, t6r4, # t7r4, t8r4, t9r4, t10r4, t11r4, t12r4,
    t1r5, t2r5, t3r5, t4r5, t5r5, t6r5, # t7r5, t8r5, t9r5, t10r5, t11r5, t12r5,
    t1r6, t2r6, t3r6, t4r6, t5r6, t6r6#, t7r6, t8r6, t9r6, t10r6, t11r6, t12r6,
    # t1r7, t2r7, t3r7, t4r7, t5r7, t6r7, t7r7, t8r7, t9r7, t10r7, t11r7, t12r7,
    # t1r8, t2r8, t3r8, t4r8, t5r8, t6r8, t7r8, t8r8, t9r8, t10r8, t11r8, t12r8,
    # t1r9, t2r9, t3r9, t4r9, t5r9, t6r9, t7r9, t8r9, t9r9, t10r9, t11r9, t12r9,
    # t1r10, t2r10, t3r10, t4r10, t5r10, t6r10, t7r10, t8r10, t9r10, t10r10, t11r10, t12r10,
    # t1r11, t2r11, t3r11, t4r11, t5r11, t6r11, t7r11, t8r11, t9r11, t10r11, t11r11, t12r11,
    # t1r12, t2r12, t3r12, t4r12, t5r12, t6r12, t7r12, t8r12, t9r12, t10r12, t11r12, t12r12
)

# Set paths for level data
script_dir = os.path.dirname(os.path.abspath(__file__))
tutorial_path = os.path.join(script_dir, 'maps/tutorial_maps.json')
game_path = os.path.join(script_dir, 'maps/game_maps.json')

# Load the tutorial maps
with open(tutorial_path, 'r') as file:
    tutorial_data = json.load(file)

# Load the game maps
with open(game_path, 'r') as file:
    game_data = json.load(file)

# Initiate variables to store levels from the JSON data
tutorial_map = []
game_map =[]
level_map = []

tutorial_title = []
game_title =[]
map_title = []

tutorial_active_boxes = []
game_active_boxes = []
active_boxes = []

tutorial_positions = []
game_positions = []
positions = []

tutorial_player_start = []
game_player_start = []
player_start = []

tutorial_player_direction = []
game_player_direction = []
player_direction = []

tutorial_active_exit = []
game_active_exit = []
active_exit = []

game_score = []
level_score = []

# Add the tutorial maps
for level in tutorial_data['levels']:
    # Create the level map
    tutorial_map.append([tutorial_data['game_board_elements'][item] for row in level['map'] for item in row])
    # Extract other level data
    tutorial_title.append(level['title'])
    tutorial_active_boxes.append(level['active_boxes'])

    # Convert box positions
    box_positions = []
    for pos in level['box_positions']:
            box_positions.append(tuple(int(x * 100) for x in pos))
    tutorial_positions.append(box_positions)

    # Convert player start position
    tutorial_player_start.append(tuple(int(x * 100) for x in level['player_start']))

    tutorial_player_direction.append(level['player_direction'])
    tutorial_active_exit.append(level['exit_active'])

# Add the game maps
for level in game_data['levels']:
    # Create the level map
    game_map.append([game_data['game_board_elements'][item] for row in level['map'] for item in row])

    # Extract other level data
    game_title.append(level['title'])
    game_active_boxes.append(level['active_boxes'])

    # Convert box positions
    box_positions = []
    for pos in level['box_positions']:
            box_positions.append(tuple(int(x * 100) for x in pos))
    game_positions.append(box_positions)

    # Convert player start position
    game_player_start.append(tuple(int(x * 100) for x in level['player_start']))

    game_player_direction.append(level['player_direction'])
    game_active_exit.append(level['exit_active'])
    game_score.append(level['score'])

# Update the level variables
level_map.append(tutorial_map)
level_map.append(game_map)
print(f'level_map: {level_map}')

map_title.append(tutorial_title)
map_title.append(game_title)
print(f'\nmap_title: {map_title}')

active_boxes.append(tutorial_active_boxes)
active_boxes.append(game_active_boxes)
print(f'\nactive_boxes: {active_boxes}')

positions.append(tutorial_positions)
positions.append(game_positions)
print(f'\npositions: {positions}')

player_start.append(tutorial_player_start)
player_start.append(game_player_start)
print(f'\nplayer_start: {player_start}')

player_direction.append(tutorial_player_direction)
player_direction.append(game_player_direction)
print(f'\nplayer_direction: {player_direction}')

active_exit.append(tutorial_active_exit)
active_exit.append(game_active_exit)
print(f'\nactive_exit: {active_exit}')

level_score.append(game_score)
print(f'\nlevel_score: {level_score}')


# CLASS for setup of levels and blitting of game elements
class BoardElements():
    '''BoardElements'''

    def __init__(self):
        '''__init__'''
        print("BoardElements instance created")  # Debug statement

        if not hasattr(self, 'initialized'):
            # Initialization code...
            self.initialized = True

        # Initialize game board size to default values
        self.game_board_x = 600
        self.game_board_y = 600

        # List of map titles
        self.map_title = map_title

        # Variable to keep track of numbers of Levels
        self.no_of_levels = [sum(type(i) == type([]) for i in level_map[0])]
        self.no_of_levels.append(sum(type(i) == type([]) for i in level_map[1]))

        # Variable to tell if Player finished the Game or fell into a Pit
        self.play = True

        # Variable for active/inactive Exit
        self.exit = False

        # Variables for active/inactive Pit
        self.pit1 = True
        self.pit2 = True
        self.pit3 = True
        self.pit4 = True

        # Variables for Box to fill Pit with
        self.in_pit1 = False
        self.in_pit2 = False
        self.in_pit3 = False
        self.in_pit4 = False

        # Lists for creation of Levels
        self.elements = []
        self.box = []
        self.pit_box = []

        # Variable to keep track of Levels
        self.lv = 0

        # Variable to toggle blackout effect
        self.blackout = False

        # Default initial beam angle
        self.current_beam_angle = -1.55

        self.offset_y = 40


    def update_game_board_size(self, level_map):
        '''Update game board size based on level map'''
        # Calculate the dimensions of the game board
        max_x = max(pos[0] for pos in tiles) + TILE_SIZE
        max_y = max(pos[1] for pos in tiles) + TILE_SIZE
        self.game_board_x = max_x
        self.game_board_y = max_y


    # Blit start tile
    def __start__(self, game_board, pos):
        '''__start__'''
        game_board.blit(gfx.start, (pos))


    # Blit floor tile
    def __floor__(self, game_board, pos, i):
        '''__floor__'''
        game_board.blit(gfx.floor[i], (pos))


    # Blit wall tile
    def __wall__(self, game_board, pos):
        '''__wall__'''
        game_board.blit(gfx.wall, (pos))


    # Blit pit1 tile
    def __pit_1__(self, game_board, pos, box):
        '''__pit_1__'''
        # If Pit active
        # - Blit pit1 
        if self.pit1:
            game_board.blit(gfx.pit, (pos))

        # Else
        # - Blit box_n's box_in_pit
        else:
            game_board.blit(gfx.boxes[self.pit_box[box - 1]], (pos))


    # Blit pit2 tile
    def __pit_2__(self, game_board, pos, box):
        '''__pit_2__'''
        # If Pit active
        # - Blit pit2
        if self.pit2:
            game_board.blit(gfx.pit, (pos))

        # Else
        # - Blit box_n's box_in_pit
        else:
            game_board.blit(gfx.boxes[self.pit_box[box - 1]], (pos))


    # Blit pit3 tile
    def __pit_3__(self, game_board, pos, box, i):
        '''__pit_3__'''
        # If Pit active
        # - Blit pit3
        if self.pit3:
            game_board.blit(gfx.pit_crazy[i], (pos))

        # Else
        # - Blit box_n's box_in_pit
        else:
            game_board.blit(gfx.boxes[self.pit_box[box - 1]], (pos))

    # Blit pit4 tile
    def __pit_4__(self, game_board, pos, box, i):
        '''__pit_4__'''
        # If Pit active
        # - Blit pit4
        if self.pit4:
            game_board.blit(gfx.pit_evil[i], (pos))

        # Else
        # - Blit box_n's box_in_pit
        else:
            game_board.blit(gfx.boxes[self.pit_box[box - 1]], (pos))


    # Blit pit_as_wall tile
    def __pit_as_wall__(self, game_board, pos):
        '''__pit_as_wall__'''
        game_board.blit(gfx.pit, (pos))


    # Blit exit tile
    def __exit___(self, game_board, pos):
        '''__exit___'''
        # If Exit is active
        # - Blit exit
        if self.exit:
            game_board.blit(gfx.exit, (pos))

        # Else
        # - Blit no_exit
        else:
            game_board.blit(gfx.no_exit, (pos))


    # Setup tiles for Level n
    def __create_level__(self, game_board, level_map):
        '''__create_level__'''
        # For each coordinate in level_map
        # - Set tiles depending on value of Game Board element
        for i in range(len(level_map)):
            # Genrate random floor and pit tile
            rand_floor = randrange(0, 40)
            rand_pit = randrange(0, 20)

            # Set tile cooresponding to value of Game Board element
            if level_map[i] == 0:
                self.__start__(game_board, tiles[i])

            elif level_map[i] == 1:
                self.__floor__(game_board, tiles[i], rand_floor)

            elif level_map[i] == 2:
                self.__wall__(game_board, tiles[i])

            elif level_map[i] == 3:
                self.__pit_1__(game_board, tiles[i], self.in_pit1)

            elif level_map[i] == 4:
                self.__pit_2__(game_board, tiles[i], self.in_pit2)

            elif level_map[i] == 5:
                self.__pit_3__(game_board, tiles[i], self.in_pit3, rand_pit)

            elif level_map[i] == 6:
                self.__pit_4__(game_board, tiles[i], self.in_pit4, rand_pit)

            elif level_map[i] == 7:
                self.__pit_as_wall__(game_board, tiles[i])

            elif level_map[i] == 8:
                self.__exit___(game_board, tiles[i])

            # Append tile to list of elements for Level n
            self.elements.append([level_map[i], tiles[i], rand_floor, rand_pit])


    # Setup of Boxes graphics
    def __create_boxes__(self, level_boxes):
        '''__create_boxes__'''
        # Generate random Box
        rand = randrange(1, 8, 2)
        # Set graphic for random Box
        rand_box = [rand, level_boxes[rand]]
        # Set box_in_pit to coorespond to Box graphic
        rand_pit_box = (rand - 1)

        # Append graphics for Box to list of Boxes
        self.box.append(rand_box)
        self.pit_box.append(rand_pit_box)

        # Set counter to 1
        r = 1

        # While counter is less than 4
        while r < 4:
            # Generate new random Box
            rand = randrange(1, 8, 2)
            # Set graphic for random Box
            rand_box = [rand, level_boxes[rand]]
            # Set box_in_pit to coorespond to Box graphic
            rand_pit_box = (rand - 1)

            # If Box not in list of Boxes
            # - Set graphics for Box to list of Boxes
            if rand_box not in self.box:
                self.pit_box.append(rand_pit_box)
                self.box.append(rand_box)

                # Increase counter
                r += 1
        
    # Place Boxes, Player, and reset Pits
    def __place_boxes_player_and_reset_pits_and_exit__(self, active_boxes, positions, player_start, active_exit):
        '''__place_boxes_player_and_reset_pits__'''
        # Activate/inactivate box1
        self.box1 = active_boxes[0]
        # Set startpoint for box1
        self.b1x, self.b1y = positions[0]
        print(f"Box 1: Active={self.box1}, Position={(self.b1x, self.b1y)}")  # Debug statement

        # Activate/inactivate box2
        self.box2 = active_boxes[1]
        # Set startpoint for box2
        self.b2x, self.b2y = positions[1]
        print(f"Box 2: Active={self.box2}, Position={(self.b2x, self.b2y)}")  # Debug statement

        # Activate/inactivate box3
        self.box3 = active_boxes[2]
        # Set startpoint for box3
        self.b3x, self.b3y = positions[2]
        print(f"Box 3: Active={self.box3}, Position={(self.b3x, self.b3y)}")  # Debug statement

        # Activate/inactivate box4
        self.box4 = active_boxes[3]
        # Set startpoint for box4
        self.b4x, self.b4y = positions[3]
        print(f"Box 4: Active={self.box4}, Position={(self.b4x, self.b4y)}")  # Debug statement

        # Set startpoint for Player
        self.px, self.py = player_start

        # Activate/inactivate exit
        self.exit = active_exit

        # Set all Pits to active
        self.pit1 = True
        self.pit2 = True
        self.pit3 = True
        self.pit4 = True


    # Blit tiles for Level n
    def blit_level(self, game_board):
        '''blit_level'''
        # For each element in list of Level elements
        # - Blit tiles depending on value of Game Board element
        for el in self.elements:
            # Blit tile corresponding to value of Game Board element
            if el[0] == 0:
                self.__start__(game_board, (el[1][0], el[1][1] + self.offset_y))

            elif el[0] == 1:
                self.__pit_1__(game_board, (el[1][0], el[1][1] + self.offset_y), self.in_pit1)

            elif el[0] == 2:
                self.__pit_2__(game_board, (el[1][0], el[1][1] + self.offset_y), self.in_pit2)

            elif el[0] == 3:
                self.__pit_3__(game_board, (el[1][0], el[1][1] + self.offset_y), self.in_pit3, el[3])

            elif el[0] == 4:
                self.__pit_4__(game_board, (el[1][0], el[1][1] + self.offset_y), self.in_pit4, el[3])

            elif el[0] == 5:
                self.__pit_as_wall__(game_board, (el[1][0], el[1][1] + self.offset_y))

            elif el[0] == 6:
                self.__floor__(game_board, (el[1][0], el[1][1] + self.offset_y), el[2])

            elif el[0] == 7:
                self.__wall__(game_board, (el[1][0], el[1][1] + self.offset_y))

            elif el[0] == 8:
                self.__exit___(game_board, (el[1][0], el[1][1] + self.offset_y))

    # Setup of new Level
    def generate_level(self, game_board, game_state, new_level, option):
        '''generate_level'''
        # If new_level equals True
        # - Reset elements list and setup tiles,
        #   reset box and pit_box list and Pits then place Boxes and Player,
        #   increase level counter, and set new_level to False
        if new_level:
            self.elements = []
            print(f'Length of Level Map: {len(level_map)}')
            self.__create_level__(game_board, level_map[option][self.lv])
            # self.update_game_board_size(level_map[option][self.lv])
            self.box = []
            self.pit_box = []
            self.__create_boxes__(gfx.boxes)

            # Debug statements to check the values of option, self.lv, and positions
            print(f'Option: {option}, Level: {self.lv}')
            print(f'Length of positions: {len(positions)}')
            print(f'Length of positions[option]: {len(positions[option]) if option < len(positions) else "Option out of range"}')

            self.__place_boxes_player_and_reset_pits_and_exit__(active_boxes[option][self.lv],
                                                                positions[option][self.lv],
                                                                player_start[option][self.lv],
                                                                active_exit[option][self.lv])

            game_state.facing_direction = player_direction[option][self.lv]
            print(f"Player Directions: {player_direction[option][self.lv]}")

            if game_state.facing_direction == 'up':
                self.current_beam_angle = math.atan2(-1, 0)
            elif game_state.facing_direction == 'down':
                self.current_beam_angle = math.atan2(1, 0)
            elif game_state.facing_direction == 'left':
                self.current_beam_angle = math.atan2(0, -1)
            elif game_state.facing_direction == 'right':
                self.current_beam_angle = math.atan2(0, 1)

            self.lv += 1

            return False


    # Blit box1
    def blit_box_1(self, game_board, b1_travel, b1_move):
        '''blit_box_1'''
        # If box1 is active
        if self.box1:
            # If movement is Up or Down
            # - Blit box1 in direction of y corresponding of b1_move' value
            if b1_travel == 1 or b1_travel == 2:
                game_board.blit(self.box[0][1], (self.b1x, b1_move + self.offset_y))

            # Else if movement is Left or Right
            # - Blit box1 in direction of x corresponding of b1_move' value
            elif b1_travel == 3 or b1_travel == 4:
                game_board.blit(self.box[0][1], (b1_move, self.b1y + self.offset_y))

            # Else
            # - Blit position of box1
            else:
                game_board.blit(self.box[0][1], (self.b1x, self.b1y + self.offset_y))


    # Blit box2
    def blit_box_2(self, game_board, b2_travel, b2_move):
        '''blit_box2'''
        # If box2 is active
        if self.box2:
            # If movement is Up or Down
            # - Blit box2 in direction of y corresponding of b2_move' value
            if b2_travel == 1 or b2_travel == 2:
                game_board.blit(self.box[1][1], (self.b2x, b2_move + self.offset_y))

            # Else if movement is Left or Right
            # - Blit box2 in direction of x corresponding of b2_move' value
            elif b2_travel == 3 or b2_travel == 4:
                game_board.blit(self.box[1][1], (b2_move, self.b2y + self.offset_y))

            # Else
            # - Blit position of box2
            else:
                game_board.blit(self.box[1][1], (self.b2x, self.b2y + self.offset_y))



    # Blit box3
    def blit_box_3(self, game_board, b3_travel, b3_move):
        '''blit_box3'''
        # If box3 is active
        if self.box3:
            # If movement is Up or Down
            # - Blit box3 in direction of y corresponding of b3_move' value
            if b3_travel == 1 or b3_travel == 2:
                game_board.blit(self.box[2][1], (self.b3x, b3_move + self.offset_y))

            # Else if movement is Left or Right
            # - Blit box3 in direction of x corresponding of b3_move' value
            elif b3_travel == 3 or b3_travel == 4:
                game_board.blit(self.box[2][1], (b3_move, self.b3y + self.offset_y))

            # Else
            # - Blit position of box3
            else:
                game_board.blit(self.box[2][1], (self.b3x, self.b3y + self.offset_y))



    # Blit box4
    def blit_box_4(self, game_board, b4_travel, b4_move):
        '''blit_box4'''
        # If box4 is active
        if self.box4:
            # If movement is Up or Down
            # - Blit box4 in direction of y corresponding of b4_move' value
            if b4_travel == 1 or b4_travel == 2:
                game_board.blit(self.box[3][1], (self.b4x, b4_move + self.offset_y))

            # Else if movement is Left or Right
            # - Blit box4 in direction of x corresponding of b4_move' value
            elif b4_travel == 3 or b4_travel == 4:
                game_board.blit(self.box[3][1], (b4_move, self.b4y + self.offset_y))

            # Else
            # - Blit position of box4
            else:
                game_board.blit(self.box[3][1], (self.b4x, self.b4y + self.offset_y))



    # Blit player
    def blit_player(self, game_board, game_state, p_move):
        '''blit_player'''
        # If play equals True
        if self.play and game_state.normal_movement:
            # If movement is Up
            # - Blit player in direction of y corresponding of p_move' value
            if game_state.travel == 1 and not game_state.is_pulling:
                game_board.blit(gfx.player_up, (self.px, p_move + self.offset_y))

            # Else iff movement is Down
            # - Blit player in direction of y corresponding of p_move' value
            elif game_state.travel == 2 and not game_state.is_pulling:
                game_board.blit(gfx.player_down, (self.px, p_move + self.offset_y))

            # Else iff movement is Left
            # - Blit player in direction of x corresponding of p_move' value
            elif game_state.travel == 3 and not game_state.is_pulling:
                game_board.blit(gfx.player_left, (p_move, self.py + self.offset_y))

            # Else iff movement is Right
            # - Blit player in direction of x corresponding of p_move' value
            elif game_state.travel == 4 and not game_state.is_pulling:
                game_board.blit(gfx.player_right, (p_move, self.py + self.offset_y))

            # Else
            # - Blit position of player
            else:
                if game_state.lights_out:
                    if game_state.facing_direction == 'up':
                        game_board.blit(gfx.player_up, (self.px, self.py + self.offset_y))
                    elif game_state.facing_direction == 'down':
                        game_board.blit(gfx.player_down, (self.px, self.py + self.offset_y))
                    elif game_state.facing_direction == 'left':
                        game_board.blit(gfx.player_left, (self.px, self.py + self.offset_y))
                    elif game_state.facing_direction == 'right':
                        game_board.blit(gfx.player_right, (self.px, self.py + self.offset_y))
                else:
                    game_board.blit(gfx.player, (self.px, self.py + self.offset_y))
        else:
            if game_state.facing_direction == 'up':
                game_board.blit(gfx.player_up, (self.px, self.py + self.offset_y))
            elif game_state.facing_direction == 'down':
                game_board.blit(gfx.player_down, (self.px, self.py + self.offset_y))
            elif game_state.facing_direction == 'left':
                game_board.blit(gfx.player_left, (self.px, self.py + self.offset_y))
            elif game_state.facing_direction == 'right':
                game_board.blit(gfx.player_right, (self.px, self.py + self.offset_y))



    # Blit Game Level score
    def blit_stars(self, game_board, game_state):
        '''blit_stars'''
        # Set least movements for three stars
        self.top_score = level_score[0][game_state.current_level]

        # Blit stars depending on number of moves
        if game_state.moves <= self.top_score:
            # Blit 3 highlighted Stars
            game_board.blit(gfx.stars[3], (186, 155 - self.offset_y))

        elif game_state.moves > self.top_score and game_state.moves <= (self.top_score + 2):
            # Blit 2 highlighted Stars
            game_board.blit(gfx.stars[2], (186, 155 - self.offset_y))

        else:
            # Blit 1 highlighted Star
            game_board.blit(gfx.stars[1], (186, 155 - self.offset_y))

        # Update all changes to display
        pygame.display.update()
        # Pause for 3 seconds to show Stars
        time.sleep(3)


    def __lerp_angle__(self, current, target, factor):
        """
        Linearly interpolate between two angles (in radians) with a given factor,
        handling wrap-around.
        """
        diff = (target - current + math.pi) % (2 * math.pi) - math.pi
        return current + diff * factor

    def apply_blackout(self, game_board, game_state):
        '''
        Apply blackout with a flashlight beam effect that smoothly rotates to
        a new direction before the player moves and has a rounded outer edge.
        '''
        if self.blackout:
            # Create a mask for the game board with per-pixel alpha.
            mask = pygame.Surface((self.game_board_x, self.game_board_y + self.offset_y), pygame.SRCALPHA)
            # Start with nearly full opacity
            mask.fill((0, 0, 0, 249))  # Semi-transparent black overlay.

            # Flashlight parameters.
            beam_length = int(2 * TILE_SIZE)        # How far the beam extends.
            beam_angle = math.radians(60)           # Total angular width of the beam (60°)

            # Determine the player's center.
            player_center_x = self.px + (TILE_SIZE // 2)
            player_center_y = self.py + (TILE_SIZE // 2) + self.offset_y  # Add the offset here
            player_center = (player_center_x, player_center_y)

            target_angle = None
            # Define a mapping of directions to their corresponding angles
            direction_to_angle = {
                'up': math.atan2(-1, 0),
                'down': math.atan2(1, 0),
                'left': math.atan2(0, -1),
                'right': math.atan2(0, 1)
            }

            # Determine the target angle based on the game state
            if game_state.is_pulling:
                # Map travel directions to opposite angles when pulling
                travel_to_opposite = {1: 'down', 2: 'up', 3: 'right', 4: 'left'}
                if game_state.direction in travel_to_opposite:
                    target_angle = direction_to_angle[travel_to_opposite[game_state.direction]]
            elif game_state.is_searching:
                # Map search directions to angles
                search_to_direction = {1: 'up', 2: 'down', 3: 'left', 4: 'right'}
                if game_state.search in search_to_direction:
                    target_angle = direction_to_angle[search_to_direction[game_state.search]]
            else:
                if game_state.normal_movement:
                    # Map travel directions to angles when normal_movement is True
                    travel_to_direction = {1: 'up', 2: 'down', 3: 'left', 4: 'right'}
                    if game_state.travel in travel_to_direction:
                        target_angle = direction_to_angle[travel_to_direction[game_state.travel]]
                else:
                    # Use the facing direction to determine the angle
                    target_angle = direction_to_angle[game_state.facing_direction]

            smoothing_factor = game_state.search_speed  # 1 is fastest, lower is slower rotation/not full rotation in one go.
            if target_angle is not None:
                self.current_beam_angle = self.__lerp_angle__(self.current_beam_angle, target_angle, smoothing_factor)
            direction_angle = self.current_beam_angle

            # Instead of one polygon with a sharp boundary,
            # build up a series of translucent slices for a gradient edge.
            # The inner slices will be fully transparent out to some fraction of the beam_length,
            # and the outer slices will gradually blend.
            slices = 60  # Number of slices for transitioning the gradient.
            inner_ratio = 0.2  # Fraction of the beam that is fully transparent (hard cutout).
            # Loop over slices from inner to outer edge.
            for i in range(slices):
                # Compute a normalized value [0,1] for this slice.
                slice_norm = i / float(slices - 1)
                # Determine the start and end distances of this slice.
                # Slices start at inner_ratio * beam_length and extend to full beam_length.
                slice_start = inner_ratio * beam_length + slice_norm * (beam_length * (1 - inner_ratio))
                slice_end = inner_ratio * beam_length + (slice_norm + 1.0/slices) * (beam_length * (1 - inner_ratio))
                # Compute the transparency based on slice position.
                # Slices closer to the inner area are more transparent (alpha=0)
                # outer slices are less transparent.
                alpha = int(255 * slice_norm)
                # Create a polygon for this slice. Its angular width is the same as the beam_angle,
                # but we draw an annular arc from slice_start to slice_end.
                steps = 60  # Smoother curve for this slice.
                arc_points = []
                left_edge_angle = direction_angle - (beam_angle / 2)
                right_edge_angle = direction_angle + (beam_angle / 2)
                angle_step = (right_edge_angle - left_edge_angle) / steps
                # Create points for the outer boundary of the slice.
                outer_points = []
                for j in range(steps + 1):
                    angle = left_edge_angle + j * angle_step
                    x = player_center_x + slice_end * math.cos(angle)
                    y = player_center_y + slice_end * math.sin(angle)
                    outer_points.append((x, y))
                # Create points for the inner boundary (in reverse order so polygon is closed).
                inner_points = []
                for j in range(steps + 1):
                    angle = right_edge_angle - j * angle_step
                    x = player_center_x + slice_start * math.cos(angle)
                    y = player_center_y + slice_start * math.sin(angle)
                    inner_points.append((x, y))
                # Combine into one polygon.
                polygon_points = outer_points + inner_points
                # Draw this polygon onto the mask with full transparency.
                # We subtract from the base overlay by drawing a polygon with low alpha.
                # Here, the color (0,0,0,alpha) means we are “erasing” that portion of the darkness.
                pygame.draw.polygon(mask, (0, 0, 0, alpha), polygon_points)

            # You can also draw a central circle if you want the beam to be more rounded at the origin.
            inner_circle_radius = int(inner_ratio * beam_length)
            pygame.draw.circle(mask, (0, 0, 0, 0), player_center, inner_circle_radius)
            # Finally, blit the mask onto the game board.
            game_board.blit(mask, (0, 0))

    def flicker_effect(self, game_board, game_state, board, screen):
        if self.blackout:
            screen.fill((30, 30, 30))
            if game_state.game == True:
                # Status bar
                font = pygame.font.SysFont('Lucida Console', 24)  # Font for UI text
                moves_text = font.render(f'Moves: {game_state.moves}', True, (255, 255, 255))
                total_moves_text = font.render(f'Total Moves: {game_state.total_moves}', True, (255, 255, 255))
                lives_text = font.render(f'Lives: {game_state.lives}', True, (255, 255, 255))
            else:
                # Tutorial bar
                tutorial_font = pygame.font.SysFont('Lucida Console', 12)  # Font for tutorial text
                tutorial_text = tutorial_font.render(f'{board.map_title[0][game_state.current_level]}', True, (255, 255, 255)) # Set window bar

            bar_rect = pygame.Rect(0, board.offset_y - board.offset_y, screen.get_width(), board.offset_y)

            # Define the base pattern of on/off durations in seconds
            base_pattern = [
                (0.8, 0.2),
                (0.15, 0.05),
                (0.3, 0.05),
                (0.035, 0.05),
                (0.015, 0.01)
            ]

            first_iteration = True  # Flag to track the first iteration

            # Loop through the base pattern and apply random variations
            for on_time, off_time in base_pattern:
                # Apply slight random variations to the on and off times
                on_time = max(0.015, on_time + random.uniform(-0.05, 0.05))
                off_time = max(0.01, off_time + random.uniform(-0.05, 0.05))

                if first_iteration:
                    # First iteration: no mask
                    game_board.fill((30, 30, 30))
                    self.blit_level(game_board)
                    self.blit_box_1(game_board, 0, 0)
                    self.blit_box_2(game_board, 0, 0)
                    self.blit_box_3(game_board, 0, 0)
                    self.blit_box_4(game_board, 0, 0)
                    self.blit_player(game_board, game_state, 0)  # Assuming 0 as a placeholder for p_move
                    # Render status bar
                    if game_state.game == True:
                        pygame.display.set_caption(f'Escape the Werehouse! - {board.map_title[1][game_state.current_level]}')
                        pygame.draw.rect(screen, (50, 50, 50), bar_rect)  # Dark gray color for the bar
                        screen.blit(moves_text, (10, 10))
                        screen.blit(total_moves_text, (200, 10))
                        screen.blit(lives_text, (480, 10))
                        pygame.display.update()
                    else:
                        pygame.display.set_caption(f'Escape the Werehouse! - Tutorial {game_state.current_level + 1}')
                        pygame.draw.rect(screen, (50, 50, 50), bar_rect)  # Dark gray color for the bar
                        screen.blit(tutorial_text, (15, 15))
                    time.sleep(on_time)
                    first_iteration = False
                else:
                    # Apply the on time with a mask of lower opacity
                    mask = pygame.Surface((self.game_board_x, self.game_board_y + self.offset_y), pygame.SRCALPHA)
                    mask.fill((0, 0, 0, 76))  # Lower opacity
                    game_board.fill((30, 30, 30))
                    self.blit_level(game_board)
                    self.blit_box_1(game_board, 0, 0)
                    self.blit_box_2(game_board, 0, 0)
                    self.blit_box_3(game_board, 0, 0)
                    self.blit_box_4(game_board, 0, 0)
                    self.blit_player(game_board, game_state, 0)  # Assuming 0 as a placeholder for p_move
                    game_board.blit(mask, (0, 0))
                    # Render status bar
                    if game_state.game == True:
                        pygame.display.set_caption(f'Escape the Werehouse! - {board.map_title[1][game_state.current_level]}')
                        pygame.draw.rect(screen, (50, 50, 50), bar_rect)  # Dark gray color for the bar
                        screen.blit(moves_text, (10, 10))
                        screen.blit(total_moves_text, (200, 10))
                        screen.blit(lives_text, (480, 10))
                        pygame.display.update()
                    else:
                        pygame.display.set_caption(f'Escape the Werehouse! - Tutorial {game_state.current_level + 1}')
                        pygame.draw.rect(screen, (50, 50, 50), bar_rect)  # Dark gray color for the bar
                        screen.blit(tutorial_text, (15, 15))
                    pygame.display.update()
                    time.sleep(on_time)

                # Apply the off time with a mask of higher opacity
                mask = pygame.Surface((self.game_board_x, self.game_board_y + self.offset_y), pygame.SRCALPHA)
                mask.fill((0, 0, 0, 249))  # Higher opacity
                game_board.fill((30, 30, 30))
                self.blit_level(game_board)
                self.blit_box_1(game_board, 0, 0)
                self.blit_box_2(game_board, 0, 0)
                self.blit_box_3(game_board, 0, 0)
                self.blit_box_4(game_board, 0, 0)
                game_board.blit(mask, (0, 0))
                # Render status bar
                if game_state.game == True:
                    pygame.display.set_caption(f'Escape the Werehouse! - {board.map_title[1][game_state.current_level]}')
                    pygame.draw.rect(screen, (50, 50, 50), bar_rect)  # Dark gray color for the bar
                    screen.blit(moves_text, (10, 10))
                    screen.blit(total_moves_text, (200, 10))
                    screen.blit(lives_text, (480, 10))
                    pygame.display.update()
                else:
                    pygame.display.set_caption(f'Escape the Werehouse! - Tutorial {game_state.current_level + 1}')
                    pygame.draw.rect(screen, (50, 50, 50), bar_rect)  # Dark gray color for the bar
                    screen.blit(tutorial_text, (15, 15))
                pygame.display.update()
                time.sleep(off_time)

            # Add a delay before turning on the flashlight beam
            flashligtht_on_delay = 0.7 + random.uniform(-0.2, 0.3)
            time.sleep(flashligtht_on_delay)

            # Turn on the flashlight beam
            self.apply_blackout(game_board, game_state)
            pygame.display.update()

    def fade_out(self, game_state, screen, width, height):
        """Create a fade-out effect."""
        fade = pygame.Surface((width, height))
        fade.fill((10, 10, 10))

        if game_state.lights_out:
            delay = 120
            start_alpha = 20
            end_alpha = 180
            inc_alpha = 10
            init = 300
        else:
            delay = 40
            start_alpha = 0
            end_alpha = 180
            inc_alpha = 10
            init = 200

        for alpha in range(start_alpha, end_alpha, inc_alpha):  # Increase alpha gradually
            fade.set_alpha(alpha)
            screen.blit(fade, (0, 0))
            pygame.display.update()
            if alpha == 0:
                pygame.time.wait(init)
            pygame.time.wait(delay)  # Small delay to control the speed of the fade

        if game_state.player_in_pit:
            # Render the warning text
            font = pygame.font.SysFont('Arial Black', 42)
            warning_text = font.render("Watch out for those pits!", True, (220, 0, 10))  # Red text
            warning_text_rect = warning_text.get_rect(center=(width // 2, 200))

            # Blit the warning text
            screen.blit(warning_text, warning_text_rect)
            pygame.display.update()

            # Wait for a moment to let the player read the warning
            pygame.time.wait(1500)  # Wait for 1.5 seconds

    def fade_in(self, screen, width, height, board, game_state):
        """Create a fade-in effect while re-blitting the game board and player."""
        if game_state.game == True:
            # Status bar
            font = pygame.font.SysFont('Lucida Console', 24)  # Font for UI text
            moves_text = font.render(f'Moves: {game_state.moves}', True, (255, 255, 255))
            total_moves_text = font.render(f'Total Moves: {game_state.total_moves}', True, (255, 255, 255))
            lives_text = font.render(f'Lives: {game_state.lives}', True, (255, 255, 255))
        else:
            # Tutorial bar
            tutorial_font = pygame.font.SysFont('Lucida Console', 12)  # Font for tutorial text
            tutorial_text = tutorial_font.render(f'{board.map_title[0][game_state.current_level]}', True, (255, 255, 255)) # Set window bar

        bar_rect = pygame.Rect(0, board.offset_y - board.offset_y, screen.get_width(), board.offset_y)

        fade = pygame.Surface((width, height))
        fade.fill((10, 10, 10))

        # Decrease alpha gradually from 255 (opaque) to 0 (transparent)
        for alpha in range(255, 0, -10):
            # Re-blit the game state each frame
            screen.fill((30, 30, 30))
            board.blit_level(screen)
            board.blit_box_1(screen, 0, 0)
            board.blit_box_2(screen, 0, 0)
            board.blit_box_3(screen, 0, 0)
            board.blit_box_4(screen, 0, 0)
            board.blit_player(screen, game_state, 0)

            if game_state.game == True:
                pygame.display.set_caption(f'Escape the Werehouse! - {board.map_title[1][game_state.current_level]}')
                pygame.draw.rect(screen, (50, 50, 50), bar_rect)  # Dark gray color for the bar
                screen.blit(moves_text, (10, 10))
                screen.blit(total_moves_text, (200, 10))
                screen.blit(lives_text, (480, 10))
                pygame.display.update()
            else:
                pygame.display.set_caption(f'Escape the Werehouse! - Tutorial {game_state.current_level + 1}')
                pygame.draw.rect(screen, (50, 50, 50), bar_rect)  # Dark gray color for the bar
                screen.blit(tutorial_text, (15, 15))

            fade.set_alpha(alpha)
            screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.wait(30)
        return