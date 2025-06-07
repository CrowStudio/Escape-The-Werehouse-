import pygame
import json
import math
import os
import random
from random import randrange
import time
from game_board.elements import gfx

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
tutorial_path = os.path.join(script_dir, 'stages/level_maps/tutorial_maps.json')
maps_stage_1_path = os.path.join(script_dir, 'stages\level_maps\maps_stage_1.json')

# Load the tutorial maps
with open(tutorial_path, 'r') as file:
    tutorial_data = json.load(file)

# Load the game maps
with open(maps_stage_1_path, 'r') as file:
    stage_1_level_data = json.load(file)

# Initiate variables to store levels from the JSON data
tutorial_maps = []
stage_maps =[]
level_maps = []

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
    tutorial_maps.append([tutorial_data['game_board_elements'][item] for row in level['map'] for item in row])
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
for level in stage_1_level_data['levels']:
    # Create the level map
    stage_maps.append([stage_1_level_data['game_board_elements'][item] for row in level['map'] for item in row])

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
level_maps.append(tutorial_maps)
level_maps.append(stage_maps)
print(f'level_maps: {level_maps}')

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

        # Initialize game board size to default values
        self.width = 600
        self.height = 600
        self.height_offset = 40
        self.game_board = pygame.display.set_mode((self.width, (self.height + self.height_offset)))  # Set the screen size to 600x640

        # List of map titles
        self.map_title = map_title

        # Variable to keep track of numbers of Levels
        self.no_of_levels = [sum(type(i) == type([]) for i in level_maps[0])]
        self.no_of_levels.append(sum(type(i) == type([]) for i in level_maps[1]))

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
        self.index = 0

        # Default initial beam angle
        self.current_beam_angle = -1.55


    def update_game_board_size(self, level_maps):
        '''Update game board size based on level map'''
        # Calculate the dimensions of the game board
        max_x = max(pos[0] for pos in tiles) + TILE_SIZE
        max_y = max(pos[1] for pos in tiles) + TILE_SIZE
        self.width = max_x
        self.height = max_y


    # Blit start tile
    def __start__(self, pos):
        self.game_board.blit(gfx.start, pos)

    # Blit floor tile
    def __floor__(self, pos, i):
        self.game_board.blit(gfx.floor[i], pos)

    # Blit wall tile
    def __wall__(self, pos):
        self.game_board.blit(gfx.wall, pos)

    # Blit pit1 tile
    def __pit_1__(self, pos, box):
        self._pit_common(pos, box, pit_index=1, eye_index=None)

    # Blit pit2 tile
    def __pit_2__(self, pos, box):
        self._pit_common(pos, box, pit_index=2, eye_index=None)

    # Blit pit3 tile
    def __pit_3__(self, pos, box, i):
        self._pit_common(pos, box, pit_index=3, eye_index=i)

    # Blit pit4 tile
    def __pit_4__(self, pos, box, i):
        self._pit_common(pos, box, pit_index=4, eye_index=i)

    # Blit pit_as_wall tile
    def __pit_as_wall__(self, pos):
        # identical to a “dead” pit
        self.game_board.blit(gfx.pit, pos)

    # Blit exit tile
    def __exit___(self, pos):
        # If Exit is active
        # - Blit exit
        if self.exit:
            self.game_board.blit(gfx.exit, pos)
        # Else
        # - Blit no_exit
        else:
            self.game_board.blit(gfx.no_exit, pos)

    # Internal helper for pits 1-4
    def _pit_common(self, pos, box, pit_index, eye_index):
        active = getattr(self, f'pit{pit_index}')
        if active:
            # Pick correct pit graphic
            if pit_index in (1, 2):
                surf = gfx.pit
            elif pit_index == 3:
                surf = gfx.pit_crazy[eye_index]
            else:
                surf = gfx.pit_evil[eye_index]
            self.game_board.blit(surf, pos)
        else:
            # Blit box in pit
            bx = self.pit_box[box - 1]
            self.game_board.blit(gfx.boxes[bx], pos)


    # Setup tiles for level n
    def __create_level__(self, level_map):
        self.elements.clear()
        # For each coordinate in level_maps
        # - Set tiles depending on value of the level element
        for i, element in enumerate(level_map):
            pos        = tiles[i]
            rand_floor = randrange(0, 40)
            rand_pit   = randrange(0, 20)
            # store exactly the tuple [element, pos, rand_floor, rand_pit]
            self.elements.append([element, pos, rand_floor, rand_pit])


    # Setup of Boxes graphics
    def __create_boxes__(self, level_boxes):
        """
        Pick four random odd indices in the range 1..7 **with replacement**.
        This will genuinely randomize each of the 4 graphics, possibly with repeats.
        """
        self.box.clear()
        self.pit_box.clear()

        count = 0
        while count < 4:
            # Generate new random Box
            rand = randrange(1, 8, 2)  # picks 1,3,5,7 at random
            self.box.append([rand, level_boxes[rand]])
            # Set box_in_pit to coorespond to Box graphic
            self.pit_box.append(rand - 1)
            count += 1


    # Place Boxes, Player, reset Pits, and Exit
    def __place_boxes_player_and_reset_pits_and_exit__(self,
                active_boxes, positions, player_start, active_exit):
        self.box1, (self.b1x, self.b1y) = active_boxes[0], positions[0]
        self.box2, (self.b2x, self.b2y) = active_boxes[1], positions[1]
        self.box3, (self.b3x, self.b3y) = active_boxes[2], positions[2]
        self.box4, (self.b4x, self.b4y) = active_boxes[3], positions[3]

        self.px, self.py = player_start
        self.pit1 = self.pit2 = self.pit3 = self.pit4 = True
        self.exit = active_exit


    # Blit tiles for level n with the help of dispatch
    def blit_level(self):
        # dispatch: tile_code → (method, args...)
        dispatch = {
            0: (self.__start__,         ()),
            1: (self.__pit_1__,         ('in_pit1', None)),
            2: (self.__pit_2__,         ('in_pit2', None)),
            3: (self.__pit_3__,         ('in_pit3', 'eyes')),
            4: (self.__pit_4__,         ('in_pit4', 'eyes')),
            5: (self.__pit_as_wall__,   ()),
            6: (self.__floor__,         ('floor',)),
            7: (self.__wall__,          ()),
            8: (self.__exit___,         ())
        }

        for element, pos, rand_floor, rand_pit in self.elements:
            method, args = dispatch[element]
            x, y = pos[0], pos[1] + self.height_offset

            # unwrap args tuple into the correct call
            if not args:
                method((x, y))
            elif args == ('floor',):
                method((x, y), rand_floor)
            elif args == ('in_pit1', None):
                method((x, y), self.in_pit1)
            elif args == ('in_pit2', None):
                method((x, y), self.in_pit2)
            elif args == ('in_pit3', 'eyes'):
                method((x, y), self.in_pit3, rand_pit)
            elif args == ('in_pit4', 'eyes'):
                method((x, y), self.in_pit4, rand_pit)


    # Setup of new level
    def generate_level(self, game_state, new_level, option):
        if not new_level:
            return True

        # Reset element table & create new
        self.__create_level__(level_maps[option][self.index])

        # Reset Boxes & Pits
        self.__create_boxes__(gfx.boxes)

        # Debug prints
        print(f'Option={option}, Level={self.index}')
        print(f'positions count={len(positions[option])}')

        # Place boxes, rest Player and Exit
        self.__place_boxes_player_and_reset_pits_and_exit__(
            active_boxes[option][self.index],
            positions[option][self.index],
            player_start[option][self.index],
            active_exit[option][self.index]
        )

        # Facing & beam angle
        game_state.facing_direction = player_direction[option][self.index]
        fd = game_state.facing_direction
        if   fd == 'up':    ang = math.atan2(-1, 0)
        elif fd == 'down':  ang = math.atan2( 1, 0)
        elif fd == 'left':  ang = math.atan2( 0, -1)
        else:               ang = math.atan2( 0, 1)
        self.current_beam_angle = ang

        self.index += 1
        return False


    # Generic box blitter
    def blit_box(self, index, travel, move):
        """
        Generic blitter for box at self.box[index],
        ground‐truth positions self.b{n}x/y, active flag self.box{n}.
        """
        active = getattr(self, f'box{index + 1}')
        if not active:
            return

        # Pick sprite
        sprite = self.box[index][1]

        # Movement in y axis
        if travel in (1, 2):
            x = getattr(self, f'b{index + 1}x')
            y = move + self.height_offset

        # Movement in x axis
        elif travel in (3, 4):
            x = move
            y = getattr(self, f'b{index + 1}y') + self.height_offset

        # No movement
        else:
            x = getattr(self, f'b{index + 1}x')
            y = getattr(self, f'b{index + 1}y') + self.height_offset

        self.game_board.blit(sprite, (x, y))


    # Blit Boxes 1-4 with the help of the generic blit_box()
    def blit_box_1(self, b1_travel, b1_move):
        '''blit_box_1'''
        self.blit_box(0, b1_travel, b1_move)

    def blit_box_2(self, b2_travel, b2_move):
        '''blit_box2'''
        self.blit_box(1, b2_travel, b2_move)

    def blit_box_3(self, b3_travel, b3_move):
        '''blit_box3'''
        self.blit_box(2, b3_travel, b3_move)

    def blit_box_4(self, b4_travel, b4_move):
        '''blit_box4'''
        self.blit_box(3, b4_travel, b4_move)


    # Blit player
    def blit_player(self, game_state, p_move):
        '''blit_player'''
        # If lights out or Up is moving direction
        # - Blit facing direction of player
        if game_state.lights_out or not game_state.normal_movement:
            if game_state.facing_direction == 'up':
                self.game_board.blit(gfx.player_up, (self.px, self.py + self.height_offset))
            elif game_state.facing_direction == 'down':
                self.game_board.blit(gfx.player_down, (self.px, self.py + self.height_offset))
            elif game_state.facing_direction == 'left':
                self.game_board.blit(gfx.player_left, (self.px, self.py + self.height_offset))
            elif game_state.facing_direction == 'right':
                self.game_board.blit(gfx.player_right, (self.px, self.py + self.height_offset))

        else:
            # If movement is Up
            # - Blit player in direction of y corresponding of p_move' value
            if game_state.travel == 1 and not game_state.is_pulling:
                self.game_board.blit(gfx.player_up, (self.px, p_move + self.height_offset))

            # Else iff movement is Down
            # - Blit player in direction of y corresponding of p_move' value
            elif game_state.travel == 2 and not game_state.is_pulling:
                self.game_board.blit(gfx.player_down, (self.px, p_move + self.height_offset))

            # Else iff movement is Left
            # - Blit player in direction of x corresponding of p_move' value
            elif game_state.travel == 3 and not game_state.is_pulling:
                self.game_board.blit(gfx.player_left, (p_move, self.py + self.height_offset))

            # Else iff movement is Right
            # - Blit player in direction of x corresponding of p_move' value
            elif game_state.travel == 4 and not game_state.is_pulling:
                self.game_board.blit(gfx.player_right, (p_move, self.py + self.height_offset))

            # - Blit no player with no travel
            else:
                self.game_board.blit(gfx.player, (self.px, self.py + self.height_offset))


    # Blit level score (stars), identical logic but shorter
    def blit_stars(self, game_state):
        '''blit_stars'''
        least_moves = level_score[0][game_state.current_level]

        # Blit stars depending on number of moves
        if game_state.moves <= least_moves:
            # Set 3 highlighted Stars
            count = 3
        elif game_state.moves <= least_moves + 2:
            # Set 2 highlighted Stars
            count = 2
        else:
            # Set 1 highlighted Star
            count = 1

        # Blit numbers of highlighted Stars
        self.game_board.blit(gfx.stars[count], (186, 155 - self.height_offset))
        pygame.display.update()
        # Pause for 2 seconds to show Stars
        time.sleep(2)


    def __lerp_angle__(self, current, target, factor):
        """
        Linearly interpolate between two angles (in radians) with a given factor,
        handling wrap-around.
        """
        diff = (target - current + math.pi) % (2 * math.pi) - math.pi
        return current + diff * factor

    def apply_blackout(self, game_state):
        '''
        Apply blackout with a flashlight beam effect that smoothly rotates to
        a new direction before the player moves and has a rounded outer edge.
        '''
        # Create a mask for the game board with per-pixel alpha.
        mask = pygame.Surface((self.width, self.height + self.height_offset), pygame.SRCALPHA)
        # Start with nearly full opacity
        mask.fill((0, 0, 0, 249))  # Semi-transparent black overlay.

        # Flashlight parameters.
        beam_length = int(2 * TILE_SIZE)        # How far the beam extends.
        beam_angle = math.radians(60)           # Total angular width of the beam (60°)

        # Determine the player's center.
        player_center_x = self.px + (TILE_SIZE // 2)
        player_center_y = self.py + (TILE_SIZE // 2) + self.height_offset  # Add the offset here
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
        self.game_board.blit(mask, (0, 0))

    def flicker_effect(self, game_state):
        self.game_board.fill((30, 30, 30))

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
                self.__blit_level_elements__(game_state)

                if game_state.game == True:
                    # Render Status bar
                    self.__render_status_bar__(game_state)
                else:
                    # Render Tutorial bar
                    self. __render_tutorial_bar__(game_state)
                pygame.display.update()
                time.sleep(on_time)
                first_iteration = False
            else:
                # Apply the on time with a mask of lower opacity
                mask = pygame.Surface((self.width, self.height + self.height_offset), pygame.SRCALPHA)
                mask.fill((0, 0, 0, 76))  # Lower opacity
                self.__blit_level_elements__(game_state)
                self.game_board.blit(mask, (0, 0))

                if game_state.game == True:
                    # Render Status bar
                    self.__render_status_bar__(game_state)
                else:
                    # Render Tutorial bar
                    self. __render_tutorial_bar__(game_state)
                pygame.display.update()
                time.sleep(on_time)

            # Apply the off time with a mask of higher opacity
            mask = pygame.Surface((self.width, self.height + self.height_offset), pygame.SRCALPHA)
            mask.fill((0, 0, 0, 249))  # Higher opacity
            self.game_board.fill((30, 30, 30))
            self.blit_level()
            self.blit_box_1(0, 0)
            self.blit_box_2(0, 0)
            self.blit_box_3(0, 0)
            self.blit_box_4(0, 0)
            self.game_board.blit(mask, (0, 0))

            if game_state.game == True:
                # render Status bar
                self.__render_status_bar__(game_state)
            else:
                # render Tutorial bar
                self. __render_tutorial_bar__(game_state)
            pygame.display.update()
            time.sleep(off_time)

        # Add a delay before turning on the flashlight beam
        flashligtht_on_delay = 0.7 + random.uniform(-0.2, 0.3)
        time.sleep(flashligtht_on_delay)

        # Turn on the flashlight beam
        self.apply_blackout(game_state)
        pygame.display.update()

    def fade_out(self, game_state):
        """Create a fade-out effect."""
        fade = pygame.Surface((self.width, (self.height + self.height_offset)))
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
            self.game_board.blit(fade, (0, 0))
            pygame.display.update()
            if alpha == 0:
                pygame.time.wait(init)
            pygame.time.wait(delay)  # Small delay to control the speed of the fade

        if game_state.player_in_pit:
            # Render the warning text
            font = pygame.font.SysFont('Arial Black', 42)
            warning_text = font.render("Watch out for those pits!", True, (220, 0, 10))  # Red text
            warning_text_rect = warning_text.get_rect(center=(self.width // 2, 200))

            # Blit the warning text
            self.game_board.blit(warning_text, warning_text_rect)
            pygame.display.update()

            # Wait for a moment to let the player read the warning
            pygame.time.wait(1500)  # Wait for 1.5 seconds

    def fade_in(self, game_state):
        """Create a fade-in effect while re-blitting the game board and player."""
        fade = pygame.Surface((self.width, (self.height + self.height_offset)))
        fade.fill((10, 10, 10))

        # Decrease alpha gradually from 255 (opaque) to 0 (transparent)
        for alpha in range(255, 0, -10):
            # Re-blit the game state each frame
            self.__blit_level_elements__(game_state)

            if game_state.game == True:
                # Render Status bar
                self.__render_status_bar__(game_state)
            else:
                # Render Tutorial bar
                self.__render_tutorial_bar__(game_state)
            fade.set_alpha(alpha)
            self.game_board.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.wait(30)
        return

    def __render_status_bar__(self, game_state):
        # Status bar
        font = pygame.font.SysFont('Lucida Console', 24)  # Font for UI text
        moves_text = font.render(f'Moves: {game_state.moves}', True, (255, 255, 255))
        total_moves_text = font.render(f'Total Moves: {game_state.total_moves}', True, (255, 255, 255))
        lives_text = font.render(f'Lives: {game_state.lives}', True, (255, 255, 255))

        bar_rect = pygame.Rect(0, self.height_offset - self.height_offset, self.game_board.get_width(), self.height_offset)

        pygame.display.set_caption(f'Escape the Werehouse! - {self.map_title[1][game_state.current_level]}')
        pygame.draw.rect(self.game_board, (50, 50, 50), bar_rect)  # Dark gray color for the bar
        self.game_board.blit(moves_text, (10, 10))
        self.game_board.blit(total_moves_text, (200, 10))
        self.game_board.blit(lives_text, (480, 10))

    def __render_tutorial_bar__(self, game_state):
        # Tutorial bar
        tutorial_font = pygame.font.SysFont('Lucida Console', 12)  # Font for tutorial text
        tutorial_text = tutorial_font.render(f'{self.map_title[0][game_state.current_level]}', True, (255, 255, 255)) # Set window bar

        bar_rect = pygame.Rect(0, self.height_offset - self.height_offset, self.game_board.get_width(), self.height_offset)

        pygame.display.set_caption(f'Escape the Werehouse! - Tutorial {game_state.current_level + 1}')
        pygame.draw.rect(self.game_board, (50, 50, 50), bar_rect)  # Dark gray color for the bar
        self.game_board.blit(tutorial_text, (15, 15))

    def __blit_level_elements__(self, game_state):
        self.game_board.fill((30, 30, 30))
        self.blit_level()
        self.blit_box_1(0, 0)
        self.blit_box_2(0, 0)
        self.blit_box_3(0, 0)
        self.blit_box_4(0, 0)
        self.blit_player(game_state, 0)