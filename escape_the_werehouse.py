import pygame
from blit import levels

# Initiate PyGame Mixer to avoid delay of sound playback 
pygame.mixer.pre_init(44100, -16, 1, 2048)
# Initiate PyGame
pygame.init()

# Game mode variable
# - 0 = tutorial, 1 = game
s = 0

# Create BoardElements objekt
board = levels.BoardElements(s)   

# Set size of game board surface with a color depth of 24-bit 
game_board = pygame.display.set_mode((board.game_board_x, board.game_board_y), 0, 24)
# Set background color - this will be the color of the fill between the tiles and the color of the walls
game_board.fill((30, 30, 30))

# Setup audio channels
ch1 = pygame.mixer.Channel(0)
ch2 = pygame.mixer.Channel(1)
ch3 = pygame.mixer.Channel(2)
ch4 = pygame.mixer.Channel(3)

# Set wave files for sound effects
moving = pygame.mixer.Sound('sound/moving.wav')
fall_in_pit = pygame.mixer.Sound('sound/fall_in_pit.wav')

# Value of game board elements 
S = 0  # Start
F = 1  # Floor
W = 2  # Wall
P1 = 3  # Pit1
P2 = 4  # Pit2
P3 = 5  # Pit3
P4 = 6  # Pit4
PW = 7  # Pit as Wall - not able to put box in it
E = 8  # Exit

# Movement coefficients
DIFF = 100
ANIMATE = 17



