import pygame
from random import randrange
import time

# Set images for blitting
start = pygame.image.load('graphics/start.png')

floor = [pygame.image.load('graphics/floor1.png'), pygame.image.load('graphics/floor2.png'), \
        pygame.image.load('graphics/floor3.png'), pygame.image.load('graphics/floor4.png'),\
        pygame.image.load('graphics/floor5.png'),pygame.image.load('graphics/floor6.png'),\
        pygame.image.load('graphics/floor7.png'), pygame.image.load('graphics/floor8.png'),\
        pygame.image.load('graphics/floor9.png'), pygame.image.load('graphics/floor10.png'),\
        pygame.image.load('graphics/floor11.png'), pygame.image.load('graphics/floor12.png'),\
        pygame.image.load('graphics/floor13.png'), pygame.image.load('graphics/floor14.png'),\
        pygame.image.load('graphics/floor15.png'),pygame.image.load('graphics/floor16.png'),\
        pygame.image.load('graphics/floor17.png'), pygame.image.load('graphics/floor18.png'),\
        pygame.image.load('graphics/floor19.png'), pygame.image.load('graphics/floor20.png'),\
        pygame.image.load('graphics/floor21.png'), pygame.image.load('graphics/floor22.png'),\
        pygame.image.load('graphics/floor23.png'), pygame.image.load('graphics/floor24.png'),\
        pygame.image.load('graphics/floor25.png'),pygame.image.load('graphics/floor26.png'),\
        pygame.image.load('graphics/floor27.png'), pygame.image.load('graphics/floor28.png'),\
        pygame.image.load('graphics/floor29.png'), pygame.image.load('graphics/floor30.png'),\
        pygame.image.load('graphics/floor31.png'), pygame.image.load('graphics/floor32.png'),\
        pygame.image.load('graphics/floor33.png'), pygame.image.load('graphics/floor34.png'),\
        pygame.image.load('graphics/floor35.png'),pygame.image.load('graphics/floor36.png'),\
        pygame.image.load('graphics/floor37.png'), pygame.image.load('graphics/floor38.png'),\
        pygame.image.load('graphics/floor39.png'), pygame.image.load('graphics/floor40.png')]

wall = pygame.image.load('graphics/wall.png')

pit = pygame.image.load('graphics/pit.png')
pit_evil = [pygame.image.load('graphics/pit_evil1.png'), pygame.image.load('graphics/pit.png'),
           pygame.image.load('graphics/pit_evil2.png'), pygame.image.load('graphics/pit.png'),\
           pygame.image.load('graphics/pit_evil3.png'), pygame.image.load('graphics/pit.png'),\
           pygame.image.load('graphics/pit_evil4.png'), pygame.image.load('graphics/pit.png')]

exit = pygame.image.load('graphics/exit.png')

boxes = [pygame.image.load('graphics/box_in_pit.png'), pygame.image.load('graphics/box.png'),\
        pygame.image.load('graphics/box_in_pit_return_.png'), pygame.image.load('graphics/box_return.png'),\
        pygame.image.load('graphics/box_in_pit_fragile.png'), pygame.image.load('graphics/box_fragile.png'),\
        pygame.image.load('graphics/box_in_pit_biohazard.png'), pygame.image.load('graphics/box_biohazard.png')]

player = pygame.image.load('graphics/player.png')
player_up = pygame.image.load('graphics/player_up.png')
player_down = pygame.image.load('graphics/player_down.png')
player_left = pygame.image.load('graphics/player_left.png')
player_right = pygame.image.load('graphics/player_right.png')

stars = [pygame.image.load('graphics/0_stars.png'), pygame.image.load('graphics/1_stars.png'),\
        pygame.image.load('graphics/2_stars.png'), pygame.image.load('graphics/3_stars.png')]


# Set tile coordinate for X
x1 = 0
x2 = 100
x3 = 200
x4 = 300
x5 = 400
x6 = 500

# Set tile coordinate for Y
y1 = 0
y2 = 100
y3 = 200
y4 = 300
y5 = 400
y6 = 500

