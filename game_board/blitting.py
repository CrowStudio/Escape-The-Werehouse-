import pygame
import math
from random import randrange
import time
from game_board.maps import game_maps, tutorial_maps
from game_board.elements import gfx


# Rename variable for imported tiles (tiles are the same in tutorial_maps)
tiles = game_maps.tiles

# Creates a list of maps from tutorial_maps and game_maps
level_map = [tutorial_maps.tutorial_map]
level_map.append(game_maps.level_map)

# Creates a list of maps titles from tutorial_maps and game_maps
map_title = [tutorial_maps.title]
map_title.append(game_maps.title)

# Creates a list of active boxes from tutorial_maps and game_maps
active_boxes = [tutorial_maps.active_boxes]
active_boxes.append(game_maps.active_boxes)

# Creates a list of box positions from tutorial_maps and game_maps
positions = [tutorial_maps.positions]
positions.append(game_maps.positions)

# Creates a list of start positions from tutorial_maps and game_maps
player_start = [tutorial_maps.player_start]
player_start.append(game_maps.player_start)

# Creates a list of active/inactive exits from tutorial_maps and game_maps
active_exit = [tutorial_maps.active_exit]
active_exit.append(game_maps.active_exit)

# Define TILE_SIZE at the beginning of your file or in a constants section
TILE_SIZE = 100  # Adjust this value to match the size of your tiles


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
        self.current_beam_angle = -1.5

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
    def generate_level(self, game_board, new_level, option):
        '''generate_level'''
        # If new_level equals True
        # - Reset elements list and setup tiles,
        #   reset box and pit_box list and Pits then place Boxes and Player, 
        #   increase level counter, and set new_level to False
        if new_level:
            self.elements = []
            self.__create_level__(game_board, level_map[option][self.lv])
            # self.update_game_board_size(level_map[option][self.lv])
            self.box = []
            self.pit_box = []
            self.__create_boxes__(gfx.boxes)

            self.__place_boxes_player_and_reset_pits_and_exit__(active_boxes[option][self.lv],\
                                                                positions[option][self.lv],\
                                                                player_start[option][self.lv],\
                                                                active_exit[option][self.lv])

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
    def blit_player(self, game_board, p_travel, p_move):
        '''blit_player'''
        # If play equals True
        if self.play:
            # If movement is Up
            # - Blit player in direction of y corresponding of p_move' value
            if p_travel == 1:
                game_board.blit(gfx.player_up, (self.px, p_move + self.offset_y))

            # Else iff movement is Down
            # - Blit player in direction of y corresponding of p_move' value
            elif p_travel == 2:
                game_board.blit(gfx.player_down, (self.px, p_move + self.offset_y))

            # Else iff movement is Left
            # - Blit player in direction of x corresponding of p_move' value
            elif p_travel == 3:
                game_board.blit(gfx.player_left, (p_move, self.py + self.offset_y))

            # Else iff movement is Right
            # - Blit player in direction of x corresponding of p_move' value
            elif p_travel == 4:
                game_board.blit(gfx.player_right, (p_move, self.py + self.offset_y))

            # Else
            # - Blit position of player
            else:
                game_board.blit(gfx.player, (self.px, self.py + self.offset_y))


    # Blit Game Level score
    def blit_stars(self, game_board, moves):
        '''blit_stars'''
        # Blit score for LEVEL 1 depending on number of moves
        if self.lv == 1:
            if moves <= 19:
                # Blit 3 highlighted Stars
                game_board.blit(gfx.stars[3], (186, 155 - self.offset_y))

            elif moves > 19 and moves <= 21:
                # Blit 2 highlighted Stars
                game_board.blit(gfx.stars[2], (186, 155 - self.offset_y))

            else:
                # Blit 1 highlighted Star
                game_board.blit(gfx.stars[1], (186, 155 - self.offset_y))

        # Blit score for LEVEL 2 depending on number of moves
        elif self.lv == 2:
            if moves <= 24:
                # Blit 3 highlighted Stars
                game_board.blit(gfx.stars[3], (186, 155 - self.offset_y))

            elif moves > 24 and moves <= 26:
                # Blit 2 highlighted Stars
                game_board.blit(gfx.stars[2], (186, 155 - self.offset_y))

            else:
                # Blit 1 highlighted Star
                game_board.blit(gfx.stars[1], (186, 155 - self.offset_y))

        # Blit score for LEVEL 3 depending on number of moves
        elif self.lv == 3:
            if moves <= 35:
                # Blit 3 highlighted Stars
                game_board.blit(gfx.stars[3], (186, 155 - self.offset_y))

            elif moves > 35 and moves <= 37:
                # Blit 2 highlighted Stars
                game_board.blit(gfx.stars[2], (186, 155 - self.offset_y))

            else:
                # Blit 1 highlighted Star
                game_board.blit(gfx.stars[1], (186, 155 - self.offset_y))

        # Blit score for LEVEL 4 depending on number of moves
        elif self.lv == 4:
            if moves <= 38:
                # Blit 3 highlighted Stars
                game_board.blit(gfx.stars[3], (186, 115))

            elif moves > 38 and moves <= 40:
                # Blit 2 highlighted Stars
                game_board.blit(gfx.stars[2], (186, 115))

            else:
                # Blit 1 highlighted Star
                game_board.blit(gfx.stars[1], (186, 115))

        # Blit score for LEVEL 5 depending on number of moves
        elif self.lv == 5:
            if moves <= 92:
                # Blit 3 highlighted Stars
                game_board.blit(gfx.stars[3], (186, 155 - self.offset_y))

            elif moves > 92 and moves <= 94:
                # Blit 2 highlighted Stars
                game_board.blit(gfx.stars[2], (186, 155 - self.offset_y))

            else:
                # Blit 1 highlighted Star
                game_board.blit(gfx.stars[1], (186, 155 - self.offset_y))

        # Blit score for LEVEL 6 depending on number of moves
        elif self.lv == 6:
            if moves <= 58:
                # Blit 3 highlighted Stars
                game_board.blit(gfx.stars[3], (186, 155 - self.offset_y))

            elif moves > 58 and moves <= 60:
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

            # Determine the new target angle based on game_state.travel.
            target_angle = None
            if game_state.travel == 1:  # UP
                target_angle = math.atan2(-1, 0)
            elif game_state.travel == 2:  # DOWN
                target_angle = math.atan2(1, 0)
            elif game_state.travel == 3:  # LEFT
                target_angle = math.atan2(0, -1)
            elif game_state.travel == 4:  # RIGHT
                target_angle = math.atan2(0, 1)

            smoothing_factor = 0.2  # Lower is slower rotation.
            if target_angle is not None:
                self.current_beam_angle = self.__lerp_angle__(self.current_beam_angle, target_angle, smoothing_factor)
            direction_angle = self.current_beam_angle

            # Instead of one polygon with a sharp boundary,
            # build up a series of translucent slices for a gradient edge.
            # The inner slices will be fully transparent out to some fraction of the beam_length,
            # and the outer slices will gradually blend.
            slices = 50  # Number of slices for transitioning the gradient.
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
                steps = 30  # Smoother curve for this slice.
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