# CLASS for Player and Box movements
class Movements():
    '''Movements'''

    def __init__(self):
        '''__init__'''
        # Variables to keep track of Player's moves to get score and numbers of retries
        self.moves = 0
        self.total_moves = 0
        self.retries = 3

        # Varibales for Player's and Boxes movements
        self.p_travel = False
        self.p_dest = 0
        self.p_move = 0

        self.b1_travel = False
        self.b1_dest = 0
        self.b1_move = 0

        self.b2_travel = False
        self.b2_dest = 0
        self.b2_move = 0

        self.b3_travel = False
        self.b3_dest = 0
        self.b3_move = 0

        self.b4_travel = False
        self.b4_dest = 0
        self.b4_move = 0

        # Variable for Box sound ON/OFF
        self.b_sound = False


    # Checks for Pits when Box bn is moved
    def __detect_pit__(self, x, y, box_active, bn,):
        '''__detect_pit__''' 
        # Checks for Pit tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]
            
            # If Box bn's coordinates matches coordinates of pit1
            # - Set pit1 equals False to fill pit, box_active to False to inactivate Box bn,
            #   and set in_pit1 equals to Box bn's box_in_pit sprite to fill pit, then break foor loop
            if pos_o == (x, y) and tile == P1 and board.pit1:
                board.pit1 = False
                box_active = False
                board.in_pit1 = bn
                # Play fall_in_pit sound if Box fell in pit
                ch2.play(fall_in_pit)
                ch2.fadeout(350)
                break

            # If Box bn's coordinates matches coordinates of pit2
            # - Set pit2 equals False to fill pit, box_active to False to inactivate Box bn,print(bn)
            #   and set in_pit2 equals to Box bn's box_in_pit sprite to fill pit, then break foor loop
            elif pos_o == (x, y) and tile == P2 and board.pit2:
                board.pit2 = False
                box_active = False
                board.in_pit2 = bn
                # Fade out moving sound and play fall_in_pit sound if Box fell in pit
                ch2.play(fall_in_pit)
                ch2.fadeout(350)
                break

            # If Box bn's coordinates matches coordinates of pit3
            # - Set pit3 equals False to fill pit, box_active to False to inactivate Box bn,print(bn)
            #   and set in_pit3 equals to Box bn's box_in_pit sprite to fill pit, then break foor loop
            elif pos_o == (x, y) and tile == P3 and board.pit3:
                board.pit3 = False
                box_active = False
                board.in_pit3 = bn
                # Fade out moving sound and play fall_in_pit sound if Box fell in pit
                ch2.play(fall_in_pit)
                ch2.fadeout(350)
                break

            # If Box bn's coordinates matches coordinates of pit4
            # - Set pit4 equals False to fill pit, box_active to False to inactivate Box bn,print(bn)
            #   and set in_pit4 equals to Box bn's box_in_pit sprite to fill pit, then break foor loop
            elif pos_o == (x, y) and tile == P4 and board.pit4:
                board.pit4 = False
                box_active = False
                board.in_pit4 = bn
                # Fade out moving sound and play fall_in_pit sound if Box fell in pit
                ch2.play(fall_in_pit)
                ch2.fadeout(350)
                break

        # Returns state of active_box
        return box_active


    # Logic for Box detection used in private methods __detect_box_* 
    def __detect_other_box__(self, x, y):
        '''__detect_other_box__'''
        # List of logic to detect if other box is blocking active Box
        self.box_pos = [x == board.b1x and y == board.b1y and board.box1,\
                        x == board.b2x and y == board.b2y and board.box2,\
                        x == board.b3x and y == board.b3y and board.box3,\
                        x == board.b4x and y == board.b4y and board.box4]


    # Detect Wall when moving Up         
    def __detect_wall_up__(self, x, y, travel, dest, move):
        '''__detect_wall_up__'''
        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]

            # If Box coordinates matches coordinates of Wall, and if within game_bord
            # - Stop moving sound, and correct Player's/Box direction coordinate, then break for loop
            if (pos_o == (x, dest) and tile == W) or dest < 0:
                ch1.stop()

                self.p_travel = False
                self.p_dest = board.py - DIFF
                self.p_move += board.py
                self.moves -= 1

                travel = False
                dest = y - DIFF
                move += y
                break

        # Returns reset of Box movment
        return y, travel, dest, move


    # Detect other box when moving Up 
    def __detect_box_up__(self, x, y, travel, dest, move, box_n):
        '''__detect_box_up__'''
        # Refresh box_pos with logic
        self.__detect_other_box__(x, dest)
        # Remove box_n's compare logic from box_pos
        self.box_pos.pop(box_n)

        # If Box coordinates matches coordinates of other Box coordinates
        # - Stop moving sound, and correct Player's/Box direction coordinate
        if self.box_pos[0] or self.box_pos[1] or self.box_pos[2]:
            ch1.stop()

            self.p_travel = False
            self.p_dest = board.py - DIFF
            self.p_move += board.py
            self.moves -= 1

            travel = False
            dest = y - DIFF
            move += y

        # Returns reset of Box movment
        return y, travel, dest, move

    
    # Set blit direction, and start-/end-point for Box movement    
    def __start_movement_up__(self, y, travel, dest, move):
        '''__start_movement_up__'''
        # Set blit direction
        travel = 1
        # Set endpoint
        dest = y - DIFF
        # Set startpoint
        move = y

        # If ch1 is free and box sound is turned on
        # - Play moving sound, and set box sound to off
        if not ch1.get_busy() and self.b_sound:
            ch1.play(moving)
            ch1.fadeout(350)
            self.b_sound = False

        # Returns state of travel, destination, and startpoint for Box movement
        return travel, dest, move

    # Refresch movement and set endpoint 
    def __move_up__(self, y, travel, dest, move):
        '''__move_up__'''
        # If destination is not reached
        # - Move Box
        if move > dest:
            move -= ANIMATE
        # Else
        # - Set endpoint equals move rounded to closest hundred, set travel to False, and turn off Box sound
        else: 
            y = int(round(move, - 2))
            travel = False
            self.b_sound = False

        # Returns endpoint, state of travel, and movement of Box
        return y, travel, move


    # Move Player Up
    def move_player_up(self):
        '''move_player_up'''
        # Update direction coordinates
        if not self.p_travel:
            self.p_travel, self.p_dest, self.p_move = \
            self.__start_movement_up__(board.py, self.p_travel, self.p_dest, self.p_move)

        elif self.p_travel:
            board.py, self.p_travel, self.p_move = \
            self.__move_up__(board.py, self.p_travel, self.p_dest, self.p_move)

        # Checks for Walls, and refresh direction coordinates for Player
        self.__detect_wall_up__(board.px, board.py, self.p_travel, self.p_dest, self.p_move)


    # Move Box Up
    def move_box_up(self, box_n, bn, pit_bn, bx, by, b_travel, b_dest, b_move):
        '''move_box_up'''         
        # If Player's coorinates matches coordinates of box_n, and dragging Box up (space + up key)
        if board.px == bx and self.p_dest + (DIFF * 2)  == by\
        and key[pygame.K_SPACE] and key[pygame.K_UP]:
            # Update direction coordinate of box_n
            if not b_travel:
                self.b_sound = True
                b_travel, b_dest, b_move = \
                self.__start_movement_up__(by, b_travel, b_dest, b_move)

            elif b_travel:
                by, b_travel, b_move = \
                self.__move_up__(by, b_travel, b_dest, b_move)

        # If Player's coorinates matches coordinates of box_n, moving up and box_n is active
        if board.px == bx and self.p_dest == by and key[pygame.K_UP] and box_n:
            # Update direction coordinate of box_n
            if not b_travel:
                self.b_sound = True
                b_travel, b_dest, b_move = \
                self.__start_movement_up__(by, b_travel, b_dest, b_move)
            
            elif b_travel:
                by, b_travel, b_move = \
                self.__move_up__(by, b_travel, b_dest, b_move)

            # Checks for Pits when box_n is moved, and set state of box_n
            box_n = self.__detect_pit__(bx, by, box_n, pit_bn)
            
            # If box_n still active
            if box_n:
                # Check for Walls, and refresh direction coordinates for box_n
                by, b_travel, b_dest, b_move = \
                self.__detect_wall_up__(bx, by, b_travel, b_dest, b_move)
                # Check if other box is blocking, and refresh direction coordinates for box_n
                by, b_travel, b_dest, b_move = \
                self.__detect_box_up__(bx, by, b_travel, b_dest, b_move, bn)
        
        # Returns Box, coordinates, state of travel, destination, and movement
        return box_n, bx, by, b_travel, b_dest, b_move


    # Detect Wall when moving up 
    def __detect_wall_down__(self, x, y, travel, dest, move):
        '''__detect_wall_down__'''
        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]

            # If Box coordinates matches coordinates of Wall, and if within game_bord
            # - Stop moving sound, and correct Player's/Box direction coordinate, then break for loop
            if (pos_o == (x, dest) and tile == W) or dest > board.game_board_y - DIFF:
                ch1.stop()

                self.p_travel = False
                self.p_dest = board.py + DIFF
                self.p_move += board.py
                self.moves -= 1

                travel = False
                dest = y + DIFF
                move += y
                break

        # Returns reset of Box movment
        return y, travel, dest, move


    # Detect other box when moving down
    def __detect_box_down__(self, x, y, travel, dest, move, box_n):
        '''__detect_box_down__'''
        # Refresh box_pos with logic
        self.__detect_other_box__(x, dest)
        # Remove box_n's compare logic from box_pos
        self.box_pos.pop(box_n)

        # If Box coordinates matches coordinates of other box coordinates
        # - Stop moving sound, and correct Player's/Box direction coordinate
        if self.box_pos[0] or self.box_pos[1] or self.box_pos[2]:
            ch1.stop()

            self.p_travel = False
            self.p_dest = board.py + DIFF
            self.p_move += board.py
            self.moves -= 1

            travel = False
            dest = y + DIFF
            move += y

        # Returns reset of Box movment
        return y, travel, dest, move


    # Set blit direction, and start/end coordinates for piece to animate
    def __start_movement_down__(self, y, travel, dest, move):
        '''__start_movement_down__'''
        # Set blit direction
        travel = 2
        # Set endpoint
        dest = y + DIFF
        # Set startpoint
        move = y

        # If ch1 is free and box sound is turned on
        # - Play moving sound, and set box sound to off
        if not ch1.get_busy() and self.b_sound:
            ch1.play(moving)
            ch1.fadeout(350)
            self.b_sound = False

        # Returns state of travel, destinationt-/end-point for Box movement
        return travel, dest, move


    # Refresch movement and set endpoint  
    def __move_down__(self, y, travel, dest, move):
        '''__move_down__'''
        # If destination is not reached
        # - Move Box
        if move < dest:
            move += ANIMATE
        # Else
        # - Set endpoint equals move rounded to closest hundred, set travel to False, and turn off Box sound
        else: 
            y = int(round(move, - 2))
            travel = False
            self.b_sound = False

        # Returns endpoint, state of travel, and movement of Box
        return y, travel, move


    # Move Player Down
    def move_player_down(self):
        '''move_player_down'''
        # Update direction coordinates
        if not self.p_travel:
            self.p_travel, self.p_dest, self.p_move = \
            self.__start_movement_down__(board.py, self.p_travel, self.p_dest, self.p_move)

        elif self.p_travel:
            board.py, self.p_travel, self.p_move = \
            self.__move_down__(board.py, self.p_travel, self.p_dest, self.p_move)

        # Checks for Walls, and refresh direction coordinates for Player
        self.__detect_wall_down__(board.px, board.py, self.p_travel, self.p_dest, self.p_move)


    # Move Box Down
    def move_box_down(self, box_n, bn, pit_bn, bx, by, b_travel, b_dest, b_move):
        '''move_box_down'''         
        # If Player's coorinates matches coordinates of box_n, and dragging Box Down (space + down key)
        if board.px == bx and self.p_dest - (DIFF * 2)  == by\
        and key[pygame.K_SPACE] and key[pygame.K_DOWN]:
            # Update direction coordinate of box_n
            if not b_travel:
                self.b_sound = True
                b_travel, b_dest, b_move = \
                self.__start_movement_down__(by, b_travel, b_dest, b_move)
            
            elif b_travel:
                by, b_travel, b_move = \
                self.__move_down__(by, b_travel, b_dest, b_move)

        # If Player's coorinates matches coordinates of box_n, moving down and box_n is active
        if board.px == bx and self.p_dest == by and key[pygame.K_DOWN] and box_n:
            # Update direction coordinate of box_n
            if not b_travel:
                self.b_sound = True
                b_travel, b_dest, b_move = \
                self.__start_movement_down__(by, b_travel, b_dest, b_move)
            
            elif b_travel:
                by, b_travel, b_move = \
                self.__move_down__(by, b_travel, b_dest, b_move)

            # Checks for Pits when box_n is moved, and set state of box_n
            box_n = self.__detect_pit__(bx, by, box_n, pit_bn)
            
            # If box_n still active
            if box_n:
                # Check for Walls, and refresh direction coordinates for box_n
                by, b_travel, b_dest, b_move = \
                self.__detect_wall_down__(bx, by, b_travel, b_dest, b_move)
                # Check if other box is blocking, and refresh direction coordinates for box_n
                by, b_travel, b_dest, b_move = \
                self.__detect_box_down__(bx, by, b_travel, b_dest, b_move, bn)

        # Returns Box, coordinates, state of travel, destination, and movement 
        return box_n, bx, by, b_travel, b_dest, b_move

    #  Detect Wall when moving Left
    def __detect_wall_left__(self, x, y, travel, dest, move):
        '''__detect_wall_left__'''
        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]

            # If Box coordinates matches coordinates of Wall, and if within game_bord
            # - Stop moving sound, and correct Player's/Box direction coordinate, then break for loop
            if (pos_o == (dest, y) and tile == W) or dest < 0:
                ch1.stop()

                self.p_travel = False
                self.p_dest = board.px - DIFF
                self.p_move += board.px
                self.moves -= 1

                travel = False
                dest = x - DIFF
                move += x
                break

        # Returns reset of Box movment
        return x, travel, dest, move


    # Detect other box when moving left
    def __detect_box_left__(self, x, y, travel, dest, move, box_n):
        '''__detect_box_left__'''
        # Refresh box_pos with logic
        self.__detect_other_box__(dest, y)
        # Remove box_n's compare logic from box_pos
        self.box_pos.pop(box_n)

        # If Box coordinates matches coordinates of other box coordinates
        # - Stop moving sound, and correct Player's/Box direction coordinate
        if self.box_pos[0] or self.box_pos[1] or self.box_pos[2]:
            ch1.stop()

            self.p_travel = False
            self.p_dest = board.px - DIFF
            self.p_move += board.px
            self.moves -= 1

            travel = False
            dest = x - DIFF
            move += x

        # Returns reset of Box movment
        return x, travel, dest, move


    # Set blit direction, and start-/end-point for Box movement  
    def __start_movement_left__(self, x, travel, dest, move):
        '''__start_movement_left__'''
        # Set blit direction
        travel = 3
        # Set endpoint
        dest = x - DIFF
        # Set startpoint
        move = x

        # If ch1 is free and box sound is turned on
        # - Play moving sound, and set box sound to off
        if not ch1.get_busy() and self.b_sound:
            ch1.play(moving)
            ch1.fadeout(350)
            self.b_sound = False

        # Returns state of travel, destination, and startpoint for Box movement
        return travel, dest, move


    # Increase movement and set endpoint
    def __move_left__(self, x, travel, dest, move):
        '''__move_left__'''
        # If destination is not reached
        # - Move Box
        if move > dest:
            move -= ANIMATE
        # Else
        # - Set endpoint equals move rounded to closest hundred, set travel to False, and turn off Box sound
        else: 
            x = int(round(move, -2))
            travel = False
            self.b_sound = False

        # Returns endpoint, state of travel, and movement of Box
        return x, travel, move


    # Move Player Left
    def move_player_left(self):
        '''move_player_left'''
        # Update direction coordinates
        if not self.p_travel:
            self.p_travel, self.p_dest, self.p_move = \
            self.__start_movement_left__(board.px, self.p_travel, self.p_dest, self.p_move)

        elif self.p_travel:
            board.px, self.p_travel, self.p_move = \
            self.__move_left__(board.px, self.p_travel, self.p_dest, self.p_move)

        # Checks for Walls, and refresh direction coordinates for Player
        self.__detect_wall_left__(board.px, board.py, self.p_travel, self.p_dest, self.p_move)


    # Move Box Left
    def move_box_left(self, box_n, bn, pit_bn, bx, by, b_travel, b_dest, b_move):
        '''move_box_left'''         
        # If Player's coorinates matches coordinates of box_n, and dragging Box Left (space + left key)
        if self.p_dest + (DIFF * 2) == bx and board.py == by\
        and key[pygame.K_SPACE] and key[pygame.K_LEFT]:
        # Update direction coordinate of box_n
            if not b_travel:
                self.b_sound = True
                b_travel, b_dest, b_move = \
                self.__start_movement_left__(bx, b_travel, b_dest, b_move)
                      
            if b_travel:
                bx, b_travel, b_move = \
                self.__move_left__(bx, b_travel, b_dest, b_move)

        # If Player's coorinates matches coordinates of box_n, moving left and box_n is active
        if self.p_dest == bx and board.py == by and key[pygame.K_LEFT] and box_n:
            # Update direction coordinate of box_n
            if not b_travel:
                self.b_sound = True
                b_travel, b_dest, b_move = \
                self.__start_movement_left__(bx, b_travel, b_dest, b_move)
            
            elif b_travel:
                bx, b_travel, b_move = \
                self.__move_left__(bx, b_travel, b_dest, b_move)

            # Checks for Pits when box_n is moved, and set state of box_n
            box_n = self.__detect_pit__(bx, by, box_n, pit_bn)
            
            # If box4 still active
            if box_n:
                # Check for Walls, and refresh direction coordinates for box_n
                bx, b_travel, b_dest, b_move = \
                self.__detect_wall_left__(bx, by, b_travel, b_dest, b_move)
                # Check if other box is blocking, and refresh direction coordinates for box_n
                bx, b_travel, b_dest, b_move = \
                self.__detect_box_left__(bx, by, b_travel, b_dest, b_move, bn)
        
        # Returns Box, coordinates, state of travel, destination, and movement
        return box_n, bx, by, b_travel, b_dest, b_move


    # Detect Wall when moving up 
    def __detect_wall_right__(self, x, y, travel, dest, move):
        '''__detect_wall_right__'''
        # Checks for Wall tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]

            # If Box coordinates matches coordinates of Wall, and if within game_bord
            # - Stop moving sound, and correct Player's/Box direction coordinate, then break for loop
            if (pos_o == (dest, y) and tile == W) or dest > board.game_board_x - DIFF:
                ch1.stop()

                self.p_travel = False
                self.p_dest = board.px - DIFF
                self.p_move += board.px
                self.moves -= 1

                travel = False
                dest = x - DIFF
                move += x
                break

        # Returns reset of Box movment
        return x, travel, dest, move


    # Detect other box when moving right
    def __detect_box_right__(self, x, y, travel, dest, move, box_n):
        '''__detect_box_right__'''
        # Refresh box_pos with logic
        self.__detect_other_box__(dest, y)
        # Remove box_n's compare logic from box_pos
        self.box_pos.pop(box_n)

        # If Box coordinates matches coordinates of other box coordinates
        # - Stop moving sound, and correct Player's/Box direction coordinate
        if self.box_pos[0] or self.box_pos[1] or self.box_pos[2]:
            ch1.stop()

            self.p_travel = False
            self.p_dest = board.px - DIFF
            self.p_move += board.px
            self.moves -= 1

            travel = False
            dest = x - DIFF
            move += x

        # Returns reset of Box movment
        return x, travel, dest, move


    # Set blit direction, and start-/end-point for Box movement  
    def __start_movement_right__(self, x, travel, dest, move):
        '''__start_movement_right__'''
        # Set blit direction
        travel = 4
        # Set endpoint
        dest = x + DIFF
        # Set startpoint
        move = x

        # If ch1 is free and box sound is turned on
        # - Play moving sound, and set box sound to off
        if not ch1.get_busy() and self.b_sound:
            ch1.play(moving)
            ch1.fadeout(350)
            self.b_sound = False

        # Returns state of travel, destination, and startpoint for Box movement
        return travel, dest, move

    # Increase movement and set endpoint 
    def __move_right__(self, x, travel, dest, move):
        '''__move_right__'''
        # If destination is not reached
        # - Move Box
        if move < dest:
            move += ANIMATE
        # Else
        # - Set endpoint equals move rounded to closest hundred, set travel to False, and turn off Box sound
        else: 
            x = int(round(move, -2))
            travel = False
            self.b_sound = False

        # Returns endpoint, state of travel, and movement of Box
        return x, travel, move


    # Move Player Up
    def move_player_right(self):
        '''move_player_right'''
        # Update direction coordinates
        if not self.p_travel:
            self.p_travel, self.p_dest, self.p_move = \
            self.__start_movement_right__(board.px, self.p_travel, self.p_dest, self.p_move)

        elif self.p_travel:
            board.px, self.p_travel, self.p_move = \
            self.__move_right__(board.px, self.p_travel, self.p_dest, self.p_move)

        # Checks for Walls, and refresh direction coordinates for Player
        self.__detect_wall_right__(board.px, board.py, self.p_travel, self.p_dest, self.p_move)


    # Move Box Right
    def move_box_right(self, box_n, bn, pit_bn, bx, by, b_travel, b_dest, b_move):
        '''move_box_right'''         
        # If Player's coorinates matches coordinates of box_n, and dragging Box Right (space + right key)
        if self.p_dest - (DIFF * 2) == bx and board.py == by\
        and key[pygame.K_SPACE] and key[pygame.K_RIGHT]:
        # Update direction coordinate of box_n
            if not b_travel:
                self.b_sound = True
                b_travel, b_dest, b_move = \
                self.__start_movement_right__(bx, b_travel, b_dest, b_move)

            if b_travel:
                bx, b_travel, b_move = \
                self.__move_right__(bx, b_travel, b_dest, b_move)

        # If Player's coorinates matches coordinates of box_n, moving right and box_n is active
        if self.p_dest == bx and board.py == by and key[pygame.K_RIGHT] and box_n:
            # Update direction coordinate of box_n
            if not b_travel:
                self.b_sound = True
                b_travel, b_dest, b_move = \
                self.__start_movement_right__(bx, b_travel, b_dest, b_move)
            
            elif b_travel:
                bx, b_travel, b_move = \
                self.__move_right__(bx, b_travel, b_dest, b_move)

            # Checks for Pits when box_n is moved, and set state of box_n
            box_n = self.__detect_pit__(bx, by, box_n, pit_bn)
            
            # If box4 still active
            if box_n:
                # Check for Walls, and refresh direction coordinates for box_n
                bx, b_travel, b_dest, b_move = \
                self.__detect_wall_right__(bx, by, b_travel, b_dest, b_move)
                # Check if other box is blocking, and refresh direction coordinates for box_n
                bx, b_travel, b_dest, b_move = \
                self.__detect_box_right__(bx, by, b_travel, b_dest, b_move, bn)
        
        # Returns Box, coordinates, state of travel, destination, and movement
        return box_n, bx, by, b_travel, b_dest, b_move


    # Check if Player hit Exit or Pit 
    def player_detect_exit_or_pit(self, new_level, s):
        '''player_detect_exit_or_pit'''
        # Check for Exit or Pit tiles in list of board elements 
        for e in board.elements:
            tile = e[0]
            pos_o = e[1]

            # If Player's coordinates matches coordinates of Pit
            # - Set play and new_level to False
            if pos_o == (board.px, board.py) and tile == P1 and board.pit1\
            or pos_o == (board.px, board.py) and tile == P2 and board.pit2\
            or pos_o == (board.px, board.py) and tile == P3 and board.pit3\
            or pos_o == (board.px, board.py) and tile == P4 and board.pit4\
            or pos_o == (board.px, board.py) and tile == PW:
                board.play = False
                new_level = False
                break
            
            # If Player's coordinates matches coordinates of Exit, and there is more levels
            # - Add moves to total_moves, set moves to 0, and set new_level to True
            elif pos_o == (board.px, board.py) and tile == E and board.lv < board.no_of_levels:
                self.total_moves += self.moves

                # If s equals game (1)
                # - show scores
                if s:
                    stars = self.moves
                    board.blit_stars(game_board, stars)

                self.moves = 0
                new_level = True
                break

            # If Player's coordinates matches coordinates of Exit, and there is no more levels
            # - Set play to False and new_level to True 
            elif pos_o == (board.px, board.py) and tile == E and board.lv >= board.no_of_levels:
                board.play = False
                new_level = True

        # Player has not yet finished the level
        if board.play and not new_level:
            # Returns state for game_on and new_level
            return s, True, False

        # Player has finished the level
        elif board.play and new_level:
            # Returns state for game_on and new_level
            return s, True, True

        # Player has finished the last level
        elif not board.play and new_level:
            # If s equals 1
            # - game_mode equals game, and will show score
            
            if s:
                # Compare moves to level score table, and set number of Stars accordingly
                stars = self.moves
                board.blit_stars(game_board, stars)

                print('Congratulations! You finished the last level!')
                print(f'Your have made a total of {self.total_moves} successful moves!')
            
                # Returns state for game_on and new_level
                return s, False, False
            else:
                s = 1
                self.moves = 0
                board.lv = 0

                return s, True, True


        # Player fell into a Pit
        else:
            # Player lose 1 retry
            self.retries -= 1
            
            # If retries greater than 0
            # - Reset level and moves
            if self.retries > 0:
                board.play = True
                self.moves = 0
                board.lv -= 1
                # Returns state for game_on and new_level
                return s, True, True    
            
            # Else Game Over
            else:
                print('Game Over!')
                # Returns state for game_on and new_level
                return s, False, False


