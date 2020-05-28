import pygame
from random import randrange
import time
from game_board.maps import game_maps, tutorial_maps
from game_board.elements import gfx


# Rename variable for imported tiles (tiles are the same in tutorial_maps)
tiles = game_maps.tiles

# Creates a list of maps from tutorial_maps and game_maps
level_map = [tutorial_maps.tutorial_map]
level_map.append(game_maps.level_map)

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


# CLASS for setup of levels and blitting of game elements
class BoardElements():
    '''BoardElements'''
    #
    def __init__(self):
        '''__init__'''
        # Setup of Game Board size
        self.game_board_x = 600
        self.game_board_y = 600

        # List of Tutorial map titles
        self.titel = tutorial_maps.titel

        # Variable to keep track of numbers of Levels
        self.no_of_levels = [sum(type(i) == type([]) for i in level_map[0])]
        self.no_of_levels.append(sum(type(i) == type([]) for i in level_map[1]))

        # Variable to tell if Player finished the Game or fell into a Pit
        self.play = True

        # Variable for active/inactive Exit
        self.exit = 0

        # Variables for active/inactive Pit
        self.pit1 = 1
        self.pit2 = 1
        self.pit3 = 1
        self.pit4 = 1

        # Variables for Box to fill Pit with
        self.in_pit1 = 0
        self.in_pit2 = 0
        self.in_pit3 = 0
        self.in_pit4 = 0

        # Lists for creation of Levels
        self.elements = []
        self.box = []
        self.pit_box = []

        # Variable to keep track of Levels
        self.lv = 0


    # Blit start tile
    def __start__(self, game_board,pos):
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
            game_board.blit(gfx.boxes[box], (pos))


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
            game_board.blit(gfx.boxes[box], (pos))


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
            game_board.blit(gfx.boxes[box], (pos))

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
            game_board.blit(gfx.boxes[box], (pos))


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
            rand_pit = randrange(0,20)

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

        # Activate/inactivate box2
        self.box2 = active_boxes[1]
        # Set startpoint for box2
        self.b2x, self.b2y = positions[1]
        
        # Activate/inactivate box3
        self.box3 = active_boxes[2]
        # Set startpoint for box3
        self.b3x, self.b3y = positions[2]
        
        # Activate/inactivate box4
        self.box4 = active_boxes[3]
        # Set startpoint for box4
        self.b4x, self.b4y = positions[3]

        # Set startpoint for Player
        self.px, self.py = player_start

        # Activate/inactivate exit
        self.exit = active_exit

        # Set all Pits to active
        self.pit1 = 1
        self.pit2 = 1
        self.pit3 = 1
        self.pit4 = 1


    # Blit tiles for Level n
    def blit_level(self, game_board):
        '''blit_level'''
        # For each element in list of Level elements
        # - Blit tiles depending on value of Game Board element
        for el in self.elements:
            # Blit tile cooresponding to value of Game Board element
            if el[0] == 0:
                self.__start__(game_board, el[1])

            elif el[0] == 1:
                self.__floor__(game_board, el[1], el[2])

            elif el[0] == 2:
                self.__wall__(game_board, el[1])

            elif el[0] == 3:
                self.__pit_1__(game_board, el[1], self.in_pit1)

            elif el[0] == 4:
                self.__pit_2__(game_board, el[1], self.in_pit2)

            elif el[0] == 5:
                self.__pit_3__(game_board, el[1], self.in_pit3, el[3])

            elif el[0] == 6:
                self.__pit_4__(game_board, el[1], self.in_pit4, el[3])

            elif el[0] == 7:
                self.__pit_as_wall__(game_board, el[1])

            elif el[0] == 8:
                self.__exit___(game_board, el[1])


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
                game_board.blit(self.box[0][1], (self.b1x, b1_move))

            # Else if movement is Left or Right
            # - Blit box1 in direction of x corresponding of b1_move' value
            elif b1_travel == 3 or b1_travel == 4: 
                game_board.blit(self.box[0][1], (b1_move, self.b1y))

            # Else
            # - Blit position of box1
            else:
                game_board.blit(self.box[0][1], (self.b1x, self.b1y))


    # Blit box2
    def blit_box_2(self, game_board, b2_travel, b2_move):
        '''blit_box2'''
        # If box2 is active 
        if self.box2:
            # If movement is Up or Down
            # - Blit box2 in direction of y corresponding of b2_move' value
            if b2_travel == 1 or b2_travel == 2:
                game_board.blit(self.box[1][1], (self.b2x, b2_move))

            # Else if movement is Left or Right
            # - Blit box2 in direction of x corresponding of b2_move' value
            elif b2_travel == 3 or b2_travel == 4:
                game_board.blit(self.box[1][1], (b2_move, self.b2y))

            # Else
            # - Blit position of box2
            else:
                game_board.blit(self.box[1][1], (self.b2x, self.b2y))


    # Blit box3
    def blit_box_3(self, game_board, b3_travel, b3_move):
        '''blit_box3'''
        # If box3 is active 
        if self.box3:
            # If movement is Up or Down
            # - Blit box3 in direction of y corresponding of b3_move' value
            if b3_travel == 1 or b3_travel == 2:
                game_board.blit(self.box[2][1], (self.b3x, b3_move))

            # Else if movement is Left or Right
            # - Blit box3 in direction of x corresponding of b3_move' value
            elif b3_travel == 3 or b3_travel == 4:
                game_board.blit(self.box[2][1], (b3_move, self.b3y))

            # Else
            # - Blit position of box3
            else:
                game_board.blit(self.box[2][1], (self.b3x, self.b3y))


    # Blit box4
    def blit_box_4(self, game_board, b4_travel, b4_move):
        '''blit_box4'''
        # If box4 is active     
        if self.box4:
            # If movement is Up or Down
            # - Blit box4 in direction of y corresponding of b4_move' value
            if b4_travel == 1 or b4_travel == 2:
                game_board.blit(self.box[3][1], (self.b4x, b4_move))

            # Else if movement is Left or Right
            # - Blit box4 in direction of x corresponding of b4_move' value
            elif b4_travel == 3 or b4_travel == 4:
                game_board.blit(self.box[3][1], (b4_move, self.b4y))

            # Else
            # - Blit position of box4
            else:
                game_board.blit(self.box[3][1], (self.b4x, self.b4y))


    # Blit player
    def blit_player(self, game_board, p_travel, p_move):
        '''blit_player'''
        # If play eqauls True 
        if self.play:
            # If movement is Up
            # - Blit player in direction of y corresponding of p_move' value
            if p_travel == 1:
                game_board.blit(gfx.player_up, (self.px, p_move))

            # Else iff movement is Down
            # - Blit player in direction of y corresponding of p_move' value
            elif p_travel == 2:
                game_board.blit(gfx.player_down, (self.px, p_move))

            # Else iff movement is Left
            # - Blit player in direction of x corresponding of p_move' value
            elif p_travel == 3:
                game_board.blit(gfx.player_left, (p_move, self.py))

            # Else iff movement is Right
            # - Blit player in direction of x corresponding of p_move' value
            elif p_travel == 4:
                game_board.blit(gfx.player_right, (p_move, self.py))

            # Else
            # - Blit position of player
            else:
                game_board.blit(gfx.player, (self.px, self.py))


    # Blit Game Level score
    def blit_stars(self, game_board, moves):
        '''blit_stars'''
        # Blit score for LEVEL 1 depending on number of moves
        if self.lv == 1:
            if moves <= 17:
                # Blit 3 highlighted Stars
                game_board.blit(gfx.stars[3], (186, 115))
    
            elif moves > 17 and moves <= 19:
                # Blit 2 highlighted Stars
                game_board.blit(gfx.stars[2], (186, 115))

            else:
                # Blit 1 highlighted Star
                game_board.blit(gfx.stars[1], (186, 115))
        
        # Blit score for LEVEL 2 depending on number of moves
        elif self.lv == 2:
            if moves <= 24:
                # Blit 3 highlighted Stars
                game_board.blit(gfx.stars[3], (186, 115))
    
            elif moves > 24 and moves <= 28:
                # Blit 2 highlighted Stars
                game_board.blit(gfx.stars[2], (186, 115))

            else:
                # Blit 1 highlighted Star
                game_board.blit(gfx.stars[1], (186, 115))

        # Blit score for LEVEL 3 depending on number of moves
        elif self.lv == 3:
            if moves <= 35:
                # Blit 3 highlighted Stars
                game_board.blit(gfx.stars[3], (186, 115))
    
            elif moves > 35 and moves <= 39:
                # Blit 2 highlighted Stars
                game_board.blit(gfx.stars[2], (186, 115))

            else:
                # Blit 1 highlighted Star
                game_board.blit(gfx.stars[1], (186, 115))

        # Update all changes to display
        pygame.display.update()
        # Pause for 3 seconds to show Stars
        time.sleep(3)