# Tile coordinates
t1r1 = (x1, y1)
t2r1 = (x2, y1)
t3r1 = (x3, y1)
t4r1 = (x4, y1)
t5r1 = (x5, y1)
t6r1 = (x6, y1)
t1r2 = (x1, y2)
t2r2 = (x2, y2)
t3r2 = (x3, y2)
t4r2 = (x4, y2)
t5r2 = (x5, y2)
t6r2 = (x6, y2)
t1r3 = (x1, y3)
t2r3 = (x2, y3)
t3r3 = (x3, y3)
t4r3 = (x4, y3)
t5r3 = (x5, y3)
t6r3 = (x6, y3)
t1r4 = (x1, y4)
t2r4 = (x2, y4)
t3r4 = (x3, y4)
t4r4 = (x4, y4)
t5r4 = (x5, y4)
t6r4 = (x6, y4)
t1r5 = (x1, y5)
t2r5 = (x2, y5)
t3r5 = (x3, y5)
t4r5 = (x4, y5)
t5r5 = (x5, y5)
t6r5 = (x6, y5)
t1r6 = (x1, y6)
t2r6 = (x2, y6)
t3r6 = (x3, y6)
t4r6 = (x4, y6)
t5r6 = (x5, y6)
t6r6 = (x6, y6)

# Game Board coordinates
tiles = (t1r1, t2r1, t3r1, t4r1, t5r1, t6r1,\
        t1r2, t2r2, t3r2, t4r2, t5r2, t6r2,\
        t1r3, t2r3, t3r3, t4r3, t5r3, t6r3,\
        t1r4, t2r4, t3r4, t4r4, t5r4, t6r4,\
        t1r5, t2r5, t3r5, t4r5, t5r5, t6r5,\
        t1r6, t2r6, t3r6, t4r6, t5r6, t6r6,)

# Value of Game Board elements 
S = 0  # Start
F = 1  # Floor
W = 2  # Wall
P1 = 3  # Pit1
P2 = 4  # Pit2
P3 = 5  # Pit3
P4 = 6  # Pit4
PW = 7  # Pit as Wall - not able to put box in it
E = 8  # Exit


# LEVEL 1
# Setup for tiles
level_map = [[F, F, F, W, E, F,\
            P1, W, W, W, W, F,\
            F, F ,F, F, F, P2,\
            F, W ,F, F, F, W,\
            F, W, F, F, W, W,
            S, W, W, F, W, W]]

# Setup for active Boxes
active_boxes = [[True, True, True, True]]
# Setup of Boxes startpoints
positions = [[t1r4, t4r3, t5r3, t4r5]]

# Set startpoint for Player
player_start = [t1r6]


# LEVEL 2
# Setup for tiles
level_map.append([E, F, F, F, F, PW,\
                 F, F, F, W, F, PW,\
                 PW, PW ,PW, P4, P3, W,\
                 W, F ,F, F, F, F,\
                 PW, F, W, F, F, F,
                 PW, S, PW, W, W, W])

# Setup for active Boxes
active_boxes.append([True, True, True, False])
# Setup of Boxes startpoints
positions.append([t6r4, t5r2, t4r1, t3r4])

# Set startpoint for Player
player_start.append(t2r6)


# LEVEL 2
# Setup for tiles
level_map.append([F, F, W, W, W, E,\
                 F, F, F, F, P4, F,\
                 F, F ,W, P2, W, W,\
                 P3, W ,F, F, F, S,\
                 F, F, F, F, W, PW,
                 F, F, F, F, W, W])

# Setup for active Boxes
active_boxes.append([True, True, True, True])
# Setup of Boxes startpoints
positions.append([t1r1, t2r1, t6r2, t3r6])

# Set startpoint for Player
player_start.append(t6r4)