# FUNCTIONS for movement data
# Send data for box1-box4 to move_boxes_up method
def move_boxes_up():
    board.box1, board.b1x, board.b1y, movements.b1_travel, movements.b1_dest, movements.b1_move = \
    movements.move_box_up(board.box1, 0, board.pit_box[0], board.b1x, board.b1y, movements.b1_travel, movements.b1_dest, movements.b1_move)

    board.box2, board.b2x, board.b2y, movements.b2_travel, movements.b2_dest, movements.b2_move = \
    movements.move_box_up(board.box2, 1, board.pit_box[1], board.b2x, board.b2y, movements.b2_travel, movements.b2_dest, movements.b2_move)

    board.box3, board.b3x, board.b3y, movements.b3_travel, movements.b3_dest, movements.b3_move = \
    movements.move_box_up(board.box3, 2, board.pit_box[2], board.b3x, board.b3y, movements.b3_travel, movements.b3_dest, movements.b3_move)

    board.box4, board.b4x, board.b4y, movements.b4_travel, movements.b4_dest, movements.b4_move = \
    movements.move_box_up(board.box4, 3, board.pit_box[3], board.b4x, board.b4y, movements.b4_travel, movements.b4_dest, movements.b4_move)


# Send data for box1-box4 to move_boxes_down method
def move_boxes_down():
    board.box1, board.b1x, board.b1y, movements.b1_travel, movements.b1_dest, movements.b1_move = \
    movements.move_box_down(board.box1, 0, board.pit_box[0], board.b1x, board.b1y, movements.b1_travel, movements.b1_dest, movements.b1_move)

    board.box2, board.b2x, board.b2y, movements.b2_travel, movements.b2_dest, movements.b2_move = \
    movements.move_box_down(board.box2, 1, board.pit_box[1], board.b2x, board.b2y, movements.b2_travel, movements.b2_dest, movements.b2_move)

    board.box3, board.b3x, board.b3y, movements.b3_travel, movements.b3_dest, movements.b3_move = \
    movements.move_box_down(board.box3, 2, board.pit_box[2], board.b3x, board.b3y, movements.b3_travel, movements.b3_dest, movements.b3_move)

    board.box4, board.b4x, board.b4y, movements.b4_travel, movements.b4_dest, movements.b4_move = \
    movements.move_box_down(board.box4, 3, board.pit_box[3], board.b4x, board.b4y, movements.b4_travel, movements.b4_dest, movements.b4_move)


# Send data for box1-box4 to move_boxes_left method
def move_boxes_left():
    board.box1, board.b1x, board.b1y, movements.b1_travel, movements.b1_dest, movements.b1_move = \
    movements.move_box_left(board.box1, 0, board.pit_box[0], board.b1x, board.b1y, movements.b1_travel, movements.b1_dest, movements.b1_move)

    board.box2, board.b2x, board.b2y, movements.b2_travel, movements.b2_dest, movements.b2_move = \
    movements.move_box_left(board.box2, 1, board.pit_box[1], board.b2x, board.b2y, movements.b2_travel, movements.b2_dest, movements.b2_move)

    board.box3, board.b3x, board.b3y, movements.b3_travel, movements.b3_dest, movements.b3_move = \
    movements.move_box_left(board.box3, 2, board.pit_box[2], board.b3x, board.b3y, movements.b3_travel, movements.b3_dest, movements.b3_move)

    board.box4, board.b4x, board.b4y, movements.b4_travel, movements.b4_dest, movements.b4_move = \
    movements.move_box_left(board.box4, 3, board.pit_box[3], board.b4x, board.b4y, movements.b4_travel, movements.b4_dest, movements.b4_move)


# Send data for box1-box4 to move_boxes_right method
def move_boxes_right():
    board.box1, board.b1x, board.b1y, movements.b1_travel, movements.b1_dest, movements.b1_move = \
    movements.move_box_right(board.box1, 0, board.pit_box[0], board.b1x, board.b1y, movements.b1_travel, movements.b1_dest, movements.b1_move)

    board.box2, board.b2x, board.b2y, movements.b2_travel, movements.b2_dest, movements.b2_move = \
    movements.move_box_right(board.box2, 1, board.pit_box[1], board.b2x, board.b2y, movements.b2_travel, movements.b2_dest, movements.b2_move)

    board.box3, board.b3x, board.b3y, movements.b3_travel, movements.b3_dest, movements.b3_move = \
    movements.move_box_right(board.box3, 2, board.pit_box[2], board.b3x, board.b3y, movements.b3_travel, movements.b3_dest, movements.b3_move)

    board.box4, board.b4x, board.b4y, movements.b4_travel, movements.b4_dest, movements.b4_move = \
    movements.move_box_right(board.box4, 3, board.pit_box[3], board.b4x, board.b4y, movements.b4_travel, movements.b4_dest, movements.b4_move)