# CLASS for setup of levels and blitting of game elements
class BoardElements():
    '''BoardElements'''
    #
    def __init__(self):
        '''__init__'''
        # Setup of Game Board size
        self.game_board_x = 600
        self.game_board_y = 600

        # Variable to keep track of numbers of Levels
        self.no_of_levels = sum(type(i) == type([]) for i in level_map)

        # Variable to tell if Player finished the Game or fell into a Pit
        self.play = True

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
        game_board.blit(start, (pos))


    # Blit floor tile
    def __floor__(self, game_board, pos, i):
        '''__floor__'''
        game_board.blit(floor[i], (pos))


    # Blit wall tile
    def __wall__(self, game_board, pos):
        '''__wall__'''
        game_board.blit(wall, (pos))


    # Blit pit1 tile
    def __pit_1__(self, game_board, pos, box):
        '''__pit_1__'''
        # If Pit active
        # - Blit pit1 
        if self.pit1:
            game_board.blit(pit, (pos))

        # Else
        # - Blit box_n's box_in_pit 
        else:
            game_board.blit(boxes[box], (pos))


    # Blit pit2 tile
    def __pit_2__(self, game_board, pos, box):
        '''__pit_2__'''
        # If Pit active
        # - Blit pit2 
        if self.pit2:
            game_board.blit(pit, (pos))

        # Else
        # - Blit box_n's box_in_pit 
        else:
            game_board.blit(boxes[box], (pos))


    # Blit pit3 tile
    def __pit_3__(self, game_board, pos, box, i):
        '''__pit_3__'''
        # If Pit active
        # - Blit pit3
        if self.pit3:
            game_board.blit(pit_evil[i], (pos))

        # Else
        # - Blit box_n's box_in_pit 
        else:
            game_board.blit(boxes[box], (pos))

    # Blit pit4 tile
    def __pit_4__(self, game_board, pos, box):
        '''__pit_4__'''
        # If Pit active
        # - Blit pit4
        if self.pit4:
            game_board.blit(pit, (pos))

        # Else
        # - Blit box_n's box_in_pit 
        else:
            game_board.blit(boxes[box], (pos))


    # Blit pit_w tile
    def __pit_w__(self, game_board, pos):
        '''__pit_w__'''
        game_board.blit(pit, (pos))


    # Blit exit tile
    def __exit___(self, game_board, pos):
        '''__exit___'''        
        game_board.blit(exit, (pos))


    # Setup tiles for Level n
    def __create_level__(self, game_board, level_map):
        '''__create_level__'''
        # For each coordinate in level_map
        # - Set tiles depending on value of Game Board element
        for i in range(len(level_map)):
            # Genrate random floor and pit tile
            rand_floor = randrange(0, 40)
            rand_pit = randrange(0,5)

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
                self.__pit_4__(game_board, tiles[i], self.in_pit4)

            elif level_map[i] == 7:
                self.__pit_w__(game_board, tiles[i])

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
    def __place_boxes__player_and_reset_pits__(self, active_boxes, positions, player_start):
        '''__place_boxes__player_and_reset_pits__'''
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
                self.__pit_4__(game_board, el[1], self.in_pit4)

            elif el[0] == 7:
                self.__pit_w__(game_board, el[1])

            elif el[0] == 8:
                self.__exit___(game_board, el[1])


    # Setup of new Level
    def generate_level(self, game_board, new_level):
        '''generate_level'''
        # If new_level equals True
        # - Reset elements list and setup tiles,
        #   reset box and pit_box list and Pits then place Boxes and Player, 
        #   increase level counter, and set new_level to False
        if new_level:
            self.elements = []
            self.__create_level__(game_board, level_map[self.lv])

            self.box = []
            self.pit_box = []
            self.__create_boxes__(boxes)
            self.__place_boxes__player_and_reset_pits__(active_boxes[self.lv],\
                                                        positions[self.lv], player_start[self.lv])
            
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
                game_board.blit(player_up, (self.px, p_move))

            # Else iff movement is Down
            # - Blit player in direction of y corresponding of p_move' value
            elif p_travel == 2:
                game_board.blit(player_down, (self.px, p_move))

            # Else iff movement is Left
            # - Blit player in direction of x corresponding of p_move' value
            elif p_travel == 3:
                game_board.blit(player_left, (p_move, self.py))

            # Else iff movement is Right
            # - Blit player in direction of x corresponding of p_move' value
            elif p_travel == 4:
                game_board.blit(player_right, (p_move, self.py))

            # Else
            # - Blit position of player
            else:
                game_board.blit(player, (self.px, self.py))


    # Blit Level score
    def blit_stars(self, game_board, moves):
        '''blit_stars'''
        # Blit score for LEVEL 1 depending on number of moves
        if self.lv == 1:
            if moves <= 17:
                # Blit 3 highlighted Stars
                game_board.blit(stars[3], (186, 115))
    
            elif moves > 17 and moves <= 19:
                # Blit 2 highlighted Stars
                game_board.blit(stars[2], (186, 115))

            else:
                # Blit 1 highlighted Star
                game_board.blit(stars[1], (186, 115))
        
        # Blit score for LEVEL 2 depending on number of moves
        elif self.lv == 2:
            if moves <= 24:
                # Blit 3 highlighted Stars
                game_board.blit(stars[3], (186, 115))
    
            elif moves > 24 and moves <= 28:
                # Blit 2 highlighted Stars
                game_board.blit(stars[2], (186, 115))

            else:
                # Blit 1 highlighted Star
                game_board.blit(stars[1], (186, 115))

        # Blit score for LEVEL 3 depending on number of moves
        elif self.lv == 3:
            if moves <= 35:
                # Blit 3 highlighted Stars
                game_board.blit(stars[3], (186, 115))
    
            elif moves > 35 and moves <= 39:
                # Blit 2 highlighted Stars
                game_board.blit(stars[2], (186, 115))

            else:
                # Blit 1 highlighted Star
                game_board.blit(stars[1], (186, 115))

        # Update all changes to display
        pygame.display.update()
        # Pause for 3 seconds to show Stars
        time.sleep(3)