# Initiate Movements object
movements = Movements()


# FUNCITON for bliting Level, Boxes, Player, update Moves and Retries
def blit(): 
    game_board.fill((30, 30, 30))
    # Blit current level
    board.blit_level(game_board)
    # Blit position of Boxes
    board.blit_box_1(game_board, movements.b1_travel, movements.b1_move)
    board.blit_box_2(game_board, movements.b2_travel, movements.b2_move)
    board.blit_box_3(game_board, movements.b3_travel, movements.b3_move)
    board.blit_box_4(game_board, movements.b4_travel, movements.b4_move)
    # Blit direction of Player's marker
    board.blit_player(game_board, movements.p_travel, movements.p_move)
    
    # Set caption for window

    if s:
        pygame.display.set_caption(f'Escape the Werehouse!                 Moves: {movements.moves}                 Retries: {movements.retries}     ')

    else:
        pygame.display.set_caption(f'Escape the Werehouse!                    {board.titel[board.lv - 1]}')

    # Update all changes to display
    pygame.display.update()


# Initiate clock for frame rate 
clock = pygame.time.Clock()
# Initiate game_on
game_on = True
# Initiate new_level
new_level = True
# Initiate bounce - used for debouncing key press
bounce = 0

s = 0

#MAIN LOOP
while game_on:
    # Set frame rate to 20 frames per second
    clock.tick(24)

    # Blit new level if new_level equals True, refresh state of new_level
    new_level = board.generate_level(game_board, new_level, s)

    # Check for pygame.QUIT event (close window button)
    for event in pygame.event.get():
            # If window is closed
            # - Quite PyGame and Exit program
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                exit()

    # Log state of pressed keys
    key = pygame.key.get_pressed()

    # Movement Debouncing
    if bounce > 0:
        bounce += 1
    if bounce > 3:
        bounce = 0
    
    # If arrow-up key is pressed and Player's coordinate is within game_board
    # - +1 to moves, increase debounce varibale, refresh direction coordinate, and move Player and Box 
    if bounce == 0 and board.py > 0 and (key[pygame.K_UP] or key[pygame.K_UP] and key[pygame.K_SPACE]):
        movements.moves += 1
        bounce = 1
        movements.move_player_up()
        move_boxes_up() 

        # While destination not reached
        # - Animate movement of Player and Boxes
        while movements.p_travel == 1:
            clock.tick(24)
            blit()
            movements.move_player_up()
            move_boxes_up()      

    # If arrow-down key is pressed and Player's coordinate is within game_board
    # - +1 to moves, increase debounce varibale, refresh direction coordinate, and move Player and Box 
    if bounce == 0 and board.py < (board.game_board_y - DIFF) and (key[pygame.K_DOWN] or key[pygame.K_DOWN] and key[pygame.K_SPACE]):
        movements.moves += 1
        bounce = 1
        movements.move_player_down()
        move_boxes_down()

        # While destination not reached
        # - Animate movement of Player and Boxes
        while movements.p_travel == 2:
            clock.tick(24)
            blit()
            movements.move_player_down()
            move_boxes_down()
    
    # If arrow-left key is pressed and Player's coordinate is within game_board
    # - +1 to moves, increase debounce varibale, refresh direction coordinate, and move Player and Box 
    if bounce == 0 and board.px > 0 and (key[pygame.K_LEFT] or key[pygame.K_LEFT] and key[pygame.K_SPACE]):
        movements.moves += 1
        bounce = 1
        movements.move_player_left()
        move_boxes_left()

        # While destination not reached
        # - Animate movement of Player and Boxes
        while movements.p_travel == 3:
            clock.tick(24)
            blit()
            movements.move_player_left()
            move_boxes_left()

    # If arrow-right key is pressed and Player's coordinate is within game_board
    # - +1 to moves, increase debounce varibale, refresh direction coordinate, and move Player and Box 
    if bounce == 0 and board.px < (board.game_board_x - DIFF) and (key[pygame.K_RIGHT] or key[pygame.K_RIGHT] and key[pygame.K_SPACE]):
        movements.moves += 1
        bounce = 1
        movements.move_player_right()
        move_boxes_right()

        # While destination not reached
        # - Animate movement of Player and Boxes
        while movements.p_travel == 4:
            clock.tick(24)
            blit()
            movements.move_player_right()
            move_boxes_right()

    # Check for Exit or Pit tiles
    prev_s, game_on, new_level = movements.player_detect_exit_or_pit(new_level, s)
    # Blit Level, Boxes, Player, update Moves and Retries 
    

    if prev_s != s:
        s = 1
        prev_s = 0
        blit()

    else:
        blit()

# Game Over
# - Quite PyGame and Exit program
pygame.mixer.quit()
pygame.quit()
exit()
